# Reflected XSS via #tags= Parameter with Callback in Newswire

## Metadata
- **Source:** HackerOne
- **Report:** 153618 | https://hackerone.com/reports/153618
- **Submitted:** 2016-07-25
- **Reporter:** nahamsec
- **Program:** Rockstar Games
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Callback Parameter Injection, JSONP Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Rockstar Games newswire application via the #tags= hash parameter when combined with a callback parameter. An attacker can inject arbitrary JavaScript that executes in the victim's browser context by crafting a malicious URL with callback= parameter pointing to a JSONP endpoint.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the callback parameter
2. Attacker sends the URL to victim via phishing email, chat, or social media
3. Victim clicks the link and visits rockstargames.com/newswire with the payload in the hash fragment
4. Application processes the #tags= parameter and passes it to a callback function
5. Callback parameter injects code that gets executed in the victim's browser
6. Attacker gains ability to steal session cookies, perform actions as the user, or redirect to malicious sites

## Root cause
The application fails to properly sanitize or validate user-supplied input in the #tags= and callback parameters before using them in JSONP responses. The callback parameter is directly reflected without encoding, allowing arbitrary JavaScript execution. Hash-based parameters are processed client-side without proper security validation.

## Attacker mindset
An attacker identified that the newswire application uses JSONP with user-controllable callback parameters - a common but dangerous pattern. By chaining the #tags= parameter with a callback injection, they found a way to execute arbitrary JavaScript. The use of // to comment out trailing code suggests understanding of JSONP structure and JavaScript syntax.

## Defensive takeaways
- Never allow user input to control JSONP callback function names; use a whitelist of allowed callbacks
- Validate and sanitize all user inputs, including those in hash fragments
- Implement Content Security Policy (CSP) headers to restrict script execution
- Use JSON instead of JSONP when possible; if JSONP is required, wrap callbacks in strict validation
- Encode callback parameter output to prevent special character injection
- Implement input validation on callback parameter format (alphanumeric only, no special characters)
- Use security headers like X-Content-Type-Options: nosniff to prevent MIME type sniffing
- Perform security code review of all JSONP implementations in the application

## Variant hunting
Search for other JSONP endpoints with callback parameters across Rockstar domains
Test other hash-based parameters (#search=, #filter=, etc.) for similar injection points
Check for callback parameter in query strings, not just hash fragments
Audit all API endpoints that support JSONP responses
Test for callback parameter bypass techniques (padding, encoding, nested callbacks)
Look for similar patterns in other game-related websites and social platforms

## MITRE ATT&CK
- T1190
- T1566.002
- T1598

## Notes
This is a classic JSONP callback injection vulnerability combined with hash-based XSS. The use of # (fragment identifier) is significant as it's not sent to the server and can bypass some server-side filters. The path traversal notation (../../) in the URL may have been an attempt to bypass URL validation, though the actual vulnerability lies in callback injection. The alert(document.domain) payload is relatively benign but demonstrates arbitrary code execution capability.

## Full report
<details><summary>Expand</summary>

Hello,

Here's the link:

http://www.rockstargames.com/newswire/tags#/?tags=../../comments_dal/users/getGlobalLoginSettings.json?callback=alert%28document.domain%29//

Thanks,
Ben

</details>

---
*Analysed by Claude on 2026-05-12*
