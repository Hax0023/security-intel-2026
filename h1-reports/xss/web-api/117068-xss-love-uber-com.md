# XSS @ love.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 117068 | https://hackerone.com/reports/117068
- **Submitted:** 2016-02-18
- **Reporter:** siddiki
- **Program:** Uber
- **Bounty:** Not eligible - domain out of scope
- **Severity:** medium
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in love.uber.com through the icl_action and target parameters. The application fails to properly sanitize user input before reflecting it in the response, allowing arbitrary JavaScript execution in the victim's browser.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'target' parameter
2. Attacker sends the link to a victim via email, social media, or other communication channels
3. Victim clicks the link and is redirected to love.uber.com with the malicious payload
4. The application reflects the unsanitized payload into the page without proper encoding
5. Victim's browser executes the JavaScript payload in the context of love.uber.com
6. Attacker gains ability to steal cookies, session tokens, or perform actions as the victim

## Root cause
Insufficient input validation and output encoding on the 'target' parameter combined with the 'icl_action=reminder_popup' functionality. The application directly incorporates user-supplied input into the page response without proper HTML/JavaScript escaping.

## Attacker mindset
Opportunistic researcher identifying low-hanging fruit. The attacker demonstrated responsible disclosure by testing against a subdomain and acknowledging scope concerns, suggesting interest in security rather than malicious exploitation.

## Defensive takeaways
- Implement strict input validation on all URL parameters, especially those used in dynamic functionality
- Apply proper output encoding based on context (HTML entity encoding, JavaScript encoding, URL encoding)
- Use security-focused templating engines that auto-escape by default
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Maintain a comprehensive scope definition that includes all subdomains and related properties
- Conduct regular security audits of all web properties, including marketing/promotional domains

## Variant hunting
Look for similar parameter-based XSS in other Uber subdomains (drivers.uber.com, partners.uber.com, etc.), test other parameters passed to reminder_popup functionality, examine other icl_action values for injection points, and check for stored XSS variants if the target parameter is persisted anywhere.

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
Report was marked as informative since love.uber.com was not explicitly listed in the bug bounty program scope. However, it represents a valid security issue that should be remediated. The researcher demonstrated good security practices by responsibly disclosing the vulnerability despite scope concerns.

## Full report
<details><summary>Expand</summary>

Hello Team,
I found a Cross-Site Scripting (XSS) in http://love.uber.com/

> I'm not sure if it is eligible for bounty, as this domain is not listed under scope of the program. still as the issue is an **XSS**, i wanted to bring it to your attention.

please mark this report as **informative** if you're not looking for issues in this domain.

###POC:
http://love.uber.com/australia/?icl_action=reminder_popup&target=javascript%3aalert%28%2fhello+world%2f%29%3b%2f%2f

+ Open this^ link, XSS will be executed!

Looking forward!

</details>

---
*Analysed by Claude on 2026-05-12*
