# Reflected XSS via Improper Redirect URL Validation

## Metadata
- **Source:** HackerOne
- **Report:** 1988560 | https://hackerone.com/reports/1988560
- **Submitted:** 2023-05-15
- **Reporter:** rektile404
- **Program:** Undisclosed
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Open Redirect, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on the target domain due to improper validation of redirect URL parameters. The vulnerable code checks if a URL's host portion (after '://') matches whitelisted domains, but fails to validate the protocol itself, allowing attackers to inject 'javascript:' protocol handlers. The malicious payload can be bypassed by appending a comment sequence that makes the validation function return true.

## Attack scenario
1. Attacker crafts a malicious URL with redirect parameter: redirect=javascript:alert(document.cookie);//://whitelisted-domain/
2. Attacker sends the link to a victim via email, chat, or social engineering
3. Victim clicks the link and is taken to the legitimate domain first
4. The isSafeHost() function checks if the portion after '://' starts with a whitelisted host, finding '://whitelisted-domain' matches
5. Function returns true due to the comment bypassing proper host validation
6. window.location.href is set to the javascript: URI, executing arbitrary JavaScript in the victim's browser context

## Root cause
The validation logic uses string slicing and startsWith() to check if a URL's host is whitelisted, but performs no protocol validation. It extracts everything after '://' and checks if it begins with a safe host. By prepending 'javascript:' before the protocol, the attacker can execute arbitrary code while the validation logic only examines content after the first '://', which in this case is the injected protocol itself. Adding '//' comments at the end masks the actual redirect target.

## Attacker mindset
An attacker recognizing that client-side URL validation often has protocol-level bypasses would test whether the validation function checks the scheme itself. Finding it only validates the host portion after the protocol delimiter, the attacker exploits this by using an alternative protocol (javascript:) that bypasses the whitelist check entirely.

## Defensive takeaways
- Always validate the protocol/scheme explicitly (only allow http:// and https://)
- Use URL parsing APIs (URL constructor) rather than string operations for URL validation
- Implement a blocklist for dangerous protocols (javascript:, data:, vbscript:, file:)
- Perform whitelist validation on the complete normalized URL, not partial segments
- Consider using a URL validation library that handles edge cases and normalization
- Avoid client-side redirect validation when possible; validate on the server
- Test redirect validation with common bypass patterns (protocol manipulation, encoding, special characters)

## Variant hunting
Test data: URI scheme with base64-encoded payloads (data:text/html;base64,...)
Test vbscript: protocol on IE/older browsers
Test file: protocol to access local resources
Test protocol-relative URLs (//attacker.com) if not explicitly blocked
Test URL encoding and double-encoding of ':' and '/' characters
Test mixed case variations (JaVaScript:, jAvAsCrIpT:)
Test null byte injection and Unicode normalization bypasses
Test similar validation functions in other parts of the application
Test redirect parameters with different names (url, target, goto, return, next)

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a classic example of insufficient protocol validation in client-side redirect handling. The developer attempted to implement a whitelist but failed to consider that the protocol scheme itself must be validated before checking the host. The use of string operations (indexOf, slice, startsWith) instead of proper URL parsing APIs contributed to the vulnerability. The comment injection (;//://) is a clever bypass that exploits the fact that the validation only checks if the host 'starts with' a safe value, not that it equals the entire host portion. This is a common pattern in bug bounty reports and should be considered in code review checklists.

## Full report
<details><summary>Expand</summary>

**Description:**
The domain ███ is vulnerable to reflective xss.
By clicking the following link you will get an alert message: https://█████/sec.html?redirect=javascript:alert(document.cookie);//://██████/
The error occurs due to a flaw in the check that verifies the validity of the redirect URL. 
The function takes the value of the redirect parameter and checks if the portion after the first `://` begins with any of the values in the array. 
This check does not include protocol checking, allowing us to prepend the value with `javascript:`. 
Then we can append a commented-out section at the end to ensure that the `isSafeHost` function returns True.
This is the function that checks if it is valid:
```js
function isSafeHost(uri) {
      var safeHosts = ['█████/', '███/', '████/', '██████████'];
      // Only consider localhost for local testing
      if (window.location.host.includes('localhost')) {
        safeHosts.push('localhost');
      }
      return safeHosts.find((host) => uri.slice(uri.indexOf('://') + 3).startsWith(host));
    }
```
At the end of the check the redirect parameter is used as follows:

```js
window.location.href = rawRedirect;
```

## References

## Impact

- Take over a user's account
- Phish users
- Show malicious content 
- Redirect users

## System Host(s)
██████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Click on the following link: https://█████████/sec.html?redirect=javascript:alert(1);//://████/
You can change the `alert(1)` for your own payload

## Suggested Mitigation/Remediation Actions
Do a check for protocol and make sure the host comes directly after this protocol.



</details>

---
*Analysed by Claude on 2026-05-12*
