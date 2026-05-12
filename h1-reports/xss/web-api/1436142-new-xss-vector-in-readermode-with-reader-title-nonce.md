# XSS in Brave iOS ReaderMode via %READER-CREDITS% Meta Tag Injection with Nonce Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1436142 | https://hackerone.com/reports/1436142
- **Submitted:** 2021-12-26
- **Reporter:** nishimunea
- **Program:** Brave
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Meta Tag Injection, Nonce Mishandling
- **CVEs:** None
- **Category:** web-api

## Summary
A CSP relaxation in Brave iOS ReaderMode allows scripts with nonce-%READER-TITLE-NONCE% to execute. The vulnerability exists because the %READER-CREDITS% template variable (populated from the HTML meta author tag) is not properly escaped before insertion, allowing attackers to inject malicious scripts that bypass CSP and execute with the correct nonce.

## Attack scenario
1. Attacker creates a malicious webpage containing a crafted meta author tag with embedded script: `<meta name="author" content="Evil <script nonce=%READER-TITLE-NONCE%>malicious_code</script>!--">`
2. Victim visits the attacker's webpage in Brave iOS browser
3. Victim activates ReaderMode by tapping the reader mode button
4. The ReaderMode parser extracts the author meta tag value without HTML escaping and inserts it into the ReaderMode template
5. The nonce replacement function replaces %READER-TITLE-NONCE% with the actual nonce value, making the script valid
6. The script executes with full privileges, allowing theft of ReaderMode page content, session data, and potentially access to privileged pages via uuidkey exposure

## Root cause
Insufficient input sanitization: The %READER-CREDITS% template variable derived from the HTML meta author tag is inserted into the ReaderMode HTML template without proper HTML entity escaping. Combined with the CSP relaxation to allow nonce-based scripts, this creates an XSS vector. The nonce replacement mechanism does not validate or escape the content before processing.

## Attacker mindset
An attacker recognizes that while CSP was tightened by disallowing general scripts, the nonce-based exception creates a new attack surface. By identifying that user-controlled metadata (author tag) is directly interpolated into the template without escaping, they craft an injection that leverages the nonce replacement to achieve code execution. The attacker aims to steal sensitive page content and session identifiers to escalate privileges.

## Defensive takeaways
- Always HTML-escape user-controlled content before insertion into HTML templates, regardless of CSP policies
- When implementing nonce-based CSP exceptions, validate that nonce replacement occurs only on explicitly safe content, not on template variables from untrusted sources
- Sanitize metadata tags (meta, title, author, etc.) extracted from user-supplied HTML with the same rigor as body content
- Implement a Content Security Policy that does not rely on nonce-based exceptions for dynamically generated content
- Use templating engines with automatic escaping enabled by default
- Apply defense-in-depth: combine output encoding, input validation, and strict CSP rules
- Regularly audit the flow of external data through template systems to identify similar injection points

## Variant hunting
Look for similar issues in other ReaderMode template variables (%READER-TITLE%, %READER-CONTENT%, etc.) that might be populated from untrusted sources. Check for nonce bypass patterns in other browser features using dynamic nonce insertion. Investigate whether other metadata tags (description, keywords, og:* tags) are similarly vulnerable. Search for template variable injection in other offline/privileged pages hosted on localhost.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Generic Phishing
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1059 - Command and Scripting Interpreter

## Notes
The vulnerability is particularly severe because: (1) ReaderMode pages are hosted on a localhost origin with potential privilege isolation, (2) the uuidkey in URL query strings could grant access to sensitive data, (3) the attack requires only that a user visits a malicious site and activates ReaderMode. The CSP relaxation was well-intentioned but created a regression by trusting nonce values in contexts where untrusted content is processed. This is a classic example of how security mitigations can paradoxically create new vulnerabilities if not carefully integrated with input validation.

## Full report
<details><summary>Expand</summary>

## Summary:
Previously, script execution in ReaderMode pages was prohibited by CSP. However, three months ago, [this commit](https://github.com/brave/brave-ios/pull/4209/files#diff-eaeef15a290e9e5e9bcaae784f18d874f8c932dfa3de416a5820eccd6b2d8cfbR54) partially relaxed the CSP and scripts with `nonce-%READER-TITLE-NONCE%` are now allowed to be executed. This relaxation of the CSP rule can be exploited for XSS attacks on ReaderMode pages.

Here, the attack vector is `%READER-CREDITS%` which is also [included in the ReaderMode HTML template](https://github.com/brave/brave-ios/blob/6f667506228eeff77daf4df7c9dddae22eb0ad1b/Client/Frontend/Reader/Reader.html#L18). The `%READER-CREDITS%` is replaced with the value of the `<meta name="author">` tag in the original page, but then the HTML tags are not escaped. So, when the following meta tag is embedded in the original page and the page is displayed in ReaderMode, [this Swift code](https://github.com/brave/brave-ios/blob/6f667506228eeff77daf4df7c9dddae22eb0ad1b/Client/Frontend/Reader/ReaderModeUtils.swift#L30)  replaces `%READER-TITLE-NONCE%` with the correct nonce value.
```
<meta name="author" content="Evil &lt;script nonce=%READER-TITLE-NONCE%&gt;alert(document.location);&lt;/script&gt;!--">
```

As a result, the malicious script will be executed on a page `http://localhost:6571/reader-mode?uri={uri}&uuidkey={value}`.
In Brave, all readalized pages are hosted on `http://localhost:6571`. Therefore, through this XSS, any cross-origin pages, that has been converted to ReaderMode, can be stolen by embedding an iframe and reading out them. Also, please find that the `uuidkey` is included in the URL query string. By obtaining this key, the attacker can gain access to Brave's privileged pages.

## Products affected: 

 * Brave iOS 1.31.1 and higher (including the latest Nightly)

## Steps To Reproduce:

 * Show https://csrf.jp/2021/brave/author_xss.php
 * Push reader mode button on the address bar
 * An alert dialog is shown

## Supporting Material/References:

 * See the screenshot of the alert dialog when the bug is reproduced.

## Impact

* Any cross-origin pages, that has been converted to ReaderMode, can be stolen
* Attacker can gain access to Brave's privileged pages

</details>

---
*Analysed by Claude on 2026-05-12*
