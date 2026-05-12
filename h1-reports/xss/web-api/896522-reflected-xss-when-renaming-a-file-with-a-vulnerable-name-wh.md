# Reflected XSS in File Rename Error Messages via Malicious Filename

## Metadata
- **Source:** HackerOne
- **Report:** 896522 | https://hackerone.com/reports/896522
- **Submitted:** 2020-06-12
- **Reporter:** yzy9951
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Output Encoding, Error Message Handling
- **CVEs:** CVE-2021-22878
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Nextcloud's file rename functionality where error messages fail to properly encode filenames containing XSS payloads. When a user attempts to rename a file with a previously crafted malicious filename to an invalid name, the error response reflects the unencoded filename, allowing arbitrary JavaScript execution. The vulnerability requires bypassing Content Security Policy (CSP) protections.

## Attack scenario
1. Attacker creates or uploads a file with a malicious filename: '<img src=x onerror=prompt(1)>.jpg'
2. Attacker crafts a URL or triggers a rename operation targeting this file to an invalid filename (e.g., one containing backslashes)
3. The rename operation fails due to the invalid target filename
4. Nextcloud's error handler reflects the original filename unsafely in the error message response
5. The malicious JavaScript payload executes in the victim's browser context
6. Attacker can modify attack to bypass CSP headers through various payload techniques (svg, event handlers, etc.)

## Root cause
The file rename error handler fails to properly HTML-encode or sanitize the original filename before including it in error messages returned to the client. This allows arbitrary HTML and JavaScript to be reflected in the response without proper escaping.

## Attacker mindset
Opportunistic vulnerability chaining - leveraging previously created malicious files as stepping stones. The attacker recognizes that error handling code often receives less security scrutiny than primary functionality, making it an attractive target for XSS exploitation.

## Defensive takeaways
- Always encode user-controlled data (including filenames) in all output contexts, especially error messages
- Implement context-aware output encoding (HTML encoding for HTML context, JavaScript encoding for JS context, etc.)
- Apply defense-in-depth: rely on both output encoding AND CSP, not CSP alone
- Review all error handling paths for XSS vulnerabilities, as they are commonly overlooked
- Implement input validation on filenames to reject obviously malicious patterns
- Test error cases with XSS payloads as part of security testing regime
- Use templating engines with auto-escaping enabled by default

## Variant hunting
Check other error message handlers in file operations (copy, move, delete)
Examine all user-supplied input reflected in error responses across the application
Test other file manager operations that display filenames in error conditions
Look for similar issues in other Nextcloud apps that handle file operations
Check if comments, tags, or metadata on files are similarly vulnerable
Test bulk file operations error messages for similar XSS issues

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1203 - Exploitation for Client Execution

## Notes
This is a follow-up to report #896511, suggesting the initial XSS was CSP-protected. This variant demonstrates that attackers actively probe for alternative code paths and error handling flows to bypass security controls. The requirement to 'bypass CSP' indicates Nextcloud may have been relying on CSP as primary defense rather than proper encoding, which violates defense-in-depth principles.

## Full report
<details><summary>Expand</summary>

Hi,

It looks like Nextcloud team will accept the XSS protected by the CSP. (Report #896511)
Here is another XSS.
1. Rename an existing filename to <img src=x onerror=prompt(1)>.jpg.
2. Anyone tries to rename this <img src=x onerror=prompt(1)>.jpg with an invalid filename, like add a "\" in it, will trigger the XSS attack.
3. Need bypass the CSP.

Thanks

## Impact

Cross-Site Scripting

</details>

---
*Analysed by Claude on 2026-05-12*
