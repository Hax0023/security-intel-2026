# XSS via Mod Log Removed Posts

## Metadata
- **Source:** HackerOne
- **Report:** 1504410 | https://hackerone.com/reports/1504410
- **Submitted:** 2022-03-09
- **Reporter:** ahacker1
- **Program:** Reddit
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Reddit's mod notes feature where malicious JavaScript payloads injected into post titles execute when moderators view the mod log of removed posts. The vulnerability is triggered when a moderator removes a post containing XSS payload in its title and subsequently accesses the attacker's mod notes or profile.

## Attack scenario
1. Attacker creates a new post on a subreddit with an XSS payload embedded in the post title
2. Subreddit moderator reviews the post and decides to remove it from the subreddit
3. The removed post information (including unsanitized title) is stored in the mod log/mod notes
4. When the moderator opens the mod notes section to view actions taken on the attacker's account, the stored payload executes
5. Alternatively, if the moderator hovers over the attacker's profile after recent mod action, mod notes are displayed and payload triggers
6. Attacker gains ability to execute arbitrary JavaScript in moderator's browser session, potentially stealing session tokens or performing actions as the mod

## Root cause
The mod log/mod notes feature fails to properly sanitize or encode user-controlled input (post title) before storing and displaying it. The application trusts the stored data and renders it without HTML escaping, allowing arbitrary script execution.

## Attacker mindset
An attacker with basic forum access can craft a simple malicious post title to compromise moderator accounts. This is an attractive vector because moderators have elevated privileges, making their session compromise highly valuable. The attack requires minimal effort and low technical skill.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-controlled content, including post titles
- Apply HTML entity encoding/escaping to all data before rendering in HTML context
- Use Content Security Policy (CSP) headers to mitigate XSS impact
- Store data in a safe format and perform contextual output encoding at display time rather than relying on input sanitization alone
- Implement security headers like X-XSS-Protection
- Regular security testing of mod tools and admin interfaces which handle user-generated content
- Use a template engine that auto-escapes by default

## Variant hunting
Check other mod action displays (bans, approvals, removals) for similar XSS vectors
Examine user profile displays that show mod notes or recent actions
Test other fields in post metadata (flair, custom fields) for similar vulnerabilities
Check comment removal mod logs and notes
Investigate user report notes and mod team communication features for similar flaws
Test other moderation interfaces that display user-generated content from removed posts

## MITRE ATT&CK
- T1190
- T1566

## Notes
This is a classic stored XSS vulnerability with a privilege escalation component - the attacker targets moderators who have elevated platform privileges. The vulnerability is particularly dangerous because mod tools are critical infrastructure for platform safety. The dual trigger mechanism (direct mod notes view + profile hover) increases the likelihood of exploitation.

## Full report
<details><summary>Expand</summary>

## Summary:
I have discovered an XSS vulnerability regarding the mod notes feature. Specifically, the XSS payload executes when the victim removes a post in a subreddit and opens up the mod notes of the attacker.

## Steps To Reproduce:

1. The attacker creates a new post with the title containing the XSS payload.
2. The victim (mods of the subreddit) then must remove your post.
3. The payload executes when a victim (subreddit mod) opens up your mod notes. Sometimes, the mod notes are displayed when the victim hovers on your profile (this is true when a recent mod action has been taken on the user). 

## Supporting Material/References:

█████
█████

## Impact

Impact Below:

</details>

---
*Analysed by Claude on 2026-05-12*
