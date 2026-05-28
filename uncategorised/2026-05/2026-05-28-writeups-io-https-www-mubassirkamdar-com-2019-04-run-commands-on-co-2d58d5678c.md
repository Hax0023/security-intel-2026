# CSV Injection via User-Agent Header in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** redacted.com
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
An attacker can inject malicious Excel formulas into the User-Agent header during failed login attempts, which gets logged in the activity log. When an administrator exports this log as a CSV file and opens it in Excel, the formula executes on the admin's machine, enabling arbitrary command execution. This vulnerability chains authentication attempts with insufficient input sanitization in exported data.

## Attack scenario (step by step)
1. Attacker identifies that failed login attempts log User-Agent and IP address to an activity log accessible by administrators
2. Attacker crafts a login request with a malicious User-Agent containing Excel formula payload (e.g., '=cmd|' /C calc'!A0') instead of legitimate user agent string
3. Attacker sends failed authentication request with formula-injected User-Agent; the payload is stored unsanitized in the activity log database
4. Administrator reviews security logs and exports activity log as CSV file for analysis
5. Administrator opens CSV file in Microsoft Excel or compatible spreadsheet application
6. Excel auto-executes the embedded formula, running arbitrary commands (e.g., calculator) on administrator's machine with their privileges

## Root cause
User-supplied input (User-Agent header) is stored in the activity log without sanitization and exported as CSV without proper escaping. CSV format interprets lines beginning with formula characters (=, +, -, @) as executable formulas when opened in spreadsheet applications, combined with lack of input validation and output encoding.

## Attacker mindset
An opportunistic pentester who recognized that limited application functionality could be bypassed through indirect exploitation vectors. Rather than giving up after finding no direct vulnerabilities, they methodically analyzed every feature and data flow, discovering that administrative export functionality could be weaponized. The attacker understood that defensive layers (login protection) could be circumvented by targeting the admin's trust in their own security logs.

## Defensive takeaways
- Sanitize and validate all user input including HTTP headers; treat User-Agent as untrusted data
- When exporting data to CSV, escape formula characters (=, +, -, @, |) at the beginning of cells or prefix with single quote
- Implement output encoding appropriate for the file format (CSV escaping) separate from storage encoding
- Configure spreadsheet applications with security policies disabling automatic formula execution, or use non-executable formats for exports
- Log sanitization should occur at export time, not just storage time
- Implement Content-Disposition headers forcing CSV files to download rather than open in browser
- Monitor and alert on unusual User-Agent patterns in authentication logs
- Educate users not to enable macros when opening exported logs from untrusted sources
- Consider using alternative formats (JSON, XML with proper escaping) instead of CSV for administrative exports

## Variant hunting
['Check other export functions (reports, user lists, transaction logs) for similar CSV injection vulnerabilities', 'Test other HTTP headers (Referer, Accept-Language, X-Forwarded-For) logged and exported by application', 'Look for formula injection in email headers, comment fields, or any user-controlled data exported as spreadsheet formats', 'Test TSV (Tab-Separated Values) exports which may have different escaping rules', 'Check if application logs are exported to other formats (PDF, Excel directly) which may execute formulas', 'Investigate if API responses can be exported and if they contain injection vectors', "Test Unicode and encoding bypasses (e.g., '=1+1' vs encoded variants) to circumvent basic filters"]

## MITRE ATT&CK
- T1190
- T1203
- T1598
- T1566
- T1204
- T1059

## Notes
The writeup demonstrates practical exploitation but lacks specific bounty amount and program confirmation. The researcher chose safe payloads (=1+1, calculator) instead of actual harm, showing responsible disclosure mindset. The vulnerability required social engineering component (waiting for admin to download and open export) but with high impact potential. This is a well-documented CSV injection variant specifically targeting administrative functions. The technique is database-agnostic and would work against any application performing unsanitized CSV export of logged data.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
