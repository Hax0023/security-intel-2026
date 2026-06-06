# Tale of a Wormable Twitter XSS - Stored XSS with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Twitter/X
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Stored Cross-Site Scripting (XSS), XSS Worm, Content Security Policy Bypass, HTML Tag Stripping Bypass, Input Validation Bypass
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's direct message welcome message feature where user input was reflected in a JSON serialization object within an iframe without proper sanitization. The vulnerability could be chained with HTML tag stripping bypass and CSP policy exploitation to create a self-propagating XSS worm that spreads across user accounts.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL using Twitter's messages deeplink with a carefully crafted payload in the text parameter
2. The payload exploits improper HTML tag stripping by using nested tags (e.g., <</<x>/script>) to bypass the filter
3. The Twitter card renders the deeplink as an unsandboxed iframe pointing to twitter.com/i/cards/tfw/v1/[id]
4. The payload gets reflected in the inline JSON object within a <script type='text/twitter-cards-serialization'> tag as the default_composer_text value
5. The HTML parser encounters an unescaped </script> closing tag in the string, terminating the script block prematurely and executing attacker code
6. The injected iframe and scripts execute with DOM access, allowing automated retweeting or propagation to followers, creating a worm effect

## Root cause
Multiple layered input validation failures: (1) HTML tag stripping implemented with regex/parsing rather than proper encoding, (2) insufficient context-aware escaping in JSON serialization within script tags, (3) unsandboxed iframe allowing DOM access, (4) HTML parser behavior allowing premature script tag termination via unescaped closing tags in string values

## Attacker mindset
Researcher identified that character escaping alone was insufficient and recognized HTML tag stripping as typically error-prone. Systematically fuzzed payloads with nested tags and special characters to bypass filters. Recognized the worm potential through iframe-based automated actions (retweet form submission). Understood HTML parsing semantics to exploit script tag termination rules.

## Defensive takeaways
- Never rely on regex-based HTML tag stripping; use proper HTML parsers and context-aware output encoding
- Apply appropriate encoding based on context: HTML entity encoding for HTML context, JSON escaping for JSON context, JavaScript escaping for script context
- Implement defense-in-depth: combine output encoding, CSP, input validation, and sandboxing
- Use nonce-based or hash-based CSP for inline scripts rather than unsafe-inline or overly permissive whitelists
- Sandbox all third-party iframes and limit DOM access to parent frames where possible
- Implement strict Content-Security-Policy with 'strict-dynamic' to prevent JSONP and similar bypasses
- Test security controls with polyglot payloads and nested encoding attempts
- Consider double-encoding user input in JSON contexts within script tags, or move data outside script tags entirely

## Variant hunting
['Hunt for other parameters that get reflected in JSON serialization objects within unescaped script tags', 'Search for additional unsandboxed iframes with DOM access to parent windows', 'Test other deeplink parameters for similar tag stripping weaknesses', 'Look for JSONP endpoints that could be abused via CSP whitelist bypasses', 'Examine other Twitter features using similar card rendering mechanisms (share buttons, embed previews)', 'Test for HTML tag stripping bypasses using other character combinations: null bytes, Unicode normalization, double-encoding']

## MITRE ATT&CK
- T1190
- T1566.002
- T1059.007
- T1204.001

## Notes
This vulnerability exemplifies a 'wormable' XSS where the payload can self-replicate through automated actions (retweeting). The chaining of multiple weak controls (escaping + stripping + CSP) created a false sense of security. The HTML parser behavior regarding script tag termination is a critical semantic to understand. Writeup is incomplete regarding full CSP bypass details but demonstrates deep technical knowledge of attack vectors. The vulnerability required understanding of Twitter's architecture including cards, deeplinks, iframes, and JSONP callback mechanisms.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
