# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Injection
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript and call functions without using parentheses or semi-colons by leveraging the onerror handler and throw statement. The method works across multiple browsers by adapting exception handling behavior, using block statements, throw expressions, and eval evaluation to bypass input filters.

## Attack scenario (step by step)
1. Attacker identifies that target application filters parentheses and semi-colons from user input to prevent XSS
2. Attacker injects <script>{onerror=alert}throw 1337</script> using block statement syntax to bypass semi-colon filter
3. Attacker uses throw expression syntax: <script>throw onerror=alert,'payload'</script> to assign and invoke handler without semi-colon
4. Attacker chains eval handler with throw to execute arbitrary code: <script>{onerror=eval}throw'=alert\x281337\x29'</script>
5. On Firefox, attacker uses Error object properties to bypass 'uncaught exception' prefix: <script>{onerror=eval}throw{lineNumber:1,columnNumber:1,fileName:1,message:'alert\x281\x29'}</script>
6. Payload executes in victim's browser context, bypassing WAF/filter rules that only block parentheses and semi-colons

## Root cause
Input validation filters that only blacklist parentheses and semi-colons fail to account for alternative JavaScript syntax for function invocation. The onerror event handler combined with throw statements provides a legitimate language feature that bypasses shallow filtering.

## Attacker mindset
Exploit overly simplistic input filters by understanding JavaScript language features and exception handling mechanisms. Recognize that filters targeting specific characters miss alternative syntax patterns, and leverage browser-specific behavior differences (Chrome vs Firefox) to craft cross-browser payloads.

## Defensive takeaways
- Do not rely on character-based blacklists for JavaScript prevention; use whitelist-based Content Security Policy (CSP) headers
- Implement output encoding/escaping based on context (HTML, JavaScript, URL, CSS) rather than input filtering
- Deploy strict CSP policies (script-src: none or 'nonce-value') to prevent inline script execution
- Use context-aware templating engines that automatically escape user input
- Test filters against known XSS bypass techniques including function invocation variants
- Consider disabling onerror handlers when not needed or restrict event handler attributes with CSP
- Validate server-side and assume all client-side filters can be bypassed

## Variant hunting
['Test other event handlers (onerror, onload, onmouseover) with throw statements', 'Explore alternative exception handlers and their prefixes across browsers', 'Investigate template literals and other ES6 syntax for function invocation without parentheses', 'Test tagged template functions as alternative code execution mechanism', 'Research Proxy objects and other metaprogramming features for bypass', 'Examine browser-specific quirks in error message formatting', 'Test combinations with other stripped characters (spaces, quotes, etc.)']

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
Research published by PortSwigger researcher Gareth Heyes demonstrating sophisticated XSS filter evasion. The technique highlights the danger of shallow input validation and the importance of understanding JavaScript's alternative syntax patterns. Browser compatibility differences (Chrome vs Firefox) are key to payload adaptability. Originally discovered years before publication; demonstrates long-term applicability of the technique.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
