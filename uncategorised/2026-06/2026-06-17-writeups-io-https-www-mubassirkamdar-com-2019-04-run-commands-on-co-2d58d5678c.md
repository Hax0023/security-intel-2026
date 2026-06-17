# CSV Injection in Activity Log Export - Remote Command Execution on Admin Machine

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Redacted Company (Private Disclosure)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Remote Code Execution, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
A CSV injection vulnerability was discovered in the activity log export feature that allows an attacker to inject Excel formulas into the user agent field during failed login attempts. When an administrator downloads the activity log as a CSV file, the malicious formula executes on their machine with their privileges, enabling arbitrary command execution.

## Attack scenario (step by step)
1. Attacker creates an account on the target application (redacted.com)
2. Attacker navigates to the login page and attempts authentication with a company employee's email and random password
3. Attacker intercepts the failed login HTTP request using a proxy tool
4. Attacker modifies the User-Agent header to contain a malicious Excel formula such as '=cmd|' /C calc'!A0' or similar payload
5. Attacker forwards the modified request, causing the formula to be logged in the activity log database
6. Administrator reviews activity logs and exports them as a CSV file for analysis
7. When the CSV file is opened in Microsoft Excel or similar spreadsheet software, the formula is executed with the administrator's system privileges, launching the arbitrary command

## Root cause
The application fails to sanitize or escape user-controlled input (User-Agent header) before storing it in activity logs and exporting to CSV format. Excel and other spreadsheet applications execute formulas that begin with special characters (=, +, -, @) without user confirmation, treating them as legitimate spreadsheet functions rather than data.

## Attacker mindset
The attacker demonstrates persistence and lateral thinking by identifying an indirect attack vector through limited application interaction. Rather than abandoning the target after failing to find common vulnerabilities, they studied the application's functionality thoroughly, discovered the activity logging feature, and recognized that CSV export functionality combined with unsanitized headers could be weaponized for command execution. The attacker cleverly uses the legitimate failed login mechanism to inject payloads that reach administrative users.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-controlled data, especially headers like User-Agent, regardless of apparent business criticality
- Escape or prefix potentially dangerous characters in CSV exports (=, +, -, @, etc.) before writing to file, or convert them to harmless alternatives
- Apply output encoding specific to CSV format when exporting data that may contain user input
- Implement Content-Security-Policy headers and disable formula execution in exported files when possible
- Consider exporting to safer formats (JSON, XML with proper encoding) or protected Excel formats that require macro confirmation
- Establish logging of all data modifications and exports for audit trails and anomaly detection
- Educate administrators about the risks of opening CSV files from untrusted or user-influenced sources
- Implement allowlisting for User-Agent values if business requirements permit, or enforce format validation

## Variant hunting
['Test other export functions for CSV injection (reports, user lists, transaction logs, audit trails)', 'Examine all HTTP headers for injection opportunities (X-Forwarded-For, Referer, Accept-Language, Custom headers)', 'Investigate whether other file export formats (XLSX, PDF, TSV) are vulnerable to similar injection', 'Check if formula injection exists in search functionality, comments, or descriptions that get exported', 'Probe for second-order CSV injection where data is logged by one user but exported by another', 'Test for LDAP injection, command injection, or SQL injection in user agent fields that might be processed server-side', 'Examine if other social engineering vectors exist (email headers, phone numbers, addresses) that reach CSV exports']

## MITRE ATT&CK
- T1190
- T1203
- T1566
- T1566.001
- T1559
- T1559.002

## Notes
The writeup demonstrates a real-world CSV injection vulnerability with practical exploitation against administrative users. The attacker's methodology of thorough application review after initial enumeration failures is commendable. The severity is heightened because exploitation reaches administrative accounts with likely elevated system privileges. The vulnerability exemplifies how low-interaction attack surfaces can still yield critical findings when researchers invest time in understanding application functionality. The specific formula payload mentioned (=cmd|' /C calc'!A0) is a known CSV injection technique that works in Excel, though syntax variations may be needed depending on Excel version and system configuration.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
