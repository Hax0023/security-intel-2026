# Open Redirect on paragonie.com

## Metadata
- **Source:** HackerOne
- **Report:** 113112 | https://hackerone.com/reports/113112
- **Submitted:** 2016-01-27
- **Reporter:** hat_mast3r
- **Program:** Paragon Initiative Enterprises
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability was discovered on paragonie.com allowing attackers to redirect users to arbitrary external domains. The vulnerability exploits improper URL validation by using double slashes in the redirect parameter.

## Attack scenario
1. Attacker crafts a malicious URL: https://paragonie.com//google.com/
2. Attacker shares link via phishing email, social engineering, or trusted platform
3. Victim clicks the link trusting the paragonie.com domain
4. Application redirects victim to attacker-controlled domain (google.com in PoC)
5. Victim lands on lookalike or malicious site controlled by attacker
6. Attacker can harvest credentials, distribute malware, or perform phishing

## Root cause
Insufficient URL validation in redirect functionality. The application likely uses a simple prefix check or startswith() validation that fails to properly canonicalize URLs with double slashes (//), allowing bypass of domain whitelist controls.

## Attacker mindset
Low-effort exploit targeting user trust in legitimate domains. Attackers leverage the legitimate domain reputation for phishing and credential harvesting campaigns, exploiting the natural inclination of users to trust established organizations.

## Defensive takeaways
- Implement strict URL parsing using URL parsing libraries rather than string operations
- Validate redirects against a whitelist of allowed domains
- Use URL normalization/canonicalization before validation checks
- Avoid client-side redirects; use server-side validation with proper parsing
- Implement CSP headers to restrict redirect destinations
- Log all redirect attempts for security monitoring

## Variant hunting
Test encoded redirect parameters (%2F%2F)
Check for bypass using backslash variants (\\google.com)
Test protocol-relative URLs (//google.com)
Attempt data: and javascript: protocol redirects
Test with additional path traversal sequences
Check multiple redirect parameters for chain attacks

## MITRE ATT&CK
- T1598.003
- T1598.002
- T1598

## Notes
This is a relatively straightforward open redirect discovered through basic URL manipulation. The double slash technique suggests the application is using simple string matching rather than proper URL parsing libraries. No monetary bounty amount was disclosed in the report.

## Full report
<details><summary>Expand</summary>

Hello, 

I would like to report about open-redirect on  paragonie.com

Here is the PoC that redirects to URL. For example::https://paragonie.com//google.com/

Regards,

Hat_Mast3r

</details>

---
*Analysed by Claude on 2026-05-24*
