# XSS @ store.steampowered.com via agecheck path name

## Metadata
- **Source:** HackerOne
- **Report:** 406704 | https://hackerone.com/reports/406704
- **Submitted:** 2018-09-07
- **Reporter:** tvmpt
- **Program:** Steam
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Input Validation Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in store.steampowered.com's /agecheck/ endpoint where the path parameter is not properly sanitized before being reflected in the response. An attacker can inject arbitrary JavaScript code via the URL path to execute malicious scripts in a victim's browser.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the /agecheck/ path segment
2. Attacker tricks victim into clicking the link via phishing email, social media, or other social engineering
3. Victim's browser sends request to store.steampowered.com with the crafted URL
4. Server reflects the unsanitized path parameter back in the HTML response without proper escaping
5. Victim's browser parses and executes the injected JavaScript code in the context of store.steampowered.com
6. Attacker's script can steal cookies, session tokens, perform actions as the user, or redirect to phishing pages

## Root cause
The /agecheck/ endpoint accepts user-supplied input via the URL path and reflects it directly into the HTTP response without proper HTML encoding or input validation. The application failed to sanitize special characters like quotes and backticks that can break out of JavaScript string contexts.

## Attacker mindset
An attacker discovered that the agecheck path parameter was being reflected in the page source without sanitization. By crafting a payload that breaks out of the existing JavaScript context and injects an alert statement, they demonstrated the ability to execute arbitrary code. The attacker recognized this could be leveraged for session hijacking, credential theft, or malware distribution by injecting phishing forms.

## Defensive takeaways
- Implement strict input validation and whitelist only allowed characters in URL path segments
- Apply context-appropriate output encoding: HTML entity encoding for HTML context, JavaScript escaping for JS context
- Use Content Security Policy (CSP) headers to restrict inline script execution and limit XSS impact
- Employ a template engine with auto-escaping enabled to prevent accidental injection
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Conduct security code reviews focusing on user input handling in routing and request processing
- Perform regular penetration testing and input fuzzing on all user-facing endpoints
- Use web application firewalls (WAF) with XSS detection rules as defense-in-depth

## Variant hunting
Look for similar reflective endpoints in other Valve/Steam properties. Search for other path-based parameters that may be reflected: /checkout/, /news/, /search/, /app/, and any dynamic routing handlers. Test file upload features where filenames are displayed. Check API endpoints that echo back parameters. Test query parameters with similar injection attempts on other endpoints.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566.002: Phishing: Spearphishing Link
- T1539: Steal Web Session Cookie
- T1056.004: Interaction with Devices: Keylog

## Notes
The vulnerability demonstrates a classic reflected XSS pattern where user input flows directly to output without sanitization. The payload cleverly closes the JavaScript function context and injects an alert to prove code execution. This vulnerability type has been extensively documented and should be caught by basic SAST tools and code review. The /agecheck/ endpoint is likely used for age verification flows, making it high-traffic and a valuable attack vector.

## Full report
<details><summary>Expand</summary>

Hi,

I found a Cross-Site Scripting (XSS) in store.steampowered.com because the path after /agecheck/ is not sanitized as it should.

```
https://store.steampowered.com/agecheck/appmhuh2',{ sessionid: g_sessionID, ageDay: '', ageMonth: '', ageYear: '' } ).done( function( response ) { }%20 );}alert`XSS-by-TvM`;function x(){$J.post('mr2n2/247660/
```

Open this^ link, and XSS will be executed! Tested on FF 61.0.2

Looking forward!

Best regards,
Pedro

## Impact

A cross-site scripting vulnerability allows an attacker to modify the page. The attacker can inject forms to steal usernames, passwords, cookies,etc. In short, XSS opens the doors to plenty of phishing techniques.

</details>

---
*Analysed by Claude on 2026-05-24*
