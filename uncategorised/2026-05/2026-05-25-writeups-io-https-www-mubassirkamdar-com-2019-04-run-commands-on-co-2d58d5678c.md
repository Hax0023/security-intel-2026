# CSV Injection via User Agent String in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Redacted Company
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
A CSV injection vulnerability was discovered in the activity log export functionality where user-supplied input (User-Agent header) was not sanitized before being included in downloadable CSV files. An attacker could inject Excel formulas into the User-Agent field during failed login attempts, which would execute arbitrary code when the CSV was opened by an administrator.

## Attack scenario (step by step)
1. Attacker identifies that failed login attempts are logged with User-Agent information
2. Attacker accesses the login page and obtains the login form
3. Attacker intercepts the login request and modifies the User-Agent header to contain a malicious Excel formula such as '=cmd|' /C calc'!A0'
4. Attacker submits the failed login attempt, causing the malicious User-Agent to be logged in the activity log
5. Administrator reviews activity logs and exports them to CSV format
6. When the administrator opens the CSV file in Microsoft Excel or compatible spreadsheet application, the formula is executed with the privileges of the administrator, potentially allowing arbitrary command execution

## Root cause
Insufficient input validation and output encoding on user-controlled data (User-Agent header) before inclusion in CSV export. The application failed to sanitize or escape formula characters (=, +, -, @, etc.) that trigger formula evaluation in spreadsheet applications.

## Attacker mindset
The attacker demonstrated persistence and lateral thinking by identifying an indirect attack vector through limited application interaction. Rather than targeting obvious input fields, they leveraged HTTP headers combined with export functionality to create a two-stage exploitation method where the attack vector is invisible until the file is processed by the target.

## Defensive takeaways
- Implement strict input validation on all user-controlled data including HTTP headers (User-Agent, Referer, etc.)
- Apply output encoding when exporting data to CSV - prefix suspicious characters with single quote or remove formula indicators
- Configure spreadsheet applications to disable automatic formula execution or warn users before executing formulas
- Sanitize any data that will be exported to spreadsheet formats by escaping formula metacharacters (=, +, -, @, tab, carriage return)
- Implement Content Security Policy headers to prevent formula injection vectors
- Use allowlisting for User-Agent strings rather than blindly accepting all values
- Log and monitor unusual User-Agent strings for security analysis
- Test all export functionality (CSV, Excel, PDF) for injection vulnerabilities during security testing

## Variant hunting
['Check other export functions (reports, logs, user data exports) for similar CSV injection vulnerabilities', 'Test other HTTP headers (Referer, X-Forwarded-For, X-Original-IP, Authorization) that may be logged and exported', 'Examine API endpoints that return user-controlled data in CSV/Excel format', 'Look for similar formula injection in PDF exports or other document formats', 'Check if other user-input fields (comments, descriptions, email) in activity logs have similar protections', 'Test filter/search functionality that may build dynamic spreadsheet exports', 'Investigate if the vulnerability exists in other log types (error logs, audit logs, access logs)']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204.002 - User Execution: Malicious File
- T1203 - Exploitation for Client Execution
- T1105 - Ingress Tool Transfer
- T1059.001 - Command and Scripting Interpreter: PowerShell

## Notes
This vulnerability demonstrates the importance of testing non-obvious input vectors and understanding how data flows through applications. The attacker's observation that HTTP headers are logged and exportable led to discovering a critical vulnerability that appeared to have limited interaction surface. The post emphasizes that understanding application functionality deeply often yields better security discoveries than automated scanning. The PoC uses a benign formula (=1+1) for testing but demonstrates the potential for RCE with appropriate payloads.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
