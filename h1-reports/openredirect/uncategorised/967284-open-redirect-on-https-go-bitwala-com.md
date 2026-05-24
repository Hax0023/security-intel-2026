# Open Redirect on https://go.bitwala.com/

## Metadata
- **Source:** HackerOne
- **Report:** 967284 | https://hackerone.com/reports/967284
- **Submitted:** 2020-08-26
- **Reporter:** soe_htet
- **Program:** Bitwala
- **Bounty:** Not awarded (out of scope domain)
- **Severity:** medium
- **Vuln:** Open Redirect, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on go.bitwala.com where the 'fallback' parameter accepts arbitrary URLs and redirects users to attacker-controlled destinations. The vulnerability allows bypassing domain restrictions through URL parameter manipulation, enabling phishing and credential harvesting attacks.

## Attack scenario
1. Attacker identifies the open redirect in go.bitwala.com's fallback parameter
2. Attacker crafts a malicious URL with fallback parameter pointing to a phishing site (e.g., https://go.bitwala.com/d4ffbnr?fallback=https://phishing-site.com)
3. Attacker distributes the crafted URL via email or social media, appearing legitimate due to Bitwala domain
4. Victim clicks the link from trusted source (Bitwala)
5. User is redirected to attacker's phishing page which mimics Bitwala login
6. Attacker steals credentials or sensitive information from redirected user

## Root cause
The 'fallback' parameter is not validated or sanitized before being used in redirect logic. The application fails to implement allowlist-based URL validation, domain whitelist checks, or relative URL enforcement.

## Attacker mindset
Leverage legitimate domain reputation to conduct phishing campaigns. Use the redirect to bypass email filters and security warnings. Chain with social engineering for high success rates in credential harvesting.

## Defensive takeaways
- Implement strict URL validation using allowlists for redirect destinations
- Enforce same-origin/same-domain redirect policies
- Use relative URLs or redirect tokens instead of absolute URL parameters
- Validate fallback parameter against whitelist of approved domains
- Implement Content Security Policy (CSP) headers
- Log and monitor all redirect requests for suspicious patterns
- Educate users to verify domain in address bar before entering credentials

## Variant hunting
Check other tracking/redirect services on Bitwala infrastructure (bit.ly-style services). Audit all URL parameters containing 'redirect', 'return', 'callback', 'fallback', 'next', 'target'. Test parameter encoding bypass (double encoding, Unicode). Examine campaign tracking infrastructure for similar issues.

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1200

## Notes
Reporter explicitly noted the domain is out of scope but submitted for informational purposes. This is good practice for defense-in-depth awareness. The vulnerability is straightforward and exploitable. The presence of utm_* parameters suggests this is a marketing campaign tracking system, making it attractive for attacker reputational abuse.

## Full report
<details><summary>Expand</summary>

Hello 
I found  open redirect bug on https://go.bitwala.com.
I know that domain is not in scope.I just want to inform a bug.

 Steps To Reproduce:

1. go to `https://go.bitwala.com/d4ffbnr?campaign=brand-nov&adgroup=native&creative=link-liquidity%20&fallback=https%3A%2F%2Fwww.bitwala.com%2F%3Futm_source%3Dcryptomonday%26utm_campaign%3Dbrand-nov%26utm_medium%3Dnative%26utm_content%3Dlink-liquidity%20`

2. Change the url like this`https://go.bitwala.com/d4ffbnr?campaign=brand-nov&adgroup=native&creative=link-liquidity%20&fallback=https://www.google.com`

3. It will redirect to `https://www.google.com`

## Impact

An attacker can use this vulnerability to redirect  other malicious,evil websites
.
https://cwe.mitre.org/data/definitions/601.html

</details>

---
*Analysed by Claude on 2026-05-24*
