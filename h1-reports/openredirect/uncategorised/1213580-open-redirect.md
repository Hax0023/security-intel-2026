# Open Redirect via Unvalidated Redirect Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1213580 | https://hackerone.com/reports/1213580
- **Submitted:** 2021-05-31
- **Reporter:** 0xpugal
- **Program:** Affirm
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, URL Redirection to Untrusted Site, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on affirm.com where users can be redirected to arbitrary external domains through a maliciously crafted URL parameter. The vulnerability allows attackers to craft phishing URLs that appear to originate from Affirm's domain but redirect users to attacker-controlled sites.

## Attack scenario
1. Attacker crafts a malicious URL: https://www.affirm.com///google.com/?www.affirm.com/?category=interview&page=2
2. Attacker sends the URL via phishing email claiming to be from Affirm
3. User clicks the link, trusting the affirm.com domain prefix
4. Affirm's redirect mechanism processes the request without proper validation
5. User is redirected to google.com (or attacker's phishing site in real scenario)
6. Attacker steals credentials or deploys malware from the fake site

## Root cause
The application fails to validate or sanitize redirect URL parameters before redirecting users. The triple slash (///) bypasses path-based validation and the parameter parsing allows arbitrary domains to be injected into the redirect chain.

## Attacker mindset
Leverage trust in legitimate domain to conduct phishing attacks. Use technical obfuscation (triple slashes, parameter chaining) to evade basic validation and craft URLs that appear legitimate while redirecting to attacker infrastructure.

## Defensive takeaways
- Implement strict URL validation for all redirect parameters using allowlist approach
- Validate that redirects only go to known internal endpoints or explicitly whitelisted domains
- Use relative redirects instead of absolute URLs when possible
- Implement proper URL parsing that handles edge cases like multiple slashes
- Add security headers (Referrer-Policy) to prevent sensitive data leakage
- Log and monitor all redirect requests for suspicious patterns
- Educate users about verifying actual URLs in browser address bar before entering credentials

## Variant hunting
Check other redirect parameters: ?return=, ?redirect=, ?goto=, ?next=, ?url=
Test for javascript:// and data:// protocol handlers
Test URL encoding bypasses: %2f%2f, %252f%252f
Test backslash variants in Windows environments: \\domain.com
Check subdomain redirects: //attacker.affirm.com
Test parameter pollution attacks combining multiple redirect params
Test fragment-based redirects: #@evil.com

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1187 - Forced Authentication
- T1192 - Spearphishing Link

## Notes
This is a classic open redirect reported with minimal detail. The POC URL syntax suggests parameter confusion - the application may be processing query parameters incorrectly. The report lacks information about bounty amount, remediation timeline, and response from Affirm. This vulnerability is typically medium severity unless combined with CSRF or used in specific contexts that could elevate risk to high.

## Full report
<details><summary>Expand</summary>

Open Redirect Vulnerability:

URL : https://www.affirm.com/

User can be redirect to malicious site
POC:https://www.affirm.com///google.com/?www.affirm.com/?category=interview&page=2

I hope you know the impact of open redirect and more info refer
https://cwe.mitre.org/data/definitions/601.html

## Impact

User can be redirect to malicious site

</details>

---
*Analysed by Claude on 2026-05-24*
