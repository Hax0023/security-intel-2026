# CSV Injection via User Agent Header - Remote Command Execution on Admin Machine

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** redacted.com
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** CSV Injection, Formula Injection, Remote Code Execution, Improper Input Validation
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
A CSV injection vulnerability exists in the activity log export functionality where user-controlled data (User-Agent header) is not sanitized before being written to CSV files. An attacker can inject Excel formulas into the User-Agent field which execute when an administrator downloads the activity log, achieving remote command execution on the admin's machine.

## Attack scenario (step by step)
1. Attacker creates an account on redacted.com or attempts login with company email
2. Attacker intentionally provides incorrect credentials to trigger failed login event logged in activity log
3. Attacker intercepts the login request and modifies the User-Agent header to contain Excel formula payload (e.g., '=cmd|' /C calc'!A0' or '=1+1')
4. Attacker forwards the modified request, causing the malicious User-Agent to be stored in the activity log database
5. Administrator accesses the activity log and exports it as CSV format
6. When administrator opens the CSV file in Excel or similar spreadsheet application, the formula is executed on their machine, running arbitrary commands

## Root cause
The application fails to sanitize or escape user-controlled input (User-Agent header) before exporting it to CSV format. CSV injection occurs because spreadsheet applications interpret formulas starting with '=', '+', '-', or '@' as executable code rather than literal strings.

## Attacker mindset
Persistence and lateral thinking - after finding limited attack surface through common vulns (XSS, CSRF, session issues), the attacker noticed a secondary feature (activity logging) and identified an unexpected trust boundary (User-Agent header) as injectable. The attacker recognized that admin-only functionality could be weaponized to compromise privileged users.

## Defensive takeaways
- Sanitize all user input regardless of origin (headers, parameters, etc.) before exporting to CSV
- Prefix exported CSV data with single quotes or spaces to prevent formula interpretation (e.g., ' =1+1')
- Validate User-Agent headers and reject suspicious patterns
- Implement Content-Disposition: attachment; filename=X headers with proper MIME types to force download behavior
- Use CSV libraries that automatically escape dangerous characters
- Implement strict Content-Security-Policy headers
- Log and monitor for suspicious User-Agent patterns in activity logs
- Educate administrators about risks of opening untrusted CSV files

## Variant hunting
['Check other export functions (PDF, Excel, JSON) for similar injection issues', 'Test other HTTP headers (Referer, X-Forwarded-For, X-Original-URL) for injection in logs', 'Examine error logs and debug logs exported to CSV format', "Look for formula injection in API response data that's exported as CSV", 'Test file upload functionality where filenames are exported in activity reports', 'Check database backup/export features for CSV injection in metadata fields', 'Verify if other user-controlled fields (email, username, comment fields) in logged activities are vulnerable']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1598.003 - Phishing: Spearphishing Link
- T1566.001 - Phishing: Spearphishing Attachment
- T1204.002 - User Execution: Malicious File

## Notes
The writeup uses intentionally generic formulas (=1+1) to demonstrate the concept safely, but notes that real attackers could use '=cmd|' /C calc'!A0' to execute arbitrary system commands. This is a chained attack requiring user interaction from the privileged admin user. The vulnerability is critical in environments where CSV exports are opened directly in spreadsheet applications without user awareness of formula injection risks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
