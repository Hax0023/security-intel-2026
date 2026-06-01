# CSV Injection via User-Agent Header in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** redacted.com
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
A CSV injection vulnerability was discovered in the activity log export functionality where user-controlled input (User-Agent header) from failed login attempts was not sanitized before being exported to CSV format. An attacker could inject Excel formulas into the User-Agent field that would execute arbitrary commands when an administrator opens the downloaded CSV file in a spreadsheet application.

## Attack scenario (step by step)
1. Attacker attempts to login to a target employee account using a company email address with an incorrect password
2. Attacker intercepts the failed login request and modifies the User-Agent header to contain a malicious Excel formula (e.g., '=cmd|' /C calc'!A0')
3. The failed login attempt is recorded in the activity log with the injected User-Agent formula stored in the database
4. Administrator reviews account activity and exports the activity log as a CSV file
5. Administrator opens the downloaded CSV file in Microsoft Excel or similar spreadsheet application
6. Excel automatically executes the formula, running the arbitrary command (calculator, reverse shell, etc.) on the administrator's machine with their privileges

## Root cause
Insufficient input validation and output encoding on user-supplied data (User-Agent header) before inclusion in CSV exports. The application failed to sanitize or escape formula characters (=, +, -, @) that trigger code execution in spreadsheet applications.

## Attacker mindset
The attacker recognized that activity logs containing user-controlled input (User-Agent) represented an overlooked attack surface. They understood that while direct XSS/CSRF were not present, the export functionality created a secondary attack vector targeting administrators. By targeting the User-Agent header rather than typical input fields, they exploited the assumption that HTTP headers would not be weaponized.

## Defensive takeaways
- Sanitize all user-supplied input before including it in CSV exports, especially prefixing formula characters with single quotes or spaces
- Implement strict input validation on HTTP headers like User-Agent, limiting to known safe formats
- Apply output encoding appropriate for the export format (CSV escaping) to all dynamic content
- Configure spreadsheet applications to disable automatic formula execution or prompt users before executing formulas
- Log and monitor suspicious User-Agent strings that contain formula syntax patterns
- Validate that exported data does not contain special characters that trigger formula evaluation
- Implement Content Security Policy headers and consider disabling formula execution in exported reports by default

## Variant hunting
['Check other CSV/Excel export functionalities for similar formula injection (reports, user lists, transaction logs)', 'Test other HTTP headers for CSV injection (Referer, Accept-Language, X-Forwarded-For, Custom headers)', 'Review any fields populated from user input or external sources before CSV export', 'Test PDF/JSON exports for similar injection patterns', 'Search for other activity logs or audit trails that may include user-controlled data', 'Verify if formula injection works with other formula syntaxes (Google Sheets, LibreOffice)', 'Check if similar vulnerabilities exist in batch operations or scheduled report generation']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1203: Exploitation for Client Execution
- T1566: Phishing (attachment-based if exported file is sent)
- T1059: Command and Scripting Interpreter

## Notes
The vulnerability demonstrates the importance of treating all user-controllable data as potentially malicious, including HTTP headers. The attack is particularly dangerous because it targets administrators who have higher privileges. The writeup uses a PoC with a calculator instead of a destructive payload, showing responsible disclosure practices. The attacker's persistence in reconnoitering the application after initial easy-win attempts paid off, highlighting that thorough application analysis of all features is essential.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
