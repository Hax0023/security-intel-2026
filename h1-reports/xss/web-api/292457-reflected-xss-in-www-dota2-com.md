# Reflected XSS in www.dota2.com International Live Page

## Metadata
- **Source:** HackerOne
- **Report:** 292457 | https://hackerone.com/reports/292457
- **Submitted:** 2017-11-22
- **Reporter:** jr0ch17
- **Program:** Valve (Dota 2)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Unsafe JavaScript Template Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Dota 2 international/live endpoint where user-supplied path parameters are directly injected into JavaScript code without proper sanitization. An attacker can craft a malicious URL containing JavaScript payload that executes in the victim's browser when visited, potentially stealing authentication cookies or performing account takeover.

## Attack scenario
1. Attacker discovers that path parameters in /international/live/{param1}/{param2}/{param3} are reflected in JavaScript context
2. Attacker crafts a payload that breaks out of the JavaScript context using })}});alert(document.cookie);(test=>{{({<!-- syntax
3. Attacker sends the malicious URL to a victim via phishing email, social media, or other social engineering technique
4. Victim clicks the link and visits the crafted URL in their browser
5. The JavaScript payload executes in the victim's browser with their session context
6. Attacker's JavaScript exfiltrates cookies, session tokens, or performs malicious actions on behalf of the victim

## Root cause
User-controlled path parameters are directly concatenated into JavaScript code without proper output encoding or context-aware escaping, allowing an attacker to break out of the intended JavaScript context and inject arbitrary code.

## Attacker mindset
The attacker methodically tested various URL paths to identify patterns, discovered the reflection point in JavaScript context, and crafted a syntax-aware payload to break out and execute arbitrary code. The attacker demonstrated this works across multiple browsers by bypassing Chrome's XSS filter through direct reflection in script context rather than HTML attributes.

## Defensive takeaways
- Implement strict input validation on all URL path parameters with whitelist of allowed values
- Use context-aware output encoding: JavaScript string escaping for JavaScript context, HTML entity encoding for HTML context
- Avoid directly concatenating user input into JavaScript code; use data attributes or APIs instead
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Use security headers like X-XSS-Protection and X-Content-Type-Options
- Apply template engines with auto-escaping enabled by default
- Conduct regular security testing including reflected XSS testing across all user-controlled input points

## Variant hunting
Test other path-based parameters on Dota 2 domain for similar reflection vulnerabilities
Check query string parameters in international/live endpoint for XSS
Test other Valve properties (Steam, CS:GO) for similar template injection patterns
Look for stored XSS variants if user input is persisted (replays, user profiles, etc)
Test DOM-based XSS vectors if JavaScript frameworks are used client-side
Fuzz numeric parameters to identify other injection points in URL structure

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
The vulnerability is particularly concerning because it works across multiple browsers and successfully bypasses Chrome's built-in XSS filter due to the reflection being directly in a JavaScript context rather than in HTML attributes. The attacker's payload demonstrates good understanding of JavaScript syntax and breakout techniques. The fact that any numeric values work in the path parameters suggests a generic template or mapping issue rather than specific business logic validation.

## Full report
<details><summary>Expand</summary>

Hi guys,

##Description
I found another XSS in www.dota2.com. This time it is located in **http://www.dota2.com/international/live/5/5/1**. However it seems that when you can change the /5/5 folders to any other number (to confirm) and it still worked. I tested this on http://www.dota2.com/international/live/1/1/1 and with other random digits.

##Steps to reproduce
1. Using any browser (except IE), go to
`www.dota2.com/international/live/5/5/1})}});alert(document.cookie);(test=>{{({<!--`
2. You'll see an alert box with your cookie.

I was able to confirm the XSS works in Firefox, Chrome and Opera so the payload successfully bypasses the Chrome XSS filter since the reflection point is directly in a javascript.

{F241581}

## Impact

As you know, with a reflected XSS, a malicious user could trick a user into browsing to a URL which would trigger the XSS and steal the user's cookie, capture keyboard strokes, etc and eventually take over a user's account. 

Thanks,

JR0ch17

</details>

---
*Analysed by Claude on 2026-05-12*
