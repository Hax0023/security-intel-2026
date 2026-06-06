# CSV Injection via User-Agent Header in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Redacted company (not disclosed)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
A CSV injection vulnerability was discovered in the activity log export functionality where user-controlled input (User-Agent header) was not sanitized before being written to CSV files. An attacker could inject Excel formulas through the User-Agent header during failed login attempts, which would execute arbitrary commands on the administrator's machine when the CSV file was opened in Excel.

## Attack scenario (step by step)
1. Attacker navigates to the target application's signup/login page
2. Attacker performs multiple failed login attempts while modifying the User-Agent header to contain malicious Excel formulas (e.g., '=cmd|' /C calc'!A0')
3. The failed login attempts are logged in the activity log with the malicious User-Agent stored without sanitization
4. Administrator accesses the activity log and downloads it as a CSV file
5. Administrator opens the CSV file in Microsoft Excel or similar spreadsheet application
6. Excel automatically executes the injected formula, running arbitrary commands on the administrator's machine with their privileges

## Root cause
The application failed to sanitize or validate user-controlled input (User-Agent header) before including it in CSV export files. Most spreadsheet applications automatically interpret cells beginning with formula indicators (=, +, -, @) as formulas and execute them, creating a code execution vector.

## Attacker mindset
The researcher demonstrated excellent persistence and lateral thinking by continuing enumeration after initial low-hanging fruit findings. Instead of giving up on limited-interaction targets, they thoroughly tested all application functions and identified an unconventional attack vector through seemingly benign logging mechanisms. This reflects the mindset that comprehensive testing of all input vectors, including HTTP headers, can reveal critical vulnerabilities.

## Defensive takeaways
- Sanitize all user-controlled input before including in CSV/Excel exports by prefixing suspicious characters with single quotes or removing formula indicators
- Implement strict input validation on all HTTP headers, not just request bodies
- Use secure CSV generation libraries that automatically escape formula characters
- Configure Excel/spreadsheet applications to disable automatic formula execution or use safer file formats like ODS
- Log security-relevant events (failed logins) with minimal user-controlled data or with heavily validated/controlled data only
- Apply principle of least privilege to administrator accounts and restrict access to activity logs
- Implement Content Security Policy for downloaded files to restrict execution contexts

## Variant hunting
['Check other CSV export features for similar injection points (user profiles, reports, audit logs, transaction histories)', 'Test other HTTP headers for injection (Referer, Accept-Language, X-Forwarded-For, custom headers)', 'Examine other logging mechanisms that might export to spreadsheet formats', 'Test direct formula injection in any user-controllable fields that appear in reports', 'Look for PDF export features that might have similar issues with formula interpretation', 'Check for LDAP injection in user agent fields that might be logged and exported', 'Test for similar injection in backup/export functionality across different modules']

## MITRE ATT&CK
- T1190
- T1204.002
- T1566.002
- T1203
- T1598.003

## Notes
The writeup lacks specific details about the company name, bounty amount, and disclosure timeline. The POC uses '=1+1' as a safe demonstration but shows the dangerous payload '=cmd|' /C calc'!A0' for actual command execution. This vulnerability is particularly dangerous because it leverages administrative functionality and requires minimal attacker privileges (ability to trigger failed logins). The attack has high impact as it affects high-value targets (administrators) with significant capabilities. The researcher's approach demonstrates the importance of understanding business logic and file export functionality in security testing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
