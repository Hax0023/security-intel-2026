# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript code without using parentheses or semicolons by leveraging the onerror handler combined with throw statements. The method works across multiple browsers by assigning functions to onerror and using throw expressions to invoke them with custom arguments, bypassing common WAF and input validation filters.

## Attack scenario (step by step)
1. Attacker identifies input validation filter blocking parentheses and semicolons
2. Attacker crafts XSS payload using onerror=alert;throw syntax or block statement variant
3. Attacker injects payload into vulnerable parameter: <script>{onerror=alert}throw 1337</script>
4. Browser parses script and assigns alert function to onerror handler
5. Throw statement triggers exception, invoking onerror handler with throw argument as parameter
6. Arbitrary code executes without needing parentheses or semicolons

## Root cause
Insufficient input validation filtering that only blocks parentheses and semicolons while missing the onerror/throw technique. Developers assumed these characters were necessary for function execution, failing to account for alternative JavaScript syntax.

## Attacker mindset
An attacker would actively search for incomplete filtering rules that block obvious function call syntax. Understanding JavaScript's flexible exception handling and expression evaluation provides alternative execution paths. The goal is to identify whitelisting gaps and abuse language features meant for error handling.

## Defensive takeaways
- Implement context-aware output encoding based on where content appears (HTML, JavaScript, URL)
- Use Content Security Policy (CSP) with strict script-src directives to prevent inline script execution
- Avoid blacklist-based filtering; prefer whitelist validation with strict parsing
- Block event handlers (onerror, onclick, etc.) in user-supplied content
- Employ a robust, well-maintained templating engine with automatic escaping
- Test filters against known bypass techniques and maintain updated filter rules
- Use static analysis tools to detect onerror/throw patterns in sanitization reviews

## Variant hunting
Look for similar event handler abuse (onload, oninput, onmouseover), alternative throw syntax variants, eval-based payloads, object literal bypass techniques, and filter evasion using encoding (\x hex escapes, unicode). Test against frameworks with custom sanitizers.

## MITRE ATT&CK
- T1190
- T1059
- T1566

## Notes
Original research by Gareth Heyes. Multiple variants exist: block statement form {onerror=alert}throw 1337 and expression form throw onerror=alert,'arg'. Firefox requires special Error object literal properties (lineNumber, columnNumber, fileName, message) to avoid 'uncaught exception' prefix issues. Chrome prefixes with 'Uncaught' but can be bypassed using eval with '=' prefix. Technique demonstrates importance of understanding language semantics beyond obvious syntax.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
