# Tale of a Wormable Twitter XSS

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Stored XSS, CSP Bypass, Input Validation Bypass, HTML Tag Stripping Bypass
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's direct message welcome message feature that could be weaponized as a self-propagating worm. The vulnerability exploited improper HTML tag stripping logic and CSP policy weaknesses to execute arbitrary JavaScript across user accounts.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL containing XSS payload in the text parameter of Twitter's direct message deeplink
2. Victim clicks the link which renders a Twitter card containing an iframe pointing to twitter.com/i/cards/tfw/v1/...
3. The payload gets reflected into an inline JSON object within a <script type='twitter-cards-serialization'> tag as the default_composer_text value
4. Attacker bypasses HTML tag stripping by using nested angle brackets (e.g., <</<x>/script>) that get normalized to valid HTML tags
5. Attacker injects iframe and script tags that leverage whitelisted syndication.twimg.com domain to bypass CSP restrictions
6. XSS executes in same-origin context with DOM access, allowing automatic retweet propagation and infection of follower accounts

## Root cause
Multiple compounding issues: (1) Unsafe HTML tag stripping implementation using regex instead of proper HTML parsing, (2) Reflection of user input into inline script tag context without proper escaping, (3) CSP policy that whitelists attacker-controllable domains (syndication.twimg.com), (4) Unsandboxed same-origin iframe allowing DOM manipulation

## Attacker mindset
The researcher demonstrated sophisticated understanding of HTML parsing edge cases, script tag termination semantics, and CSP bypass techniques. They systematically probed limitations (quote escaping, tag stripping, character truncation, CSP) and iterated through payload variations until finding the specific nested tag syntax that bypassed validation. The worm concept shows intent to understand cascading impact and account-to-account propagation.

## Defensive takeaways
- Never use regex or custom string manipulation for HTML parsing; use proper HTML parsing libraries
- Do not reflect user input directly into script tag context; use JSON escaping and safe DOM APIs
- Implement strict CSP with no whitelisting of user-controllable domains; use nonces for legitimate inline scripts
- Sandbox all iframes and avoid same-origin iframes for untrusted content
- Test input validation bypasses using variations: nested tags, entity encoding, case variations, Unicode normalization
- Perform security-focused code review of all input filtering logic, particularly tag stripping
- Use Content-Security-Policy with script-src 'nonce-...' only, avoiding domain whitelisting when possible

## Variant hunting
['Test similar nested angle bracket patterns (<</, <><, etc.) against other tag stripping implementations', 'Search for other Twitter endpoints that reflect user input into script contexts', 'Investigate other whitelisted domains in CSP policies for JSONP or callback-based injection points', 'Look for similar deeplink patterns in other social platforms that render cards/previews', 'Test character truncation boundaries (300 chars) to find alternative payload lengths', "Probe for other HTML serialization contexts that might use script type='...' tags for data storage"]

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1566.002
- T1204.001

## Notes
This writeup is from May 2019 and demonstrates a critical chaining of multiple vulnerabilities. The researcher responsibly disclosed after initial XSS confirmation rather than waiting for full CSP bypass. The tag stripping bypass using nested syntax (<</<x>/script>) is particularly noteworthy as a common implementation error. The worm potential via retweet automation and automatic iframe injection shows high impact. URL contains percent-encoded payload: %3C%3Cx%3E represents <<x> which demonstrates the nesting technique used.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
