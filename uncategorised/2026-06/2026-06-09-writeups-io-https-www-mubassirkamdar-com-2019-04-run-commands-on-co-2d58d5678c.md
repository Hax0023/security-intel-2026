# CSV Injection via User Agent in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Redacted Company
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
An attacker can inject malicious Excel formulas into the User-Agent header during failed login attempts, which are logged and exported by administrators as CSV files. When an administrator opens the exported CSV in Excel, the formula executes on their machine, enabling arbitrary command execution. This vulnerability allows remote code execution on company machines through a simple login interception.

## Attack scenario (step by step)
1. Attacker navigates to redacted.com/signup and creates an account with valid company email
2. Attacker attempts login with random password to trigger failed login logging
3. Attacker intercepts the failed login request and modifies User-Agent header to contain Excel formula (e.g., =cmd|'/C calc'!A0)
4. Failed login event is recorded in activity log with malicious User-Agent string
5. Administrator reviews account activity and exports activity log as CSV file
6. Administrator opens CSV in Excel; formula auto-executes, running arbitrary commands on administrator's machine

## Root cause
User-Agent header input from login requests is not sanitized before being stored in activity logs and exported as CSV. The application fails to escape or validate formula characters (=, +, -, @) that Excel interprets as executable commands when the CSV is opened.

## Attacker mindset
The attacker demonstrates persistence and creative thinking by identifying a low-interaction attack vector. Rather than giving up after finding no obvious vulnerabilities, they methodically tested application features and recognized that unsanitized user input in exported logs could be exploited through a client-side formula injection attack, achieving code execution without direct application vulnerabilities.

## Defensive takeaways
- Sanitize all user-controlled input before exporting to CSV, especially headers and metadata (User-Agent, IP, timestamps)
- Escape formula characters (=, +, -, @, tab, carriage return) in CSV exports by prepending single quote or using safe alternatives
- Implement output encoding based on export format; use CSV writers that automatically escape dangerous characters
- Validate and normalize User-Agent headers at ingestion point, rejecting overly long or suspicious patterns
- Add Content-Disposition headers to force downloads rather than inline opening in Excel
- Warn users when opening CSV files or disable formula evaluation for exported logs
- Log raw User-Agent values separately from display values; sanitize only for export
- Implement Content Security Policy and disable macros/formulas in exported reports

## Variant hunting
['Check other export functionality (reports, analytics, user lists) for similar CSV injection opportunities', 'Test IP address field in activity logs for formula injection if user can control source IP (via proxy headers)', 'Investigate timestamp and session data fields for formula injection vectors', 'Search for other user-supplied headers (Referer, X-Forwarded-For, Custom headers) being logged and exported', 'Test other export formats (JSON, XML, TSV) for similar injection issues', 'Check administrative dashboards for similar unescaped exports of user-controlled data', 'Review any email/document generation features that might include unsanitized user input']

## MITRE ATT&CK
- T1190
- T1203
- T1559.001
- T1566.001
- T1566.002

## Notes
The writeup uses 'redacted.com' placeholder but lacks specific program details. Bounty amount not disclosed. The proof-of-concept uses benign formulas (=1+1) during testing, demonstrating responsible disclosure. The actual exploit payload (=cmd|'/C calc'!A0) opens calculator as proof-of-concept. This vulnerability is particularly dangerous because it requires no user interaction beyond normal admin functionality, making it a reliable attack vector. The technique is a well-known CSV injection attack but the specific vector (User-Agent logging) is context-dependent and required application-specific reconnaissance to discover.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
