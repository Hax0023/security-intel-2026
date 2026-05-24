# Full Path Disclosure via Array Parameter Injection in XML Import

## Metadata
- **Source:** HackerOne
- **Report:** 8091 | https://hackerone.com/reports/8091
- **Submitted:** 2014-04-19
- **Reporter:** faisalahmed
- **Program:** localize.io
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Information Disclosure, Full Path Disclosure (FPD), Type Confusion, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The XML import functionality fails to properly validate input parameters, allowing an attacker to inject an array instead of a string by appending '[]' to POST parameters. This causes a type mismatch when the application passes the array to the trim() function, resulting in a PHP warning that leaks the full server file path and line number.

## Attack scenario
1. Attacker identifies the XML import endpoint at POST /import/[projectID]
2. Attacker crafts a multipart form POST request with standard import parameters
3. Attacker appends '[]' to the 'import[overwrite]' parameter name to convert it from a scalar to an array
4. Attacker submits the request with an empty or malformed importFileXML
5. Application's index.php line 410 calls trim() on the array parameter instead of a string
6. PHP generates a warning error message revealing the full path: /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php

## Root cause
The application does not validate parameter types before passing them to built-in PHP functions. The import handler expects 'import[overwrite]' to be a string but does not enforce this, allowing array injection through bracket notation. The trim() function at line 410 expects a string parameter and fails when receiving an array, causing an unhandled warning that outputs sensitive path information.

## Attacker mindset
Reconnaissance and information gathering through type confusion attacks. The attacker recognized that PHP's flexible parameter handling allows array injection via bracket notation and leveraged this to trigger type errors that expose system information useful for further attacks.

## Defensive takeaways
- Implement strict input type validation: verify that expected scalar parameters are actually scalar types before processing
- Use isset() and is_array() checks before passing user input to functions expecting specific types
- Configure PHP error_reporting to not display errors in HTTP responses; log them server-side instead
- Enable production environment settings: display_errors=Off, log_errors=On
- Sanitize and validate all file upload parameters including language ID, group ID, and overwrite flags
- Use a whitelist approach: explicitly allow only expected parameter names and structures
- Implement proper exception handling to catch type errors gracefully without exposing paths

## Variant hunting
Test all file upload endpoints (CSV, JSON, other formats) with array parameter injection
Try bracket notation on other form parameters expecting strings (languageID, groupID, MAX_FILE_SIZE)
Attempt nested array injection: import[overwrite][][]
Test with other built-in PHP functions that have strict type requirements: strlen(), explode(), str_replace()
Look for similar patterns in other POST endpoints that process user input without type validation
Test error handling in different PHP configurations to identify other information disclosure vectors

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1592: Gather Victim Host Information
- T1083: File and Directory Discovery

## Notes
This is a classic type confusion vulnerability combined with improper error handling. The FPD itself is low-risk but reveals valuable reconnaissance information (hosting provider, directory structure, application path) that aids further attacks. The underlying issue is inadequate input validation and error suppression in production. Similar to CVE-2012-1823 pattern where type mismatches expose system information.

## Full report
<details><summary>Expand</summary>

Hello,
I found another information disclosure vulnerability/Full Path Disclosure on your application.
now its on *Import XML* Section 

Proof of Concept
-------------------------

POST  : http://www.localize.io/import/ [project ID]
POST CONTENT: 
`-----------------------------97823247315770\r\n
Content-Disposition: form-data; name="CSRFToken"\r\n
\r\n
MTcwMTAzMDk2MDUzNTFjN2I1NGE5MWYxLjkzMjk2OTM0\r\n
-----------------------------97823247315770\r\n
Content-Disposition: form-data; name="import[overwrite][]"\r\n
\r\n
0\r\n
-----------------------------97823247315770\r\n
Content-Disposition: form-data; name="import[languageID]"\r\n
\r\n
0\r\n
-----------------------------97823247315770\r\n
Content-Disposition: form-data; name="import[groupID]"\r\n
\r\n
0\r\n
-----------------------------97823247315770\r\n
Content-Disposition: form-data; name="MAX_FILE_SIZE"\r\n
\r\n
1572864\r\n
-----------------------------97823247315770\r\n
Content-Disposition: form-data; name="importFileXML"; filename=""\r\n
Content-Type: application/octet-stream\r\n
\r\n
\r\n
-----------------------------97823247315770--\r\n`

I just Added "[]" after *import[overwrite]* and Replied.

### The information from page:
> Warning: trim() expects parameter 1 to be string, array given in /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php on line 410 

I Also Added a Screenshot of that FPD as attachment..
Hope You'll fix this one also..
Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
