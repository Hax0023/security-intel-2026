# Reflected Cross-Site Scripting in utm_source Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 104917 | https://hackerone.com/reports/104917
- **Submitted:** 2015-12-13
- **Reporter:** hussain_0x3c
- **Program:** Instacart
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected XSS, Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the utm_source, utm_medium, and utm_campaign parameters on Instacart's main domain. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser when the link is visited, potentially compromising user sessions or stealing sensitive data.

## Attack scenario
1. Attacker discovers that utm_source parameter is reflected without proper sanitization
2. Attacker crafts a malicious URL with JavaScript payload in utm_source parameter
3. Attacker distributes the URL via social engineering, email, or advertisement
4. Victim clicks the link and visits the malicious URL
5. JavaScript executes in victim's browser within Instacart's domain context
6. Attacker can steal cookies, session tokens, or perform actions on behalf of the victim

## Root cause
The application reflects user-supplied input from query parameters directly into the HTML response without proper validation, sanitization, or encoding. UTM parameters were likely trusted as safe and not subjected to output encoding before rendering.

## Attacker mindset
Opportunistic vulnerability hunter identifying low-hanging fruit in marketing/analytics parameters. Recognized that UTM parameters are often overlooked in security reviews because they are treated as benign marketing data rather than user input requiring sanitization.

## Defensive takeaways
- Implement output encoding for all user-supplied data reflected in HTML context (use HTML entity encoding)
- Apply input validation to reject unexpected characters in utm_* parameters
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Treat all query parameters as untrusted input regardless of intended purpose
- Implement automated security scanning for common parameter names used in tracking/analytics
- Conduct security training on secure coding practices for web developers
- Regular penetration testing focused on parameter injection vectors

## Variant hunting
Test other tracking parameters: utm_content, utm_term, gclid, fbclid
Check for stored XSS if utm parameters are saved to user profiles or shared links
Verify if vulnerabilities exist in other domains or subdomains
Test for DOM-based XSS if JavaScript processes these parameters client-side
Check for bypass techniques using encoding variations (double-encoding, unicode, etc.)
Test SVG-based XSS payloads and event handler injections
Investigate if vulnerability exists in legacy versions or parallel services

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001

## Notes
This is a straightforward reflected XSS vulnerability in a high-traffic e-commerce platform. The report lacks technical depth (poor English, minimal detail) but the vulnerability is clearly exploitable. The use of multiple parameters (utm_source, utm_medium, utm_campaign) all vulnerable suggests systematic lack of input validation. The POC uses basic alert() payload; real attacks would involve session theft or credential harvesting. Report tested in Firefox and IE, suggesting broad browser compatibility of the payload.

## Full report
<details><summary>Expand</summary>

**Hi** Security Team instacart

I'm Found Have Vulnerability Cross-Site Scripting Reflected on Main Domain in Variable **utm_source**

POC
---
https://www.instacart.com/green-zebra-grocery?utm_source=>"'><script>alert(/Hussain/)</script>&utm_medium=>"'><script>alert(/XSS/)</script>&utm_campaign=>"'><script>alert(/injection/)</script>

**Img** :- http://i.imgur.com/wSn4EU7.jpg

Test :- FF - IE 


**Regards**
@Hussain

</details>

---
*Analysed by Claude on 2026-05-12*
