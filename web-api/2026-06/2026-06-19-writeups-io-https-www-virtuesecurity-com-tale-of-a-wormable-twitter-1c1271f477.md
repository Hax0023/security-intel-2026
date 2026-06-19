# Tale of a Wormable Twitter XSS - Stored XSS in Welcome Messages with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Twitter
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Stored Cross-Site Scripting (XSS), HTML Tag Stripping Bypass, Content Security Policy (CSP) Bypass, JSONP Injection, Unsafe iframe usage
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's welcome message deeplinks that could be weaponized as a self-propagating XSS worm. The vulnerability exploited flawed HTML tag stripping validation, unsafe iframe rendering without sandbox restrictions, and JSONP callback mechanisms to bypass CSP protections.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL containing nested HTML tags designed to bypass tag-stripping regex: https://twitter.com/messages/compose with text parameter containing <<x>/script><script src=...>
2. User clicks the URL or receives it in a message, which renders as a Twitter card (iframe pointing to twitter.com/i/cards/tfw/v1/...)
3. The iframe is same-origin and unsandboxed, allowing DOM access to parent. Payload reflects into inline JSON object within <script type="text/twitter-cards-serialization">
4. HTML parser encounters closing </script> tag injected via tag-stripping bypass, terminating the JSON serialization script block prematurely and executing attacker's injected script
5. Injected script uses JSONP callbacks to `syndication.twimg.com/timeline/profile` with callback parameter set to `__twttr/alert` or `__twttr/frames[0].retweet_btn_form.submit`
6. Worm automatically retweets original malicious tweet to attacker's followers, propagating infection throughout the network with each new victim

## Root cause
Multiple compounded vulnerabilities: (1) HTML tag stripping using regex/parsing instead of proper HTML entity encoding, (2) unsafe iframe with same-origin policy and no sandbox attribute, (3) user input reflected into JSON object without proper escaping, (4) JSONP endpoints accepting arbitrary callback functions, (5) CSP policy with whitelisted domains that support JSONP

## Attacker mindset
Researchers recognized that while individual mitigations (quote escaping, tag stripping, character truncation, CSP) appeared sufficient in isolation, chaining vulnerabilities together could bypass all protections. The key insight was that HTML tag stripping is inherently fragile compared to encoding, and that whitelisted domains for CSP can become attack vectors if they support unsafe patterns like JSONP.

## Defensive takeaways
- Never rely on tag stripping for XSS prevention - use proper HTML entity encoding/escaping instead
- Apply sandbox attribute to all iframes, especially those containing user-generated content or reflecting parameters
- Sanitize user input before inserting into JSON/JavaScript contexts, not just HTML contexts
- Audit whitelisted CSP domains for unsafe patterns (JSONP, open redirects, parameter injection)
- Use Content-Security-Policy: script-src with strict nonces or hashes, avoid relying on domain whitelisting alone
- Implement multiple layers of validation: input validation, output encoding, CSP, and frame sandboxing
- Test tag stripping with nested/malformed tag combinations: <<x>/tag>, </<x>, etc.
- Consider using structured serialization formats with type safety instead of embedding JSON in script tags

## Variant hunting
Search for other parameters reflected into JSON objects within script tags on Twitter and other platforms. Hunt for iframe endpoints that accept user-controlled parameters without proper sanitization. Examine JSONP endpoints on whitelisted CSP domains for callback parameter injection. Look for nested tag bypass patterns in HTML parsers: <<x>, </</x>, <x/>, <x x=, etc. Test character truncation combined with tag stripping - can you inject closing tags before truncation point?

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1204 - User Execution
- T1566 - Phishing
- T1552 - Unsecured Credentials

## Notes
This writeup demonstrates the critical importance of defense-in-depth. Twitter had implemented multiple security controls (input validation, CSP, character limits) but vulnerability chaining defeated all of them. The worm potential is particularly dangerous as it would have automatically retweet itself to followers, creating exponential spread. The researcher responsibly reported after identifying the core XSS without waiting to fully develop the CSP bypass, showing mature responsible disclosure practices. The use of JSONP with user-controlled callback parameters on whitelisted domains is a common CSP bypass pattern worth monitoring.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
