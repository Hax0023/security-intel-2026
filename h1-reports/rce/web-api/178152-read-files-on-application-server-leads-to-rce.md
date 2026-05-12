# Arbitrary File Read via Symlink in GitLab Export Upload Leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 178152 | https://hackerone.com/reports/178152
- **Submitted:** 2016-10-26
- **Reporter:** jobert
- **Program:** GitLab
- **Bounty:** Not specified in excerpt
- **Severity:** critical
- **Vuln:** Arbitrary File Read, Symlink Following, Information Disclosure, Improper Error Handling, Path Traversal
- **CVEs:** CVE-2016-9086
- **Category:** web-api

## Summary
GitLab's project export import feature fails to validate symlinks in uploaded tar archives, allowing attackers to read arbitrary files via symlink references in VERSION and project.json files. Error messages expose full file contents through JSON parsing exceptions and version mismatch error messages, enabling information disclosure of sensitive files like /etc/passwd.

## Attack scenario
1. Attacker exports a legitimate GitLab project to obtain valid export structure
2. Attacker extracts the tar archive and replaces VERSION or project.json with symlinks pointing to sensitive files (/etc/passwd, configuration files, keys)
3. Attacker re-archives the modified export and uploads it via GitLab's import functionality
4. GitLab processes the upload and attempts version validation, reading the symlinked file
5. Exception is raised containing full file contents which is reflected in error message to attacker
6. Attacker repeats process with different symlink targets to enumerate sensitive information

## Root cause
The import process fails to validate or reject symlinks within uploaded tar archives before processing. Two separate code paths expose file contents: (1) VERSION file parsing with version mismatch exceptions, and (2) project.json JSON parsing errors that expose the full file contents in ActiveSupport JSON decoder error messages.

## Attacker mindset
Reconnaissance-focused approach exploiting error handling as an information disclosure vector. Attacker recognizes that exceptions contain sensitive data and methodically chains multiple vulnerabilities (symlink following + error message leakage) to read arbitrary files. This enables further attacks like identifying RCE vectors from configuration files.

## Defensive takeaways
- Implement symlink validation: reject or warn on symlinks in uploaded archives before extraction
- Sanitize error messages: avoid including file contents or raw input data in exception messages returned to users
- Use tar extraction with security flags: consider using --no-symlinks or equivalent to prevent symlink following
- Implement allowlist-based file validation: only process expected files (VERSION, project.json, project.bundle) with strict type checking
- Add file type validation: ensure VERSION is a regular file and project.json contains valid JSON before processing
- Separate error logging from user feedback: log full errors internally but return generic messages to users
- Input validation: validate file permissions and ownership before reading uploaded content

## Variant hunting
Check for similar symlink-following vulnerabilities in other archive-based import features (backup restoration, theme uploads, plugin installations)
Search for other code paths using IO.read or File.open on user-controlled paths without symlink validation
Audit all uses of ActiveSupport::JSON.decode with user input to identify error message leakage
Test other archive formats (zip, rar) that may have similar symlink handling issues
Review exception handling in restore/import procedures to identify information disclosure patterns
Check for path traversal in addition to symlinks (../../etc/passwd style attacks)

## MITRE ATT&CK
- T1190
- T1040
- T1526
- T1087
- T1083
- T1552

## Notes
This is a sophisticated multi-stage vulnerability chain combining symlink following with error-based information disclosure. The VERSION file symlink allows reading first line only, but project.json symlink combined with JSON parsing errors allows reading entire files. Attacker provides proof-of-concept showing actual /etc/passwd from gitlab.com. Vulnerability likely enables further exploitation (RCE if configuration files, SSH keys, or application secrets are readable).

## Full report
<details><summary>Expand</summary>

The GitLab export upload feature contains a vulnerability that allows an attacker to read arbitrary files on a GitLab instance. This vulnerability is caused by the behaviour of `JSON.parse`, your error handling, and the possibility to reference a symbolic link in a GitLab export. When I started looking into this functionality, I created a demo repository and created a GitLab export through the project's admin panel. GitLab exports can be imported when creating a new project, for example at https://gitlab.com/projects/new (click GitLab export). Anyway, a simple, extracted GitLab export file contains the following files:

```
export $ ls -lash
total 48
 8 -rw-r--r--@   1 jobert  staff     5B Oct 25 19:52 VERSION
 8 -rw-r--r--@   1 jobert  staff   341B Oct 25 19:53 project.bundle
 8 lrwxr-xr-x    1 jobert  staff    11B Oct 25 20:43 project.json
```

