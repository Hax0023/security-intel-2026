# PayPal demo.paypal.com Node.js Code Injection (RCE) via Dust.js Template Engine

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Code Injection, Remote Code Execution, Template Injection, Unsafe use of eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A Node.js application on demo.paypal.com used the Dust.js templating engine with unsafe eval() in the 'if' helper function. By sending array parameters instead of strings, the attacker bypassed HTML entity encoding protections and achieved remote code execution.

## Attack scenario (step by step)
1. Attacker performs fuzzing of HTTP parameters and discovers that backslash (\) and newline (%0a) characters cause syntax errors, indicating server-side code evaluation
2. Attacker identifies Dust.js templating engine from error messages and reviews its source code, discovering unsafe eval() usage in 'if' helpers
3. Attacker discovers the application HTML-encodes dangerous characters (quotes) to prevent direct code injection when parameters are strings
4. Attacker realizes Node.js query string parsing converts array syntax (device[]=value) to Array objects instead of strings, bypassing the HTML encoding function which expects string input
5. Attacker crafts payload using array parameters: device[]=x&device[]=y'-require('child_process').exec(...)-' to inject arbitrary code
6. Attacker executes shell commands on the server through child_process module, exfiltrating /etc/passwd file

## Root cause
Multiple compounding issues: (1) Use of eval() in Dust.js 'if' helper for expression evaluation, (2) Type-unsafe sanitization that only HTML-encodes strings but fails when receiving Array objects, (3) Array parameter parsing that circumvents the string-based sanitization logic

## Attacker mindset
Methodical fuzzing approach to identify unusual server behavior; deep code review of open-source dependencies to understand implementation details; creative type-confusion exploitation to bypass input validation; understanding of Node.js runtime and module system to craft working payloads

## Defensive takeaways
- Never use eval() for untrusted input evaluation; use safe expression evaluators or abstract syntax trees instead
- Implement type-safe input validation that handles all possible input types (strings, arrays, objects), not just the expected type
- Sanitize and validate input before any processing, including before template engine parsing
- Keep dependencies updated and monitor for security advisories in templating engines
- Use Content Security Policy and other defense-in-depth measures
- Prefer template engines with sandboxed evaluation rather than those using eval()
- Apply principle of least privilege to application runtime (disable shell command execution if possible)

## Variant hunting
['Check other Dust.js helpers for similar eval() usage patterns', 'Test other templating engines (EJS, Handlebars, Jade) for similar type-confusion bypass in sanitization', 'Search for other instances where array parameters bypass string-based validation across the application', 'Look for other uses of child_process or vm modules with unsanitized input', 'Test other PayPal endpoints and subdomains for similar template injection vectors', 'Check if other query string parsers (express-qs, body-parser) have similar type-handling issues']

## MITRE ATT&CK
- T1190
- T1059
- T1592
- T1583

## Notes
This vulnerability demonstrates the critical importance of type-safe input validation and the dangers of eval(). The attacker's exploitation of type confusion in the qs module (Array vs String) to bypass sanitization is particularly clever. The write-up is from 2016, and Dust.js has since removed the unsafe 'if' helper in newer versions. This is an excellent example of defense in depth failure where multiple layers (eval usage, weak sanitization, unsafe defaults) contributed to critical RCE.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
