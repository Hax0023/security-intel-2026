# Tale of a Wormable Twitter XSS - Stored XSS via Welcome Message with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Twitter
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Stored Cross-Site Scripting (XSS), HTML Tag Stripping Bypass, Content Security Policy (CSP) Bypass, Input Validation Bypass, JSONP Injection
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A critical stored XSS vulnerability was discovered in Twitter's Welcome Message deeplinks that could be weaponized as a wormable XSS attack. The vulnerability exploited flawed HTML tag stripping logic combined with JSONP endpoints to bypass both input validation and CSP policies, allowing arbitrary script execution and automatic worm propagation across the platform.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL using Twitter's Welcome Message deeplink with specially crafted payload in the text parameter: https://twitter.com/messages/compose?recipient_id=XXX&text=PAYLOAD
2. When the link is shared or tweeted, Twitter renders it as a Twitter card containing an unsandboxed iframe pointing to https://twitter.com/i/cards/tfw/v1/[card_id]
3. The payload is reflected in the iframe's JSON serialization within the default_composer_text field, bypassing HTML tag stripping via nested tag technique (e.g., <</<x>/script/> becomes </script>)
4. The attacker injects closing script tags and iframe elements that load JSONP endpoints from whitelisted domains (syndication.twimg.com) with custom callbacks
5. JSONP callback parameter chains execution: callback=__twttr/alert or callback=__twttr/frames[0].retweet_btn_form.submit automatically retweets the malicious message
6. Any user viewing the malicious card becomes infected, automatically retweeting it to their followers, creating exponential worm propagation across the platform

## Root cause
Multiple compounding vulnerabilities: (1) Improper HTML tag stripping using regex-based parsing instead of proper HTML parsing, allowing nested tag bypass; (2) Unsandboxed iframe with DOM access to parent context; (3) User input (text parameter) reflected unsanitized in JSON object within script tags; (4) CSP policy that whitelists JSONP endpoints without restricting callback parameters; (5) Lack of output encoding when placing user input inside JSON context

## Attacker mindset
The attacker demonstrated sophisticated understanding of browser parsing rules (script tag termination behavior), HTML sanitization flaws, and JSONP abuse. Rather than exploiting immediately, they responsibly reported after confirming the vulnerability, showing mature security research ethics. The focus on creating a 'wormable' XSS reveals thinking about impact amplification and self-propagating attacks.

## Defensive takeaways
- Never use regex-based HTML tag stripping; use a proper HTML parser library with whitelist-based sanitization
- Always sandbox iframes unless DOM access to parent is absolutely necessary; use 'sandbox' attribute
- Properly encode all user input based on context (HTML encoding, JSON encoding, URL encoding, JavaScript encoding)
- Implement strict CSP policies that don't whitelist endpoints accepting arbitrary callback parameters; restrict JSONP callbacks to specific allowlisted values
- Escape script tag delimiters in JSON contexts or move dynamic content outside script tags entirely
- Avoid reflecting user input in JSON objects within script tags; use data attributes or separate API calls instead
- Implement multiple layers of validation: input validation, output encoding, and CSP enforcement
- Test security controls with polyglot payloads and context-aware bypasses, not just basic XSS vectors

## Variant hunting
Look for: (1) Other deeplinks or card endpoints with similar reflection patterns; (2) Alternative nested tag combinations that bypass HTML strippers (e.g., <<<, <</x>, malformed tags); (3) Other whitelisted JSONP endpoints accepting callback parameters; (4) Places where user input reaches script tag contexts in JSON serialization; (5) Similar iframe+JSONP chains in other parts of Twitter or competitor platforms; (6) CSP policy bypasses using other whitelisted domains or callback manipulation; (7) DOM-based XSS variants leveraging the unsandboxed iframe access

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Link injection via Twitter card
- T1566 - Phishing - Delivery via social media
- T1203 - Exploitation for Client Execution
- T1059 - Command and Scripting Interpreter - JavaScript execution

## Notes
This is an exemplary bug bounty report demonstrating: (1) responsible disclosure (reported before full exploit chain completed); (2) sophisticated chaining of multiple flaws into critical impact; (3) deep understanding of browser behavior and sanitization logic; (4) creative payload engineering (nested tag bypass technique); (5) business impact assessment (wormability = exponential damage). The writeup itself is incomplete (CSP bypass section cuts off) but the disclosed information is sufficient to understand the vulnerability class. Key insight: input validation through blacklist/stripping is inherently weaker than whitelist-based sanitization with proper encoding.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
