# Full Path Disclosure (FPD) via Type Confusion in Form Parameter Handling

## Metadata
- **Source:** HackerOne
- **Report:** 8088 | https://hackerone.com/reports/8088
- **Submitted:** 2014-04-19
- **Reporter:** faisalahmed
- **Program:** localize.io
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Full Path Disclosure, Type Confusion, Debug Information Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
A Full Path Disclosure vulnerability exists in the project creation endpoint where appending array notation (e.g., `[]`) to form parameters causes type confusion, triggering PHP warnings that expose the absolute file path and internal code location. The vulnerability allows unauthenticated attackers to obtain sensitive server path information by manipulating parameter types sent in POST requests.

## Attack scenario
1. Attacker identifies the project creation endpoint at /pages/create_project/
2. Attacker crafts a POST request with form parameters modified to use array notation (e.g., create_project[name][] instead of create_project[name])
3. The application passes the unexpected array type to the trim() function in UI.php which expects a string parameter
4. PHP raises a type error warning that includes the absolute file path and line number
5. Error message is displayed in the HTTP response revealing internal server structure (e.g., /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/classes/UI.php:1495)
6. Attacker documents the server infrastructure details for further reconnaissance and potential attacks

## Root cause
The application lacks proper input validation and type checking before passing user-supplied parameters to PHP functions. The code does not validate that create_project[name] and create_project[editRepositoryID] are strings before calling trim(), and error reporting is enabled with verbose error messages exposed to users.

## Attacker mindset
An information gatherer performing reconnaissance. The attacker is systematically testing parameter handling to discover server architecture details. This appears to be automated fuzzing or manual testing of common type-confusion patterns, suggesting methodical application testing rather than sophisticated exploitation.

## Defensive takeaways
- Implement strict input validation and type checking before processing user parameters
- Validate parameter types match expected values (string vs array) and reject malformed input
- Disable verbose PHP error reporting in production; log errors server-side only
- Configure error_reporting and display_errors directives to prevent sensitive information disclosure
- Use try-catch blocks or type hints to handle unexpected parameter types gracefully
- Implement a Web Application Firewall (WAF) to detect and block parameter manipulation patterns
- Sanitize and validate all user input, including form parameter structure
- Use custom error pages that don't expose file paths or code locations

## Variant hunting
Test other form parameters with array notation suffixes to identify similar type confusion issues
Try nested array notation (e.g., create_project[name][][]) to trigger different code paths
Test other endpoints with POST parameters to find similar input validation gaps
Attempt to trigger type errors with other string-expecting PHP functions (strlen, explode, etc.)
Check GET request parameters for similar FPD vulnerabilities
Test file upload parameters with unexpected types
Investigate other form handlers for inadequate type checking before function calls

## MITRE ATT&CK
- T1592
- T1598
- T1592.004

## Notes
This is a low-severity but valid information disclosure. While FPD alone rarely enables direct attacks, it provides valuable reconnaissance data. The vulnerability chain involves (1) inadequate input validation, (2) type confusion when passing parameters to built-in PHP functions, (3) exposure of error messages to end users. The IP address 178.77.99.228 was exposed in the error message. Fix priority should be high for preventing information leakage but severity is low since it doesn't directly compromise functionality. Similar to CVE patterns in legacy PHP applications where error reporting wasn't properly configured in production environments.

## Full report
<details><summary>Expand</summary>

Hi,
I found an information disclosure vulnerability/Full Path Disclosure on your application.

Proof of Concept
-------------------------

GET  : http://www.localize.io/pages/create_project/ [project ID]
POST CONTENT: CSRFToken=TOKEN VALUE&create_project[visibility]=1&create_project[name][]=My+Android&create_project[defaultLanguage]=1&create_project[editRepositoryID][]=72

Just Add "[]" after *create_project[name]* and *create_project[editRepositoryID]*

### The information from page:
> Warning: trim() expects parameter 1 to be string, array given in /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/classes/UI.php on line 1495

I Also Added a Screenshot of that FPD as attachment..
Hope You'll fix this one..
Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
