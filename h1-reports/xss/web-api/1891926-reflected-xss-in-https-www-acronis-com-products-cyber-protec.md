# Reflected XSS in Acronis Cyber Protect Trial Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1891926 | https://hackerone.com/reports/1891926
- **Submitted:** 2023-03-04
- **Reporter:** tomblorg
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Acronis Cyber Protect trial page via the SFDCCampaignID parameter that allows arbitrary JavaScript execution. The vulnerability is geo-restricted and only exploitable outside the USA, suggesting different validation logic based on geographic origin.

## Attack scenario
1. Attacker crafts malicious URL containing JavaScript payload in SFDCCampaignID parameter: https://www.acronis.com/products/cyber-protect/trial/?SFDCCampaignID=zz`;(alert)();// 
2. Attacker sends crafted link to target users located outside the USA via phishing email or social engineering
3. Target user clicks the link from a non-USA location (VPN or direct)
4. Malicious JavaScript executes in user's browser with the context of acronis.com domain
5. Attacker can exfiltrate session cookies, authentication tokens, or sensitive user data displayed on the page
6. Attacker can perform actions on behalf of the user such as modifying form data or redirecting to credential harvesting page

## Root cause
The SFDCCampaignID parameter is reflected in the page response without proper HTML encoding or sanitization. The parameter appears to be processed server-side with conditional validation that differs by geographic location, allowing the payload to pass through when not originating from USA IP addresses.

## Attacker mindset
An attacker identified that marketing/campaign tracking parameters are often trusted and under-validated. They recognized the geo-restriction bypass opportunity and weaponized it by crafting a payload that breaks out of existing context (backtick and function call syntax). This suggests reconnaissance of the application's validation rules and testing across multiple regions.

## Defensive takeaways
- Implement consistent input validation across all geographic regions - do not vary security controls by location
- Apply HTML entity encoding to all user-supplied parameters before rendering in response
- Use Content Security Policy (CSP) headers to restrict script execution origins
- Implement parameterized output encoding for the specific context (HTML, JavaScript, URL, CSS)
- Sanitize and validate all tracking/marketing parameters server-side using a whitelist approach
- Apply security testing across multiple geographic locations to identify region-specific bypass conditions
- Use automatic scanning tools and manual code review to identify parameter reflection vulnerabilities

## Variant hunting
Test other marketing/tracking parameters (utm_source, utm_medium, campaign_id, etc.) for similar XSS
Check if other Acronis trial or product pages have the same vulnerable parameter
Test from different geographic regions for other parameters that may have geo-specific validation bypass
Attempt DOM-based XSS via the SFDCCampaignID parameter if processed client-side
Test for stored XSS if the campaign parameter is saved in user profiles or databases
Check for JavaScript template injection if the parameter is used in template rendering

## MITRE ATT&CK
- T1190
- T1566.002

## Notes
The geo-restriction bypass is the most interesting aspect - it indicates either A) different validation logic per region, B) WAF/filtering rules that vary by location, or C) CDN/reverse proxy configuration differences. The payload syntax (backtick escape with function invocation) suggests targeting template strings or eval contexts. The attacker provided working proof-of-concept with specific geographic conditions, demonstrating good reconnaissance.

## Full report
<details><summary>Expand</summary>

Enter:
https://www.acronis.com/products/cyber-protect/trial/?SFDCCampaignID=zz`;(alert)();//

* will only work outside of USA (I've tried several countries with VPN)

## Impact

Leaking users data and and modify the webpage.

</details>

---
*Analysed by Claude on 2026-05-12*
