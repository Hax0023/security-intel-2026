# CSV Injection via User Agent in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** redacted.com
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
A CSV injection vulnerability was discovered in the activity log export feature where user agent data from failed login attempts was not properly sanitized before being exported to CSV format. An attacker could inject malicious Excel formulas in the User-Agent header that would execute commands on the administrator's machine when the CSV file was opened.

## Attack scenario (step by step)
1. Attacker visits the target application's login page and identifies that failed login attempts are logged with user agent information
2. Attacker intercepts the login request and modifies the User-Agent header to contain a malicious Excel formula such as '=cmd|' /C calc'!A0'
3. Attacker submits the crafted request with the formula-injected User-Agent
4. The malicious User-Agent string is stored in the activity log without proper sanitization
5. Administrator accesses the activity log and exports it as a CSV file
6. When the administrator opens the CSV file in Excel, the formula is automatically executed, running the arbitrary command (e.g., opening calculator) on the victim's machine

## Root cause
User-supplied input from HTTP headers (User-Agent) was logged and exported to CSV format without proper sanitization or encoding, allowing formula injection attacks. The application failed to escape special characters that trigger formula evaluation in spreadsheet applications.

## Attacker mindset
The attacker demonstrated persistence by thoroughly reconnoitering the application, analyzing all available functions, and identifying a non-obvious attack vector through activity logs. They recognized that administrative workflows (downloading logs) could be weaponized when combined with unsanitized user input.

## Defensive takeaways
- Sanitize all user-supplied input before including it in exported files, especially CSV and Excel formats
- Prefix potentially dangerous characters (=, +, -, @) with a single quote or other escape sequence in CSV exports
- Implement input validation on all HTTP headers, not just request bodies
- Use whitelisting for User-Agent headers or reject suspicious patterns
- Apply output encoding appropriate to the export format being used
- Consider exporting to formats that don't support formula evaluation (e.g., plain text, PDF)
- Educate administrators about opening files from untrusted sources and disabling auto-execution of formulas

## Variant hunting
['Test CSV export functionality in other admin panels (reports, audit logs, user lists, transaction logs)', 'Check if other HTTP headers (Referer, X-Forwarded-For, custom headers) are logged and exported without sanitization', 'Test export functionality with different formats (Excel, TSV, JSON) for formula injection', 'Investigate whether file upload features sanitize filenames before CSV export', 'Check if user-controlled data in error messages is exported unsanitized', 'Test for LDAP injection in User-Agent if LDAP is used for authentication logging']

## MITRE ATT&CK
- T1190
- T1203
- T1559
- T1204

## Notes
The writeup uses 'redacted.com' as a placeholder but does not disclose the actual vendor, making it impossible to verify the fix status. The researcher properly demonstrated the concept with low-impact payloads (calculator) rather than destructive commands, showing responsible disclosure practices. The vulnerability required authenticated access (creating an account) but could be exploited via automatic login attempt functionality if available. The severity assessment considers that the payload requires user interaction (opening CSV) and admin-level access to trigger export functionality.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
