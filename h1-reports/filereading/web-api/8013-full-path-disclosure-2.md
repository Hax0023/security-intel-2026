# Full Path Disclosure via Modified Input Type and Invalid XML Import

## Metadata
- **Source:** HackerOne
- **Report:** 8013 | https://hackerone.com/reports/8013
- **Submitted:** 2014-04-18
- **Reporter:** siddiki
- **Program:** Unknown (referenced domain: swarthmore.edu or related service)
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Full Path Disclosure, Information Disclosure, Error-Based Information Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can trigger a Full Path Disclosure (FPD) vulnerability by modifying an XML file import input field from type 'file' to type 'url' and attempting to import an invalid XML file. The application's error handling fails to sanitize error messages, exposing the complete server file path and application structure.

## Attack scenario
1. Attacker inspects the HTML form containing the XML file import functionality
2. Attacker modifies the input element type attribute from 'file' to 'url' using browser developer tools
3. Attacker enters a URL pointing to an invalid or non-XML file (e.g., http://www.swarthmore.edu/libraries.xml)
4. Application attempts to process the URL input through the XML import handler
5. Application encounters an error when attempting to parse the invalid XML or access the file variable
6. Unhandled exception causes error message to be displayed, revealing full server path: /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php

## Root cause
Lack of proper error handling and output encoding in the XML import functionality. The application exposes PHP notices/warnings directly to users without sanitization, revealing server directory structure and file paths. Additionally, insufficient input validation allows the modified input type to be processed.

## Attacker mindset
Reconnaissance-focused; using minor input manipulation to trigger verbose error messages that disclose sensitive infrastructure information. This information can be leveraged for further attacks by identifying the exact application structure, hosting provider, and file organization.

## Defensive takeaways
- Implement comprehensive error handling that catches and logs exceptions without exposing system paths to users
- Configure PHP to suppress error display in production (display_errors=Off) and log errors server-side only
- Validate and sanitize all user inputs before processing, including type checking for file uploads
- Implement input type validation server-side rather than relying on HTML input type attributes
- Use generic error messages for users while logging detailed errors internally
- Disable PHP notices/warnings display or properly handle undefined array indices with isset() checks

## Variant hunting
Test other form fields for similar FPD vulnerabilities by triggering errors
Attempt to change other input types (file→text, file→email, etc.) to bypass validation
Try malformed URLs or special characters in URL input field to trigger parsing errors
Test with file:// protocol URLs to access local files
Attempt XXE (XML External Entity) injection to see if detailed error messages leak information
Test error conditions in other import/upload functionalities in the application

## MITRE ATT&CK
- T1590.003 - Gather Victim Identity Information: Commercial Relationships
- T1592.004 - Gather Victim Host Information: Client Configurations
- T1087 - Account Discovery

## Notes
This is a relatively low-severity vulnerability (Information Disclosure) but can be valuable for reconnaissance. The bug demonstrates the importance of proper error handling in production environments. The vulnerability chain shows how minor HTML modifications combined with error-handling oversights can leak infrastructure details. The hosting provider information (hosteurope.de) and directory structure are now exposed, potentially aiding further attacks.

## Full report
<details><summary>Expand</summary>

During the import of an XML file,I edited the "file" to "url" for importing XML's through URL.So it became:
```html
<input id="importFileXML" class="form-control" type="url" name="importFileXML"></input>
```
And then I tried to import a random XML file.I tried with this:
http://www.swarthmore.edu/libraries.xml
It was not a valid XML file.And after the importing it showed the following error which discloses full path of the application.

```text
Notice: Undefined index: importFileXML in /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php on line 421 
```

</details>

---
*Analysed by Claude on 2026-05-24*
