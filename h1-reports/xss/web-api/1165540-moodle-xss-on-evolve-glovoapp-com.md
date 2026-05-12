# Moodle XSS on evolve.glovoapp.com via redirect_uri Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1165540 | https://hackerone.com/reports/1165540
- **Submitted:** 2021-04-15
- **Reporter:** sn3akysnak3
- **Program:** Glovo (evolve.glovoapp.com)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Open Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Moodle's LTI authentication module on the redirect_uri parameter, allowing attackers to execute arbitrary JavaScript in the victim's browser context. The vulnerability stems from insufficient input sanitization and validation of the redirect_uri parameter, which also allows open redirect attacks. An attacker can steal session cookies, hijack admin accounts, or impersonate other users.

## Attack scenario
1. Attacker crafts malicious URL: https://evolve.glovoapp.com/mod/lti/auth.php?redirect_uri=javascript:alert(document.domain)
2. Attacker sends link to victim (social engineering, phishing email)
3. Victim clicks link while logged into Glovo/Moodle instance
4. JavaScript payload executes in victim's browser with full application privileges
5. Attacker exfiltrates session cookies, authentication tokens, or sensitive data
6. Attacker uses stolen credentials to hijack admin or user accounts

## Root cause
The redirect_uri parameter is not properly validated or sanitized before being used in HTTP redirects or DOM operations. The application likely uses client-side or unsafe server-side redirect handling without checking for javascript: URIs or validating against a whitelist of allowed domains.

## Attacker mindset
An opportunistic attacker exploiting inadequate input validation in Moodle's LTI authentication flow. The chaining of open redirect with XSS suggests systematic reconnaissance of parameter handling. The focus on stealing admin cookies indicates motivation for privilege escalation and account takeover.

## Defensive takeaways
- Implement strict whitelist validation for redirect_uri parameters (validate against approved domains only)
- Use allow-list based URI validation, rejecting javascript:, data:, and other dangerous schemes
- Apply URL parsing libraries to prevent scheme bypasses and encoding tricks
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Use httpOnly and Secure flags on session cookies to prevent JavaScript access
- Sanitize and encode all user input before rendering in HTML/JavaScript context
- Add X-XSS-Protection and X-Content-Type-Options headers
- Conduct security testing of all redirect/navigation parameters in Moodle
- Use parameterized redirect mechanisms instead of raw user input

## Variant hunting
Test other redirect parameters in Moodle (return_uri, callback, next, goto, redirect, url, target)
Check LTI launch and OAuth2 callback endpoints for similar flaws
Test for DOM-based XSS in JavaScript redirect handlers using fetch/XMLHttpRequest
Look for XSS in other Moodle modules handling external links or integrations
Test for unicode/UTF-8 encoding bypasses in redirect validation
Check for protocol-relative URLs (//attacker.com) that bypass scheme validation
Test mutation XSS (mXSS) vectors in redirect handling
Investigate other Glovo services for similar LTI or OAuth parameter flaws

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1056
- T1185

## Notes
Moodle is widely deployed in educational institutions; this vulnerability affects admin and student accounts. The chaining from open redirect to XSS demonstrates the importance of testing multiple attack vectors on the same parameter. Escalation path to admin account takeover significantly increases risk. Report lacks specific bounty amount and resolution timeline.

## Full report
<details><summary>Expand</summary>

**Cross Site Scripting (XSS) / Moodle XSS **

**Summary : ** *Cross-site scripting (XSS) is a type of computer security vulnerability typically found in web applications. XSS enables attackers to inject client-side scripts into web pages viewed by other users. A cross-site scripting vulnerability may be used by attackers to bypass access controls such as the same-origin policy. Cross-site scripting carried out on websites accounted for roughly 84% of all security vulnerabilities documented by Symantec as of 2007. *

*An attacker can use XSS to send a malicious script to an unsuspecting user. The end user's browser has no way to know that the script should not be trusted and will execute the script. Because it thinks the script came from a trusted source, the malicious script can access any cookies, session tokens, or other sensitive information retained by the browser and used with that site. These scripts can even rewrite the content of the HTML page. For more details on the different types of XSS flaws, see: Types of Cross-Site Scripting.*

**Payload : **javascript:alert(document.domain)
**Vulnerable Param: ** ?redirect_uri=

**Affected IP's : IP Address	Port**
https://evolve.glovoapp.com/	443

**Recommendations : **
*Sanitize all the user inputs before executing them, also add XSS protection headers on server and client side.* 

**References :**
https://www.acunetix.com/websitesecurity/cross-site-scripting/
https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet 
https://portswigger.net/web-security/cross-site-scripting 

**Proof of Concept :**
-  https://evolve.glovoapp.com:443/mod/lti/auth.php?redirect_uri=javascript:alert(document.domain)

** This XSS is escalated from Open-Redirect on the same Parameter **
** Here is the POC for the open-redirect: **

-  https://evolve.glovoapp.com/mod/lti/auth.php?redirect_uri=https://example.com

## Impact

**Impact :** *An Adversary can carry out XSS attack and also can take the cookie of the Admin and login through Admin Account. 
Also, an adversary can manage to login through any other users account with valid session cookies. *

</details>

---
*Analysed by Claude on 2026-05-12*
