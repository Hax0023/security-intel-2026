# DOM XSS on duckduckgo.com via norw Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 868934 | https://hackerone.com/reports/868934
- **Submitted:** 2020-05-08
- **Reporter:** cujanovic
- **Program:** DuckDuckGo
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), DOM-based XSS, Improper Input Validation, Inadequate Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in DuckDuckGo's search functionality through the 'norw' parameter, which fails to properly sanitize or encode user input before rendering it in the DOM. An attacker can inject arbitrary JavaScript code that will execute in the victim's browser with the privileges of the DuckDuckGo domain.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'norw' parameter: https://duckduckgo.com/?q=a&norw="><img src=/ onerror=alert(document.domain)>
2. Attacker distributes the URL via phishing email, social media, or other social engineering tactics
3. Victim clicks the malicious link while authenticated to DuckDuckGo
4. Browser processes the URL and the 'norw' parameter is inserted unsanitized into the DOM
5. The injected HTML/JavaScript is parsed and executed by the browser
6. Attacker's JavaScript executes with access to the victim's cookies, session tokens, and sensitive data within the DuckDuckGo context

## Root cause
The 'norw' parameter is directly rendered into the DOM without proper output encoding or HTML entity escaping. The application fails to sanitize special characters like quotes and angle brackets that are necessary for breaking out of HTML attribute/element context.

## Attacker mindset
An attacker recognizes that search engines often pass URL parameters directly to the DOM for functionality like displaying the current search query or settings. By testing special characters in various parameters, they discovered the 'norw' parameter lacks sanitization, allowing them to inject arbitrary HTML/JavaScript that executes in the user's browser under the DuckDuckGo domain.

## Defensive takeaways
- Implement strict output encoding for all user-supplied data rendered in the DOM (use context-aware encoding: HTML entity encoding, JavaScript encoding, URL encoding, CSS encoding)
- Apply Content Security Policy (CSP) headers to restrict script execution and prevent inline script injection
- Use templating engines with auto-escaping enabled to prevent accidental XSS
- Validate and whitelist input parameters; reject unexpected characters or formats
- Conduct regular security code reviews focusing on DOM manipulation and parameter handling
- Implement automated XSS detection in parameter fuzzing during QA testing
- Use Security linters and static analysis tools to identify DOM XSS patterns
- Apply the principle of least privilege when handling user input, especially in search/query parameters

## Variant hunting
Test all URL parameters for similar XSS vulnerabilities (q, kp, ko, k, etc.)
Try alternative payload encodings (Unicode escapes, HTML entities, double encoding)
Test reflected parameters in different HTML contexts (attributes, tag content, script context)
Check for XSS in other DuckDuckGo properties and subdomains
Look for DOM manipulation in JavaScript that processes URL parameters
Test for mutations filtering (attempts to bypass XSS filters with nested tags or case variations)
Investigate other search parameters that might interact with the 'norw' parameter

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1059.007

## Notes
The 'norw' parameter likely stands for 'no rewrite' or similar functionality. The vulnerability demonstrates the importance of consistently applying output encoding across all parameters, not just obvious ones like 'q' (query). Even parameters controlling application behavior should be treated as untrusted input. This type of vulnerability is prevalent in search engines and requires defense-in-depth strategies.

## Full report
<details><summary>Expand</summary>

Hello, 
The is a DOM XSS vulnerability on https://duckduckgo.com search through the ```norw``` parameter.

PoC URL:  ```https://duckduckgo.com/?q=a&norw="><img src=/ onerror=alert(document.domain)>```

Screenshot: {F820482}

## Impact

The attacker can execute JS code.

</details>

---
*Analysed by Claude on 2026-05-11*
