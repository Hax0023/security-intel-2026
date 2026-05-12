# Reflected XSS via utm_source Parameter on Starbucks UK

## Metadata
- **Source:** HackerOne
- **Report:** 140616 | https://hackerone.com/reports/140616
- **Submitted:** 2016-05-24
- **Reporter:** meals
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in Starbucks UK's e-gift card page through the utm_source parameter. The parameter value was reflected directly into the HTML response without proper encoding, allowing attackers to inject arbitrary HTML and JavaScript code. An attacker could craft a malicious URL to execute JavaScript in a victim's browser within the context of starbucks.co.uk.

## Attack scenario
1. Attacker identifies that the utm_source parameter is reflected unsanitized in the response
2. Attacker crafts a malicious URL with XSS payload: utm_source=SBUXcouk"><b onbeforescriptexecute=prompt(document.domain)>
3. Attacker distributes the link via email, social media, or other channels targeting Starbucks customers
4. Victim clicks the malicious link while authenticated to starbucks.co.uk
5. JavaScript payload executes in victim's browser with access to session cookies and sensitive data
6. Attacker could steal session tokens, perform actions on behalf of victim, or redirect to phishing pages

## Root cause
The application failed to properly encode user-supplied input from the utm_source parameter before reflecting it into the HTML response. UTM parameters are commonly trusted as safe but were not validated or encoded at output, allowing HTML/JavaScript injection.

## Attacker mindset
An opportunistic attacker who recognized that marketing tracking parameters (utm_*) are often overlooked in security testing and assumed to be safe. Leveraged common parameter pollution and encoding bypass techniques to inject event handlers.

## Defensive takeaways
- Implement output encoding appropriate to context (HTML encoding for HTML context) on all user-supplied input
- Apply input validation whitelist for utm_* parameters restricting to alphanumeric characters
- Use security headers like Content-Security-Policy to prevent inline script execution
- Include marketing/analytics parameters in security review and threat modeling
- Implement automated XSS scanning in CI/CD pipeline targeting parameter injection points
- Apply principle of least privilege - avoid reflecting untrusted data directly into HTML

## Variant hunting
Test other utm_* parameters (utm_campaign, utm_medium, utm_content, utm_term, utm_id)
Check for stored XSS if utm parameters are saved in user profiles or analytics
Test HTML attribute contexts vs tag contexts for encoding bypass opportunities
Investigate whether analytics platforms properly encode these parameters client-side
Check for same issue on other Starbucks regional sites and subdomains
Test for DOM-based XSS if JavaScript processes these parameters client-side

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing

## Notes
The payload uses URL encoding (%3e = >, %3b = ;) to bypass basic filters. The onbeforescriptexecute event is IE-specific. This report demonstrates why security researchers must test often-overlooked parameters like UTM tracking codes. The vulnerability is a classic reflected XSS requiring user interaction (clicking link) but in authenticated context could enable account compromise or fraud.

## Full report
<details><summary>Expand</summary>

https://www.starbucks.co.uk/shop/card/egift?utm_campaign=egift&utm_content=WinterFY16&utm_medium=GPH&utm_source=SBUXcouk"%3e%3cb%20onbeforescriptexecute=prompt(document.domain)%3e

Payload: "%3e%3cb%20onbeforescriptexecute=prompt(document.domain)%3e

</details>

---
*Analysed by Claude on 2026-05-12*
