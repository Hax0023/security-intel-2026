# Wormable XSS on Twitter via Welcome Message Deeplink with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Twitter
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Stored XSS, Reflected XSS, HTML Tag Stripping Bypass, CSP Bypass, XSS Worm
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's Welcome Message deeplink feature that could be weaponized as an XSS worm to spread from account to account. The vulnerability exploited improper HTML tag stripping logic combined with Twitter Card iframe rendering to inject malicious scripts that bypass Content Security Policy restrictions.

## Attack scenario (step by step)
1. Attacker crafts a specially-formatted URL using Twitter's Welcome Message deeplink with a malicious payload in the text parameter
2. The payload is designed to bypass input validation by exploiting the HTML tag stripping regex using nested angle bracket patterns (e.g., <</<x>/script/>)
3. When a victim visits the link, it renders as a Twitter Card with an unsandboxed iframe pointing to the message composition interface
4. The malicious payload gets reflected into an inline JSON object within a script tag, with the closing </script> tag terminating the script block early
5. The injected iframe and script tags execute in the context of Twitter's same-origin domain, gaining full DOM access
6. The worm uses JSONP callbacks to the Twitter syndication API to automatically retweet and spread the payload to the victim's followers

## Root cause
Three compounding vulnerabilities: (1) Improper HTML tag stripping using regex instead of proper HTML parsing, allowing nested bracket patterns to bypass the filter; (2) Unsafe reflection of user input into inline script tags within JSON objects without proper escaping; (3) Unsandboxed iframe rendering of Twitter Cards that provides DOM access to parent page and access to form submission mechanisms

## Attacker mindset
The attacker demonstrated sophisticated understanding of HTML parsing quirks, Twitter's internal architecture (cards, syndication APIs, JSONP endpoints), and CSP policy structure. The approach was methodical: first identify the injection point, then iteratively fuzz the tag-stripping filter, chain multiple vulnerabilities together, and weaponize the XSS as a self-propagating worm using legitimate Twitter features (retweet functionality, message cards). This represents thinking like a platform architect trying to abuse legitimate features rather than simple input injection.

## Defensive takeaways
- Never use regex or manual string operations for HTML tag stripping; use proper HTML parsing libraries
- Properly escape or sanitize all user input before reflection into inline script tags, especially within JSON structures
- Always sandbox third-party and untrusted iframes using the 'sandbox' attribute with minimal necessary permissions
- Avoid using same-origin iframes for user-controlled content rendering; consider using separate origins
- Test CSP policies against practical bypass techniques like JSONP endpoints and syndication APIs
- Be cautious of deeplink parameters that control rendered content, as they can introduce multiple injection vectors
- Implement input length limits thoughtfully; 300 character limit was insufficient given nested payload techniques
- Regularly audit and minimize CSP whitelist to avoid including APIs that can be abused for script injection (JSONP callbacks)

## Variant hunting
['Look for other Twitter Card types that might have similar unsafe reflection patterns in their iframe content', 'Search for other deeplink parameters that control inline JSON serialization in script tags', 'Investigate other Twitter APIs that accept JSONP callbacks and might be whitelisted in CSP', 'Test similar tag-stripping implementations on other platforms for nested bracket bypass patterns', 'Hunt for unsandboxed iframes on other social platforms that render user-controlled content', "Look for other places where Twitter's syndication API endpoints are whitelisted in CSP policies", 'Examine other message composition features that might reflect user input without proper sanitization']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204
- T1059
- T1485

## Notes
This vulnerability exemplifies the danger of chaining multiple seemingly minor security weaknesses into a critical attack. The tag-stripping bypass using <</<x>/script/> is particularly instructive as it shows how parsing edge cases can defeat naive input validation. The worm aspect makes this especially severe as it could spread exponentially without user interaction beyond viewing a malicious tweet. The researcher's decision to report before fully weaponizing the CSP bypass demonstrates responsible disclosure. The use of JSONP callbacks and form submission methods shows deep understanding of how to abuse legitimate platform features for exploitation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
