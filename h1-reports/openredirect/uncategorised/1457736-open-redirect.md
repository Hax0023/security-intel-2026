# Open Redirect via redirecturl Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1457736 | https://hackerone.com/reports/1457736
- **Submitted:** 2022-01-21
- **Reporter:** mmdz
- **Program:** Unknown (Redacted)
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Open Redirect, URL Redirect Validation Failure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application accepts a 'redirecturl' parameter without proper validation, allowing attackers to redirect users to arbitrary external websites. This vulnerability can be exploited for phishing attacks, credential harvesting, or distributing malware by crafting malicious URLs that appear to originate from the trusted domain.

## Attack scenario
1. Attacker identifies the vulnerable redirecturl parameter in the target application
2. Attacker crafts a malicious URL: https://[victim-domain]?redirecturl=https://attacker-phishing-site.com
3. Attacker sends the crafted URL to victims via email, social media, or other channels
4. Victim clicks the link trusting the victim-domain prefix
5. Application redirects the victim to the attacker's phishing site without validation
6. Attacker harvests credentials or distributes malware from the fake site

## Root cause
The application fails to validate or sanitize the 'redirecturl' parameter before performing a redirect. No whitelist of allowed redirect destinations, origin validation, or protocol restrictions were implemented.

## Attacker mindset
An attacker would leverage the trusted domain's authority to make phishing attacks more convincing. The URL appears legitimate to users since it starts with the trusted domain, increasing click-through rates on malicious links.

## Defensive takeaways
- Implement a whitelist of allowed redirect destinations and validate against it
- Use relative redirects instead of accepting user-supplied absolute URLs
- Validate that redirect URLs belong to the same domain or approved domains only
- Implement proper URL parsing and validation using secure libraries
- Add user confirmation dialogs when redirecting to external sites
- Use Content Security Policy (CSP) headers to restrict redirect destinations
- Log all redirect activities for security monitoring
- Implement input validation for all user-supplied URL parameters

## Variant hunting
Check for other redirect parameters: 'redirect', 'url', 'return', 'next', 'target', 'returnurl'
Test with URL encoding and double encoding: %252F%252F for bypassing basic filters
Try protocol-relative URLs: //example.com
Test with javascript: and data: URI schemes
Look for same vulnerability in logout, login, and password reset flows
Check POST parameters and headers for redirect functionality
Test case variations: 'RedirectUrl', 'REDIRECTURL', 'redirect_url'

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1598.002 - Phishing: Spearphishing Attachment
- T1187 - Forced Authentication

## Notes
This is a low-severity vulnerability by modern standards but remains exploitable for social engineering attacks. The impact depends on context - if used in high-privilege operations, severity could increase. The report lacks detailed analysis and remediation steps. Many bug bounty programs award minimal bounty for open redirects (typically $50-$250 depending on context and exploitability).

## Full report
<details><summary>Expand</summary>

The following URL is vulnerable to an open redirect (it will redirect to example.com):
https://█████?redirecturl=https://example.com
I hope you know the impact of open redirect and more info refer

## Impact

User can be redirect to malicious site.

</details>

---
*Analysed by Claude on 2026-05-24*
