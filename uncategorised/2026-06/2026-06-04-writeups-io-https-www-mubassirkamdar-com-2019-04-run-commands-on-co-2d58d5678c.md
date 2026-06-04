# CSV Injection via User Agent Header in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Undisclosed/Redacted Company
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
An unauthenticated attacker can inject Excel formulas into the User-Agent header during failed login attempts, which are logged and exported as CSV by administrators. When the administrator opens the exported CSV in Excel, the formula executes arbitrary commands on their machine with their privileges.

## Attack scenario (step by step)
1. Attacker navigates to target application login page
2. Attacker enters a valid company email address and random password to trigger a failed login
3. Attacker intercepts the login request and modifies the User-Agent header to contain a malicious Excel formula such as '=cmd|' /C calc'!A0'
4. Failed login attempt is recorded in activity logs with the malicious User-Agent string
5. Administrator reviews activity logs and exports them to CSV format for analysis
6. Administrator opens the CSV file in Microsoft Excel, triggering automatic formula execution and executing arbitrary commands on their machine

## Root cause
The application fails to sanitize or validate user-controlled input (User-Agent header) before storing it in logs that are exported to CSV format. CSV parsers like Excel automatically execute formulas beginning with special characters (=, +, -, @) without user confirmation.

## Attacker mindset
Thorough reconnaissance and persistence when initial attack vectors fail. The attacker noted limited application interaction but continued probing, ultimately discovering that modifying HTTP headers could affect logged data. This demonstrates the value of understanding data flow and export functionality as attack surfaces.

## Defensive takeaways
- Sanitize all user-controllable input before logging, especially HTTP headers
- Prefix potentially dangerous data with single quotes or safe characters when exporting to CSV
- Implement input validation on User-Agent and other headers to reject or escape formula-like patterns
- Configure Excel and other office applications to disable automatic formula execution for imported data
- Apply principle of least privilege so even if admin credentials are compromised, impact is limited
- Log data in structured formats (JSON) rather than CSV when possible, and validate on import
- Implement Content Security Policy and application-level controls to restrict formula injection patterns

## Variant hunting
['Check other HTTP headers (Referer, X-Forwarded-For, Accept-Language) for similar CSV injection in logs', 'Test CSV export functionality in other admin panels (payment logs, user actions, error logs)', 'Investigate if application exports other user-generated content to CSV without sanitization', 'Check for similar vulnerabilities in webhook logs or API request logging features', 'Test if error messages or stack traces are logged and exported, potentially containing formulas', 'Examine database backup/export functionality for CSV injection vulnerabilities']

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1566
- T1566.001

## Notes
The writeup demonstrates a realistic attack chain where an unauthenticated user can achieve code execution on privileged accounts. The vulnerability chain relies on three factors: (1) unvalidated input in logs, (2) CSV export functionality accessible to admins, and (3) automatic formula execution in Excel. While the author used a benign PoC (=1+1), the formula =cmd|' /C calc'!A0' demonstrates full command execution capability. This is a critical vulnerability affecting confidentiality, integrity, and availability of systems.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
