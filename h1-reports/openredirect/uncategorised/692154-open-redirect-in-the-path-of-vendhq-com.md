# Open Redirect in vendhq.com Path via Protocol-Relative URL

## Metadata
- **Source:** HackerOne
- **Report:** 692154 | https://hackerone.com/reports/692154
- **Submitted:** 2019-09-11
- **Reporter:** zoidsec
- **Program:** Vend (vendhq.com)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, Unvalidated Redirect, Protocol-Relative URL Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in vendhq.com allowing attackers to redirect users to arbitrary external domains using protocol-relative URLs (//). By injecting //evil.com/ into the URL path, the application fails to validate and sanitize redirect destinations, enabling phishing and malware distribution attacks.

## Attack scenario
1. Attacker crafts malicious URL: https://www.vendhq.com//evil.com/
2. Attacker sends phishing email to Vend users with legitimate-looking link
3. User clicks link, trusting the vendhq.com domain in the URL bar
4. Application parses the path and redirects to //evil.com/ (attacker's server)
5. Browser resolves protocol-relative URL using attacker's domain
6. User arrives at attacker's phishing site or malware distribution point

## Root cause
Insufficient input validation on redirect destinations. The application likely processes URL paths without properly validating that redirect targets are internal or whitelisted, allowing protocol-relative URLs (beginning with //) to bypass validation and redirect to external domains.

## Attacker mindset
Exploit trusted domain reputation for credential harvesting and malware delivery. Use legitimate vendhq.com domain to establish initial trust, then leverage open redirect to seamlessly transition users to attacker-controlled infrastructure while maintaining appearance of legitimacy.

## Defensive takeaways
- Implement strict whitelist validation for all redirect destinations (internal URLs only)
- Reject or sanitize protocol-relative URLs (//domain.com pattern)
- Use absolute path redirects or relative paths restricted to same-origin
- Validate redirect URLs against a whitelist before processing
- Implement Content Security Policy (CSP) with frame-ancestors and redirect-uri restrictions
- Avoid using user-supplied input directly in Location headers
- Log and monitor redirect attempts to unusual domains for anomaly detection

## Variant hunting
Test other URL path variations: ///evil.com/, /\\evil.com/, /..@evil.com/
Check for open redirects in other endpoint paths (login, logout, callback URLs)
Test URL scheme variations: javascript:, data:, vbscript: payloads
Verify redirect behavior with internationalized domain names (IDN homograph attacks)
Test POST-based redirects if application supports redirect parameters
Check for chained redirects across multiple endpoints
Investigate redirect behavior in API endpoints

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1563.001 - Bash Memory Injection
- T1187 - Forced Authentication

## Notes
Simple yet effective vulnerability. The protocol-relative URL bypass (// prefix) is a well-known technique that strips the scheme, causing the browser to use the attacker's domain. This report lacks specific bounty amount and remediation timeline. Severity should be Medium-to-High given legitimate domain reputation abuse potential for credential theft. Common in applications that accept redirect parameters without proper validation.

## Full report
<details><summary>Expand</summary>

**Summary:** 
There is an open redirection vulnerability in the path of 
```
https://www.vendhq.com/
```

**Description:**
An attacker can redirect anyone to malicious sites.

## Steps To Reproduce:

Type in this URL:

```
https://www.vendhq.com//evil.com/
```

As, you can see it redirects to that website when you inject this payload:
 ```
//evil.com/
```

evil.com was used as an example but this could be any website note, the `//` is the bypass.



## Supporting Material/References:

  * https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html

## Impact

* Attackers can serve malicious websites that steal passwords or download ransomware to their victims machine due to a redirect and there are a heap of other attack vectors.

</details>

---
*Analysed by Claude on 2026-05-24*
