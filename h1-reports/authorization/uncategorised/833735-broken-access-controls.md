# Broken Access Control via .html Extension Bypass on notary.acronis.com

## Metadata
- **Source:** HackerOne
- **Report:** 833735 | https://hackerone.com/reports/833735
- **Submitted:** 2020-03-29
- **Reporter:** lucasandracoli
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Authentication Bypass, Path Traversal/Extension-Based Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The notary.acronis.com endpoint implements access controls that restrict unauthenticated users from accessing the admin panel. However, the security mechanism can be bypassed by appending .html extensions to requests, allowing unauthenticated attackers to access restricted panel functions. This authentication bypass undermines the entire access control mechanism protecting sensitive administrative functionality.

## Attack scenario
1. Attacker identifies that notary.acronis.com requires authentication to access the admin panel
2. Attacker discovers that direct requests to protected endpoints return 401/403 errors
3. Attacker crafts a request by appending .html extension to a protected resource URL (e.g., /admin/.html or /admin/dashboard.html)
4. The server processes the .html extension request differently, bypassing the authentication middleware
5. Attacker gains unauthorized access to panel functions and sensitive administrative operations
6. Attacker can enumerate, modify, or exfiltrate data accessible through the panel

## Root cause
The authentication/authorization middleware likely checks routes using a whitelist or pattern matching that does not account for alternate file extensions. The .html extension causes the request to bypass the authentication filter, possibly due to: (1) middleware evaluating authentication before static file handlers, (2) regex patterns that don't match .html variants, or (3) web server configuration serving .html files without enforcing authentication checks

## Attacker mindset
A reconnaissance-focused attacker testing common bypass techniques (file extensions, path variations) against access-controlled endpoints. The attacker demonstrates methodical fuzzing of file extensions to find authentication weaknesses, exploiting a gap between the intended security model and actual implementation.

## Defensive takeaways
- Implement authentication/authorization at the application layer, not relying on routing or middleware alone
- Use a deny-by-default approach: explicitly whitelist which endpoints don't require authentication rather than blacklisting
- Normalize all request paths/extensions before authentication checks to prevent extension-based bypasses
- Ensure authentication checks apply to all file types and extensions, not just specific ones
- Implement proper web server configuration to enforce authentication headers regardless of file extension
- Use security headers like X-Frame-Options and X-Content-Type-Options to reduce attack surface
- Conduct thorough testing of authentication mechanisms including fuzzing with various file extensions
- Apply principle of least privilege to all admin panel functions and API endpoints

## Variant hunting
Test with double extensions (.html.php, .php.html)
Try case variations (.HTML, .Html)
Attempt null byte injection (.html%00, .html;.php)
Test with trailing slashes (/admin/.html/)
Try other file extensions (.htm, .txt, .json, .xml)
Test encoded extensions (.html%2e, %2ehtml)
Attempt path traversal combinations (../admin.html)
Test with query parameters (?format=html, ?ext=html)

## MITRE ATT&CK
- T1190
- T1566
- T1110
- T1021

## Notes
The report references a video PoC that is critical for understanding the exact exploitation method but is not detailed in the text. The vulnerability appears to stem from a common misconfiguration where static file handlers bypass authentication middleware. This type of vulnerability is frequently seen in frameworks where routing and authentication are not properly integrated. The fix is relatively straightforward but requires careful implementation to ensure all access paths are protected uniformly.

## Full report
<details><summary>Expand</summary>

The End Point `notary.acronis.com` Blocks access to the panel if you are not an authenticated user.
More is possible to access some functions of the panel by adding the .html at the end

See Poc From Video Below

## Impact

Broken access control vulnerabilities exist when a user can in fact access some resource or perform some action that they are not supposed to be able to access.

</details>

---
*Analysed by Claude on 2026-05-24*
