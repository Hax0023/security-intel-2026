# Timeline Editor Self-XSS (Previous Fix #738072 Incomplete)

## Metadata
- **Source:** HackerOne
- **Report:** 755679 | https://hackerone.com/reports/755679
- **Submitted:** 2019-12-11
- **Reporter:** mosuan
- **Program:** Unknown
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Self-XSS, Improper Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
A self-XSS vulnerability exists in the Timeline Editor feature due to incomplete sanitization of user input. The vulnerability allows injection of malicious JavaScript code through crafted HTML tags that bypass previous security fix #738072. An attacker can execute arbitrary JavaScript in the admin's browser context when the admin interacts with the crafted payload.

## Attack scenario
1. Attacker identifies the Timeline Editor accepts user input with minimal sanitization
2. Attacker crafts a payload combining multiple HTML elements: img tags, anchor tags with javascript: protocol, and SVG elements
3. Attacker injects payload: `<img src=1111111><img src=1111111><a href="javascript:alert&#40/1/&#41">axxx</a><svg></svg><img src=1>`
4. When admin opens or interacts with the timeline containing the payload, the JavaScript executes in admin context
5. Attacker gains ability to perform actions as the admin (CSRF, account manipulation, data theft)
6. Impact is limited to the admin who processes the malicious timeline entry

## Root cause
The original fix #738072 for XSS in Timeline Editor was incomplete. The sanitization logic failed to properly handle edge cases including: multiple consecutive img tags, HTML entity encoding in href attributes (&#40 for parenthesis), nested SVG elements, and mixed payload patterns. The filter likely used blacklist approach or regex that could be bypassed with encoding or tag combinations.

## Attacker mindset
Low-skill attacker targeting administrative interfaces. The attacker discovered the previous patch was incomplete through fuzzing or by testing variations of the original payload. Self-XSS limitation reduced impact, but admin privileges made it valuable for escalation attacks.

## Defensive takeaways
- Use whitelist-based HTML sanitization libraries (DOMPurify, sanitize-html) instead of blacklist/regex approaches
- Implement Content Security Policy (CSP) with script-src restrictions to mitigate XSS execution
- Apply defense-in-depth: sanitize on input, validate on output, use HTML encoding for all user content
- Test sanitization against OWASP XSS Filter Evasion cheatsheet and entity encoding variations
- Implement proper unit tests covering HTML entities, nested tags, and protocol handlers
- Use automated security scanning (SAST) to detect DOM-based XSS patterns in code
- Consider disabling dangerous HTML elements (img with onerror, svg with onload, javascript: protocol) completely if not needed
- Perform security regression testing when patching XSS vulnerabilities to catch bypass attempts

## Variant hunting
Search for similar incomplete sanitization in other editors (Rich Text Editor, Markdown Editor, Code Editor). Test other admin interfaces with entity-encoded payloads (&#40, &#41, &#34). Look for other uses of Timeline Editor component with different input vectors. Test SVG injection variants with different event handlers. Check if img tag onerror handlers can be triggered instead of href javascript protocol.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing (social engineering to get admin to click timeline)
- T1566 - Phishing: Email Attachment (if timeline is exported/shared)
- T1204.001 - User Execution: Malicious Link
- T1059.007 - Command and Scripting Interpreter: JavaScript

## Notes
The POC explicitly uses HTML entity encoding (&#40 for '(' and &#41 for ')') to obfuscate the javascript: protocol, indicating the original fix likely checked for literal 'javascript:' strings. The combination of multiple img tags with src=1111111 suggests fuzzing to find working payloads. The reference number #738072 indicates this is a regression of a previous security patch. High severity due to admin impact despite self-XSS limitation.

## Full report
<details><summary>Expand</summary>

1.Consistent steps
2.poc: `<img src=1111111><img src=1111111><a href="javascript:alert&#40/1/&#41">axxx</a><svg></svg><img src=1>`
3. {F656339}

## Impact

admin

</details>

---
*Analysed by Claude on 2026-05-12*
