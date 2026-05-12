# CSS Injection via BB Code Tag Attribute Filtering Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 587727 | https://hackerone.com/reports/587727
- **Submitted:** 2019-05-22
- **Reporter:** hanno
- **Program:** HackerOne (undisclosed platform)
- **Bounty:** Not specified in writeup
- **Severity:** Medium
- **Vuln:** CSS Injection, Improper Input Validation, UI Redressing/Clickjacking
- **CVEs:** CVE-2019-16108
- **Category:** memory-binary

## Summary
A BB code tag fails to properly sanitize CSS style input, allowing attackers to inject arbitrary CSS properties through the style attribute. While quote characters are filtered to prevent breakout, CSS positioning properties enable UI redressing attacks. This permits malicious actors to visually manipulate page layout in forum posts.

## Attack scenario
1. Attacker crafts malicious BB code post containing the vulnerable tag with injected CSS
2. CSS properties like position:fixed and z-index are injected to position elements over legitimate UI
3. Post is submitted to forum where victims view the content
4. Browser renders the post and applies the injected CSS styles to create visual overlays
5. Victim believes they are interacting with legitimate UI but are actually clicking attacker-controlled overlay elements
6. Attacker captures clicks or sensitive interactions through the positioned UI redressing layer

## Root cause
Input filtering removes only quote characters but fails to implement a whitelist-based CSS property validator or Content Security Policy. The application converts user input directly into style attributes without proper CSS parsing or validation, allowing dangerous properties like position, z-index, and top/left coordinates to pass through.

## Attacker mindset
Exploit the incomplete input sanitization by focusing on CSS properties that don't require quotes. Use CSS positioning (position:fixed, z-index, absolute positioning with coordinates) to create UI redressing attacks that trick users into unintended actions while browsing forums.

## Defensive takeaways
- Implement whitelist-based CSS property validation rather than blacklist filtering of characters
- Use CSS parsing libraries to validate and sanitize all CSS input before applying to DOM
- Disable dangerous CSS properties in user-controlled styles (position, z-index, display, visibility, opacity in certain contexts)
- Implement Content Security Policy (CSP) with style-src restrictions to limit inline style impact
- Use CSS namespacing or shadow DOM to isolate user-generated content from page styling
- Consider converting BB code to plain text with minimal formatting rather than CSS-based styling
- Apply defense-in-depth with additional clickjacking protections (X-Frame-Options, frame-busting JavaScript)

## Variant hunting
Test other BB code tags for similar CSS injection vulnerabilities
Check if other quote-like characters (single quotes, backticks, unicode variants) bypass filtering
Test CSS @import and @keyframes injection within style attributes
Attempt to inject CSS expressions or calc() functions for dynamic values
Check if other delimiters or escape sequences can bypass the quote filter
Test with CSS custom properties (--var) for potential indirect injection
Verify if the vulnerability exists in other user-generated content contexts (comments, profiles)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071.001 - Application Layer Protocol
- T1648 - Serverless Execution
- T1656 - Impersonation

## Notes
The writeup references a specific BB code tag with redacted name (shown as █████). The vulnerability demonstrates classic input validation weakness where character-level filtering (removing quotes) provides false sense of security. CSS injection is particularly dangerous in user-controlled content contexts due to the breadth of CSS capabilities for visual manipulation and UI redressing attacks.

## Full report
<details><summary>Expand</summary>

The input to the "█████" BBcode tag is not properly filtered. It gets converted into a CSS style attribute for a span HTML element.

Quotes (") are removed, so there's no way to break out of the CSS style attributed. However it is possible to arbitrarily dress the resulting span element.

To illustrate this here's an example:

███████

This will place a skull on the top of the page (by using position:fixed). I'll attach a screenshot as well.

The power of CSS pretty much allows arbitrary placement of elements across the page. This may also be used in UI redressing attacks.

## Impact

Attacker can arbitrarily redress page via forum posts.

</details>

---
*Analysed by Claude on 2026-05-12*
