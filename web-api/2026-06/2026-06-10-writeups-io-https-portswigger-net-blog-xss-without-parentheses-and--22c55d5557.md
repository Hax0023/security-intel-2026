# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Code Execution
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
Researcher discovered techniques to execute arbitrary JavaScript code without using parentheses or semi-colons by leveraging the onerror handler and throw statements. The technique works across multiple browsers including Chrome and Firefox by manipulating exception handling behavior and object literals to bypass input filters.

## Attack scenario (step by step)
1. Attacker identifies a web application that filters or blocks parentheses and semi-colons in user input
2. Attacker crafts a payload using the onerror/throw technique: <script>{onerror=alert}throw 1337</script>
3. The throw statement triggers an exception which is caught by the onerror handler without requiring parentheses
4. For Firefox compatibility, attacker uses object literal with Error prototype properties to avoid 'uncaught exception' prefix
5. Attacker combines eval with onerror to evaluate arbitrary strings: <script>{onerror=eval}throw{message:'alert(1)'}</script>
6. Arbitrary JavaScript executes in victim's browser context, bypassing input validation

## Root cause
Security filters that block only parentheses and semi-colons fail to account for alternative JavaScript execution paths through exception handling mechanisms. The onerror handler automatically receives exception values, allowing function calls without parentheses, and throw statements can be chained without semi-colons using block statements or expression syntax.

## Attacker mindset
Filter evasion through deep JavaScript knowledge. Attacker studied exception handling semantics and discovered that security controls focused on obvious syntax patterns miss less common execution paths. Pragmatic approach: when direct methods are blocked, find alternative language features that achieve the same result.

## Defensive takeaways
- Avoid blacklist-based filtering for JavaScript syntax; use whitelist approaches and Content Security Policy (CSP)
- Filter entire dangerous patterns, not just individual characters (e.g., block 'onerror', 'throw', 'eval')
- Implement strict CSP headers to prevent inline script execution regardless of filter bypasses
- Use multiple layers of defense: input validation, output encoding, and execution context controls
- Test security filters against multiple JavaScript execution patterns, not just standard function call syntax
- Consider context-aware encoding rather than character-level filtering

## Variant hunting
Look for similar exception handling bypasses in other languages (Python's exception handlers, Ruby's raise/rescue). Test other handler attributes (onerror, onload, etc.). Explore template injection contexts where similar syntax restrictions exist. Investigate whether other global event handlers can replace onerror for similar bypass techniques.

## MITRE ATT&CK
- T1190
- T1059
- T1203

## Notes
Technique confirmed working on Chrome and Firefox with different approaches needed for each. Original research from 2019 shows continued evolution of XSS bypass techniques. The fileName property discovery in Error object prototype demonstrates importance of thorough object inspection when standard approaches fail. Research highlights fundamental limitation of character-based filtering versus semantic understanding of language features.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
