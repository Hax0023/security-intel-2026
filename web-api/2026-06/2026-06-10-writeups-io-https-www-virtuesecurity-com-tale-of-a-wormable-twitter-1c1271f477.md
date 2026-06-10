# Tale of a Wormable Twitter XSS - Stored XSS in Welcome Messages with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Twitter
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Stored Cross-Site Scripting (XSS), HTML Tag Stripping Bypass, Content Security Policy (CSP) Bypass, Input Validation Bypass, XSS Worm
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's Welcome Messages feature where user input in the 'text' parameter was reflected unsafely in an inline JSON object within a script tag. The vulnerability could be exploited to create a self-propagating XSS worm by chaining multiple bypasses: HTML tag stripping logic flaws, quote escaping circumvention, and CSP policy weaknesses via whitelisted external script sources.

## Attack scenario (step by step)
1. Attacker crafts a malicious Welcome Message deeplink with XSS payload in the 'text' parameter
2. The deeplink renders as a Twitter card containing an unsandboxed iframe pointing to twitter.com/i/cards/tfw/v1/
3. User input is reflected directly into an inline JSON object within a <script type='twitter-cards-serialization'> tag
4. Attacker uses nested tag syntax (<</<x>/script>) to bypass HTML tag stripping, resulting in valid closing </script> tag
5. Malicious scripts execute with access to parent DOM, including ability to trigger retweets and retransmit payload
6. Worm self-propagates as infected users retweet the malicious message, spreading to their followers

## Root cause
Multiple security control failures: (1) Unsafe reflection of user input into inline script JSON without proper escaping, (2) Flawed HTML tag stripping implementation using regex/string replacement instead of proper HTML parsing, (3) Unsandboxed iframes allowing DOM access to parent, (4) CSP policy with overly permissive whitelisting of external domains (twimg.com, ton.twitter.com) that could be exploited for callback injection

## Attacker mindset
Reconnaissance-focused approach: systematically tested tag stripping boundaries by iterating through payloads, recognized that regex-based tag stripping is inherently fragile, understood HTML parsing rules (script tag termination behavior), chained multiple weaknesses rather than relying on single bypass, and deliberately reported CSP bypass incomplete to demonstrate responsible disclosure

## Defensive takeaways
- Never use regex or string-based HTML tag stripping; use proper HTML parsing libraries (e.g., OWASP HTML Sanitizer, DOMPurify)
- Escape output when inserting user input into JSON within script tags, or better yet, avoid this pattern entirely
- Implement context-aware output encoding based on where data will be consumed (HTML, JSON, JavaScript, URL contexts require different escaping)
- Use sandboxed iframes with explicit permissions (sandbox attribute) to restrict DOM access and prevent privilege escalation
- Review CSP whitelists critically; avoid whitelisting broad domains - use nonces/hashes for inline scripts instead
- Test input validation and filtering against edge cases: nested tags, mixed case, Unicode variants, and encoding tricks
- Implement defense-in-depth: rely on multiple layers (input validation + output encoding + CSP + sandboxing) rather than single controls
- Monitor for self-propagating attack patterns; worm-capable exploits warrant immediate patching
- Conduct security code review of all tag stripping/filtering logic with emphasis on parser specification compliance

## Variant hunting
['Search for similar tag stripping logic in other endpoints handling user-supplied HTML content', 'Test quote escaping in other JSON serialization contexts (API responses, cached content, emails)', 'Audit all iframe implementations for sandbox attribute presence and necessity', 'Review CSP policies across all subdomains for overly permissive whitelisting patterns', 'Check deeplink handlers and card rendering systems for reflection vulnerabilities', 'Test nested/malformed HTML tag variations against filtering rules (case mutations, Unicode encodings, HTML entities)', 'Investigate other message-based features (DMs, comments, notifications) for similar reflection patterns', 'Examine callback parameter usage in syndication endpoints for JSONP injection vulnerabilities']

## MITRE ATT&CK
- T1190
- T1059
- T1204.001
- T1566.002

## Notes
This is a seminal example of XSS worm architecture and defense evasion. The researcher's methodology of iterating on tag stripping bypasses (<</<x>/script>) demonstrates deep understanding of HTML parsing specification. The vulnerability is particularly dangerous because it combines: (1) auto-execution via card rendering, (2) worm propagation via retweet functionality, (3) unsandboxed DOM access, and (4) victim's own credentials for retransmission. The writeup notably cuts off before fully detailing the CSP bypass mechanism, suggesting either responsible disclosure timing or technical documentation constraints. The vulnerability likely had a CVE assignment and the full CSP bypass likely involved exploiting callback parameter injection in whitelisted twimg.com endpoints to load attacker-controlled scripts.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
