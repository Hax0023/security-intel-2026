# Clickjacking via Missing X-Frame-Options Header

## Metadata
- **Source:** HackerOne
- **Report:** 17664 | https://hackerone.com/reports/17664
- **Submitted:** 2014-06-26
- **Reporter:** shahmeer-amir
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The target website is missing the X-Frame-Options HTTP security header, which prevents browsers from rendering the page within an iframe. This allows attackers to overlay the legitimate page with malicious content to trick users into performing unintended actions. The vulnerability enables clickjacking attacks where user interactions are hijacked through iframe-based UI redressing.

## Attack scenario
1. Attacker creates a malicious website and embeds the vulnerable target website in a transparent iframe
2. The attacker overlays invisible or opaque HTML elements (buttons, forms) on top of the legitimate page content
3. Victim visits the attacker's malicious website, unaware of the iframe overlay
4. When the victim clicks what appears to be a legitimate action on the target site, they actually trigger actions on the attacker's overlay layer
5. This could result in unauthorized transactions, profile modifications, permission grants, or credential theft
6. Victim realizes too late that their intended action was redirected or manipulated

## Root cause
The application fails to implement the X-Frame-Options HTTP response header (or Content-Security-Policy frame-ancestors directive) which is the standard defense mechanism against clickjacking attacks.

## Attacker mindset
An attacker identifies that the lack of framing restrictions allows them to overlay legitimate functionality with malicious controls, enabling social engineering at the browser level without requiring complex exploits.

## Defensive takeaways
- Implement X-Frame-Options header set to 'DENY' or 'SAMEORIGIN' depending on legitimate framing needs
- Alternatively, use Content-Security-Policy header with frame-ancestors directive for more flexible control
- Validate that all HTTP responses include appropriate framing restrictions
- Implement frame-busting JavaScript as a secondary defense mechanism
- Use clickjacking protection tests in security scanning and automated testing pipelines
- Monitor for unauthorized iframe embeddings through client-side detection

## Variant hunting
Check for missing X-Frame-Options on AJAX endpoints and API responses
Identify pages with overly permissive settings like 'ALLOW-FROM' on deprecated implementations
Test subdomains and alternate domains for consistent header implementation
Look for edge cases where headers are missing on specific response codes or content types
Examine cached responses that may lack security headers
Test redirect chains for header preservation throughout the redirect sequence

## MITRE ATT&CK
- T1189 - Service Exploitation
- T1566 - Phishing
- T1598 - Phishing for Information

## Notes
This is a foundational web security issue discovered early in HackerOne's bug bounty history. While conceptually simple, clickjacking remains a valid vulnerability class affecting many applications. Modern browsers have improved protections, but the attack remains viable against users on older browsers or when combined with other techniques. The report demonstrates proper vulnerability disclosure of a missing security header without exploitation proof-of-concept.

## Full report
<details><summary>Expand</summary>

Hey there
I found out that you have missing X-frame header which allows click jacking in your website

</details>

---
*Analysed by Claude on 2026-05-24*
