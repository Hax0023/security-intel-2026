# Full Path Disclosure via Type Juggling in Group Creation

## Metadata
- **Source:** HackerOne
- **Report:** 8090 | https://hackerone.com/reports/8090
- **Submitted:** 2014-04-19
- **Reporter:** faisalahmed
- **Program:** Localize.io
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Full Path Disclosure (FPD), Type Juggling/Type Confusion
- **CVEs:** None
- **Category:** web-api

## Summary
A Full Path Disclosure vulnerability exists in the group creation functionality where improper input validation allows attackers to trigger PHP warnings that leak sensitive server path information. By sending an array instead of a string to the 'addGroup[name]' parameter, the application fails to properly validate input types, causing PHP's trim() function to throw an error message revealing the file system structure.

## Attack scenario
1. Attacker navigates to the create group page on the target application
2. Attacker identifies the 'addGroup[name]' parameter used in POST requests
3. Attacker modifies the parameter syntax to 'addGroup[name][]' to force an array instead of string
4. Attacker submits the modified POST request with CSRF token
5. PHP trim() function receives array instead of expected string parameter
6. Application returns unhandled PHP warning containing full server path (/var/www/vhosts/...)

## Root cause
Insufficient input validation and type checking before passing user input to the trim() function. The application does not validate that 'addGroup[name]' is a string before processing it, and error handling is not configured to suppress PHP warnings in production environments.

## Attacker mindset
Information gathering reconnaissance. Attacker uses simple syntax manipulation (adding '[]') to explore application behavior and discover server architecture details that could be useful for future exploitation or social engineering.

## Defensive takeaways
- Implement strict input validation and type checking on all user inputs before processing
- Validate that expected parameters are of correct type (string vs array) before function calls
- Configure PHP error reporting to not display warnings/errors to end users in production
- Use error suppression (@trim()) or try-catch blocks as last resort defense layer
- Implement WAF rules to detect and block obvious parameter manipulation attempts
- Regular security testing including fuzzing parameter types and structures

## Variant hunting
Similar FPD vulnerabilities likely exist in other form processing functions. Search for: (1) Other POST endpoints accepting group/project names with insufficient validation, (2) Any functions using trim(), explode(), or string functions without type checking, (3) Similar array injection patterns in user profile, settings, or upload functionality, (4) Parameters with similar naming conventions that might be vulnerable

## MITRE ATT&CK
- T1590.004
- T1592
- T1040

## Notes
This is a low-severity information disclosure rather than a critical vulnerability, as FPD alone typically does not enable direct exploitation. However, it leaks valuable reconnaissance information (server OS, hosting provider, directory structure) that attackers can use to identify other vulnerabilities. The vulnerability demonstrates a common pattern where developers forget to validate input types when using flexible PHP syntax. The reporter's systematic approach to finding multiple similar issues suggests a thorough security audit methodology.

## Full report
<details><summary>Expand</summary>

Hi,
I found another information disclosure vulnerability/Full Path Disclosure on your application.
this time its on Creating New Group Section.

Proof of Concept
-------------------------

GET  : http://www.localize.io/pages/create_project/ [project ID]
POST CONTENT: CSRFToken=TOKEN VALUE&addGroup[name][]=new+group

I just Added "[]" after *addGroup[name]* and Replied.

### The information from page:
> Warning: trim() expects parameter 1 to be string, array given in /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/classes/Phrase.php on line 213

I Also Added a Screenshot of that FPD as attachment..
Hope You'll fix this one also..
Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
