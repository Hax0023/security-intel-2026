# Reflected XSS on theacademy.upserve.com

## Metadata
- **Source:** HackerOne
- **Report:** 415139 | https://hackerone.com/reports/415139
- **Submitted:** 2018-09-27
- **Reporter:** base_64
- **Program:** Upserve
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Brightcove video player integration on theacademy.upserve.com's admin-ajax.php endpoint. The video_id parameter is not properly sanitized or encoded before being reflected in the HTTP response, allowing attackers to inject arbitrary HTML and JavaScript code.

## Attack scenario
1. Attacker crafts a malicious URL with XSS payload in the video_id parameter: /wp-admin/admin-ajax.php?action=load_player&video_id=r"><BODY%20ONLOAD=alert(1)>&player_id=B14h0D4OM&type=pc&post_id=2712
2. Attacker shares the malicious URL via email, social media, or injects it into a compromised website
3. Victim clicks the link while authenticated to theacademy.upserve.com
4. The payload executes in the victim's browser within the origin context of theacademy.upserve.com
5. Attacker's JavaScript can steal session cookies, perform actions on behalf of the user, or redirect to phishing pages
6. Sensitive user data or credentials are compromised without the victim's knowledge

## Root cause
The video_id parameter from the wp-admin/admin-ajax.php endpoint is directly reflected in the HTTP response without proper HTML entity encoding or output sanitization. The application fails to validate the parameter format and does not escape special characters that have meaning in HTML context (>, <, quotes, etc.)

## Attacker mindset
An attacker would recognize that user-controlled parameters passed through AJAX endpoints are often overlooked in security testing. By identifying that the video_id is reflected in responses, they can craft a simple HTML breaking payload to inject script tags. The attacker would likely use this to build a phishing campaign targeting academy users or steal authentication tokens.

## Defensive takeaways
- Implement output encoding using context-appropriate functions (HTML entity encoding for HTML context) for all user-supplied data before reflection
- Use a Content Security Policy (CSP) with strict script-src directives to prevent inline script execution
- Validate and sanitize all input parameters using allowlist-based validation (video_id should only contain alphanumeric characters)
- Apply HTTP security headers (X-XSS-Protection, X-Content-Type-Options) as defense-in-depth measures
- Implement automated security testing in CI/CD pipeline to detect reflected XSS vulnerabilities
- Use security libraries/frameworks that provide automatic output encoding by default
- Conduct regular security code reviews focusing on AJAX endpoints and third-party integrations (like Brightcove)

## Variant hunting
Test other AJAX actions in admin-ajax.php for similar parameter reflection vulnerabilities
Check other player parameters (player_id, post_id, type) for XSS susceptibility
Investigate other Brightcove player implementations on Upserve properties
Search for similar parameter patterns in API endpoints that return dynamic content
Test for DOM-based XSS in client-side JavaScript that processes player parameters
Check for authentication bypass by manipulating post_id or player_id parameters

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Gather Victim Information: Web Cookies
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel

## Notes
This is a classic reflected XSS in a WordPress AJAX handler. The use of Brightcove player suggests a third-party plugin integration point. The vulnerability is easily exploitable and requires no authentication, making it suitable for mass phishing campaigns. The absence of a specified bounty amount suggests this may have been resolved during the report process or was part of a vulnerability disclosure without monetary rewards.

## Full report
<details><summary>Expand</summary>

**Vulnerabilty**
*Reflected xss* in (https://theacademy.upserve.com).

**STEPS TO REPRODUCE**
1. Go to (https://theacademy.upserve.com/playlists/all-videos/).
2. Click on any video to watch from the playlist and capture the request in burp.
3. you have to capture the request to (https://theacademy.upserve.com/wp-admin/admin-ajax.php?action=load_player&video_id=5742677405001&player_id=B14h0D4OM&type=pc&post_id=2712)
4. then replace the video_id with this payload = r"><BODY%20ONLOAD=alert(1)>.
5. Then see the response in browser and the popup will appear.

**NOTE**: *I also attached a video POC*

## Impact

With the help of *xss* a hacker or attacker can perform social engineering on users by redirecting them from real website to fake one. hacker can steal their *cookies* and download a **malware** on their system, and there are many more attacking scenarios a skilled attacker can perform with **xss**.

</details>

---
*Analysed by Claude on 2026-05-12*
