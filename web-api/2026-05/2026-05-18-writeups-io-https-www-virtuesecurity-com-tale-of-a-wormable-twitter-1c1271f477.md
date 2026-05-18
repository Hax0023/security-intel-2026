# Wormable XSS on Twitter via Welcome Message Deeplink with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Twitter/X
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Stored XSS, DOM-based XSS, CSP Bypass, Input Validation Bypass, HTML Tag Stripping Bypass
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's Welcome Message deeplink feature that could be weaponized as a self-propagating worm. The vulnerability exploited improper HTML tag stripping logic combined with inline JSON serialization to inject malicious scripts, with the ability to bypass Twitter's Content Security Policy through syndication endpoints.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL using Twitter's Welcome Message deeplink with XSS payload in the 'text' parameter
2. Victim clicks the link, which renders as a Twitter card in an unsandboxed, same-origin iframe
3. Payload bypasses HTML tag stripping through nested tag manipulation (<</<x>/script syntax)
4. Escaped payload reflects into inline JSON object within script-serialization tags, allowing script termination via </script> tag
5. Iframe uses JSONP callback to load Twitter syndication endpoints, bypassing CSP restrictions
6. Injected JavaScript automatically retweets malicious content and sends DM links to followers, propagating the worm

## Root cause
Multiple compounding issues: (1) Improper HTML tag stripping using regex instead of proper parsing, allowing nested tag bypass; (2) Reflection of unsanitized user input into inline JSON serialization context; (3) HTML parser behavior where </script> tags terminate script blocks regardless of string context; (4) Unsandboxed same-origin iframe with DOM access to parent; (5) CSP whitelist including JSONP endpoints that could be abused for callback injection

## Attacker mindset
Systematic security researcher who recognized that tag stripping is inherently fragile and error-prone compared to escaping. Rather than accepting input validation at face value, the attacker iterated through nested tag variations to find parser inconsistencies. Demonstrated deep understanding of HTML parsing semantics, JSON serialization context, CSP policy analysis, and browser callback mechanisms to chain vulnerabilities into a weaponized worm.

## Defensive takeaways
- Avoid HTML tag stripping via regex; use proper HTML parsing libraries or context-aware output encoding instead
- Never trust that input validation alone prevents XSS—always apply defense-in-depth with proper output encoding based on context (HTML, JSON, URL, etc.)
- Reflect user input into JSON within script tags only with strict escaping; consider JSON.stringify() for serialization
- Sandbox all iframes, especially those containing user-controlled content, even if same-origin
- Review CSP whitelists regularly for endpoints that support JSONP or callback parameters that could enable CSP bypass
- Understand HTML parser behavior, especially script tag termination rules and how </script> tags are recognized
- Implement feature-based security: consider whether welcome message deeplinks need iframe rendering or if alternative approaches exist

## Variant hunting
['Test other Twitter features that use inline JSON serialization for user-controlled data (quotes, captions, metadata)', 'Audit other iframe-based Twitter components for similar tag-stripping logic and unsandboxed rendering', 'Review all Twitter endpoints whitelisted in CSP policies for JSONP/callback parameter support', 'Examine other deeplink types (intent links, composer links) that may use similar Twitter card rendering', 'Fuzz HTML tag stripping implementation with various nesting patterns: <<x>tag</x>>, <x<<>/x>>, etc.', 'Test nested script tag contexts in other Twitter serialization mechanisms (timeline.js, widget.js)']

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1059.007
- T1176

## Notes
This vulnerability exemplifies how security controls can appear robust but fail under layered attack combining multiple weak points. The researcher's decision to report after discovering the XSS but before completing the CSP bypass demonstrates responsible disclosure prioritization. The wormable aspect (automatic retweeting and DM propagation) could have enabled rapid account compromise at massive scale. Twitter Card iframes represent a particular risk surface due to same-origin rendering requirements combined with user content. The specific exploit demonstrates sophisticated understanding of Twitter's architecture and browser security mechanics.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
