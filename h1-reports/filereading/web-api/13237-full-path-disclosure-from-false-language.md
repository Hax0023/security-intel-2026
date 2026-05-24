# Full Path Disclosure via Invalid Language ID Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 13237 | https://hackerone.com/reports/13237
- **Submitted:** 2014-05-24
- **Reporter:** brook2
- **Program:** Localize.im
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
The application fails to properly validate language ID parameters and exposes detailed server path information through unhandled exceptions. An attacker can enumerate invalid language IDs to trigger verbose error messages revealing the complete file system structure and internal application paths.

## Attack scenario
1. Attacker identifies the language parameter in the URL structure (/projects/{id}/languages/{lang_id})
2. Attacker submits a non-existent or invalid language ID (e.g., 4xX or 3083)
3. Application fails to validate the parameter before processing
4. Exception is thrown and caught by top-level error handler which outputs stack trace
5. Full file paths are disclosed: /srv/data/web/vhosts/www.localize.im/htdocs/classes/Language.php
6. Attacker maps application structure and identifies potential entry points for further attacks

## Root cause
Lack of input validation on language ID parameter combined with verbose error handling that exposes stack traces to users. The application does not sanitize exceptions before display or implement proper error pages.

## Attacker mindset
Information gathering phase - mapping application structure, file locations, class hierarchies, and internal logic flow to identify further vulnerabilities or attack vectors. Full path disclosure significantly reduces reconnaissance time.

## Defensive takeaways
- Implement strict input validation on all user-supplied parameters before processing
- Never display raw exception stack traces to end users; log internally instead
- Create custom error pages that provide helpful user feedback without technical details
- Use try-catch blocks to gracefully handle invalid parameter values and return appropriate HTTP status codes (404, 400)
- Implement centralized error handling middleware that sanitizes output
- Obfuscate or abstract internal file paths in any user-facing output
- Regular security testing of error conditions and invalid inputs

## Variant hunting
Test all URL parameters that accept IDs or identifiers with: non-existent values, negative numbers, extremely large numbers, alphanumeric strings, special characters. Check for similar unhandled exceptions in other endpoints (projects, users, organizations). Look for other Language class method calls that may have similar issues.

## MITRE ATT&CK
- T1598 - Phishing: reconnaissance
- T1592 - Gather Victim Host Information
- T1018 - Enumerate network resources

## Notes
This is a relatively low-severity information disclosure but valuable for attackers during reconnaissance. The actual impact depends on what sensitive information is revealed in the paths. The vulnerability chain shows: invalid input → unhandled exception → information disclosure. Proper input validation would have prevented this entirely.

## Full report
<details><summary>Expand</summary>

https://www.localize.im/projects/3t/languages/4xX

 Fatal error: Uncaught exception 'Exception' with message 'Unknown language ID 3083' in /srv/data/web/vhosts/www.localize.im/htdocs/classes/Language.php:423 Stack trace: #0 /srv/data/web/vhosts/www.localize.im/htdocs/classes/Language.php(221): Language::getLanguageName(3083) #1 /srv/data/web/vhosts/www.localize.im/htdocs/classes/Language.php(217): Language::getLanguageNameFull(3083) #2 /srv/data/web/vhosts/www.localize.im/htdocs/classes/UI.php(1375): Language->getNameFull() #3 /srv/data/web/vhosts/www.localize.im/htdocs/classes/UI.php(208): UI::getPage_Project(Array, Array) #4 /srv/data/web/vhosts/www.localize.im/htdocs/classes/UI.php(183): UI::findPage(6, Array, Array) #5 /srv/data/web/vhosts/www.localize.im/htdocs/index.php(226): UI::getPage(6) #6 {main} thrown in /srv/data/web/vhosts/www.localize.im/htdocs/classes/Language.php on line 423

</details>

---
*Analysed by Claude on 2026-05-24*
