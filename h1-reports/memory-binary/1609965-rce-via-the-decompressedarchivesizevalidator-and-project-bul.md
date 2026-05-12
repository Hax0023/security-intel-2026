# RCE via DecompressedArchiveSizeValidator and Project BulkImports

## Metadata
- **Source:** HackerOne
- **Report:** 1609965 | https://hackerone.com/reports/1609965
- **Submitted:** 2022-06-23
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Command Injection, Remote Code Execution, Improper Input Validation, Shell Metacharacter Injection
- **CVEs:** CVE-2022-2185
- **Category:** memory-binary

## Summary
The DecompressedArchiveSizeValidator constructs shell commands using unsanitized archive paths, allowing command injection. When combined with the BulkImports feature (disabled by default), an attacker can control the archive_path parameter through the project import flow, executing arbitrary commands with GitLab process privileges.

## Attack scenario
1. Attacker enables or waits for bulk_import_projects feature flag to be enabled
2. Attacker initiates a bulk import project creation request via BulkImports API
3. Attacker injects malicious shell metacharacters in archive path through data parameters that bypass ProhibitedAttributesTransformer
4. Attacker sets template_name to trigger CreateFromTemplateService, which internally calls GitlabProjectsImportService
5. The import_type gets set to gitlab_project, causing import_schedule to trigger the Importer flow
6. DecompressedArchiveSizeValidator constructs command string with attacker-controlled archive_path and executes via Open3.popen3 without shell escaping, achieving RCE

## Root cause
Open3.popen3(command) where command is a string interpolates unsanitized user input, enabling shell interpretation. The archive_path parameter originates from bulk import data that passes through transformers which don't validate path safety. The command is constructed as a string concatenation (gzip -dc #{@archive_path}) without shell argument escaping.

## Attacker mindset
Attacker seeks to exploit the bulk import feature (feature-flagged but eventually enabled in production) to achieve RCE. They leverage the transformer's selective filtering (ProhibitedAttributesTransformer only blocks specific patterns) to pass arbitrary parameters. They chain template creation logic to reach the vulnerable validator code path that most direct project creation doesn't touch.

## Defensive takeaways
- Never pass user input to Open3.popen3 as a single command string; use array syntax with separate command and arguments
- Implement comprehensive input validation on all bulk import data, not just blacklist-based filtering
- Use allowlist approach for parameters accepted in import workflows rather than blacklist
- Apply path validation/canonicalization for all file operations; verify archive paths are within expected directories
- Escape or properly quote all variables in shell commands using Shellwords.escape() if shell string unavoidable
- Add security review gates before enabling feature flags that introduce new import pathways
- Consider using safer APIs for file operations that don't invoke shell interpretation

## Variant hunting
Search for other uses of Open3.popen3/popen2/backticks with string interpolation across codebase
Identify other transformers in bulk import that may have incomplete blacklists (check for /\Aremote_/ bypass patterns)
Examine other FileImporter or Importer subclasses that may accept user-controlled paths
Review feature-flagged functionality that modifies import workflows to see if similar chains exist
Look for other validators or processors that construct commands from paths/filenames
Check if similar archive processing exists in other export/import features

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1059.007 - PowerShell
- T1203 - Exploitation for Client Execution
- T1005 - Data from Local System
- T1574.002 - Hijack Execution Flow: DLL Side-Loading
- T1027.010 - Obfuscated Files or Information: Command Obfuscation

## Notes
The vulnerability requires bulk_import_projects feature flag to be enabled, limiting immediate impact but creating a critical vulnerability once flag is enabled in production. The writeup demonstrates sophisticated chaining of multiple services and transformers to reach the vulnerable code. The attacker must be an authenticated user capable of initiating bulk imports. The ProhibitedAttributesTransformer's blacklist approach is insufficient as it doesn't block import_source or other relevant parameters when passed through template creation workflow.

## Full report
<details><summary>Expand</summary>

### Summary

The `DecompressedArchiveSizeValidator` is used to check the size of a archive before extracting it:

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.1.0-ee/lib/gitlab/import_export/decompressed_archive_size_validator.rb#L82
```ruby
      def command
        "gzip -dc #{@archive_path} | wc -c"
      end

   def validate
        pgrp = nil
        valid_archive = true

        Timeout.timeout(TIMEOUT_LIMIT) do
          stdin, stdout, stderr, wait_thr = Open3.popen3(command, pgroup: true)
          stdin.close
```

Since `command` is a string and passed directly to `Open3.popen3` it will be interpreted as a shell command, so if `archive_path` contains any special characters it can be used to run arbitrary commands.

