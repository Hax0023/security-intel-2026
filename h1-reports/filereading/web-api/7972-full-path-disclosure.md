# Full Path Disclosure via PHP unserialize() Error

## Metadata
- **Source:** HackerOne
- **Report:** 7972 | https://hackerone.com/reports/7972
- **Submitted:** 2014-04-18
- **Reporter:** nahamsec
- **Program:** Localize.io
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Full Path Disclosure, Insecure Deserialization
- **CVEs:** None
- **Category:** web-api

## Summary
The application discloses full server path information through PHP error messages when the review[phraseObject] parameter receives malformed serialized data. An attacker can trigger an unserialize() error by submitting invalid serialized objects, causing the application to expose sensitive path information in error output.

## Attack scenario
1. Attacker identifies the POST endpoint at /review/3C/languages/5
2. Attacker crafts malformed PHP serialized object data for the review[phraseObject] parameter
3. Attacker submits POST request with corrupted serialized data intentionally causing deserialization to fail
4. Application attempts to unserialize() the malformed data on line 244 of index.php
5. PHP generates error message revealing full filesystem path: /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php
6. Attacker obtains server architecture details useful for planning further attacks

## Root cause
The application deserializes user-supplied data without proper validation or error suppression. Error messages are not handled gracefully, exposing verbose PHP warnings that include absolute file paths. The serialized object is processed without verification of its integrity or format.

## Attacker mindset
Reconnaissance phase attacker seeking to map application structure and server configuration. By triggering predictable errors, the attacker gathers information about the hosting environment, file structure, and technology stack without requiring valid exploitation.

## Defensive takeaways
- Never deserialize untrusted user input; use JSON instead of PHP serialize()
- Implement error suppression with @ operator or try-catch blocks for deserialization
- Configure PHP to hide error details from users (display_errors=Off)
- Log errors server-side while showing generic messages to clients
- Validate serialized data format and origin before deserialization
- Use allowlist approach if deserialization is necessary (e.g., unserialize with options parameter)
- Implement WAF rules to detect serialized object patterns in requests

## Variant hunting
Search for other parameters accepting serialized data. Check POST/GET parameters with names suggesting object data (phraseObject, dataObject, serialized*). Look for error messages containing file paths in responses. Test cookie values and other HTTP headers for unsafe deserialization patterns.

## MITRE ATT&CK
- T1190
- T1592
- T1598

## Notes
This is a low-severity but practical disclosure issue. The vulnerability requires no authentication and reveals hosting provider details. While not directly exploitable for code execution without additional PHP object injection gadgets, it significantly aids reconnaissance. The presence of serialized object handling suggests potential for object injection attacks if gadget chains exist. Researcher acknowledgment that this is not sophisticated work indicates this may be an obvious oversight in security controls.

## Full report
<details><summary>Expand</summary>

Not my best piece of work, but the following file results in a full path disclosure if review[phraseobject] is given the wrong parameter.

http://www.localize.io/review/3C/languages/5
POST

>CSRFToken=Njg0ODMwOTM1MzUwYzk5ZTFiOWU3OC4zMDk0MzM1NQ%3D%3D&review%5BeditID%5D=cw3&review%5BreferenceValue%5D=test&review%5BphraseObject%5D=TzoyMToiUGhyYXNlX0FuZHJvaWRfU3RyaW5nIjo2OntzOjg6IgAqAHZhbHVlIaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaajtzOjQ6InRlc3QiO3M6NToiACoAaWQiO2k6MDtzOjEyOiIAKgBwaHJhc2VLZXkiO3M6NzoidGVzdGluZyI7czoxMDoiACoAZ3JvdXBJRCI7aTowO3M6MjQ6IgAqAGVuYWJsZWRGb3JUcmFuc2xhdGlvbiI7YjoxO3M6MTA6IgAqAGlzRW1wdHkiO2I6MDt9&review%5BphraseKey%5D=testing&review%5BphraseSubKey%5D=0&review%5BcontributorID%5D=sh&review%5BnewValue%5D=1&review%5Baction%5D=approve

Notice: unserialize(): Error at offset 133 of 192 bytes in /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php on line 244 

</details>

---
*Analysed by Claude on 2026-05-24*
