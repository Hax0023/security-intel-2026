# Tale of a Wormable Twitter XSS - Stored XSS via Welcome Message Deeplink with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Twitter
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** stored_xss, html_injection, csp_bypass, improper_input_validation, script_tag_stripping_bypass
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's Welcome Message feature that could be exploited via a specially crafted deeplink rendered as a Twitter card. The vulnerability allowed injection of malicious scripts by bypassing HTML tag stripping, quote escaping, and CSP policies, potentially enabling worm-like self-propagating attacks across Twitter accounts.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL containing XSS payload in the 'text' parameter of a Welcome Message deeplink (twitter.com/messages/compose?...)
2. Victim clicks the link, which renders as a Twitter card displaying an iframe pointing to twitter.com/i/cards/tfw/v1/...
3. The iframe loads unsandboxed (same-origin), giving DOM access to parent webpage
4. The malicious payload in the 'text' parameter gets reflected into an inline JSON object within a script tag as the 'default_composer_text' value
5. Attacker's crafted payload (using double-encoded tags like <</<x>/script>) bypasses HTML tag stripping and closes the script tag, executing arbitrary JavaScript
6. Injected script triggers automated retweet and message composition, spreading the worm to attacker's followers

## Root cause
Multiple layered validation bypasses: (1) HTML tag stripping implementation used naive string replacement instead of proper HTML parsing, allowing double-encoded tags like <</<x>/script> to bypass filters; (2) Reflection of user input into inline JSON within script tags without proper escaping; (3) Unsandboxed iframe with DOM access to parent; (4) CSP policy with whitelisted external domains that could be leveraged via callback parameters; (5) HTML parser's behavior of terminating script tags at first encountered </script> even within string literals

## Attacker mindset
Reconnaissance-focused approach: systematically tested basic payloads, observed tag stripping behavior, recognized it as likely vulnerable to parsing tricks, iterated with nested tag encodings until filter bypass was achieved. Demonstrated restraint by reporting to vendor before fully weaponizing with CSP bypass, suggesting responsible disclosure mindset.

## Defensive takeaways
- Never use regex or string replacement for HTML sanitization; use established libraries with proper HTML parsing (e.g., OWASP sanitizers)
- Avoid reflecting user input into script tags or JSON objects without proper escaping; if necessary, use HTML entity encoding or JSON-specific escaping
- Sandbox all iframes and disable DOM access to parent frames unless absolutely required
- Implement strict CSP with 'strict-dynamic' and avoid whitelisting broad domains; use nonces/hashes for inline scripts instead
- Test input validation bypasses with double-encoding, nested tags, and HTML parser edge cases
- Apply defense-in-depth: combine multiple validation layers (escaping + sanitization + CSP + sandboxing)
- Regularly audit third-party deeplinks and card rendering systems for reflection vulnerabilities

## Variant hunting
['Look for other user-input fields rendered into script tags or JSON within script tags on Twitter or similar platforms', 'Test other deeplink parameters and card types for similar reflection vulnerabilities', "Examine other endpoints accepting 'text' or 'message' parameters that might be rendered in inline scripts", 'Search for similar tag-stripping implementations across the codebase using regex-based HTML parsing', 'Test for JSONP endpoint exploitation where user input flows into callback parameters', 'Investigate other iframe-based features without proper sandboxing', 'Look for nested URL encoding/decoding that might further bypass filters']

## MITRE ATT&CK
- T1190
- T1059
- T1564.001
- T1566.002

## Notes
The writeup appears incomplete - CSP bypass section is cut off. The vulnerability demonstrates the difficulty of implementing secure string processing for HTML/JavaScript contexts. The use of double-encoded tags (<</<x>/script>) to bypass naive tag stripping is a classic technique worth remembering. The self-propagating nature (worm potential via automated retweet/messaging) elevates this beyond typical XSS. Timeline: discovered mid-2018, reported responsibly, fixed by time of writeup (May 2019). The vulnerability chain exemplifies how multiple 'defense' mechanisms can fail when each is implemented incorrectly.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
