# PayPal Node.js Dust.js Template Injection RCE via Array Parameter Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** PayPal (demo.paypal.com)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Server-Side Template Injection (SSTI), Code Injection, Remote Code Execution (RCE), Unsafe use of eval(), Input validation bypass
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
PayPal's demo application used Dust.js templating engine with unsafe eval() in the 'if' helper function. While the application attempted to sanitize single and double quotes by HTML encoding, an attacker could bypass this protection by sending array parameters (device[]=...) which are parsed as arrays instead of strings, allowing direct code injection into the eval() call.

## Attack scenario (step by step)
1. Attacker fuzzes HTTP parameters and discovers that backslash (\) and newline (%0a) characters trigger syntax errors, indicating code evaluation
2. Attacker identifies the application uses Dust.js templating engine with eval()-based 'if' helpers through error messages
3. Attacker recognizes that standard quote characters are HTML-encoded as a defense mechanism (single quote to &#39;)
4. Attacker discovers that Node.js qs module parses URL parameters like device[]=value as arrays instead of strings, bypassing string-based sanitization
5. Attacker crafts payload using array syntax: device[]=x&device[]=y'-require('child_process').exec('command')-' to inject arbitrary Node.js code
6. Injected code executes with application privileges, allowing command execution such as exfiltrating /etc/passwd

## Root cause
Multiple layers of insufficient security: (1) Use of unsafe eval() in Dust.js 'if' helper for expression evaluation, (2) HTML entity encoding of quotes providing false sense of security without addressing the core eval vulnerability, (3) Failure to validate that templating parameters are strings before passing to sanitization functions, allowing type confusion when arrays are supplied, (4) No parameterized/safe evaluation mechanism for Dust.js expressions

## Attacker mindset
Methodical fuzzing approach to identify injection points through differential error responses. Deep understanding of Node.js ecosystem (qs parsing, array parameters) combined with template engine internals to craft a bypass. Recognition that string-based sanitization can be circumvented by providing non-string types, demonstrating sophisticated type-based vulnerability exploitation.

## Defensive takeaways
- Never use eval() or similar dynamic code evaluation for template expression handling; use purpose-built safe evaluation frameworks
- Implement input validation that checks parameter types, not just values - ensure expected types before processing
- Understand that HTML entity encoding alone does not prevent code injection in eval contexts; it only prevents HTML/XSS injection
- Apply defense-in-depth: sanitize at multiple layers and use allowlists rather than blocklists for dangerous characters
- Keep dependencies updated; older versions of Dust.js had fundamental design flaws that should be migrated away from
- Disable eval() in templating engines entirely; use restricted expression evaluation APIs when available
- Use static analysis tools to detect eval() usage with untrusted input
- Implement strict CSP and sandboxing for template processing when possible

## Variant hunting
['Search for other Node.js template engines using eval() (EJS, Jade, Handlebars with unsafe helpers)', 'Identify applications using qs/body-parser with eval-based processing - check for similar array parameter bypasses', "Look for other applications using old Dust.js versions with 'if' helpers", 'Test other PayPal domains and properties for similar template injection patterns', 'Examine custom template implementations that attempt string-based sanitization without type checking', 'Check for similar bypasses in other JS-based template engines where sanitization is applied post-parsing', 'Search for applications that sanitize before type coercion rather than after']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (Node.js)
- T1202 - Indirect Command Execution
- T1083 - File and Directory Discovery

## Notes
This is a highly educational example of a sophisticated security bypass. The vulnerability demonstrates: (1) importance of understanding framework internals, (2) how multiple weak mitigations can be bypassed with proper understanding of the technology stack, (3) the dangers of eval() in any context, and (4) how type confusion can defeat string-based security measures. The $10,000 bounty reflects the critical nature and exploitability of RCE vulnerabilities on customer-facing properties.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
