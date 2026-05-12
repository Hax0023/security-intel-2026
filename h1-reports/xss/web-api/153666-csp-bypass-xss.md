# CSP Bypass + Reflected XSS via analytics.twitter.com and careers.twitter.com

## Metadata
- **Source:** HackerOne
- **Report:** 153666 | https://hackerone.com/reports/153666
- **Submitted:** 2016-07-25
- **Reporter:** b6117130df17feef13481e3
- **Program:** Twitter
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, Content Security Policy (CSP) Bypass, Open Redirect/CORS Misconfiguration
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability on careers.twitter.com combined with a CSP bypass on analytics.twitter.com allows attackers to execute arbitrary JavaScript. The attacker leveraged a CSP-whitelisted domain (analytics.twitter.com) that improperly handles callback parameters to bypass strict CSP restrictions and achieve XSS execution.

## Attack scenario
1. Attacker identifies reflected XSS parameter on careers.twitter.com (location parameter)
2. Attacker discovers CSP policy allows scripts from analytics.twitter.com
3. Attacker finds analytics.twitter.com accepts user-controlled callback parameter (tpm_cb) that gets reflected in script context
4. Attacker crafts payload injecting script tag pointing to analytics.twitter.com with malicious callback
5. Victim visits malicious URL on careers.twitter.com
6. Browser executes whitelisted script from analytics.twitter.com, which evaluates attacker's callback code

## Root cause
Multiple security failures: (1) Insufficient input validation on careers.twitter.com location parameter, (2) Over-broad CSP whitelist including analytics.twitter.com, (3) analytics.twitter.com improperly handles user-supplied callback parameters without sanitization, allowing code injection

## Attacker mindset
Methodical research combining multiple weak points across subdomains. Researcher documented previous CSP bypass finding and systematically chained it with a new XSS discovery to achieve exploitability. Demonstrated persistence in analyzing security controls to find bypass techniques.

## Defensive takeaways
- Implement strict input validation and output encoding on all user-supplied parameters
- Use restrictive CSP policies - avoid whitelisting entire subdomains, prefer nonce/hash-based approaches
- Sanitize and validate callback/redirect parameters on all trusted domains
- Implement CSP directives like 'unsafe-inline' = never, prefer script-src 'nonce' or 'hash'
- Regularly audit CSP policies for overly permissive whitelists
- Enforce same-origin policy for analytics and tracking endpoints
- Security review of all parameters accepting callbacks, function names, or dynamic code references
- Monitor and restrict what third-party domains in CSP whitelist can do

## Variant hunting
Search for other Twitter subdomains accepting callback parameters in analytics/tracking code
Fuzz CSP-whitelisted domains for similar parameter injection vulnerabilities
Check other subdomain XSS vulnerabilities that might be chainable with CSP bypasses
Review other callback parameter implementations (tpm_cb, callback, cb, fn, etc.) on whitelisted domains
Test if analytics.twitter.com callback parameter handles other dangerous contexts (dangerouslySetInnerHTML, eval-like functions)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1567 - Exfiltration Over Web Service
- T1598 - Phishing
- T1566 - Phishing

## Notes
This is a sophisticated chaining attack requiring knowledge of multiple vulnerabilities and CSP mechanics. The vulnerability demonstrates how CSP misconfigurations can be weaponized when combined with XSS. The researcher previously reported a related CSP bypass (report 126464) showing systematic vulnerability research. Twitter's security model failed at multiple layers - input validation, CSP policy design, and trusted domain security.

## Full report
<details><summary>Expand</summary>

Hi,

On my previous report (number 126464) I've mentioned that 
analytics.twitter.com has a CSP bypass which I couldn't exploit that time.

Now, I've found a reflected XSS on careers.twitter.com which again I couldn't exploit by itself. Because you have CSP, and I've combined two of them to successfully trigger XSS.

If you visit the url:
https://careers.twitter.com/en/jobs-search.html?location=1%22%3E%3Cscript%20src=//analytics.twitter.com/tpm?tpm_cb=alert%28document.domain%29%3E//

you will see xss triggered. 

Regards.

</details>

---
*Analysed by Claude on 2026-05-12*
