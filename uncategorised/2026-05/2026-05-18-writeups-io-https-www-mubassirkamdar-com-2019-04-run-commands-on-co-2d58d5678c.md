# CSV Injection via User-Agent Header in Activity Log Export

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Redacted company (not disclosed)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** CSV Injection, Formula Injection, Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2019/04/run-commands-on-company-machines-csv.html?m=1

## Summary
A CSV injection vulnerability was discovered in an application's activity log feature where user-controlled input (User-Agent header) was not sanitized before being exported to CSV format. When an admin downloaded the activity log as a CSV file, embedded Excel formulas in the User-Agent field would execute arbitrary commands on the admin's machine.

## Attack scenario (step by step)
1. Attacker creates an account on the target application
2. Attacker initiates a failed login attempt while intercepting the HTTP request
3. Attacker modifies the User-Agent header to contain a malicious Excel formula (e.g., '=cmd|'/C calc'!A0')
4. The malicious User-Agent is logged in the application's activity log database
5. Company administrator reviews the activity log and exports it as a CSV file
6. When the admin opens the CSV in Excel, the formula executes, running arbitrary commands (e.g., opening calculator, reverse shell) on the admin's machine

## Root cause
Insufficient input validation and output encoding of the User-Agent header before CSV export. The application failed to sanitize or escape formula-like characters (=, +, -, @) that Excel interprets as formulas when opening CSV files.

## Attacker mindset
The attacker demonstrated patience and thorough enumeration by identifying a low-interaction attack surface. Rather than giving up on common vulnerabilities, the attacker methodically tested all application functions, identified the activity log feature, and recognized that CSV exports could be abused for code execution. The attack cleverly exploits trust in admin actions (downloading logs) combined with Excel's automatic formula evaluation.

## Defensive takeaways
- Implement strict input validation on all headers including User-Agent, sanitizing or rejecting formula-like characters
- Apply output encoding when exporting data to CSV format - prefix suspicious values with a single quote or space to prevent formula interpretation
- Educate users about CSV injection risks and recommend disabling automatic formula execution in spreadsheet applications
- Use safer export formats like JSON or properly-escaped CSV with content-type headers that prevent automatic formula evaluation
- Implement a Web Application Firewall (WAF) rule to detect and block formula injection patterns in request headers
- Log sanitized, safe versions of user-controlled data rather than raw input values
- Regular security testing should include export/download functionality testing with malicious payloads

## Variant hunting
['Test other user-controlled headers (X-Forwarded-For, Referer, Authorization) that might be logged and exported', 'Check for CSV injection in error messages or debug logs that get exported', 'Attempt formula injection in other export formats (PDF, JSON) that might still interpret formulas', 'Test if logged data from comment fields, feedback forms, or chat functions are vulnerable to similar injection', 'Investigate if other admin-accessible reports or analytics dashboards have similar export vulnerabilities', 'Look for CSV injection in search results or filtered data exports', "Test formula injection with alternative payloads: '@SUM', '+2+5+cmd', '-2+5+cmd|calc'", 'Check if the application logs request bodies or POST parameters that could also be exported']

## MITRE ATT&CK
- T1190
- T1203
- T1566
- T1564
- T1204

## Notes
The writeup lacks specific details about the company, bounty amount, and verification status. The payload example '=cmd|'/C calc'!A0' is somewhat non-standard syntax; typical CSV injection payloads use '=cmd|'/C command'!A1'. The vulnerability demonstrates how seemingly non-exploitable features (activity logs) can become attack vectors when combined with user-controlled data and export functionality. This is a good example of why all data flows should be considered, regardless of limited application interaction.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
