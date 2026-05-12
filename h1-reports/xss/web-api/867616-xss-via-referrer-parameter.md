# Reflected XSS via JavaScript Scheme in Referrer Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 867616 | https://hackerone.com/reports/867616
- **Submitted:** 2020-05-07
- **Reporter:** keer0k
- **Program:** Twitter Flight School
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Unsafe URL Handling
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the referrer parameter of the award page endpoint, allowing attackers to inject JavaScript code via the javascript: URI scheme. The payload is executed when a user clicks the 'X' button in the top-left corner, potentially enabling account takeover or malicious actions.

## Attack scenario
1. Attacker crafts a malicious URL with javascript: scheme in the referer parameter pointing to the award page
2. Attacker sends the crafted URL to a victim via email, social media, or other communication channels
3. Victim visits the award page and sees the 'X' close button in the top-left corner
4. Victim clicks the 'X' button, which uses the unsanitized referrer parameter as the navigation target
5. JavaScript payload executes in the victim's browser with their session context
6. Attacker can steal session cookies, perform actions on behalf of the victim, or redirect to phishing pages

## Root cause
The application directly uses the 'referer' query parameter as a navigation URL (likely in an onclick handler) without validating or sanitizing the input. The parameter is placed in an anchor tag or button without filtering javascript: or data: URI schemes.

## Attacker mindset
An attacker recognizes that user-controlled parameters are reflected in clickable UI elements (the close button) without proper validation. They exploit the common pattern of using referrer parameters for navigation, injecting a javascript: URI to execute arbitrary code when the user interacts with the page.

## Defensive takeaways
- Implement a whitelist of allowed URL schemes (http, https) and reject javascript:, data:, vbscript:, and other dangerous schemes
- Validate referrer parameters against a whitelist of trusted domains using URL parsing APIs
- Use Content Security Policy (CSP) with script-src restrictions to prevent inline script execution
- Sanitize all user-controlled data before placing it in HTML attributes, especially href and onclick handlers
- Avoid using javascript: URIs; use event handlers or data attributes instead for navigation logic
- Implement URL validation on both client and server side
- Use security-focused templating engines that auto-escape user input by default

## Variant hunting
Check other navigation parameters (return, redirect, next, back, goto, url) for similar vulnerabilities
Search for other onclick, onmouseover, or other event handlers using user-controlled parameters
Test different URI schemes: data:text/html, vbscript:, about:blank, file://
Look for similar patterns in other pages like login, logout, or redirect endpoints
Test URL encoding bypass attempts: %6a%61%76%61%73%63%72%69%70%74: or variations
Check for DOM-based XSS where JavaScript processes the referrer parameter client-side

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a classic reflected XSS vulnerability exploiting unsafe handling of navigation parameters. The javascript: URI scheme is a well-known XSS vector that should be filtered on all applications. The attack requires user interaction (clicking the X button), making it a reflected rather than stored XSS. The use of video demonstration in the report is excellent practice for clarity. The application likely has a close/back button that references the referer parameter without validation.

## Full report
<details><summary>Expand</summary>

# Description
Hi, i would like to report an XSS via `javascript` scheme in `https://www.twitterflightschool.com/student/award/[ID]?referer=`, the payload e need just a click of user to be triggered because the link will be placed in `a` tag.

url:`https://www.twitterflightschool.com/student/award/███?referer=javascript:alert(document.domain)`

I attached a video demonstration:
{F818801}

# Steps to reproduce
1. go to `https://www.twitterflightschool.com/student/award/████████?referer=javascript:alert(document.domain)`
2. click in "X" button in top left of the screen
3. XSS will be triggered

## Impact

it is possible to perform malicious actions on the victim's account

</details>

---
*Analysed by Claude on 2026-05-12*
