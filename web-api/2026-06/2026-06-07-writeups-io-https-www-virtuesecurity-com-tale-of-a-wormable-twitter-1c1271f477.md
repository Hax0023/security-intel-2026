# Tale of a Wormable Twitter XSS

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Stored XSS, HTML Tag Stripping Bypass, CSP Bypass, Input Validation Bypass
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's welcome message deeplink feature that could be weaponized as a self-propagating XSS worm. The vulnerability exploited improper HTML tag stripping logic combined with Twitter Card rendering to bypass input validation and CSP policies, allowing arbitrary JavaScript execution.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL containing a specially-crafted payload in the 'text' parameter of a Twitter messages compose deeplink
2. The payload uses nested angle brackets (<</<x>/script/test000>) to bypass HTML tag stripping filters by exploiting regex/parsing weaknesses
3. When rendered as a Twitter Card, the payload gets reflected into an inline JSON object within a <script type='text/twitter-cards-serialization'> tag
4. HTML parser encounters the unescaped closing </script> tag embedded in the payload, prematurely terminating the script block and injecting attacker-controlled HTML/JavaScript
5. The injected JavaScript creates an iframe pointing to the retweet intent and uses JSONP callbacks from syndication.twimg.com to bypass CSP
6. Victims who click the link retweet the malicious tweet, spreading the worm to their followers

## Root cause
Twitter implemented multiple security layers but each had implementation flaws: (1) HTML tag stripping via regex instead of proper parsing, (2) Inline JSON reflection without proper escaping, (3) CSP policy with whitelisted JSONP endpoints that could be abused, (4) Unsandboxed same-origin iframes with DOM access to parent, (5) Failure to properly escape closing script tags within string contexts

## Attacker mindset
The attacker demonstrated methodical vulnerability chaining: identifying the weakest link (HTML tag stripping) through security intuition, iteratively fuzzing bypasses, recognizing the worm potential of the vulnerability, and understanding browser parsing rules (script tag termination behavior). The attacker showed restraint by reporting after initial XSS but before finding full CSP bypass.

## Defensive takeaways
- Never use regex for HTML parsing; use proper HTML parsers
- Escape all user input contextually - JSON strings need different escaping than HTML attributes
- Apply defense-in-depth: even if one layer fails, others should catch it
- Sandbox all iframes regardless of origin, or implement stricter DOM access controls
- Whitelist JSONP endpoints carefully and validate callback parameter names strictly
- Test security controls with chained bypasses, not just individual payloads
- Be especially cautious with deeplinks and card rendering mechanisms that re-expose user input
- Implement proper script tag detection that accounts for parsing context (within strings, comments, etc.)

## Variant hunting
Search for other Twitter features using similar patterns: (1) Other deeplink parameters that get rendered in iframe contexts, (2) Other Twitter Card types that reflect user input in JSON, (3) Other endpoints whitelisting syndication.twimg.com or similar JSONP services, (4) Other places using HTML tag stripping instead of proper parsing, (5) DM/message features with similar welcome message mechanisms, (6) Quote tweet or retweet functionality with similar card rendering

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1059
- T1204
- T1185

## Notes
This vulnerability is particularly significant because: (1) it could achieve mass worm propagation via retweets, (2) it demonstrates how multiple 'defense-in-depth' layers can fail when each has implementation issues, (3) the HTML tag stripping regex is a common pattern in legacy code that often has bypass techniques, (4) JSONP endpoints are a common CSP bypass vector when whitelisted, (5) the researcher showed good judgment in escalation timing. The unfinished CSP section suggests Twitter also had additional bypasses available but the researcher responsibly reported early.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
