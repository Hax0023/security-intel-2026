# CSV Injection via User Agent Leading to Arbitrary Code Execution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Redacted company web application
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
An attacker can inject malicious Excel formulas into the User-Agent header during failed login attempts, which get logged in an activity log accessible to administrators. When the admin exports and opens the CSV file, the formula executes arbitrary commands on their machine. This allows remote code execution on company systems through a seemingly innocuous activity log export feature.

## Attack scenario (step by step)
1. Attacker navigates to the target application's login page (redacted.com/login/index)
2. Attacker enters a company email address and random password to trigger a failed login
3. Attacker intercepts the HTTP request and modifies the User-Agent header to contain a malicious Excel formula such as '=cmd|' /C calc'!A0' or similar payload
4. Attacker forwards the modified request, causing the formula to be logged in the activity log associated with that email account
5. Administrator views the account activity log and exports it to CSV format for review
6. When the administrator opens the downloaded CSV file in Excel or similar application, the formula automatically executes, launching calc.exe or any other specified command on the administrator's machine

## Root cause
The application fails to sanitize user-supplied input (User-Agent header) before storing it in logs and exporting to CSV format. Additionally, the CSV export does not escape or neutralize formula characters (=, +, -, @, etc.) that Excel interprets as executable formulas. This creates a post-authentication code execution vector through administrative functionality.

## Attacker mindset
The researcher demonstrates methodical reconnaissance and patience, moving beyond low-hanging fruits to identify non-obvious attack surfaces. They recognize that administrative export features are valuable targets and understand the dangerous combination of unsanitized user input + spreadsheet formula interpretation. The attacker tests with benign formulas (=1+1) before weaponizing, showing ethical restraint during disclosure.

## Defensive takeaways
- Implement input validation and sanitization on all user-supplied data, including HTTP headers like User-Agent
- Apply output encoding when exporting data to CSV—prefix formula characters (=, +, -, @) with a single quote or use alternative safe formats
- Use security libraries designed for safe CSV generation that automatically escape dangerous patterns
- Log normalization: sanitize or validate all logged data regardless of source before making it available for export
- Consider alternative data export formats (JSON, XML with proper escaping) that are less prone to formula injection
- Educate administrators about the risks of opening untrusted CSV files and enable warnings in spreadsheet applications
- Implement content security policies and restrictions on formula execution in exported reports

## Variant hunting
['Search for other administrative export functions (reports, audits, analytics) that may log unsanitized user input', 'Test other HTTP headers (Referer, X-Forwarded-For, Accept-Language) for CSV injection in logging systems', 'Examine error messages and debug logs that may be exported—these often contain unsanitized request data', 'Check API endpoints that generate downloadable reports or data extracts', 'Test file upload features where User-Agent or other headers might influence generated output files', 'Look for CSV/Excel export features in user management, activity logs, analytics dashboards, and audit trails']

## MITRE ATT&CK
- T1190
- T1203
- T1559.001
- T1566.001
- T1204.002

## Notes
The writeup lacks specific bounty amount and exact company name (redacted for privacy). The payload example '=cmd|' /C calc'!A0' appears to be pseudo-code rather than a valid Excel formula syntax. Valid formulas would use DDE or similar vectors. The vulnerability is particularly dangerous because it targets administrators/privileged users through a trust-worthy internal feature. The researcher's ethical approach of testing with '=1+1' before providing weaponized payloads is noteworthy. This represents a common pattern where internal administrative features become high-value attack surfaces due to reduced security scrutiny.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
