# Wormable Stored XSS on Twitter via Welcome Message Deeplink with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Twitter/X Bug Bounty Program
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Stored Cross-Site Scripting (XSS), Inadequate HTML Tag Stripping, Content Security Policy (CSP) Bypass, JSONP Injection, DOM-based XSS
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A critical stored XSS vulnerability was discovered in Twitter's Welcome Message deeplink feature that could be weaponized as a self-propagating worm. The vulnerability exploited flawed HTML tag stripping logic combined with a JSONP callback mechanism to bypass CSP restrictions and execute arbitrary JavaScript, potentially spreading across the platform through automated retweets.

## Attack scenario (step by step)
1. Attacker crafts a malicious URL leveraging Twitter's Welcome Message deeplink with XSS payload in the 'text' parameter using nested angle bracket obfuscation (<</<x>/script>)
2. Victim clicks the link, which renders as a Twitter card (iframe) pointing to /i/cards/tfw/v1/ endpoint
3. The flawed HTML tag stripping logic fails to properly remove the malicious closing </script> tag, leaving it in the JSON response
4. JavaScript parser encounters the unescaped </script> in the default_composer_text JSON value, terminating the <script type="text/twitter-cards-serialization"> block
5. Attacker's injected iframe and script tags execute in the same-origin context with DOM access to parent page
6. Malicious JSONP callbacks to syndication.twimg.com endpoints are triggered to automatically retweet the original tweet, spreading the worm to all followers of infected accounts

## Root cause
Multiple compounding security failures: (1) Regex-based HTML tag stripping logic that fails to account for nested/obfuscated tag syntax; (2) Unsafe JSON serialization of user input within script tags without proper escaping of closing script delimiters; (3) Use of unsandboxed iframes for rendering user-controlled content; (4) JSONP endpoints accepting arbitrary callback parameters that can call sensitive functions like form submission; (5) CSP policy allowing whitelisted domains (twimg.com) that host exploitable JSONP endpoints

## Attacker mindset
The attacker recognized that simple input validation mechanisms (quote escaping, tag stripping) often contain implementation flaws when parsing HTML. By testing variations of obfuscated syntax (<</<x>/script>), they discovered the regex-based stripper could be bypassed through nesting. The worm potential required chaining multiple vulnerabilities: leveraging the JSON context escape combined with JSONP callback abuse to trigger automatic propagation. This demonstrates sophisticated understanding of HTML parsing edge cases and JavaScript execution contexts.

## Defensive takeaways
- Never use regex or character-level filtering for HTML sanitization; use a proper HTML parser library (e.g., jsoup, DOMPurify) that understands parsing rules
- Properly escape all user input when serializing to JSON, especially escaping forward slashes and closing delimiters that could break out of script context
- Sandbox all iframes rendering user-controlled content, especially from untrusted sources; use sandbox attributes to restrict DOM access and script execution
- Implement strict CSP policies that avoid whitelisting broad domain patterns; specifically review JSONP endpoints for callback parameter injection risks
- Apply defense-in-depth: even with CSP, assume it can be bypassed and implement server-side protections to validate and sanitize all user input
- Conduct security testing with obfuscation techniques and nested syntax to identify parsing edge cases in validation logic
- Disable JSONP or implement strict callback validation; consider using CORS with JSON instead
- Use Content-Security-Policy headers to restrict callback parameter exploitation (e.g., script-src without 'unsafe-inline')

## Variant hunting
['Test for similar HTML tag stripping flaws in other user-facing features (tweets, DMs, profile bio, etc.)', 'Hunt for other JSONP endpoints on twimg.com or related domains that accept dangerous callback parameters (form submission, navigation, DOM manipulation functions)', 'Search for other inline <script type="...-serialization"> blocks that deserialize user input without proper escaping', 'Examine other deeplink parameters that get reflected into JSON/JavaScript contexts (recipient_id, welcome_message_id, etc.)', 'Look for similar nested angle bracket obfuscation bypasses in other tag stripping implementations across the platform', 'Test whether other iframe rendering flows (embedded tweets, embeds, preview cards) have sandbox bypasses or same-origin access', 'Investigate whether the JSONP callback bypass extends to other syndication.twimg.com endpoints or related subdomains']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application (XSS vulnerability in public Twitter API/deeplinks)
- T1059: Command and Scripting Interpreter (JavaScript execution)
- T1566: Phishing (malicious link distribution via tweet)
- T1204: User Execution (user must click the link)
- T1539: Steal Web Session Cookie (potential worm propagation across accounts)
- T1570: Lateral Tool Transfer (worm spreading from account to account)
- T1021: Remote Services (automated retweet mechanism spreads payload)

## Notes
This vulnerability represents a sophisticated attack chain combining parsing flaws, serialization issues, and JSONP callback exploitation. The worm aspect is particularly dangerous as it could spread automatically without additional user interaction once an account is compromised. The writeup demonstrates excellent security research methodology: identifying the root cause (tag stripping), iteratively fuzzing bypass techniques, and escalating before completing full exploit development. The CSP bypass section was truncated in the provided content but likely detailed how the whitelisted twimg.com domain enabled JSONP exploitation. Twitter patched this in mid-2018; the researcher responsibly disclosed before publishing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
