# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** PortSwigger Research / Bug Bounty Community
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, WAF Evasion
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript code without using parentheses or semicolons by leveraging the onerror handler and throw statement. The method works across different browsers by adapting the approach to bypass parser differences, particularly in Firefox which prefixes exception messages differently than Chrome.

## Attack scenario (step by step)
1. Attacker identifies a web application that filters or blocks parentheses and semicolons in user input
2. Attacker uses onerror handler assignment combined with throw statement to execute JavaScript without these characters
3. In Chrome, attacker uses format: <script>{onerror=alert}throw 1337</script> or <script>throw onerror=alert,'payload'</script>
4. For Firefox compatibility, attacker creates object literal with Error prototype properties to bypass the 'uncaught exception' prefix
5. Attacker uses eval as exception handler with specially crafted payload: {onerror=eval}throw{message:'alert\x281337\x29',...}
6. JavaScript payload executes in victim's browser context, bypassing input validation filters

## Root cause
Input validation filters that blacklist parentheses and semicolons as XSS prevention mechanisms fail to account for alternative JavaScript syntax patterns. The onerror handler and throw statement provide legitimate JavaScript constructs that achieve function execution without these characters. Browser-specific exception message formatting also introduces additional bypass vectors.

## Attacker mindset
Determined researcher exploring the boundaries of JavaScript syntax to find creative execution methods. Focused on understanding browser-specific behaviors and using legitimate language features in unintended ways. Persistence in trying alternative approaches when initial techniques encounter obstacles (e.g., Firefox's different exception formatting).

## Defensive takeaways
- Blacklist-based input validation is insufficient; use whitelist-based approaches and Content Security Policy (CSP)
- Implement CSP headers with script-src restrictions to prevent inline script execution regardless of syntax
- Do not rely on character-level filtering as sole XSS defense; understand JavaScript syntax flexibility
- Use context-aware output encoding rather than input filtering for XSS prevention
- Apply defense-in-depth with multiple layers: validation, encoding, CSP, and security headers
- Regularly test WAF/filter rules against syntax variations and obfuscation techniques

## Variant hunting
Research other JavaScript constructs that don't require parentheses (template literals, arrow functions, tagged templates), explore event handlers beyond onerror, test alternative exception mechanisms, investigate other browser-specific error message formats in Edge/Safari, examine whether other statement types can replace throw for expression evaluation

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1059

## Notes
This research demonstrates that character-level input filtering cannot be relied upon for security. The technique evolved from earlier onerror/throw work and was adapted to handle browser differences. The Firefox workaround using Error object literal properties with specific fields (lineNumber, columnNumber, fileName, message) shows sophisticated understanding of exception handling. Published May 2019, updated March 2020 to reflect additional findings.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
