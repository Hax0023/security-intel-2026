# Phishing Link Injection via URL @ Sign Bypass in Course Discussions

## Metadata
- **Source:** HackerOne
- **Report:** 62301 | https://hackerone.com/reports/62301
- **Submitted:** 2015-05-13
- **Reporter:** zeyadk
- **Program:** Udemy
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insufficient URL Validation, Phishing/Social Engineering, URL Parsing Logic Flaw, Authentication Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
The course discussion feature implements a whitelist-based link filter that blocks suspicious domains but fails to properly validate URLs containing the @ character. An attacker can craft URLs like https://support.udemy.com@evil.com which pass validation but redirect users to malicious sites, enabling credential theft and phishing attacks.

## Attack scenario
1. Attacker identifies that Udemy blocks direct malicious links in course discussions but whitelists domains like support.udemy.com
2. Attacker crafts a malicious URL using the @ character: https://support.udemy.com@attacker.com
3. URL passes the whitelist validation filter as it appears to start with a trusted domain
4. Attacker posts the crafted link in a course discussion with social engineering context (e.g., 'Check this support article')
5. Unsuspecting course participants click the link, trusting the visible support.udemy.com domain
6. Browser interprets the @ character as authentication data separator and redirects to attacker.com, bypassing the whitelist

## Root cause
The validation logic only checks if URLs start with or contain whitelisted domains without properly parsing the full URL structure. Modern browser URL parsing treats content before @ as credentials and the domain after @ as the actual destination, creating a semantic gap between validation and browser interpretation.

## Attacker mindset
Exploit trust-based whitelisting mechanisms by leveraging browser URL parsing quirks. Use legitimate-looking domain prefixes to pass automated filters while hijacking the actual redirect destination through URL encoding tricks.

## Defensive takeaways
- Implement strict URL parsing using official URL parsing libraries that match browser behavior
- Reject any URLs containing @ character as they indicate suspicious authentication syntax
- Validate the actual destination domain after full URL parsing, not just string matching
- Consider URL decoding payloads before validation to catch encoded bypass attempts
- Implement secondary defenses: link preview tooltips showing actual destination domain before clicking
- Log and alert on @ character usage in user-submitted URLs for threat detection
- Apply allowlist validation to the parsed hostname only, after URL normalization

## Variant hunting
Test other URL parsing bypasses: encoded characters (%40 for @), IPv6 notation, double slashes, backslash variations
Check if similar filtering exists in other user-generated content features (comments, profiles, messages)
Test URL schemes beyond https (javascript:, data:, vbscript:) against whitelist
Investigate if URL fragments (#) or query parameters (?) can be used to hide malicious paths
Test internationalized domain names (IDN) homograph attacks combined with @ bypass

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1598.004
- T1190

## Notes
The report demonstrates solid security researcher acumen by identifying browser-level semantic differences in URL interpretation. The @ symbol vulnerability is a known attack vector (RFC 3986 section 3.2.2) but often overlooked in web filtering. The researcher correctly notes that URL encoding the malicious portion would further evade string-based detection. The live example link in the report would have been valuable evidence for the vendor. This vulnerability has moderate real-world impact as it requires user interaction but exploits cognitive biases (trusting visible domain names).

## Full report
<details><summary>Expand</summary>

{refer to case number 247874}

Hey devs ,

IF you went in course discussion and tried to add for example " evil.com " it will get blocked by your system . But if you tried to add

https://support.udemy.com/ it will be added directly


So using a thing i learned in old times th ' @ ' sign after a website url like this site.com@anothersite.com it will actually redirect to to anothersite.com It is because modern browsers interpret this scheme like this "http://authorization_data@website", so, when You click on URL, they get You redirected to "http://website". so this was the way i bypassed the system adding any pishing link in the end of support.udemy.com link or any whitelisted site :


Example :

https://support.udemy.com@evil.com/


add it in a discussion and a successfull bypass is done and it will be added to discussion flawlessly .


Now ability to pish user into telling them check this support and they will be confident it's a udemy link but you will dircect them to scam site . 


Here is live example :


https://www.udemy.com/course/244336/activities?ids=1415990


So this is it you need not to allow any link with @ in it : Also if you say that the variant after @ will appear as misleading it can be URL encoded ! 

Thanks !

</details>

---
*Analysed by Claude on 2026-05-24*
