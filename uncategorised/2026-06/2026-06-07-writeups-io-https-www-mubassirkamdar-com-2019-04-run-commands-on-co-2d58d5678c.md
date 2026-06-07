# CSV Injection in Activity Log Export Leading to Remote Code Execution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Redacted.com
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** CSV Injection, Formula Injection, Remote Code Execution, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
An attacker can inject Excel formulas into the User-Agent header during failed login attempts, which are logged and later exported as CSV by administrators. When the admin opens the CSV file in Excel, the formula executes arbitrary commands on the administrator's machine with their privileges.

## Attack scenario (step by step)
1. Attacker navigates to redacted.com/signup and creates an account with a company email address
2. Attacker attempts login at redacted.com/login with the company email and random password
3. Attacker intercepts the login request and modifies the User-Agent header to contain malicious Excel formula (e.g., '=cmd|' /C calc'!A0')
4. Failed login attempt is recorded in the activity log with the malicious User-Agent formula embedded
5. Administrator accesses the activity log and exports it as CSV file format
6. Administrator opens the CSV file in Excel, triggering automatic formula execution that runs arbitrary commands (e.g., calculator, reverse shell, credential theft) on the admin's machine

## Root cause
The application fails to sanitize or escape user-controlled input (User-Agent header) before including it in CSV exports. Excel and similar spreadsheet applications automatically interpret cells starting with '=' as formulas and execute them without user consent.

## Attacker mindset
The attacker recognized that CSV injection is viable when combining two factors: (1) unsanitized user input being logged, and (2) export functionality that allows administrators to download logs. The attacker leveraged the attack surface available even with limited application interaction by targeting the activity log feature rather than more obvious endpoints.

## Defensive takeaways
- Sanitize all user-controlled input before including in CSV exports, especially prefixing potential formula characters (=, +, -, @, Tab, CR) with single quote or removing them entirely
- Implement output encoding specific to CSV format across all export functionalities
- Use secure CSV libraries that automatically escape dangerous characters
- Validate and restrict User-Agent header values server-side
- Educate administrators about CSV injection risks and instruct them to open exported files with caution or disable formula evaluation in spreadsheet applications
- Consider exporting to safer formats (PDF, JSON) or using CSV readers without formula interpretation
- Implement Content Security Policy and disable external content execution in exported files
- Log and monitor suspicious User-Agent strings for anomalies

## Variant hunting
['Check all HTTP headers (User-Agent, Referer, X-Forwarded-For, Custom headers) reflected in exportable logs or reports', 'Search for CSV/Excel export functionality in error messages, audit logs, analytics, user activity logs, billing reports, search results', 'Test other injection vectors in logged fields: request parameters, file upload names, error messages, timestamps, IP addresses', 'Look for applications that export user-submitted data to CSV without sanitization (comments, reviews, form submissions)', 'Identify APIs that return CSV data or have CSV export endpoints', 'Hunt for similar vulnerabilities in other admin panel export features across different applications']

## MITRE ATT&CK
- T1190
- T1203
- T1559
- T1566
- T1204

## Notes
This is a well-documented example of CSV injection leading to RCE. The vulnerability is particularly dangerous because it targets administrators with elevated privileges. The PoC uses '=cmd|' /C calc'!A0' syntax which is specific to Microsoft Excel's DDE (Dynamic Data Exchange) feature. Modern versions of Excel have mitigated some DDE attack vectors through security updates. The write-up demonstrates good pentesting methodology by testing all application features systematically rather than giving up on low-interaction applications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
