# RepositoryPipeline allows importing of local git repos via file:// protocol

## Metadata
- **Source:** HackerOne
- **Report:** 1685822 | https://hackerone.com/reports/1685822
- **Submitted:** 2022-08-30
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Arbitrary File Access, Path Traversal, Insufficient URL Validation, Unauthorized Data Access
- **CVEs:** None
- **Category:** uncategorised

## Summary
The BulkImports RepositoryPipeline fails to restrict URL schemes when importing repositories, allowing attackers to use file:// protocol URLs to access local git repositories on the server. By calculating the SHA2 hash of a project ID, attackers can construct file:// URLs to clone any private repository, requiring only knowledge of the target project ID.

## Attack scenario
1. Attacker identifies target GitLab project ID of a private repository
2. Attacker calculates SHA2 hash of project ID to derive storage path (e.g., Digest::SHA2.hexdigest('38006449'))
3. Attacker sets up fake GitLab instance or controls group import source returning malicious httpUrlToRepo
4. Attacker crafts file:// protocol URL pointing to local repository path: file://aw.rs/var/opt/gitlab/git-data/repositories/@hashed/b1/74/b174103b399555239923697fbe124faa61de4d441bd5c5678275eb0a5a27a562.git
5. Attacker triggers BulkImports group/project import flow with crafted URL
6. RepositoryPipeline.load() passes URL validation because UrlBlocker.validate! allows any scheme when no schemas parameter specified
7. Git fetch command executes with file:// URL, accessing and cloning the local private repository

## Root cause
The Gitlab::UrlBlocker.validate! call in RepositoryPipeline.load() is invoked without specifying allowed_schemes parameter, which defaults to permitting all schemes including file://. The validation only checks if the remaining URL structure is valid but does not restrict the protocol scheme itself. Additionally, the storage path is deterministic and calculable from public project IDs using SHA2 hashing.

## Attacker mindset
An attacker seeks to access private repositories without authorization. By understanding GitLab's deterministic storage path scheme and exploiting the URL validation bypass, they can leverage the bulk import feature to clone any private repository on an instance by only knowing its project ID. The attack is particularly powerful because it requires minimal privileges (ability to trigger group imports) and scales across multiple repositories.

## Defensive takeaways
- Always explicitly whitelist allowed URL schemes in validation functions; never rely on defaults that permit all schemes
- Implement schema validation with positive allowlist (only http/https/git/ssh) rather than negative blacklist
- Avoid exposing predictable, deterministic file paths for sensitive resources; consider using non-sequential storage identifiers
- Apply defense-in-depth: validate not just URL structure but origin/source of URLs, especially in data import pipelines
- Restrict file:// protocol access entirely in network operations unless explicitly required with strong justification
- Use access control checks before executing mirror/fetch operations to verify user authorization for source repository
- Consider implementing additional checks on imported repository paths to prevent accessing paths outside designated import locations
- Add audit logging for all repository import operations including source URLs and imported content

## Variant hunting
Check other Gitlab::UrlBlocker.validate! calls without explicit schemes parameter throughout codebase
Review all import/fetch operations (Docker, Helm, Maven, Cargo, etc.) for similar URL scheme validation bypasses
Examine other pipeline stages in BulkImports for similar URL handling vulnerabilities
Search for other uses of fetch_as_mirror or similar git operations without URL validation
Check if gopher://, ldap://, or other schemes can be abused for SSRF attacks via UrlBlocker
Verify if relative file paths or UNC paths (\\server\share) can bypass validation on Windows systems
Test if URL encoding or other obfuscation bypasses the validation logic

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1610 - Deploy Container
- T1005 - Data from Local System
- T1040 - Network Sniffing
- T1021 - Remote Services
- T1552 - Unsecured Credentials

## Notes
This vulnerability demonstrates the danger of insufficient input validation in data import pipelines. The predictable nature of GitLab's storage paths (SHA2 of project ID) combined with the ability to specify arbitrary file:// URLs creates a critical information disclosure vulnerability. The writeup includes proof-of-concept with exploitation of GitLab's own CTF project, validating severity. Exploitation requires some attack infrastructure (fake GitLab instance or Helm integration) but the barrier to entry is relatively low for sophisticated attackers. The fix should be simple: add schemes: ['http', 'https', 'git', 'ssh'] parameter to UrlBlocker.validate! call.

## Full report
<details><summary>Expand</summary>

### Summary

