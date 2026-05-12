# Stored Cross-Site Scripting (XSS) in Forum User Nickname via Search Function

## Metadata
- **Source:** HackerOne
- **Report:** 1161241 | https://hackerone.com/reports/1161241
- **Submitted:** 2021-04-12
- **Reporter:** quadrant
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored XSS, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in forum.acronis.com where user-controlled nickname data is not properly sanitized during modification and is rendered unescaped in search results. An attacker can inject malicious JavaScript in their nickname that executes when other users search for authors containing that nickname.

## Attack scenario
1. Attacker creates or modifies their forum account nickname to include JavaScript payload: '<script>alert(0)</script>'
2. Attacker's modified nickname is stored in the database without sanitization or validation
3. Victim uses the forum's search function and enters search criteria that matches the attacker's malicious nickname
4. Forum returns search results displaying the attacker's nickname without HTML encoding
5. Victim's browser parses and executes the injected JavaScript payload
6. Attacker's malicious script runs in victim's session context, potentially stealing credentials, session tokens, or performing actions on behalf of the victim

## Root cause
The application fails to implement input validation/sanitization when accepting nickname modifications and fails to apply output encoding when rendering usernames in search results. No Content Security Policy (CSP) or HTML entity encoding is applied to user-controlled data displayed in search functionality.

## Attacker mindset
An attacker recognizes that user profile fields like nicknames are often trusted and may bypass security controls. They leverage the search feature as an attack vector because it's a high-traffic function where multiple users will view unsanitized nickname data. The attacker can craft nicknames with common search terms to maximize exposure.

## Defensive takeaways
- Implement strict input validation on all user-modifiable profile fields, including nicknames - whitelist allowed characters or blacklist dangerous ones
- Apply HTML entity encoding (e.g., &lt;, &gt;, &quot;) to all user-controlled data before rendering in HTML context
- Deploy a Content Security Policy (CSP) header to prevent inline script execution
- Use templating engines with auto-escaping enabled by default
- Implement output encoding based on context (HTML, JavaScript, URL, CSS)
- Conduct security code review of all user input handling, particularly in search/display functions
- Perform regular security testing including XSS testing on dynamic content rendering

## Variant hunting
Check other user profile fields (bio, description, signature) for similar XSS vulnerabilities
Test search functionality for other user-controlled parameters (post titles, category names, tags)
Investigate comment sections and user-generated content areas for stored XSS
Review other forum features that display user data without encoding (user listings, activity feeds, notifications)
Test DOM-based XSS vectors in search result filtering/sorting JavaScript
Check email notification features that may contain unencoded usernames
Review API endpoints that return user data for JSON context XSS

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1204

## Notes
This is a classic stored XSS vulnerability with high impact due to the search function being a commonly-used feature. The attack surface is large as any user performing author searches will be affected. The fix is straightforward (input validation + output encoding) but requires defense-in-depth approach. The vulnerability demonstrates why user profile fields cannot be blindly trusted even if they seem non-critical.

## Full report
<details><summary>Expand</summary>

## Summary

There is an XSS vulnerability in the search function of the forum (forum.acronis.com).

## Steps To Reproduce

  1. Modify your own forum Nickname, add the following payload after the original nickname:

```
<script>alert(0)</script>
```

  2. Fill in your nickname in the Author form of the search function and wait for the search, it will automatically trigger a pop-up.

{F1262581}

## Recommendations

Add special character filtering to the nickname modification function of the forum.

## Impact

You can add any keywords that users may use when searching for authors to your nickname to attack the corresponding users. It is possible to execute any Javascript.

</details>

---
*Analysed by Claude on 2026-05-12*
