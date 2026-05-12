# RCE in 'Copy as Node Request' BApp via Cookie Code Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1167530 | https://hackerone.com/reports/1167530
- **Submitted:** 2021-04-18
- **Reporter:** ryotak
- **Program:** HackerOne (PortSwigger)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Code Injection, Improper Input Sanitization, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
The 'Copy as Node Request' Burp Suite extension fails to properly sanitize single quotes in HTTP cookies, allowing attackers to inject arbitrary Node.js code. When a user copies a request containing a malicious cookie as Node.js code and executes it, the injected code runs with the privileges of the Node.js process.

## Attack scenario
1. Attacker identifies that the target uses the 'Copy as Node Request' BApp extension
2. Attacker crafts a malicious cookie payload containing single quote escape sequences and Node.js code: `test='/require('child_process').exec('calc.exe')//`
3. Attacker tricks user into setting the malicious cookie (via XSS, CSRF, or social engineering)
4. User intercepts a request in Burp Suite and uses 'Copy as Node.js Request' feature to extract code
5. User pastes and executes the generated Node.js code in their development environment
6. Arbitrary code executes on the user's machine with Node.js process privileges

## Root cause
The `escapeQuotes` function in BurpExtender.java only escapes double quotes but not single quotes. Since the cookie field is wrapped in single quotes in the generated Node.js code, attackers can break out of the string literal by injecting a single quote followed by malicious JavaScript code.

## Attacker mindset
Exploit trusted development tools by poisoning their output. Target security researchers and developers who use Burp Suite, since they represent high-value targets with development privileges. Leverage user trust in 'copy-paste' convenience features to achieve code execution in trusted environments.

## Defensive takeaways
- Escape all quote characters (both single and double) when generating code from untrusted input
- Implement allowlist validation for cookie names and values before code generation
- Use parameterized or template-based code generation instead of string concatenation
- Apply context-aware encoding based on the target language syntax
- Add warnings when generating code from user-controlled data
- Use proper Node.js APIs (e.g., JSON methods) instead of string interpolation for data handling
- Implement unit tests for sanitization functions covering all quote types and special characters

## Variant hunting
Check other Burp extensions that generate code (cURL, Python requests, PowerShell, etc.) for similar quote escaping issues
Examine how other fields (headers, parameters, body) are sanitized in this extension
Test for other special characters that might break out of string contexts (backticks, semicolons, newlines)
Look for code generation features in IDE extensions and development tools
Audit any extension that converts HTTP data to executable code formats

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1059.007 - Command and Scripting Interpreter (JavaScript/Node.js)
- T1192 - Spearphishing Link (social engineering component)

## Notes
This vulnerability requires significant user interaction - the attacker must convince a developer to execute untrusted generated code. However, it's high-impact as it affects security researchers using Burp Suite. The fix is straightforward: properly escape all quote types using language-appropriate escaping functions. This is a good example of how convenience features in development tools can become attack vectors when handling untrusted data.

## Full report
<details><summary>Expand</summary>

## Description
`Copy as Node Request` is a burp suite extension that allows users to copy requests as Node.js code.
Due to improper sanitization of cookie,  it's possible to inject arbitrary Node.js code in copied text, which may lead remote code execution with a significant amount of user interaction.

## Root cause
This extension has a function named `escapeQuotes`.
While this function escapes double quotes, it doesn't escape single quotes.
https://github.com/PortSwigger/copy-as-node-request/blob/b34456463310836e93365541189626909adc70bb/src/burp/BurpExtender.java#L165-L167
As the cookie field of generated codes use single quote, it's possible to escape string literal and inject arbitrary Node.js codes.
https://github.com/PortSwigger/copy-as-node-request/blob/b34456463310836e93365541189626909adc70bb/src/burp/BurpExtender.java#L123-L125

## Step to reproduce
1. Install [Copy as Node Request extension](https://portswigger.net/bappstore/e170472f83ef4da1bca5897203b6b33d).
2. Open https://example.com
3. Open DevTools and type `document.cookie = "test='/require('child_process').exec('calc.exe')//"`
4. Enable intercept and reload the browser tab.
5. Right click on intercepted request and click `Copy as Node.js Request`.
6. Execute copied text in Node.js.
7. `calc.exe` will be popped up.

{F1269399}

## Impact

Remote code execution via Node.js code injection with user interaction.

</details>

---
*Analysed by Claude on 2026-05-11*
