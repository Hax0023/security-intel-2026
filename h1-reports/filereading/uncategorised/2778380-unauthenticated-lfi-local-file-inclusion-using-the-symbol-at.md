# Unauthenticated Local File Inclusion (LFI) via Path Traversal in Jolokia DiagnosticCommand Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 2778380 | https://hackerone.com/reports/2778380
- **Submitted:** 2024-10-12
- **Reporter:** todayisnew-
- **Program:** Department of Defense (DoD)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Local File Inclusion (LFI), Path Traversal, Unauthenticated Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated attacker can read arbitrary files from the server by exploiting a path traversal vulnerability in the Jolokia endpoint /jolokia/exec/com.sun.management:type=DiagnosticCommand/compilerDirectivesAdd/. By inserting the '!' character as a directory separator, attackers can traverse the file system and access sensitive files like /etc/passwd and /etc/crontab without authentication.

## Attack scenario
1. Attacker identifies the exposed Jolokia endpoint at /jolokia/exec/com.sun.management:type=DiagnosticCommand/compilerDirectivesAdd/
2. Attacker crafts a malicious URL using '!' as a path traversal character (e.g., !/etc!/passwd)
3. Server processes the path traversal characters and treats '!' as directory navigation
4. Attacker successfully reads sensitive files like /etc/passwd containing system user information
5. Attacker escalates attack by reading configuration files, application source code, or credentials
6. Attacker gains complete understanding of system architecture enabling further exploitation

## Root cause
The DiagnosticCommand endpoint fails to properly sanitize or validate user-supplied input in the URL path. The application treats the '!' character as a legitimate path component instead of rejecting it or recognizing it as a traversal attempt. No input validation whitelist is enforced on acceptable file paths or identifiers.

## Attacker mindset
An attacker recognizing that Jolokia endpoints often expose dangerous functionality would probe for unauthenticated access to diagnostic and management interfaces. Upon discovering the compilerDirectivesAdd endpoint accepts path parameters, they would experiment with various path traversal techniques to bypass filtering. Finding that '!' works as a separator suggests the application only filters known traversal characters (like ../ or ..) but fails to handle alternative separators.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-supplied path parameters, especially in endpoint names containing 'exec', 'diagnostic', or 'command'
- Use a whitelist approach: maintain a set of acceptable file identifiers and map them to actual file paths server-side, never exposing raw path input
- Disable or restrict access to dangerous Jolokia endpoints (DiagnosticCommand, CompilerDirectives) via authentication and authorization controls
- Filter all known path traversal characters and separators including: ../, .., !, //, backslashes, and symbolic links
- Implement principle of least privilege - ensure the application runs with minimal file system permissions
- Use Web Application Firewall (WAF) rules to detect and block suspicious path patterns in URL parameters
- Apply defense-in-depth: combine input validation, output encoding, and file system restrictions
- Regularly audit and monitor access to sensitive files and endpoints through logging and alerting

## Variant hunting
Search for similar path traversal vulnerabilities in: other Jolokia endpoints accepting path parameters, diagnostic/management interfaces in Java applications, other uncommon path separators or encoding bypass techniques (alternate Unicode path separators, null bytes, case sensitivity tricks), similar patterns in Spring Boot Actuator endpoints, and instances where user input is concatenated into file paths without validation.

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1083 File and Directory Discovery
- T1005 Data from Local System
- T1552 Unsecured Credentials
- T1087 Account Discovery

## Notes
This vulnerability demonstrates a critical design flaw in exposing dangerous diagnostic endpoints without proper access controls. Jolokia endpoints are known high-value targets. The use of '!' as an unconventional path separator suggests minimal input validation was implemented. The unauthenticated nature makes this immediately exploitable. Organizations should immediately audit for exposed Jolokia endpoints and restrict access to administrative/diagnostic functionality.

## Full report
<details><summary>Expand</summary>

Hi `DOD` Team,

# Summary:

* When accessing the endpoint on https://██████████/jolokia/exec/com.sun.management:type=DiagnosticCommand/compilerDirectivesAdd/ it is possible to path traversal on the machine and reading local files by using `!` at every new directory injected allowing an attacker to read local files with even being Unauthenticated leads to a catastrophic impact on the main server.

# Steps to reproduce:

**1. Read the listed users on the instance ---> `/etc/passwd`:**

* https://███/jolokia/exec/com.sun.management:type=DiagnosticCommand/compilerDirectivesAdd/!/etc!/passwd

**2. Read Crontab jobs on the instance ---> `/etc/crontab`:**

* https://████/jolokia/exec/com.sun.management:type=DiagnosticCommand/compilerDirectivesAdd/!/etc!/crontab


# PoC Video:

* ████


# Mitigation/Fix:

* Sanitize user input and don't trust user inputs that come for your server in a `GET` method after the endpoint `/compilerDirectivesAdd/{Attackers_Coming_From_Here_To_Read_Local_Files}`, it would be better to maintain a whitelist of acceptable filenames and use a unique corresponding identifier to access the file. Then any request containing an invalid identifier can just be rejected. Additionally, you could also sanitize any path traversal characters that may be present in any `GET` request.

## Impact

An attacker could read local files on the web server that they would normally not have access to, such as the application source code or configuration files containing sensitive information on how the website is configured, etc...

Best Regards,
Youssef


</details>

---
*Analysed by Claude on 2026-05-24*
