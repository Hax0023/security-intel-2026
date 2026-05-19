# Tale of a Wormable Twitter XSS - Stored XSS with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Twitter/X
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Stored XSS, Improper Input Validation, HTML Tag Stripping Bypass, CSP Policy Bypass, Self-XSS to Worm
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's direct message deeplinks where user-supplied text in the 'text' parameter was reflected unsafely in an inline JSON object within a same-origin iframe. The vulnerability could be weaponized as an XSS worm by chaining together multiple bypass techniques to overcome input validation and CSP restrictions, allowing automatic exploitation of any user who clicks a malicious link.

## Attack scenario (step by step)
1. Attacker crafts a malicious deeplink URL using Twitter's messages/compose endpoint with a specially crafted 'text' parameter containing XSS payload
2. Attacker bypasses HTML tag stripping by using nested angle brackets and tag splitting techniques (e.g., <</<x>/script/test000>)
3. Attacker exploits HTML parsing behavior where closing script tags terminate script context regardless of string context
4. When victim clicks the deeplink, it renders as a Twitter card (iframe) pointing to twitter.com/i/cards/tfw/v1/
5. The payload is reflected into inline JSON within a <script type='text/twitter-cards-serialization'> tag, breaking the JSON structure and executing JavaScript
6. Attacker uses JSONP callback technique with whitelisted syndication.twimg.com domain to bypass CSP, then auto-submits forms to retweet and spread the worm

## Root cause
Multiple layered failures: (1) Naive HTML tag stripping using regex/parsing rather than proper HTML entity encoding, (2) Unsafe reflection of user input into inline JSON within script tags without proper escaping, (3) Same-origin iframe without sandbox attribute allowing DOM manipulation, (4) CSP policy with overly permissive whitelisted domains (syndication.twimg.com) that support JSONP callbacks

## Attacker mindset
Sophisticated researcher with deep understanding of HTML parsing quirks, JSON/script context breaking, and CSP bypasses. Recognized that tag stripping is inherently error-prone and tested edge cases with nested tags. Understood the power of self-propagating worms and weaponized a self-XSS into a viral payload through chained exploits.

## Defensive takeaways
- Never use HTML tag stripping with regex - use proper HTML entity encoding/escaping instead
- When reflecting user input into JSON within script tags, ensure strict escaping of special characters (especially <, >, /, quotes)
- Always sandbox iframes when possible and use 'sandbox' attribute with minimal permissions
- Review CSP whitelists carefully - JSONP endpoints are particularly dangerous as they allow callback-based code execution
- Apply defense-in-depth: don't rely on single layer of protection (validation, encoding, CSP, sandbox)
- Test input validation with nested/split tag patterns: <</, <x>, tag attribute injection
- Consider Content-Security-Policy directives like 'script-src' should not include callback-based endpoints or use stricter nonce validation

## Variant hunting
Look for similar patterns in: (1) Other social platforms' deeplink/card rendering mechanisms, (2) Any endpoint that reflects URL parameters into inline script tags/JSON, (3) Tag stripping functions in legacy code, (4) iframes with same-origin but no sandbox, (5) JSONP endpoints on CDNs or whitelisted domains, (6) Welcome message/DM features in messaging platforms that support rich formatting

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing (Link-based social engineering)
- T1566 - Phishing (Email/message delivery)
- T1047 - Windows Management Instrumentation (N/A - web context)
- T1203 - Exploitation for Client Execution
- T1204 - User Execution: Malicious Link

## Notes
This is an excellent example of chaining multiple seemingly-minor vulnerabilities into a critical worm. The researcher demonstrated sophisticated understanding of HTML parsing (script tag context termination), JSON escaping, CSP policies, and JSONP callback exploitation. The use of <</<x> as a tag-splitting technique is particularly clever. Reported responsibly to Twitter without waiting for complete CSP bypass discovery. The 300-character truncation was overcome through careful payload optimization. This vulnerability showcases why input validation (stripping) without proper encoding is fundamentally flawed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
