# Wormable Twitter XSS via Welcome Message Deeplink and HTML Tag Stripping Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Twitter (Bug Bounty)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Stored XSS, Improper Input Validation, HTML Tag Stripping Bypass, CSP Bypass, XSS Worm
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's welcome message deeplink functionality where user input in the 'text' parameter was reflected in an inline JSON object without proper sanitization. By chaining multiple bypasses against input validation (HTML tag stripping) and CSP policies, an attacker could craft a wormable XSS that would automatically spread across Twitter accounts through retweet actions.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL containing XSS payload in the welcome_message_id deeplink parameter with text parameter containing crafted payload
2. Payload exploits flawed HTML tag stripping logic using nested tag fragments (e.g., <</<x>/script>) that bypass regex-based sanitization
3. Twitter card renders the deeplink as an unsandboxed iframe pointing to /i/cards/tfw/v1/ endpoint
4. User input is reflected in inline JSON within a script tag, with payload breaking out via closing script tag (</script>)
5. Payload executes to create iframe that triggers retweet intent and loads external scripts via JSONP callbacks
6. Retweet form automatically submits, propagating malicious message to all of victim's followers, creating self-propagating worm

## Root cause
The vulnerability stems from three chained weaknesses: (1) Flawed HTML tag stripping implementation using regex instead of proper HTML parsing, (2) Insufficient output encoding when reflecting user input into inline JSON within script tags, (3) Use of unsandboxed iframes and lack of CSP enforcement on card rendering endpoints, (4) Trust in JSONP callback mechanisms that could be abused for code execution

## Attacker mindset
The attacker demonstrated sophisticated understanding of HTML parsing quirks, specifically how HTML parsers terminate script tags regardless of context. They recognized that regex-based tag stripping is inherently flawed and systematically tested nested tag variations to bypass it. The attacker understood the architectural trust model (unsandboxed iframes, JSONP callbacks) and how to chain multiple weaknesses into a self-propagating worm that could scale across millions of users with minimal user interaction.

## Defensive takeaways
- Never use regex for HTML sanitization; use proper HTML parsing libraries with context-aware output encoding
- Apply context-appropriate encoding: HTML entity encoding for HTML context, JavaScript string escaping for JS context, URL encoding for URL context
- Use sandboxed iframes with restrictive sandbox attributes (allow-same-origin should be avoided when possible)
- Implement strict CSP policies and enforce them on all endpoints, including card rendering and JSONP callback handlers
- Avoid reflecting user input into inline script tags or JSON objects within script tags; use separate data attributes or API calls
- Disable or restrict JSONP callback functionality or validate callback parameter against whitelist
- Perform security testing specifically targeting tag stripping with nested/fragmented tag payloads
- Regularly audit deeplink functionality and parameter handling for injection vulnerabilities

## Variant hunting
['Test other deeplink parameters for similar reflection vulnerabilities', 'Search for other endpoints that use HTML tag stripping sanitization', 'Investigate other JSONP endpoints that might accept attacker-controlled callback parameters', 'Check if other Twitter card types (beyond message_me) have similar unsafe reflection patterns', 'Test for DOM-based XSS in card rendering JavaScript that processes the JSON data', 'Look for other nested tag fragmentation patterns that bypass tag stripping regex', 'Audit intent endpoints (/intent/retweet, /intent/like, etc.) for parameter injection', 'Test CSP bypass via other whitelisted domains in the script-src directive']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
The writeup is incomplete as it cuts off during the CSP bypass explanation. The researcher responsibly reported after discovering the HTML tag stripping bypass but before fully weaponizing the CSP bypass. This vulnerability exemplifies how security controls are ineffective when layered improperly—sanitization via broken regex, CSP without proper enforcement, and unsafe iframe architecture created a perfect storm. The wormability aspect is particularly dangerous as it could have propagated exponentially without user action beyond initial click, similar to historical internet worms like Samy XSS on MySpace.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
