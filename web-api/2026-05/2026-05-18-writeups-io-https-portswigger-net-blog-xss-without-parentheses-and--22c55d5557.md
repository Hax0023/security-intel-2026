# XSS without Parentheses and Semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Injection
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript code without using parentheses or semi-colons by leveraging the onerror handler combined with throw statements. The vulnerability bypasses input validation filters that attempt to block XSS attacks by prohibiting these characters, enabling attackers to execute malicious scripts on vulnerable applications.

## Attack scenario (step by step)
1. Attacker identifies a web application that filters parentheses and semi-colons to prevent XSS attacks
2. Attacker crafts a payload using the onerror/throw technique: <script>{onerror=alert}throw 1337</script>
3. Attacker injects the payload into a user-controlled input field or parameter
4. The application's filter allows the payload through because it doesn't contain parentheses or semi-colons
5. The browser executes the script, calling the alert function via the onerror handler
6. Malicious code executes with the same privileges as the legitimate application

## Root cause
Input validation filters that only blacklist specific characters (parentheses and semi-colons) without properly understanding JavaScript's execution semantics. The onerror handler combined with throw statements provides an alternative code execution path that bypasses simplistic character-based filters. The technique exploits the fact that onerror is triggered on exceptions and throw accepts expressions.

## Attacker mindset
Security researchers and penetration testers identifying weaknesses in filter implementations. Attackers would recognize that character-based filtering is insufficient and look for alternative JavaScript syntax to achieve code execution. This represents a classic case of finding semantic vulnerabilities in overly simplistic security controls.

## Defensive takeaways
- Never rely on blacklist-based input filtering for security-critical operations; use whitelist validation instead
- Implement context-aware output encoding (HTML, JavaScript, URL encoding) rather than input filtering
- Use Content Security Policy (CSP) headers to restrict script execution and prevent inline script execution
- Apply comprehensive input validation that understands the full JavaScript syntax and execution contexts, not just individual characters
- Employ security review of filtering mechanisms to ensure they account for alternative code execution paths
- Use template engines with automatic escaping and sandboxed execution environments
- Conduct regular security testing with advanced XSS payloads and fuzzing techniques

## Variant hunting
Search for similar filter bypasses in: JavaScript template literals, arrow functions without parentheses, eval alternatives (Function constructor), event handlers beyond onerror (onload, onmouseover), HTML5 vector bypasses, and other exception handler mechanisms. Test combinations of character filtering with JavaScript reflection capabilities.

## MITRE ATT&CK
- T1190
- T1059.007
- T1140

## Notes
This technique was discovered by Gareth Heyes and published in May 2019. The research demonstrates the limitations of signature-based and character-based security controls. Firefox requires special handling due to different exception message formatting ('uncaught exception' vs 'Uncaught'). The researcher developed variants using Error object prototypes to bypass Firefox's exception message prefixes. This research is particularly valuable for understanding filter evasion in Web Application Firewalls (WAF) and input validation mechanisms.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
