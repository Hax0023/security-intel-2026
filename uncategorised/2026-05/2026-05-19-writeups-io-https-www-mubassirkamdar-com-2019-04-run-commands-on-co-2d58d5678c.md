# CSV Injection via User-Agent Header in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Redacted company (not disclosed)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
A CSV injection vulnerability was discovered in the activity log export functionality where user-supplied input (User-Agent header) from failed login attempts was not sanitized before being written to downloadable CSV files. An attacker could inject malicious Excel formulas that execute commands on the administrator's machine when the log is opened in a spreadsheet application.

## Attack scenario (step by step)
1. Attacker performs reconnaissance on target web application and identifies login functionality with activity logging
2. Attacker creates an account and performs multiple failed login attempts while intercepting HTTP requests
3. Attacker modifies the User-Agent header in the intercepted request to contain a malicious Excel formula (e.g., '=cmd|' /C calc'!A0')
4. The modified User-Agent is logged in the activity log and stored in the application database
5. Administrator downloads the activity log in CSV format from the admin panel
6. When administrator opens the CSV file in Excel or similar spreadsheet application, the formula is auto-executed, running arbitrary commands on the administrator's machine

## Root cause
The application failed to sanitize or properly escape user-controlled data (User-Agent header) before exporting it to CSV format. The CSV export functionality did not implement input validation or output encoding to prevent formula injection attacks.

## Attacker mindset
The attacker demonstrated persistence and lateral thinking by thoroughly testing the application despite initial disappointment with low interaction surfaces. Upon discovering the activity log feature, they recognized the injection point and understood the export-to-spreadsheet workflow, enabling exploitation of a feature typically considered low-risk.

## Defensive takeaways
- Implement strict input validation on all user-controlled headers (User-Agent, X-Forwarded-For, etc.)
- Sanitize all data before CSV export by escaping formula-starting characters (=, +, -, @, tab, carriage return)
- Prefix suspicious data with a single quote (') to prevent formula interpretation in spreadsheet applications
- Set HTTP headers to force CSV files to download as plain text rather than executable spreadsheets
- Implement Content-Disposition headers with appropriate charset and ensure files are opened in read-only mode
- Apply whitelist validation to User-Agent and other header values where possible
- Test CSV export functionality as part of security testing procedures
- Educate administrators about the risks of opening untrusted files from user activity logs

## Variant hunting
['Check other export functionalities (PDF, Excel, JSON) for similar injection vulnerabilities', 'Test other user-controlled headers (X-Forwarded-For, Referer, Accept-Language) in logging and export features', 'Examine error logs, audit logs, and any admin-accessible logs for similar injection points', 'Look for other features that display user input in exportable formats', 'Test CSV injection in comment fields, search queries, or any user input reflected in reports', 'Check if similar formula injection exists in other spreadsheet-generation features']

## MITRE ATT&CK
- T1190
- T1059
- T1566
- T1203

## Notes
This is a well-documented example of CSV injection leading to RCE. The vulnerability chain is particularly effective because: (1) the attack vector (User-Agent) is inconspicuous and may bypass input validation focused on obvious fields, (2) the log export feature is typically considered administrative/low-risk, and (3) users are unlikely to suspect malicious code in system activity logs. The writeup lacks specific bounty amount and company name, but the technical details are clear and reproducible.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
