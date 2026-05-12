# DOM-based XSS in redirect parameter

## Metadata
- **Source:** HackerOne
- **Report:** 361287 | https://hackerone.com/reports/361287
- **Submitted:** 2018-06-03
- **Reporter:** flamezzz
- **Program:** Semmle (LGTM)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
The redirect parameter accepts javascript: protocol URLs, allowing attackers to inject arbitrary JavaScript code. When a victim clicks a malicious link and logs in, the attacker can execute code in the victim's authenticated session and perform unauthorized actions.

## Attack scenario
1. Attacker crafts a malicious URL with javascript: payload in the redirect parameter
2. Attacker sends the link to target victim via phishing email or social engineering
3. Victim clicks the link and is redirected to the login page with the malicious redirect parameter intact
4. Victim authenticates with valid credentials, establishing an authenticated session
5. Upon successful login, the application redirects to the javascript: URL, executing the attacker's payload
6. Attacker gains ability to steal session tokens, perform actions, or harvest sensitive data within the victim's authenticated context

## Root cause
Insufficient validation and sanitization of the redirect parameter. The application fails to whitelist safe redirect destinations or properly validate URL schemes before performing client-side redirects.

## Attacker mindset
An attacker seeking to compromise authenticated user sessions without direct access credentials. By leveraging the trust users place in legitimate domain redirects, they can execute code post-authentication when the victim's guard is down.

## Defensive takeaways
- Implement strict whitelist validation for redirect destinations - only allow internal URLs or pre-approved domains
- Reject or sanitize any redirect URLs containing javascript:, data:, or other dangerous protocols
- Use server-side redirect validation rather than relying on client-side checks
- Avoid storing user-controlled input directly in redirect parameters; use token-based redirect mapping instead
- Educate users about verifying URLs before login and recognizing phishing attempts
- Implement Content Security Policy (CSP) to restrict script execution
- Log and monitor unusual redirect patterns for security anomalies

## Variant hunting
Check for similar unvalidated redirects in other authentication flows (password reset, email verification, OAuth callbacks)
Test other parameters that might accept URLs (callback, return_to, next, continue, forward)
Look for protocol confusion vulnerabilities (vbscript:, file:, data: URIs)
Test data: URIs with base64-encoded HTML/JavaScript payloads
Check if redirect validation only occurs client-side and can be bypassed
Examine if multiple redirects are chained or if encoding bypasses are possible

## MITRE ATT&CK
- T1190
- T1566
- T1566.002
- T1598
- T1598.003

## Notes
This is a classic open redirect leading to DOM XSS vulnerability chain. The timing of execution post-authentication significantly increases impact. Similar vulnerabilities are common in OAuth implementations and post-login redirect flows where user trust is highest.

## Full report
<details><summary>Expand</summary>

#Summary
The **redirect** param can consist of a ``javascript:`` url, which results in XSS. If a victim visits a malicious URL and logs in, the attacker can perform actions on behalf of the victim.

#Steps to reproduce
1) Logout
2) Visit `` https://lgtm-com.pentesting.semmle.net/?redirect=javascript:prompt(document.domain)%2f%2f
 ``
3) Log in through email

## Impact

If a victim visits a malicious URL and logs in, the attacker can perform actions on behalf of the victim.

</details>

---
*Analysed by Claude on 2026-05-12*
