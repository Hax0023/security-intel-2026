# Wormable Twitter XSS via Welcome Message Deeplink and CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Twitter
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Stored XSS, DOM-based XSS, HTML Tag Stripping Bypass, CSP Bypass, XSS Worm
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's Welcome Message deeplink feature, where user input reflected in an inline JSON object within a non-sandboxed iframe could execute arbitrary JavaScript. The vulnerability allowed attackers to create a self-propagating XSS worm by chaining multiple bypasses including HTML tag stripping evasion and CSP policy circumvention using whitelisted Twitter domains.

## Attack scenario (step by step)
1. Attacker crafts a malicious Welcome Message deeplink containing XSS payload with obfuscated closing script tags using HTML tag stripping evasion techniques
2. User clicks the deeplink or views the Twitter card, which renders an iframe pointing to Twitter's card handler at twitter.com/i/cards/tfw/v1/[ID]
3. The unsanitized text parameter is reflected into inline JSON within a <script type="text/twitter-cards-serialization"> block in the non-sandboxed iframe
4. HTML parser processes the payload and terminates the outer script tag due to the closing </script> delimiter, allowing injected iframe and script tags to execute
5. Injected iframe auto-submits a retweet form via JSONP callback to whitelisted twimg.com domain, bypassing CSP with legitimate script-src directive
6. The worm propagates as infected users retweet the malicious tweet, spreading XSS to their followers automatically

## Root cause
Multiple compounding weaknesses: (1) User input from 'text' parameter reflected unsanitized into inline JSON object within script tag, (2) Improper HTML tag stripping using regex instead of proper HTML parsing, (3) Failure to sanitize closing script tag delimiters specifically, (4) Non-sandboxed iframe with DOM access to parent, (5) CSP whitelist included attacker-controllable callback parameter on twimg.com JSONP endpoint

## Attacker mindset
The researcher demonstrated methodical vulnerability chaining - starting with observation of error-prone tag stripping, systematically testing payload variations with nested angle brackets and x-elements to bypass the filter, recognizing the HTML parser's definitive behavior with script tag closure, then leveraging whitelisted JSONP endpoints to circumvent CSP. The worm concept shows thinking about self-propagation and epidemic spread through social network topology.

## Defensive takeaways
- Never use regex-based HTML tag stripping; use proper HTML parsing libraries that understand tag boundaries and context
- When reflecting user input into JSON within script tags, use JSON.stringify() and ensure proper escaping of all delimiters including </script>
- Sandbox all iframes with appropriate restrictions; avoid same-origin iframes processing user input unless absolutely necessary
- CSP whitelists should not include endpoints accepting user-controllable callback parameters (JSONP); use SRI or nonces for trusted third-party scripts
- Implement defense-in-depth: combine input validation (character escaping), output encoding, sandboxing, and strict CSP policies
- Test tag stripping specifically with malformed/nested tag structures like <</x>/script>, not just simple payloads
- Consider blocking deeplinks that auto-execute actions or auto-generate content cards from untrusted parameters

## Variant hunting
Look for similar deeplink/card rendering features in other URL schemes (intent links, share dialogs). Search for other JSONP endpoints on *.twimg.com and partner domains. Test embedded tweet rendering, thread cards, and quote tweet functionality for same reflection/stripping patterns. Check for similar tag-stripping regex patterns in other social platforms (Instagram, Facebook, TikTok). Hunt for other non-sandboxed iframes processing user input from URL parameters.

## MITRE ATT&CK
- T1190
- T1059
- T1566
- T1204

## Notes
The writeup is incomplete (CSP bypass section cuts off), but the core exploit chain is well-documented. The researcher responsibly disclosed to Twitter without waiting for complete CSP bypass. The <</<x>/script> bypass technique is elegant - it exploits HTML parsing order where opening < starts tag parsing, then nested tags confuse the stripping regex while parser recovers correctly. The JSONP callback auto-submission technique is particularly clever for worm propagation. This represents a sophisticated multi-stage exploit requiring understanding of HTML parsing, CSP mechanics, JSONP behavior, and social engineering via Twitter card rendering.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
