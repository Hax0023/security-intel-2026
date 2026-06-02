# CSV Injection via User-Agent Header in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Redacted company (not specified)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
An attacker can inject malicious Excel formulas into the User-Agent header during failed login attempts, which are logged and exported by administrators as CSV files. When the CSV is opened in Excel, the formula executes arbitrary commands on the administrator's machine. This vulnerability allows remote code execution on company machines through a simple login attempt.

## Attack scenario (step by step)
1. Attacker navigates to the target application's login page
2. Attacker enters a valid company email address and incorrect password to trigger a failed login attempt
3. Attacker intercepts the HTTP request and modifies the User-Agent header to contain a malicious Excel formula such as =cmd|'/C calc'!A0
4. The failed login attempt is recorded in the activity log with the attacker's malicious User-Agent string
5. Administrator checks the activity log and exports it as a CSV file for analysis
6. When the administrator opens the CSV file in Microsoft Excel, the formula is executed automatically, launching the specified command (e.g., calculator) on the admin's machine

## Root cause
The application fails to sanitize user-controlled input (User-Agent header) before storing it in activity logs. Additionally, when exporting logs to CSV format, the application does not escape or neutralize formula characters (=, +, -, @, etc.) that Excel interprets as executable formulas. The assumption that only administrators view logs provided false security.

## Attacker mindset
The attacker demonstrates methodical reconnaissance and persistence by testing common vulnerabilities first, then pivoting to less obvious attack surfaces. Upon discovering limited application interaction, rather than giving up, the attacker analyzed all available functions, identified the logging mechanism, and recognized that unsanitized user-controlled input in logs exported to CSV could be weaponized. The attacker understood Excel's dangerous formula auto-execution behavior and crafted a practical exploit that uses social engineering (relying on admin action) combined with technical vulnerability.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-controlled data, including headers like User-Agent
- Sanitize or escape special characters (=, +, -, @, etc.) before storing data that may be exported to spreadsheet formats
- When exporting to CSV, prefix potentially dangerous values with a single quote (') to prevent formula interpretation
- Disable automatic formula execution in spreadsheet applications through security policies and configuration
- Implement Content Security Policy and output encoding based on the destination format (CSV, Excel, etc.)
- Conduct security awareness training for administrators about the dangers of opening untrusted CSV exports
- Use safer export formats that don't support formula execution (e.g., PDF for read-only reporting)
- Log sanitization should occur at the point of export, not just at storage
- Apply the principle of least privilege to limit who can access and export logs

## Variant hunting
['Check other user-controlled HTTP headers (X-Forwarded-For, Referer, Accept-Language, etc.) for similar CSV injection in other exported logs', 'Test if other failed actions or error conditions also get logged with unsanitized input', 'Examine all CSV export functionality across the application for similar vulnerabilities', 'Test if the vulnerability persists in other export formats (Excel xlsx, PDF, JSON)', 'Investigate if the same injection technique works in other logging mechanisms (audit logs, API logs, webhook events)', 'Check if successful login attempts also log User-Agent and are accessible for export', 'Test whether the injection works with alternative formula syntaxes (@, -, +, or variations)', 'Determine if other headers like X-Custom-Header, Authorization, or cookies are also logged without sanitization']

## MITRE ATT&CK
- T1190
- T1566.002
- T1203
- T1059.001
- T1005

## Notes
The writeup uses a generic example (=1+1) for demonstration purposes but acknowledges the real attack payload (=cmd|'/C calc'!A0). The vulnerability is particularly dangerous because it requires minimal interaction from the attacker and relies on expected administrative behavior. The attack chain demonstrates how seemingly low-risk functions (login logging) can become critical security issues when combined with insecure data export. The writeup illustrates good security research methodology by showing persistence through apparent dead ends and thorough application analysis.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
