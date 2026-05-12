# Reflected Cross-Site Scripting (XSS) in MTN Sudan Admin Login Portal

## Metadata
- **Source:** HackerOne
- **Report:** 1158823 | https://hackerone.com/reports/1158823
- **Submitted:** 2021-04-09
- **Reporter:** renzi
- **Program:** MTN Sudan (api.mtn.sd)
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Cross-Site Scripting (Reflected), Improper Input Validation, Improper Output Encoding
- **CVEs:** CVE-2020-17453
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the login page parameter 'msgId' that fails to sanitize or encode user input before rendering it in the response. An attacker can inject arbitrary JavaScript code that executes in the victim's browser context, enabling session hijacking, credential theft, or malware distribution.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'msgId' parameter: https://api.mtn.sd/carbon/admin/login.jsp?msgId=';alert('XSS')//
2. Attacker distributes the URL via phishing emails, social engineering, or malicious websites to MTN Sudan admin users
3. Victim clicks the malicious link while authenticated or logs in through the compromised page
4. JavaScript payload executes in victim's browser with their session privileges and cookies
5. Attacker steals session tokens/cookies, captures credentials via fake login form overlay, or performs unauthorized actions
6. Victim's admin account is compromised, allowing lateral movement within MTN infrastructure

## Root cause
The application fails to implement proper output encoding when displaying the 'msgId' parameter value in the login page. Input validation is either absent or insufficient, and the parameter is directly reflected in the HTML response without HTML entity encoding or Content Security Policy protections.

## Attacker mindset
Low-skill attackers can easily exploit this vulnerability by crafting simple URLs. The admin login portal is a high-value target for credential theft and unauthorized system access. The simplicity of exploitation combined with the sensitivity of the endpoint makes this an attractive attack vector for initial compromise.

## Defensive takeaways
- Implement strict output encoding for all user-controlled input rendered in HTML context (use HTML entity encoding)
- Apply input validation on the 'msgId' parameter to accept only expected formats (whitelist approach)
- Deploy Content Security Policy (CSP) headers to restrict inline script execution
- Use templating engines with auto-escaping enabled by default
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Conduct security code review of all error message and parameter handling code
- Implement Web Application Firewall (WAF) rules to detect and block common XSS patterns
- Apply security patches from WSO2-2020-1132 if this is a WSO2 Carbon-based application

## Variant hunting
Test other URL parameters for similar XSS vulnerabilities (e.g., error messages, redirect parameters, user display names)
Check for stored XSS variants in profile settings, admin configuration pages, or message logging features
Investigate DOM-based XSS in JavaScript files that might parse the 'msgId' parameter client-side
Test different encoding bypasses: double encoding, Unicode encoding, HTML entity variations
Check if the vulnerability exists across related MTN properties or other carbon admin instances
Analyze error handling pages and feedback forms for similar reflection points

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1539 - Steal Web Session Cookie
- T1056 - Input Capture

## Notes
This vulnerability is associated with CVE-2020-17453 and WSO2 Security Advisory WSO2-2020-1132, indicating it may be a known issue in WSO2 Carbon platforms. The vulnerability demonstrates a common web application flaw affecting authentication systems. The administrative context makes this a critical security issue despite being a relatively simple XSS type. Organizations should prioritize patching and deploy compensating controls immediately.

## Full report
<details><summary>Expand</summary>

Hello,

I found a Reflected Cross site Scripting (XSS) on  https://api.mtn.sd/carbon/admin/login.jsp,  CVE-2020-17453  . With this security flaw is possible rewrite the content of page, executing JS codes...

##Steps To Reproduce:
How we can reproduce the issue:

1.Go to https://api.mtn.sd/carbon/admin/login.jsp?msgId=%27%3Balert(%27Renzi%27)%2F%2F
2.And we can see alert with Renzi message...

{F1259562}

Supporting Material/References:

* https://docs.wso2.com/display/Security/Security+Advisory+WSO2-2020-1132
* https://owasp.org/www-community/attacks/xss/

## Impact

* The attacker can execute JS code.
* Rewrite the content of Page

</details>

---
*Analysed by Claude on 2026-05-12*