When the export file is uploaded again, a few things happen. The first three are, in this order: it waits until the file has been written to disk (for big repositories), a version check based on the `VERSION` file, and creating a new `Project` model instance based on `project.json`. The first step isn't important. Lets look at the code that's being executed for the second step (line 12-18 from `Gitlab::ImportExport::VersionChecker`):

```ruby
def check!
  version = File.open(version_file, &:readline)
  verify_version!(version)
rescue => e
  shared.error(e)
  false
end
```

Pay attention to line 13. It will open the file and call the method `readline`, which will return the first line of the file. Now, on line 16 any exception is caught and the message is pushed onto the `errors` array. All these errors are returned to the frontend. Take a look at line 27-31 of the same file:

```ruby
if Gem::Version.new(version) != Gem::Version.new(Gitlab::ImportExport.version)
  raise Gitlab::ImportExport::Error.new("Import version mismatch: Required #{Gitlab::ImportExport.version} but was #{version}")
else
  true
end
```

This means if the version isn't correct, an exception is returned that contains the provided version from the GitLab export. Lets untar the GitLab export, replace the `VERSION` file with a symbolic link, and tar the GitLab export again. The structure of the tar will look like this:

```
export $ ls -lash
 8 lrwxr-xr-x    1 jobert  staff    11B Oct 25 20:43 VERSION -> /etc/passwd
 8 -rw-r--r--@   1 jobert  staff   341B Oct 25 19:53 project.bundle
 8 lrwxr-xr-x    1 jobert  staff    11B Oct 25 20:43 project.json
```

After creating a new GitLab export (run `tar -czvf test.tar.gz .` in the export directory), the new GitLab export can be uploaded. By doing so, the GitLab instance will return the first line of the error because the version matcher raises an exception:

{F130235}

However, with this only the first line of a file can be read. This is interesting, but much harder to exploit than if an entire file can be read. I kept digging to see if there was a way to read an entire file. Like I pointed out earlier, the third step in the import process is creating a new instance of the `Project` model. It executes the following code (line 11-22 from `Gitlab::ImportExport::ProjectTreeRestorer`):

```ruby
def restore
  json = IO.read(@path)
  tree_hash = ActiveSupport::JSON.decode(json)
  project_members = tree_hash.delete('project_members')

  ActiveRecord::Base.no_touching do
    create_relations
  end
rescue => e
  shared.error(e)
  false
end
```

A similar code structure as the version check is implemented: any exception that is thrown in line 13-18 is caught and the error message is pushed onto the errors array. It isn't immediately clear from the code, but the ActiveSupport implementation of JSON decoding uses `JSON.parse`, which returns the contents of the entire string to be decoded in the error message when it fails to decode. This means that if we can let the decoder raise an exception, we can read the contents of a file. This isn't so hard. Consider this file structure:

```
export $ ls -lash
 8 -rw-r--r--@   1 jobert  staff    11B Oct 25 20:43 VERSION
 8 -rw-r--r--@   1 jobert  staff   341B Oct 25 19:53 project.bundle
 8 lrwxr-xr-x    1 jobert  staff    11B Oct 25 20:43 project.json -> /etc/passwd
```

In this example, the `project.json` file is a symlink to `/etc/passwd`. The `IO.read` call on line 14 will follow a symlink to read the contents of a file. Obviously, the `/etc/passwd` file doesn't contain valid JSON, thus it will result in an exception with the contents of `/etc/passwd`. Use tar to compress the files again to prepare it for upload. An example file is attached: F130233. When this file gets imported, it'll show the contents of the linked file in the error message:

{F130234}

To proof that this isn't my own `/etc/passwd` file that was accidentally compressed with the file, here are the last 5 lines of the `/etc/passwd` of gitlab.com.

```
alejandro:x:1117:1117::/home/alejandro:/bin/bash
prometheus:x:999:999::/opt/prometheus:/bin/false
gitlab-monitor:x:998:998::/opt/gitlab-monitor:/bin/false
postgres:x:116:121:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
brian:x:1118:1118::/home/brian:/bin/bash
```

With this issue, the secrets of the GitLab rails project can be read, too. This results in an RCE because cookies can be marshalled and resigned again. It seems to also give access to the internal GitLab shell tokens, which give access to all repositories.

Let me know if you need any more information!

</details>

---
*Analysed by Claude on 2026-05-11*
