# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** PortSwigger Research / General Web Security
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Code Execution
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript and call functions without using parentheses or semicolons by leveraging the onerror handler combined with throw statements and object literals. This bypasses input filters that block these common syntax elements, enabling XSS attacks on applications with insufficient filtering.

## Attack scenario (step by step)
1. Attacker identifies a web application filtering parentheses and semicolons to prevent XSS
2. Attacker crafts payload using onerror assignment within throw statement: <script>{onerror=alert}throw 1337</script>
3. Alternative approach: embed assignment in throw expression: <script>throw onerror=alert,'payload'</script>
4. For eval-based attacks, attacker uses object literal with Error properties to bypass Firefox prefix behavior: <script>{onerror=eval}throw{lineNumber:1,columnNumber:1,fileName:1,message:'alert\x281\x29'}</script>
5. Payload executes arbitrary JavaScript when injected into vulnerable application
6. Attacker exfiltrates data, steals session tokens, or performs malicious actions in user context

## Root cause
Insufficient input validation that blocks only parentheses and semicolons while not preventing throw statements, onerror handlers, and object literals. Developers assume these syntax restrictions are sufficient, failing to account for alternative JavaScript execution patterns.

## Attacker mindset
Methodical bypass researcher analyzing restrictions to find creative workarounds. Demonstrates deep JavaScript knowledge by understanding exception handling mechanisms and prototype behavior across browsers. Persistence in testing variations (block statements, throw expressions, Error object properties) shows commitment to finding minimal viable payloads.

## Defensive takeaways
- Never rely on blocking individual characters (parentheses, semicolons) as primary XSS defense
- Implement robust Content Security Policy (CSP) with script-src restrictions
- Use allowlist-based input validation rather than blacklist filtering
- Apply proper output encoding/escaping for all user input contexts (HTML, JavaScript, URL, CSS)
- Perform server-side validation and sanitization; never trust client-side filtering
- Test filters against polyglot payloads and alternative execution methods
- Consider disabling inline scripts entirely through CSP

## Variant hunting
Search for other bypass techniques: onerror with different assignment operators, alternate error handlers (window.onerror alternatives), constructor-based function calls without parentheses, template literal abuse, getter/setter property exploitation, event handler chaining, Symbol manipulation, Proxy objects for function invocation interception.

## MITRE ATT&CK
- T1190
- T1059.007
- T1566.002

## Notes
Seminal research demonstrating the limitations of character-based filtering. The technique evolved across research iterations: simple onerror+throw → block statement variant → throw expression assignment → Firefox compatibility via Error object properties. Browser differences (Chrome vs Firefox exception prefixing) required adaptation, highlighting importance of cross-browser testing. Published May 2019 with March 2020 update showing continued refinement.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
