# Reflective Cross-Site Scripting (XSS) on SharePoint /Pages endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1794757 | https://hackerone.com/reports/1794757
- **Submitted:** 2022-12-06
- **Reporter:** predatorsparrow
- **Program:** Microsoft Security Response Center / SharePoint
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflective Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** CVE-2017-0255
- **Category:** web-api

## Summary
A reflective XSS vulnerability exists in Microsoft SharePoint Foundation 2013 SP1 where the SiteName parameter in /Pages/default.aspx is not properly sanitized before being reflected in the response. An authenticated attacker can inject arbitrary JavaScript code that executes in the context of a victim's browser session, enabling session hijacking, credential theft, and unauthorized actions on behalf of the victim.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the SiteName parameter: default.aspx?FollowSite=0&SiteName=%27-confirm(%27XSSALERT%27)-%27
2. Attacker sends the crafted URL to a victim via phishing email or social engineering
3. Victim clicks the link while authenticated to the SharePoint server
4. The malicious payload executes in the victim's browser within the SharePoint application context
5. Attacker's JavaScript can access session cookies, perform actions as the victim (modify permissions, delete content), and exfiltrate sensitive data
6. Victim is unaware of the malicious actions occurring in the background

## Root cause
The SiteName query parameter is directly reflected in the HTML response without proper input validation, sanitization, or output encoding. The application fails to neutralize special characters and code syntax before rendering user-supplied input back to the client.

## Attacker mindset
An authenticated attacker seeks to escalate privileges and abuse legitimate user sessions. The reflective nature makes this ideal for targeted spear-phishing campaigns against specific SharePoint users. The attacker can craft convincing URLs mimicking legitimate SharePoint operations to bypass user suspicion.

## Defensive takeaways
- Implement strict input validation on all query parameters, whitelisting only expected characters and formats
- Apply proper output encoding/escaping based on context (HTML entity encoding for HTML context, JavaScript encoding for script context)
- Use a Content Security Policy (CSP) header to restrict script execution from inline sources
- Implement HTTP-only and Secure flags on session cookies to prevent JavaScript access
- Apply defense-in-depth with multiple encoding layers rather than relying on single sanitization point
- Conduct security code review of all user input handling in SharePoint applications
- Patch SharePoint to latest version immediately (CVE-2017-0255 remediation)

## Variant hunting
Test other query parameters in /Pages/default.aspx for similar reflective XSS (FollowSite, other parameters)
Check other SharePoint endpoints (/sites/, /lists/, /items/) for XSS in query parameters
Test POST request bodies for stored XSS variants
Investigate if sanitization can be bypassed using encoding variations (double encoding, Unicode, HTML entities)
Test if the vulnerability exists in other SharePoint versions and editions (2010, 2016, Online)
Check for similar patterns in other Microsoft web applications (Exchange, Dynamics, Teams)

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1550

## Notes
This is a known vulnerability cataloged as CVE-2017-0255 affecting SharePoint Foundation 2013. The report demonstrates a simple confirm() dialog but actual exploits could steal session tokens, perform arbitrary actions, or inject keyloggers. The authenticated requirement reduces immediate blast radius but is still critical in environments where SharePoint is accessible to many users. The vulnerability likely affects multiple parameters and endpoints given the common pattern of insufficient input handling in legacy SharePoint code.

## Full report
<details><summary>Expand</summary>

## Reflective Cross-Site Scripting (XSS)
An elevation of privilege vulnerability exists when Microsoft SharePoint Server does not properly sanitize a specially crafted web request to an affected SharePoint server. An authenticated attacker could exploit the vulnerability by sending a specially crafted request to an affected SharePoint server. 
The attacker to read content that the attacker is not authorized to read, use the victim's identity to take actions on the SharePoint site on behalf of the user, such as change permissions and delete content, and inject malicious content in the browser of the user.

## System Host(s)
https://██████████/Pages

## Affected URLs in Scope
https://█████████/Pages/default.aspx?FollowSite=0&SiteName=%27-confirm(%27XSSALERT%27)-%27

## Affected Product(s) and Version(s)
Microsoft SharePoint Foundation 2013 Service Pack 1

██████ 

References
https://msrc.microsoft.com/update-guide/vulnerability/CVE-2017-0255

## CVE Numbers
CVE-2017-0255

## Steps to Reproduce

Injecting this XSS payload containing allows a window to pop up as a result of the payload being executed.

 1. Go to- 
https://████████/Pages/default.aspx?FollowSite=0&SiteName=%27-confirm(%27XSSALERT%27)-%27


## Suggested Mitigation/Remediation Actions
Sanitize data input (to make sure the URL input does not contain any code) is loaded from well-defined endpoints. 


</details>

---
*Analysed by Claude on 2026-05-12*
