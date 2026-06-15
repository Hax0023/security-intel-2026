# Tale of a Wormable Twitter XSS - Stored XSS in Welcome Messages with CSP Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Twitter Bug Bounty
- **Bounty:** Not disclosed in writeup
- **Severity:** critical
- **Vuln types:** Stored Cross-Site Scripting (XSS), HTML Tag Stripping Bypass, Content Security Policy (CSP) Bypass, Script Injection via JSONP, DOM-based XSS
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's welcome messages feature that could be weaponized as a self-propagating worm. The vulnerability exploited flawed HTML tag stripping logic combined with a script tag parser inconsistency to inject malicious code into Twitter cards, which then leveraged JSONP endpoints to bypass the Content Security Policy and execute arbitrary JavaScript.

## Attack scenario (step by step)
1. Attacker crafts a specially-formatted URL with XSS payload in the 'text' parameter of Twitter's direct message deeplink, using nested angle brackets to bypass HTML tag stripping (e.g., <</<x>/script/>)
2. Victim clicks the malicious link, which renders as a Twitter card containing an iframe pointing to twitter.com/i/cards/tfw/v1/...
3. The iframe is same-origin and non-sandboxed, allowing full DOM access to the parent page; the payload gets reflected in a JSON object within a script tag
4. The HTML parser terminates the initial script tag when encountering the injected </script> sequence, even though it appears within a string literal
5. Injected iframe with retweet intent/action loads, followed by JSONP script tags that call whitelisted syndication.twimg.com endpoints with callback parameters pointing to malicious functions
6. Attacker's JavaScript executes in the victim's context; the worm automatically retweets and shares the malicious link to all followers, spreading exponentially across Twitter

## Root cause
Multiple weaknesses in combination: (1) HTML tag stripping using regex rather than proper HTML parsing, allowing bypass via nested tags like <</<x>/script/>; (2) JSON data reflected unsanitized within script tags, where </script> terminates parsing regardless of context; (3) Same-origin iframes without sandboxing allowing DOM manipulation; (4) JSONP endpoints whitelisted in CSP that accept arbitrary callback parameters; (5) Insufficient output encoding of user-supplied text in welcome messages

## Attacker mindset
The attacker recognized that HTML tag stripping is notoriously error-prone and systematically probed the implementation by introducing edge cases (nested tags with forward slashes). Upon finding that basic filtering could be bypassed, they chained multiple vulnerabilities together—leveraging JSON reflection, script tag parsing quirks, and CSP whitelisted JSONP endpoints—to achieve code execution. The worm design shows sophisticated understanding of social engineering (deeplinks appearing trustworthy) and lateral movement (auto-retweet spreading).

## Defensive takeaways
- Never use regex or string manipulation for HTML parsing; use a proper HTML parser library and allowlist approach instead of tag stripping
- Encode all user input appropriately for its context (HTML, JavaScript, URL, JSON) using context-aware encoding functions
- Apply output encoding even for data already within script tags; treat JSON values as potentially injectable
- Sandbox all iframes, especially third-party content; use the sandbox attribute with minimal permissions
- Be extremely restrictive with CSP script-src; avoid whitelisting overly permissive domains or endpoints that accept user-controlled callback parameters
- Test input validation/filtering with fuzzing and edge cases (nested tags, unusual characters, parser quirks)
- Implement Content Security Policy with script nonce rotation and script-src restriction to prevent JSONP callback injection
- Consider using a Web Application Firewall (WAF) with XSS detection rules for reflected/stored payloads

## Variant hunting
['Test other tag stripping implementations for similar nested angle bracket bypasses (<</<tagname>/target/>)', 'Hunt for other endpoints that reflect user input within script tags (not just welcome messages)', 'Identify additional whitelisted JSONP or callback-based endpoints in CSP that could be leveraged for code execution', 'Check for similar vulnerabilities in Twitter Cards rendering for other card types', 'Test other deeplinks that might render unsanitized user input in iframes', 'Look for other features that allow custom text/content in embeddings (quoted tweets, profile bios, etc.)', 'Examine other social platforms with similar welcome message, DM, or card features for the same XSS pattern']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (Twitter XSS vulnerability)
- T1598 - Phishing - Link (malicious deeplink)
- T1204 - User Execution - Malicious Link (victim clicks malicious URL)
- T1059 - Command and Scripting Interpreter - JavaScript (arbitrary code execution)
- T1570 - Lateral Tool Transfer (worm spreads via retweets)
- T1005 - Data from Local System (DOM access to parent page)

## Notes
This writeup exemplifies a sophisticated multi-stage attack combining parser logic flaws, context confusion, and policy bypass. The 'wormable' aspect makes it especially dangerous—once in the wild, it self-propagates without further user interaction beyond the initial click. The researcher's approach of systematically fuzzing the tag stripping logic demonstrates the value of understanding parsing edge cases. Twitter's response time and whether this was publicly disclosed with timeline is not mentioned in the excerpt.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
