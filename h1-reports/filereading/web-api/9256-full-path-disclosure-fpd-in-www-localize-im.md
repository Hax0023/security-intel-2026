# Full Path Disclosure (FPD) in www.localize.im via Type Confusion in POST Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 9256 | https://hackerone.com/reports/9256
- **Submitted:** 2014-04-23
- **Reporter:** faisalahmed
- **Program:** localize.im
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Full Path Disclosure, Type Confusion, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can trigger a PHP warning by sending malformed POST parameters with array notation ("[]") to the language/phrase update endpoint, causing the server to disclose the full file system path in error messages. The vulnerability exists due to insufficient input validation on the updatePhrases parameter, which expects scalar values but receives arrays instead.

## Attack scenario
1. Attacker identifies the vulnerable endpoint at /projects/[ID]/languages/[ID] that accepts POST requests with updatePhrases parameters
2. Attacker crafts a malicious POST request with array notation suffix (e.g., updatePhrases[previous][yxr][0][]) to convert expected scalar values into arrays
3. The application passes this array value directly to PHP's trim() function without type validation
4. trim() function receives an array instead of the expected string, triggering a PHP warning/error
5. The error message is displayed in the HTTP response, revealing sensitive path information (/srv/data/web/vhosts/www.localize.im/htdocs/index.php:191)
6. Attacker uses disclosed path information for further reconnaissance or targeted exploitation

## Root cause
The application fails to validate parameter types before processing. Specifically, the code calls trim() on user-supplied input without first ensuring it is a string. The presence of array notation in POST parameters ([]) causes PHP to interpret the value as an array, violating the expected type and triggering an unhandled warning that exposes internal file paths.

## Attacker mindset
An information gatherer seeking to map the target application's internal structure and file system layout. This reconnaissance data can inform more sophisticated attacks. The attacker is testing common parameter manipulation techniques (array notation) that often bypass basic validation.

## Defensive takeaways
- Implement strict input validation: verify parameter types match expectations before processing (use is_string(), is_array(), etc.)
- Configure PHP to suppress error output in production (display_errors=Off, log_errors=On)
- Use try-catch blocks or type declarations to handle unexpected data types gracefully
- Sanitize and validate all POST parameters, including nested structures
- Implement a Web Application Firewall (WAF) to detect and block suspicious parameter patterns
- Use parameterized/prepared statements where applicable to reduce parameter injection attacks
- Conduct security code review focusing on user input handling in critical functions like trim(), explode(), etc.

## Variant hunting
Test other endpoints accepting updatePhrases or similar parameters with array notation suffixes
Probe parameters passed to string functions (strlen, substr, strpos, str_replace, etc.) with array values
Search for other type-sensitive PHP functions (json_encode, implode, etc.) that may also trigger warnings
Attempt similar attacks on other form parameters throughout the application
Test with deeply nested array notation to trigger different code paths
Check if other localization or translation platforms have similar validation gaps

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Reconnaissance/Identify Infrastructure

## Notes
This is a relatively low-impact vulnerability, but represents a common defensive gap: relying on type coercion in weakly-typed PHP without explicit validation. The FPD itself enables information disclosure useful for reconnaissance. The root issue is not the FPD symptom but the improper input handling that could potentially be chained with other vulnerabilities. The vulnerability demonstrates how seemingly minor type confusion issues can accumulate into security weaknesses.

## Full report
<details><summary>Expand</summary>

Hi,
I found an information disclosure vulnerability/Full Path Disclosure on your application.

Proof of Concept
-------------------------
GET  : https://www.localize.im/projects/[projiect ID/languages/[Language ID]
POST CONTENT: 
`CSRFToken=TOKEN&updatePhrases[previous][yxr][0]=&updatePhrases[edits][yxr][0]=&updatePhrases[previous][yxq][0]=&####LotsOfPhrases######&updatePhrases[secret]=[SecredCodes]&updatePhrases[translatorID]=[ID]`

Just Add "[]" after any of those *updatePhrases[previous][ID][0]*

### The information from page:
> **Warning: trim() expects parameter 1 to be string, array given in /srv/data/web/vhosts/www.localize.im/htdocs/index.php on line 191**

I Also Added a Screenshot of that FPD as attachment..
Hope You'll fix this one..
Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