When importing a project via the BulkImports, the response field `httpUrlToRepo` from the client is used to fetch the repo:

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.3.1-ee/lib/bulk_imports/projects/pipelines/repository_pipeline.rb#L17
```ruby
        def load(context, data)
          url = data['httpUrlToRepo']
          return unless url.present?

          url = url.sub("://", "://oauth2:#{context.configuration.access_token}@")
          project = context.portable

          Gitlab::UrlBlocker.validate!(url, allow_local_network: allow_local_requests?, allow_localhost: allow_local_requests?)

          project.ensure_repository
          project.repository.fetch_as_mirror(url)
        end
```

`Gitlab::UrlBlocker.validate` is called, but since no schemas are passed in it allows any (such as file) so long as the rest of the url is valid.

This means that if a url such as `file://aw.rs/var/opt/gitlab/git-data/repositories/@hashed/b1/74/b174103b399555239923697fbe124faa61de4d441bd5c5678275eb0a5a27a562.git` is supplied, this will end up being used by git fetch, eg:

```bash
$ git fetch file://aw.rs/var/opt/gitlab/git-data/repositories/@hashed/b1/74/b174103b399555239923697fbe124faa61de4d441bd5c5678275eb0a5a27a562.git
fatal: '/var/opt/gitlab/git-data/repositories/@hashed/b1/74/b174103b399555239923697fbe124faa61de4d441bd5c5678275eb0a5a27a562.git' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

This allows an attacker to import any local repository that the current machine has access to if the path is known.

The storage path for projects in gitlab is just based on a configurable folder combined with a bucketed sha2 hash of  the id, eg for project 38006449 the `Digest::SHA2.hexdigest("38006449")` is  `b174103b399555239923697fbe124faa61de4d441bd5c5678275eb0a5a27a562` so the path will be at `@hashed/b1/74/b174103b399555239923697fbe124faa61de4d441bd5c5678275eb0a5a27a562.git`.

This can then be used to import any gitlab repository via the project id by calculating the path, such as the gitlab ctf project!

`{gitlab-bounty-flag-7a3f26698d2ef146843d7209e5efc8ec}`


### Steps to reproduce

1. Create a private project with User A and edit the readme file, make note of the project id
1. Download {F1892171} and edit line 99 with the new path to the repository above (replace `b1/74/b174103b399555239923697fbe124faa61de4d441bd5c5678275eb0a5a27a562` with the new `sha2[0:2]/sha2[2:4]/sha2`)
1. Run the server with `FLASK_APP=fake_server.py FLASK_ENV=development flask run`
1. Start ngrok with `ngrok http 500`
1. User B, visit https://gitlab.com/groups/new#import-group-pane and enter your ngrok url, any token and hit connect
1. In the browser console,  replace `"destination_namespace":"vakzz"` with your gitlab username (or a group you have access too) in the code below and run it:

  ```javascript
await fetch("/import/bulk_imports.json", { method: "POST", headers: { "X-CSRF-Token": document.querySelector("[name=csrf-token]").content, "Content-Type": "application/json" }, body: `{"bulk_import":[{"source_type":"project_entity","source_full_path":"group1/project1","destination_namespace":"vakzz","destination_slug":"some_project_z_${Math.floor(Math.random() * 10000)}"}]}` });
  ```

1. After a few minutes you should see a new project appear
1. Initially it will just show `No repository`
1. After another minute or so the project will either show `The repository for this project is empty`  or it will be a clone of the project from User A
1. If you see `The repository for this project is empty` then just repeat the fetch call again, it can take a few tries to end up on the same server as the victim (I think that's what is happening)

This can also be done with a Helm install of gitlab using the base path of `/home/git/repositories` or using the omnibus edition, but you will need to check where the repositories are located on disk and use that as the base path.
 
### Impact

Allows an attacked to clone any repo on gitlab with just the project id

### Examples

Example of me cloning the gitlab ctf project - https://gitlab.com/vakzz-h1/secret_ctf_5401/-/blob/main/you/found/id/flag.txt

### What is the current *bug* behavior?

The `RepositoryPipeline` allows for arbitrary url protocols to be passed to `project.repository.fetch_as_mirror(url)`

### What is the expected *correct* behavior?

It should be restricted to https/git/ssh

### Relevant logs and/or screenshots
{F1892192}
### Output of checks

This bug happens on GitLab.com

## Impact

Allows an attacked to clone any repo on gitlab with just the project id

</details>

---
*Analysed by Claude on 2026-05-11*
