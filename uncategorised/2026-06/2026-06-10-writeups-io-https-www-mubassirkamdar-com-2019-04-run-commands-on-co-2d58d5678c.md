# CSV Injection via User Agent in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Redacted company (name withheld)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
An attacker can inject malicious Excel formulas into the User Agent field during failed login attempts, which are logged and exported as CSV by administrators. When an admin downloads the activity log and opens it in Excel, the formula executes arbitrary commands on the admin's machine.

## Attack scenario (step by step)
1. Attacker navigates to the target website's login page
2. Attacker enters a company email address and random password to trigger a failed login
3. Attacker intercepts the login request and modifies the User Agent header to contain a malicious Excel formula (e.g., '=cmd|\' /C calc\'!A0')
4. The failed login attempt is recorded in the activity log with the malicious User Agent payload
5. Company administrator reviews activity logs and exports them as CSV format
6. Admin opens the CSV file in Microsoft Excel, which automatically executes the formula, launching calculator or executing arbitrary commands on the admin's machine

## Root cause
Insufficient input validation and sanitization of the User Agent header before storing it in the activity log. The application fails to escape or neutralize characters that have special meaning in spreadsheet applications (=, +, -, @, tab).

## Attacker mindset
After exhausting common vulnerability vectors (XSS, CSRF, session issues), the attacker performed deeper application analysis. Upon discovering that user-controlled input (User Agent) was logged and exportable as CSV, they recognized the CSV injection vector as a way to achieve code execution on privileged users' machines, escalating from low-interaction bugs to RCE.

## Defensive takeaways
- Sanitize all user-controlled input before logging, particularly HTTP headers and request metadata
- Prefix untrusted data in CSV exports with a single quote (') to prevent formula execution in spreadsheet applications
- Implement Content Security Policy and disable macro execution in spreadsheet applications
- Validate and normalize User Agent strings; reject suspiciously formatted values
- Use security headers like X-Content-Type-Options to enforce safe content handling
- Educate users about dangers of opening untrusted CSV files with formula evaluation enabled
- Consider exporting logs in safer formats (JSON, XML) or using dedicated log analysis tools instead of CSV
- Implement output encoding specific to CSV format in the export functionality
- Log sanitization functions should run before data reaches the database

## Variant hunting
['Check other log export features (authentication logs, API logs, transaction logs) for similar CSV injection', 'Test other HTTP headers for CSV injection (Referer, Accept-Language, X-Forwarded-For)', 'Look for other data sources that feed into Excel exports (user profiles, reports, analytics)', 'Test CSV injection with different formula prefixes (=, +, -, @, tab character)', 'Investigate if injection works in other spreadsheet applications (Google Sheets, LibreOffice)', 'Check if downloaded files execute formulas without user interaction in newer Excel versions with security updates']

## MITRE ATT&CK
- T1190
- T1203
- T1559.001
- T1204.002

## Notes
The writeup demonstrates good security research methodology by thoroughly examining application functionality after initial reconnaissance. The proof-of-concept uses a benign formula (=1+1) during testing, which is responsible security practice. The actual exploitation path (=cmd|' /C calc'!A0) could achieve arbitrary code execution. The vulnerability highlights why even 'limited interaction' applications warrant deep investigation. No specific bounty amount is mentioned in the writeup.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
