# Path Traversal in FileOutputStream via Unsanitized CLI Argument

## Metadata
- **Source:** HackerOne
- **Report:** 1635321 | https://hackerone.com/reports/1635321
- **Submitted:** 2022-07-13
- **Reporter:** bhaskar_ram
- **Program:** Unknown (HackerOne Report 1635321)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Path Traversal, Arbitrary File Write, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Unsanitized command-line argument (arg[0]) is directly passed to java.io.FileOutputStream without validation, enabling path traversal attacks. An attacker can write to arbitrary files on the system, particularly impactful if the application runs with elevated privileges.

## Attack scenario
1. Attacker identifies application accepts a file path argument from command line
2. Attacker crafts malicious path using traversal sequences (e.g., '../../sensitive/file.txt')
3. Attacker passes payload as arg[0] when executing the application
4. Unsanitized input flows directly into FileOutputStream constructor
5. Application writes data to attacker-controlled path outside intended directory
6. If app runs as root/elevated user, attacker gains write access to system files (config, binaries, credentials)

## Root cause
Missing input validation and sanitization on command-line arguments before file path usage. No canonicalization or whitelist checking of file paths prior to FileOutputStream instantiation.

## Attacker mindset
Privilege escalation and persistence: If the vulnerable app runs with setuid/setgid or as a service with elevated privileges, writing to sensitive locations (system binaries, cron jobs, config files) enables privilege escalation, code execution, or persistence mechanisms.

## Defensive takeaways
- Always validate and sanitize file path inputs from untrusted sources (CLI args, user input, APIs)
- Use path canonicalization (e.g., File.getCanonicalPath()) and verify resolved path is within intended directory
- Implement strict whitelist validation for allowed file paths or directories
- Avoid using raw user input directly in file I/O operations
- Run applications with minimal required privileges (principle of least privilege)
- Use security managers or sandboxing to restrict file system access
- Perform static code analysis to detect unsanitized flows into file I/O functions

## Variant hunting
Check for similar patterns: all FileInputStream/FileOutputStream with arg/parameter inputs
Search for file operations accepting environment variables without validation
Look for zip extraction or archive handling without path traversal checks
Audit file operations in privileged execution contexts (setuid, service accounts)
Review symbolic link handling in file write operations
Inspect temporary file creation for predictability and traversal risks

## MITRE ATT&CK
- T1190
- T1083
- T1548

## Notes
The severity escalates significantly in privilege-escalation contexts. Even without elevated privileges, this could enable data exfiltration or overwrite of application data. The vulnerability is straightforward to exploit but potentially critical depending on deployment context.

## Full report
<details><summary>Expand</summary>

Unsanitized input from arg[0] argument flows into java.io.FileOutputStream, where it is used as a path. This may result in a Path Traversal vulnerability and allow an attacker to write to arbitrary files.

## Impact

Being able to access and manipulate an arbitrary path leads to vulnerabilities when a program is being run with privileges that the user providing the path should not have. A website with a path traversal vulnerability would allow users access to sensitive files on the server hosting it. CLI programs may also be vulnerable to path traversal if they are being ran with elevated privileges (such as with the setuid or setgid flags in Unix systems)

</details>

---
*Analysed by Claude on 2026-05-24*
