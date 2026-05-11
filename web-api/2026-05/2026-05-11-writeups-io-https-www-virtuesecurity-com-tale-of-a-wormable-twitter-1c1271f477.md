# Tale of a Wormable Twitter XSS - CSP Bypass via Malformed HTML Tag Stripping

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Twitter (X)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Stored XSS, XSS Worm, CSP Bypass, Improper Input Validation, HTML Parser Confusion
- **Category:** web-api
- **Writeup:** https://www.virtuesecurity.com/tale-of-a-wormable-twitter-xss/

## Summary
A stored XSS vulnerability was discovered in Twitter's direct message welcome card feature that could be weaponized as a self-propagating XSS worm. The vulnerability exploited flawed HTML tag stripping logic that could be bypassed using malformed tags like <</<x>/script/>, combined with JSONP-based CSP bypass techniques to execute arbitrary JavaScript across user accounts.

## Attack scenario (step by step)
1. Attacker crafts a malicious direct message deeplink with XSS payload in the 'text' parameter using obfuscated closing script tags like <</<x>/script/>
2. Victim receives and clicks the link, which renders as a Twitter card iframe containing the reflected payload in the default_composer_text JSON field
3. HTML parser encounters the malformed closing script tag which bypasses the tag-stripping filter, resulting in executable HTML/JavaScript
4. Attacker leverages Twitter's own JSONP endpoints (syndication.twimg.com/timeline/profile) to bypass CSP by injecting callback parameters that execute functions like retweet_btn_form.submit
5. The XSS automatically retweets the original malicious link to all of the victim's followers, creating a worm effect
6. Infection spreads exponentially across the social network as each new victim's account auto-propagates the payload

## Root cause
Multiple security failures: (1) Flawed HTML tag stripping using regex instead of proper HTML parsing, allowing bypass via nested tags like <</<x>/script/>; (2) Reflection of unescaped user input directly into inline JSON serialization where closing script tags terminate parsing; (3) CSP policy that whitelists syndication.twimg.com JSONP endpoints allowing callback parameter injection; (4) Lack of sandboxing on same-origin iframes containing user-controlled data

## Attacker mindset
Methodical fuzzing approach - started with basic payload, iteratively tested tag obfuscation techniques until finding bypass. Recognized that HTML parsing is inherently error-prone and regex-based approaches are vulnerable. Understood JSONP as alternative code execution vector when direct script injection blocked. Grasped the self-propagating potential of auto-retweet functionality for worm amplification.

## Defensive takeaways
- Use proper HTML parsing libraries (not regex) for tag stripping/sanitization - libraries like DOMPurify or OWASP Java HTML Sanitizer
- Apply defense-in-depth: sanitize input, escape output context-appropriately, enforce CSP, and sandbox untrusted content
- Be extremely cautious with JSONP endpoints - avoid exposing them in CSP whitelist or strictly validate callback parameters
- Escape or filter closing tags '</script>' even within JSON strings, as HTML parsing terminates at first matching closing tag
- Implement sandbox attribute on iframes containing user-generated content to prevent DOM access and script execution
- Monitor for self-propagating patterns - auto-retweet, auto-share, or auto-forwarding features need special security scrutiny
- Regularly audit CSP policies for unintended JSONP whitelisting that could enable callback injection attacks

## Variant hunting
['Search for other same-origin iframes reflecting user input without proper sanitization', 'Audit all JSONP endpoints exposed in CSP policies for callback parameter injection risks', 'Test HTML parsing in other features (comments, bios, card descriptions) for similar tag-stripping bypasses', 'Examine other auto-action features (follows, likes, retweets) for worm propagation potential', 'Look for nested tag patterns (<<<, >>>, malformed nesting) that bypass simplistic tag removal', 'Identify other Twitter-whitelisted domains in CSP that might support JSONP or callback parameters']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing: Spearphishing Link (initial delivery via DM deeplink)
- T1203 - Exploitation for Client Execution
- T1539 - Steal Web Session Cookie (via XSS access to document.cookie)
- T1059.007 - Command and Scripting Interpreter: JavaScript/Node.js

## Notes
This vulnerability demonstrates the critical importance of proper input validation and the dangers of using regex for HTML parsing. The writeup was published May 2019 and references a mid-2018 discovery, indicating responsible disclosure. The 'wormable' aspect is particularly severe as it enables exponential infection spread. The attacker showed excellent bug hunting methodology by starting with known bypass patterns (malformed tags) and iteratively refining. The CSP bypass using JSONP callback injection is a classic but effective technique that highlights why JSONP should be carefully restricted in security policies.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
