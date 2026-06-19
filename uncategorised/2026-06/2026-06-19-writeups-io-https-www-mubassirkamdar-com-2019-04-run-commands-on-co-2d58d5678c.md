# CSV Injection via User-Agent Header in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Redacted Company (Name withheld)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
An attacker can inject malicious Excel formulas into the User-Agent header during failed login attempts, which are logged in the activity log. When an administrator exports the activity log as CSV, the formula executes on their machine, enabling arbitrary command execution. This vulnerability allows remote code execution on company machines with administrative privileges.

## Attack scenario (step by step)
1. Attacker navigates to the target application's login page at /login/index
2. Attacker enters a valid company email address with an incorrect password to trigger a failed login attempt
3. Attacker intercepts the login request using a proxy tool (Burp Suite, etc.)
4. Attacker modifies the User-Agent header to contain a malicious Excel formula such as '=cmd|' /C calc'!A0' or similar command execution payload
5. Attacker forwards the modified request, causing the formula to be logged in the activity log database
6. Administrator accesses the activity log and exports it as CSV format; the formula executes on the administrator's machine with their privileges, running arbitrary commands

## Root cause
The application fails to sanitize or validate user-supplied input in the User-Agent header before storing it in the activity log. When the log is exported to CSV format, spreadsheet applications interpret the formula prefix (=) as an executable formula rather than plain text, leading to code execution.

## Attacker mindset
The attacker demonstrated persistence despite initial reconnaissance yielding no obvious vulnerabilities. By thoroughly mapping application functionality, they identified a low-interaction attack surface (activity logs) and recognized that combining input injection with CSV export could bypass typical security controls. The choice to use 'User-Agent' as the injection vector exploited the assumption that this header would be safe to log without sanitization.

## Defensive takeaways
- Sanitize and validate all user-supplied input including HTTP headers (User-Agent, Referer, etc.) before storage or display
- Implement input validation to reject or escape strings starting with formula indicators (=, +, -, @, etc.) when generating CSV exports
- Use proper CSV encoding libraries that escape potentially dangerous characters
- Apply principle of least privilege to limit what administrators can do with exported data
- Implement Content Security Policy and disable formula execution in spreadsheet applications by default
- Log security-relevant events from trusted sources only; consider rate-limiting failed login attempts
- Educate users about the risks of opening CSV files from untrusted sources or enabling macros
- Implement Web Application Firewall (WAF) rules to detect and block formula injection patterns in headers

## Variant hunting
['Test other HTTP headers that are logged (Referer, Cookie values, X-Forwarded-For, Accept-Language, etc.) for CSV injection', 'Attempt formula injection in any user input fields that generate exportable reports (error logs, audit trails, user lists)', 'Check if JSON or XML exports are vulnerable to similar injection attacks', 'Test CSV injection in other export formats (PDF, Excel, TSV) with different formula prefixes', 'Investigate whether other file upload or log export features contain similar vulnerabilities', 'Look for formula injection in API responses that might be parsed as CSV by downstream tools']

## MITRE ATT&CK
- T1190
- T1203
- T1559
- T1566
- T1204

## Notes
This writeup demonstrates a creative application of CSV injection targeting an often-overlooked attack surface (HTTP headers in logs). The vulnerability is particularly dangerous because it requires minimal attacker interaction—just triggering a failed login—and affects high-privilege users (administrators). The blog post uses a responsible disclosure approach by redacting the company name. The PoC formula '=1+1' is benign, but the payload '=cmd|' /C calc'!A0' demonstrates actual code execution capability. This type of vulnerability is frequently missed in security assessments because testers may not consider logging mechanisms as attack vectors.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
