# Stored XSS on BuddyPress Plugin via Groups Name with Accesskey Trigger

## Metadata
- **Source:** HackerOne
- **Report:** 592316 | https://hackerone.com/reports/592316
- **Submitted:** 2019-05-29
- **Reporter:** yxw21
- **Program:** BuddyPress
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Stored XSS, Improper Output Encoding, Accessibility Attribute Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the BuddyPress groups feature where group names are not properly sanitized, allowing attackers to inject malicious HTML/JavaScript using the HTML accesskey attribute. The payload is triggered when users press a specific key combination (Shift+Ctrl+Option+X on macOS or Shift+Alt+X on Windows), executing arbitrary JavaScript in their browser.

## Attack scenario
1. Attacker creates or modifies a BuddyPress group and sets the group name to a crafted payload containing HTML with accesskey and onclick handlers
2. The malicious group name is stored in the database without proper sanitization or encoding
3. The group page is rendered and the unsanitized group name is output in the HTML, creating an accessible link element with the payload
4. Legitimate users visit the group page and unknowingly press the accesskey combination (varies by OS)
5. The accesskey triggers the injected onclick handler, executing the attacker's JavaScript code
6. The JavaScript can steal session cookies, perform actions on behalf of the user, or escalate to RCE depending on server-side capabilities

## Root cause
The BuddyPress plugin fails to properly sanitize and encode user-supplied group names before storing them in the database and rendering them in HTML output. The vulnerability leverages HTML5 accesskey attributes combined with event handlers to bypass user interaction requirements.

## Attacker mindset
An attacker with the ability to create or modify groups exploits insufficient input validation to achieve persistent XSS. The accesskey-based trigger is a sophisticated obfuscation technique that evades simple scanning and makes the attack appear accidental to users.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied data, particularly group names and identifiers
- Apply proper output encoding (HTML entity encoding) when rendering user-controlled data in HTML context
- Use Content Security Policy (CSP) headers to restrict inline script execution
- Sanitize HTML attributes and remove potentially dangerous attributes like accesskey when used in untrusted contexts
- Implement both allowlist-based sanitization and context-aware encoding
- Regularly audit WordPress/BuddyPress plugins for XSS vulnerabilities
- Use security libraries like DOMPurify or OWASP HTML Sanitizer for output encoding
- Test for XSS using both event handlers and accessibility attributes

## Variant hunting
Check other input fields in BuddyPress (activity streams, forum posts, profile fields) for similar encoding issues
Test other HTML attributes that trigger JavaScript execution (onload, onerror, onfocus, onmouseover)
Investigate if other accessibility features (tabindex combined with keyboard events) can be abused
Check if group descriptions, URLs, or custom fields have similar vulnerabilities
Test for variations in different WordPress themes and BuddyPress configurations
Examine whether the vulnerability exists in related plugins like BP Activity, BP Private Messaging

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204
- T1059
- T1133

## Notes
This is a clever variant of stored XSS that requires unusual user interaction (specific keyboard shortcut) making it less likely to be triggered accidentally but still exploitable for targeted attacks. The RCE claim in the impact section is overstated without evidence of server-side code execution capability; the vulnerability is primarily client-side XSS. The vulnerability requires group creation/modification privileges, limiting the attack surface to authenticated users or installations allowing group creation.

## Full report
<details><summary>Expand</summary>

Hi, I found that there is a storage xss in another output group name, but this xss needs to press the key combination to trigger. Just create or modify the group information, set the group name to the following payload, 
```
<a href="accesskey=x onclick=alert(document .domain)//"></a>
```
and then access Group page, 
if you are macos need to press, 
shift+control+option+x,
if you are windows, 
you need to press shift+alt+x, 
then it will trigger xss
{F498582}

Don't forget to enable the group feature

## Impact

Rce via xss

</details>

---
*Analysed by Claude on 2026-05-12*