One of the places that the `DecompressedArchiveSizeValidator` is used is in the [Gitlab::ImportExport::FileImporter](https://gitlab.com/gitlab-org/gitlab/-/blob/v15.1.0-ee/lib/gitlab/import_export/file_importer.rb#L110),

```ruby
     def size_validator
        @size_validator ||= DecompressedArchiveSizeValidator.new(archive_path: @archive_file)
      end
```

It gets `@archive_file` from  the constructor, and is used by the [Gitlab::ImportExport::Importer](https://gitlab.com/gitlab-org/gitlab/-/blob/v15.1.0-ee/lib/gitlab/import_export/importer.rb#L48) which gets it from `project.import_source`.

Under normal circumstances `import_source` is nil and is generated by the `FileImporter` using `@archive_file = File.join(@shared.archive_path, Gitlab::ImportExport.export_filename(exportable: @importable))`.

Most of the places I've checked do not allow you to set the `import_source` for a project, or have the `import_type` set to something other than `gitlab_project` or `gitlab_custom_project_template` (which is required to use the `::Gitlab::ImportExport::Importer`).

There is one place though, in the `BulkImports::Projects::Pipelines::ProjectPipeline`. Luckily this is disabled by default as it requires the `bulk_import_projects` feature to be enabled. If/once this feature is enabled, it's possible to trigger the above flow.

This is possible as the two transformer on the `ProjectPipeline` are `:BulkImports::Common::Transformers::ProhibitedAttributesTransformer` and `::BulkImports::Projects::Transformers::ProjectAttributesTransformer`,  which first removes a list of prohibited keys:

```ruby
PROHIBITED_REFERENCES = Regexp.union(
          /\Acached_markdown_version\Z/,
          /\Aid\Z/,
          /_id\Z/,
          /_ids\Z/,
          /_html\Z/,
          /attributes/,
          /\Aremote_\w+_(url|urls|request_header)\Z/ # carrierwave automatically creates these attribute methods for uploads
        ).freeze
```

And then sets a few other values:
```ruby
          entity = context.entity
          visibility = data.delete('visibility')

          data['name'] = entity.destination_name
          data['path'] = entity.destination_name.parameterize
          data['import_type'] = PROJECT_IMPORT_TYPE
          data['visibility_level'] = Gitlab::VisibilityLevel.string_options[visibility] if visibility.present?
          data['namespace_id'] = Namespace.find_by_full_path(entity.destination_namespace)&.id if entity.destination_namespace.present?

          data.transform_keys!(&:to_sym)
```

All of the other params are allowed and passed directly into `project = ::Projects::CreateService.new(context.current_user, data).execute`. The first thing the create service does its to check if it's creating from a template, and if so the `CreateFromTemplateService` is used instead:

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.1.0-ee/app/services/projects/create_service.rb#L25-27
```ruby
    def execute
     if create_from_template?
        return ::Projects::CreateFromTemplateService.new(current_user, params).execute
      end
    # ...
    end

    def create_from_template?
      @params[:template_name].present? || @params[:template_project_id].present?
    end
```

Since we control all of the params, this path can be triggered by setting `template_name` to a valid template such as `rails`.  This then uses the `GitlabProjectsImportService` which allows the `import_type` to be changed from `gitlab_project_migration` to `gitlab_project`.

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.1.0-ee/app/services/projects/gitlab_projects_import_service.rb#L61-76
```ruby
    def prepare_import_params
      data = {}
      data[:override_params] = @override_params if @override_params

      if overwrite_project?
        data[:original_path] = params[:path]
        params[:path] += "-#{tmp_filename}"
      end

      if template_file
        data[:sample_data] = params.delete(:sample_data) if params.key?(:sample_data)
        params[:import_type] = 'gitlab_project'
      end

      params[:import_data] = { data: data } if data.present?
    end
```

The `Projects::CreateService` service is then called again with the updated `import_type`, but the rest of our params the same. This causes the `import_schedule` to happen as `@project.gitlab_project_migration?` is no longer true

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.1.0-ee/app/services/projects/create_service.rb#L276-282
```ruby
    def import_schedule
      if @project.errors.empty?
        @project.import_state.schedule if @project.import? && !@project.bare_repository_import? && !@project.gitlab_project_migration?
      else
        fail(error: @project.errors.full_messages.join(', '))
      end
    end
```

If a custom `import_source` was used, it will be used as the `@archive_file` for the `Gitlab::ImportExport::FileImporter`.  After `wait_for_archived_file` has reached `MAX_RETRIES` (it continues instead of failing) then `validate_decompressed_archive_size` will be called and then `Open3.popen3` with a controllable string.

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.1.0-ee/lib/gitlab/import_export/file_importer.rb#L45

```ruby
       wait_for_archived_file do
          validate_decompressed_archive_size if Feature.enabled?(:validate_import_decompressed_archive_size)
          decompress_archive
        end

      def wait_for_archived_file
        MAX_RETRIES.times do |retry_number|
          break if File.exist?(@archive_file)

          sleep(2**retry_number)
        end

        yield
      end
```

### Steps to reproduce

1. spin up a gitlab instance
1. ssh in and enable bulk project imports with from a rails console: `sudo gitlab-rails console` then `::Feature.enable(:bulk_import_projects)`
1. start watching the logs with `sudo gitlab-ctl tail`
1. create an api token
1. create a new group
1. create a new project in that group
1. download {F1785226} and change `PROJECT_PATH` to the full path of the project above and `PROJECT_ID` to its id
1. change `"import_source":"/tmp/ggg;echo lala|tee /tmp/1234;#",` to be your custom command (it cannot contain `>` as json will convert it to `\u003c`)
1. (optional) remove `proxies={"http":"http://127.0.0.1:8080", "https":"http://127.0.0.1:8080"}` if you are not using burp/another proxy
1. run it with `FLASK_APP=api_project_ql.py flask run`
1. start ngrok with `ngrok http 5000`
1.  go to new group -> import group
1. enter the ngrok http address and your token from above in the `Import groups from another instance of GitLab` section
1. select the group created above, change the parent to `No parent` and choose a new group name
1. hit import
1. you should see requests being made, then after the project is imported and the `wait_for_archived_file` has timed out (takes a few minutes) you should see something like following error in the logs and the payload will execute:

```
command exited with error code 2: tar (child): /tmp/ggg;echo lala|tee /tmp/1234;#: Cannot open: No such file or directory
tar (child): Error is not recoverable: exiting now
tar: Child returned status 2
tar: Error is not recoverable: exiting now
```

```bash
vagrant@gitlab:~$ cat /tmp/1234
lala
vagrant@gitlab:~$
```

### Impact

If the `bulk_import_projects` feature is enabled, allo

</details>

---
*Analysed by Claude on 2026-05-11*
