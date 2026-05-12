# Reflected XSS in Cisco ASA/FTD Web Services Interface (SAML ACS Endpoint)

## Metadata
- **Source:** HackerOne
- **Report:** 2233421 | https://hackerone.com/reports/2233421
- **Submitted:** 2023-10-30
- **Reporter:** r00tdaddy
- **Program:** Cisco
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (Reflected XSS), Insufficient Input Validation, SAML Protocol Abuse
- **CVEs:** CVE-2023-3580
- **Category:** web-api

## Summary
Multiple reflected XSS vulnerabilities exist in the SAML Assertion Consumer Service (ACS) endpoint of Cisco ASA and FTD web interfaces due to insufficient input validation of the SAMLResponse parameter. An unauthenticated attacker can craft a malicious link containing arbitrary JavaScript that executes in the context of an authenticated user's browser session, potentially leading to session hijacking or sensitive data theft.

## Attack scenario
1. Attacker crafts a malicious URL targeting the SAML ACS endpoint (/+CSCOE+/saml/sp/acs) with XSS payload embedded in the SAMLResponse POST parameter
2. Attacker sends this link to a legitimate user (administrator or employee) via phishing email or social engineering
3. User clicks the link while authenticated to the Cisco ASA/FTD web interface
4. The vulnerable SAML endpoint processes the malicious SAMLResponse without proper sanitization
5. Arbitrary JavaScript executes in the user's browser with their session privileges and cookies
6. Attacker steals session cookies, redirects user to phishing site, or performs actions as the authenticated user

## Root cause
The SAML ACS endpoint fails to properly validate and sanitize the SAMLResponse parameter before reflecting it in the HTTP response. The application directly includes user-supplied input into the HTML output without encoding, allowing JavaScript injection through SVG onload event handlers and similar XSS vectors.

## Attacker mindset
An attacker recognizes that SAML endpoints often receive untrusted XML/encoded data and may process it without sufficient output encoding. By targeting the ACS endpoint with a POST request containing crafted SAML response data, the attacker exploits the assumption that SAML messages are inherently trusted. The use of SVG tags with event handlers bypasses basic XSS filters that may only block script tags.

## Defensive takeaways
- Implement strict input validation and whitelist acceptable SAML response formats according to OASIS SAML specifications
- Apply context-appropriate output encoding (HTML entity encoding for HTML context) to all user-controlled data before rendering in responses
- Utilize Content Security Policy (CSP) headers to restrict inline script execution and limit script sources
- Employ automated security testing (SAST/DAST) specifically targeting SAML implementations and protocol endpoints
- Implement authentication requirements for SAML ACS endpoints or validate SAML signatures cryptographically
- Use templating engines with auto-escaping enabled rather than string concatenation for HTML generation
- Conduct security code review focusing on SAML handling, XML processing, and any parameter reflection
- Apply principle of least privilege to web service accounts and limit SAML configuration exposure

## Variant hunting
Test other SAML endpoints (SSO, SLO endpoints) for similar reflection vulnerabilities
Check if other POST parameters in the SAML flow are similarly vulnerable (RelayState, SAMLRequest, etc.)
Investigate whether other Cisco security products (ISE, Meraki, Umbrella) have SAML XSS vulnerabilities
Test GET request variations and URL encoding bypasses for the same endpoint
Look for DOM-based XSS in SAML processing logic on the client side
Check if XML External Entity (XXE) injection is possible through SAML requests
Test SAML assertion injection/modification attacks that might bypass validation
Examine other federation/authentication endpoints (OAuth, OpenID Connect) for similar issues
Investigate if the vulnerability exists in other Cisco appliance management interfaces

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002
- T1080

## Notes
CVE-2023-3580 is a critical finding in a network security appliance where users expect strong security posture. The vulnerability is particularly impactful because it affects the administrative web interface of a firewall/security device. The SAML endpoint is an authentication-critical component, making this a high-value target. The fact that it affects 'specific AnyConnect and WebVPN configurations' suggests configuration-dependent exposure. The proof-of-concept demonstrates reliable exploitation through a simple POST request with minimal prerequisites.

## Full report
<details><summary>Expand</summary>

**Description:**
Multiple vulnerabilities in the web services interface of Cisco Adaptive Security Appliance (ASA) Software and Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to conduct cross-site scripting (XSS) attacks against a user of the web services interface of an affected device. The vulnerabilities are due to insufficient validation of user-supplied input by the web services interface of an affected device. An attacker could exploit these vulnerabilities by persuading a user of the interface to click a crafted link. A successful exploit could allow the attacker to execute arbitrary script code in the context of the interface or allow the attacker to access sensitive, browser-based information. Note: These vulnerabilities affect only specific AnyConnect and WebVPN configurations. For more information, see the Vulnerable Products section.

## References
https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-xss-multiple-FCB3vPZe

## Impact

With this vulnerability, an attacker can steal users cookies, redirect users to a malicious website, or execute arbitrary javascript.

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers
CVE-2023-3580

## Steps to Reproduce
1.) Perform the following post request. 

POST /+CSCOE+/saml/sp/acs?tgname=a HTTP/1.1
Host: ███████
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36
Connection: close
Hackerone: R00tdaddy
Content-Length: 72
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip, deflate, br

SAMLResponse=%22%3E%3Csvg/onload=alert(/2XUkWJ29OE88uyTbdZ3a2UmA828/)%3E

SAML Response pops up in the browser.

## Suggested Mitigation/Remediation Actions
Patch : https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-xss-multiple-FCB3vPZe



</details>

---
*Analysed by Claude on 2026-05-12*
