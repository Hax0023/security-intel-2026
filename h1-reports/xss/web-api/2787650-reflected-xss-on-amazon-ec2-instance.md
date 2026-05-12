# Reflected XSS on Amazon EC2 Instance via errorCode Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2787650 | https://hackerone.com/reports/2787650
- **Submitted:** 2024-10-17
- **Reporter:** perigou
- **Program:** Amazon Elastic Compute Cloud (EC2)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** CVE-2022-29548
- **Category:** web-api

## Summary
A reflected XSS vulnerability in Amazon EC2 allows attackers to inject malicious JavaScript through the errorCode parameter without proper validation or sanitization. The payload is reflected back to the user, enabling arbitrary JavaScript execution in the victim's browser context.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the errorCode parameter: ███████);alert(document.domain)//
2. Attacker tricks a victim into clicking the malicious link via phishing, social engineering, or forum post
3. Victim's browser sends the request to Amazon EC2 with the injected payload
4. Server reflects the unsanitized errorCode parameter back in the HTTP response without encoding
5. Browser parses the response and executes the injected JavaScript in the victim's context
6. Attacker can steal session cookies, perform actions on behalf of the victim, or redirect to credential harvesting pages

## Root cause
The Amazon EC2 application fails to properly sanitize or encode user-supplied input in the errorCode parameter before reflecting it back in the HTTP response. The absence of output encoding (HTML entity encoding, JavaScript escaping) and input validation allows arbitrary code injection.

## Attacker mindset
An opportunistic attacker recognizes that error handling pages are often overlooked during security reviews. By identifying the errorCode parameter as a reflection point, they craft a simple proof-of-concept using alert(document.domain) to demonstrate execution in the origin context, establishing a foothold for credential theft or malware distribution.

## Defensive takeaways
- Implement strict input validation on all parameters, especially those used in error messages
- Apply context-appropriate output encoding: HTML encode for HTML context, JavaScript escape for JS context, URL encode for URL context
- Use a Content Security Policy (CSP) header to prevent inline script execution and restrict script sources
- Employ a Web Application Firewall (WAF) to detect and block common XSS payloads
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Conduct regular security code reviews focusing on data flow from user input to output
- Use templating engines with automatic escaping enabled by default
- Perform penetration testing on error handling pages and parameter reflection points

## Variant hunting
Test other parameters for reflected XSS: errorMessage, errorDetails, statusCode, returnUrl, referrer
Check for stored XSS variants if errorCode is persisted in logs or user profiles
Investigate DOM-based XSS if JavaScript processes the errorCode client-side
Test mutation XSS (mXSS) bypasses using mixed case or Unicode encoding
Examine error pages across different AWS services (ELB, CloudFront, RDS) for similar patterns
Test for XSS via HTTP headers reflected in error responses (User-Agent, Referer, X-Forwarded-For)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1566 - Phishing
- T1056 - Input Capture
- T1539 - Steal Web Session Cookie
- T1598 - Phishing for Information

## Notes
CVE-2022-29548 is assigned to this vulnerability. The proof-of-concept uses a simple alert box to demonstrate execution, but the true impact extends to session hijacking, credential theft, malware distribution, and lateral movement within AWS environments. The medium severity rating may underestimate risk in enterprise contexts where EC2 instances handle sensitive operations. Recommend immediate patching and Web Application Firewall deployment while awaiting AWS fixes.

## Full report
<details><summary>Expand</summary>

Product: Amazon Elastic Compute Cloud (Amazon EC2)

Vulnerability Type:  Reflected Cross-Site Scripting (XSS)

CVE: CVE-2022-29548
Severity:  Medium

Description:
 A reflected XSS vulnerability was discovered on the Amazon EC2 instance, allowing an attacker to inject malicious JavaScript code, potentially leading to unauthorized access to sensitive data or system compromise.
Proof of Concept:

URL: ███████);alert(document.domain)//

## Impact

## The payload is injected into the errorCode parameter, which is reflected back to the user without proper validation or sanitization. This allows an attacker to execute arbitrary JavaScript code in the context of the vulnerable page

</details>

---
*Analysed by Claude on 2026-05-12*
