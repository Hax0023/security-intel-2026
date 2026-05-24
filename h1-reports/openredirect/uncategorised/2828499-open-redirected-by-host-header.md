# Open Redirect via Host Header Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 2828499 | https://hackerone.com/reports/2828499
- **Submitted:** 2024-11-07
- **Reporter:** black_world
- **Program:** localizestaging.com
- **Bounty:** unknown
- **Severity:** medium
- **Vuln:** Open Redirect, Host Header Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application fails to validate the Host header and uses it directly in redirect logic, allowing attackers to redirect users to arbitrary external domains. An attacker can manipulate the Host header to cause victims to be redirected to malicious websites while appearing to originate from a trusted source.

## Attack scenario
1. Attacker identifies that localizestaging.com uses the Host header in redirect logic without validation
2. Attacker crafts a request to localizestaging.com with a malicious Host header pointing to attacker-controlled domain
3. Application redirects user to the domain specified in the Host header
4. Victim visits malicious site believing it originated from the trusted localizestaging.com domain
5. Attacker can host phishing pages, malware, or credential harvesting forms on the redirect destination
6. User credentials or sensitive information is compromised through the malicious site

## Root cause
The application uses the Host header directly in redirect responses without validating that the target domain is whitelisted or belongs to the application. The Host header is an untrusted client-supplied input that should never be used for security-critical decisions like determining redirect destinations.

## Attacker mindset
An attacker recognizes that users trust redirects from known domains and exploits this by manipulating server-side logic to appear as though a legitimate domain is directing them to attacker infrastructure. This is valuable for phishing campaigns where the initial domain carries weight and authority.

## Defensive takeaways
- Never trust the Host header for security decisions; use server-side configuration instead
- Maintain an explicit whitelist of allowed redirect destinations
- Validate all redirect URLs against the whitelist before performing the redirect
- Use relative URLs or explicitly construct redirect URLs from trusted configuration
- Implement security headers like X-Frame-Options and Content-Security-Policy to provide defense-in-depth
- Log all redirect operations for security monitoring
- Consider implementing anti-phishing measures and user warnings for external redirects

## Variant hunting
Test other HTTP headers (Referer, X-Forwarded-Host, X-Original-URL) for similar injection points
Check for open redirects in login flows, logout endpoints, and password reset flows
Test redirect parameters with javascript: and data: protocol handlers
Examine redirect logic in API endpoints that return redirect URLs in JSON responses
Check for double-encoding or bypasses using encoded dots or URL variations
Test with protocol-relative URLs (//attacker.com) that may bypass validation logic

## MITRE ATT&CK
- T1598.002
- T1566.002
- T1187

## Notes
The vulnerability appears to be on a staging environment (localizestaging.com) which may indicate limited real-world impact but suggests the same issue could exist in production. The reproduction steps are simple, making this a straightforward validation issue. Open redirects are often chained with phishing or used to bypass URL-based security filters. The bounty amount was not disclosed in the report.

## Full report
<details><summary>Expand</summary>

An Open Redirect vulnerability occurs when an application allows users to be redirected to an external, untrusted URL without validating the redirection target. By controlling the Host header and observing a redirection to the specified external site, you may have found an open redirect vulnerability.



STEP TO REPRODUCE:
go to  www.localizestaging.com and interpret then change host header .it will redirect to changed host header webisite

## Impact

This vulnerability can be exploited for phishing attacks, where users are misled into visiting a malicious site that appears to be trusted. It could also be used to bypass security filters or conduct other malicious activities.

</details>

---
*Analysed by Claude on 2026-05-24*
