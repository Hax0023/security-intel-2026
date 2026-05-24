# Full Path Disclosure via Session ID Validation Error

## Metadata
- **Source:** HackerOne
- **Report:** 7736 | https://hackerone.com/reports/7736
- **Submitted:** 2014-04-16
- **Reporter:** benamarouche
- **Program:** Concrete5
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
Full Path Disclosure (FPD) vulnerability in Concrete5 that reveals the absolute filesystem path through error messages when invalid session IDs are provided. The vulnerability exposes sensitive path information (/home/enterpri/public_html/...) that could be leveraged in conjunction with other attacks like SQL injection.

## Attack scenario
1. Attacker crafts an oversized or malformed CONCRETE5 session cookie containing illegal characters
2. Application validates the session ID in session.php and triggers an error due to invalid input
3. PHP error handler outputs a detailed warning message containing the full filesystem path
4. Attacker extracts the exposed path structure (/home/enterpri/public_html/updates/concrete5.6.1.2_updater/concrete/startup/session.php)
5. Attacker uses revealed paths in subsequent attacks, such as SQL injection with LOAD_FILE() function
6. Attacker gains unauthorized access to source code or sensitive files using the known paths

## Root cause
Improper error handling and information disclosure in session validation logic. The application displays verbose PHP error messages directly to users instead of logging them securely and showing generic error pages. Error suppression operator (@) was not used on session_start() call.

## Attacker mindset
Information gathering phase of reconnaissance. Path disclosure is valuable for chaining attacks; knowing exact file locations enables more precise SQL injection payloads using LOAD_FILE(), LFI attacks, and targeted exploitation of known vulnerable components.

## Defensive takeaways
- Configure PHP error_reporting to not display errors to users (set display_errors=Off in production)
- Implement custom error handlers that log detailed errors server-side while showing generic messages to clients
- Use error suppression operators carefully or wrap sensitive functions in try-catch blocks
- Validate and sanitize session IDs before passing to session_start()
- Remove version numbers and paths from error messages displayed to users
- Implement Web Application Firewall (WAF) rules to detect and block suspicious session parameters

## Variant hunting
Search for other error handling locations in Concrete5 that output file paths. Check file upload handlers, template processing, and database query error messages. Look for verbose logging output accessible via error pages, debug modes, or stack traces. Test other parameters with malformed input (cookies, file upload names, query parameters) to trigger path disclosure.

## MITRE ATT&CK
- T1526
- T1592
- T1087

## Notes
This FPD vulnerability alone is relatively low-severity but gains importance when chained with SQLi. The Concrete5 6.1.2 updater context suggests an older version. Multiple endpoints were reported as affected (/index.php, /tools/required/captcha), indicating a systemic error handling issue. The vulnerability demonstrates why verbose error messages should never reach untrusted users.

## Full report
<details><summary>Expand</summary>

Full Path Disclosure (FPD) vulnerabilities enable the attacker to see the path to the webroot/file. e.g.: /home/omg/htdocs/file/. Certain vulnerabilities, such as using the load_file() (within a SQL Injection) query to view the page source, require the attacker to have the full path to the file they wish to view. 

url: 
http://enterprise.concrete5.com/

How to fix this vulnerability
Review the source code for this script.

How to replicate:
Cookie input CONCRETE5 was set to 
Error message found: 
<b>Warning</b>:  session_start() [<a href='function.session-start'>function.session-start</a>]: The session id is too long or contains illegal characters, valid characters are a-z, A-Z, 0-9 and '-,' in <b>/home/enterpri/public_html/updates/concrete5.6.1.2_updater/concrete/startup/session.php</b> on line <b>36</b><br />

as we can see clearly the full path 

Affected params : 
/ 
/index.php 
/tools/required/captcha 


</details>

---
*Analysed by Claude on 2026-05-24*
