# RCE via DecompressedArchiveSizeValidator and Project BulkImports

## Metadata
- **Source:** HackerOne
- **Report:** 1609965 | https://hackerone.com/reports/1609965
- **Submitted:** 2022-06-23
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Command Injection, Remote Code Execution, Unsafe Shell Command Construction
- **CVEs:** CVE-2022-2185
- **Category:** memory-binary

## Summary
A command injection vulnerability exists in GitLab's DecompressedArchiveSizeValidator which passes unsanitized archive paths directly to shell commands via Open3.popen3. When combined with the BulkImports::Projects::Pipelines::ProjectPipeline feature (behind a feature flag), an attacker can inject arbitrary commands and achieve remote code execution by crafting malicious project import data.

## Attack scenario
1. Attacker enables the bulk_import_projects feature flag on a GitLab instance
2. Attacker crafts a bulk import request with malicious payload in the archive_path parameter containing shell metacharacters (e.g., backticks, semicolons, pipes)
3. The payload is passed through BulkImports::Projects::Pipelines::ProjectPipeline transformers which allow arbitrary parameters
4. ProjectAttributesTransformer sets import_type to PROJECT_IMPORT_TYPE and passes remaining params to Projects::CreateService
5. The attacker sets template_name to trigger CreateFromTemplateService, which then calls GitlabProjectsImportService
6. The import process ultimately calls DecompressedArchiveSizeValidator.validate() which executes the injected command via shell

## Root cause
The DecompressedArchiveSizeValidator constructs a shell command by string interpolation without sanitization: `gzip -dc #{@archive_path} | wc -c`. When passed to Open3.popen3 as a string (not array), it is interpreted as a shell command, allowing injection of arbitrary commands through special characters in the archive_path parameter.

## Attacker mindset
An attacker with access to trigger bulk imports would recognize that archive_path is user-controllable through the import pipeline and contains no validation. By crafting a path with shell metacharacters, they can break out of the gzip command context and execute arbitrary system commands with GitLab process privileges.

## Defensive takeaways
- Never pass user-controlled data directly to Open3.popen3 as a string; use array form to avoid shell interpretation
- Implement strict validation and sanitization of file paths before using them in shell commands
- Use allowlist validation for archive paths to ensure they match expected patterns
- Apply consistent input validation across all pipeline transformers, not just prohibited attributes
- Implement additional guards when feature flags enable sensitive functionality like bulk imports
- Consider using safer APIs that don't invoke shell subprocesses (e.g., Ruby's built-in gzip libraries)
- Add security-focused code review checkpoints for command execution code paths

## Variant hunting
Search for other instances of Open3.popen3 with string commands instead of array arguments
Audit all uses of system(), backticks, %x{}, or exec with user-controlled inputs
Review other transformers in BulkImports pipelines for similar parameter validation gaps
Examine feature-flagged code paths for incomplete security controls
Check CreateFromTemplateService and related services for parameter passthrough vulnerabilities
Look for similar archive/compression handling code that may have identical vulnerabilities
Review file upload and import functionality across other parts of GitLab for shell command injection patterns

## MITRE ATT&CK
- T1190
- T1059.003
- T1047

## Notes
This vulnerability requires the bulk_import_projects feature flag to be enabled, reducing immediate blast radius but indicating a dangerous pattern in the codebase. The attack chain involves multiple layers: bypassing prohibited attributes validator, triggering template creation flow, and leveraging import pipeline to reach vulnerable validator. The fix should be in the validator itself (use array form for Open3), but defense-in-depth measures at each pipeline stage would have prevented exploitation.

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
