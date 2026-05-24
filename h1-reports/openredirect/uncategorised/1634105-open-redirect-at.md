# Open Redirect Vulnerability in Search Redirect Handler

## Metadata
- **Source:** HackerOne
- **Report:** 1634105 | https://hackerone.com/reports/1634105
- **Submitted:** 2022-07-12
- **Reporter:** angeltsvetkov
- **Program:** Unknown
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, CWE-601: URL Redirection to Untrusted Site
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the redir.html endpoint where the 'u' parameter is not validated before redirecting users. An attacker can craft malicious URLs to redirect users to arbitrary external sites, potentially for phishing, malware distribution, or credential harvesting attacks.

## Attack scenario
1. Attacker identifies the vulnerable redir.html endpoint and discovers the unsanitized 'u' parameter
2. Attacker crafts a malicious URL with u=http://attacker-controlled-domain.com pointing to a phishing site
3. Attacker embeds this URL in a phishing email or social media post, disguising it as a legitimate search result redirect from the trusted domain
4. User clicks the link trusting the original domain, but is silently redirected to the attacker's malicious site
5. User provides credentials or downloads malware believing they are on the legitimate platform
6. Attacker gains unauthorized access to user accounts or compromises user systems

## Root cause
The redir.html endpoint accepts a user-controlled 'u' parameter and performs an HTTP redirect without validating or sanitizing the URL destination. There is no whitelist of allowed domains, URL scheme validation, or relative URL enforcement.

## Attacker mindset
An attacker would exploit this for credential harvesting campaigns by creating convincing phishing pages. They could also use it for malware distribution or as part of a watering hole attack. The trust in the legitimate domain makes users more likely to click and trust the redirect destination.

## Defensive takeaways
- Implement strict URL validation: only allow redirects to whitelisted internal domains or enforce relative URLs
- Validate URL scheme to prevent javascript: and data: URIs
- Use a redirect allowlist approach rather than blacklist
- Implement Content Security Policy (CSP) headers to prevent unauthorized redirects
- Log all redirect attempts for security monitoring and anomaly detection
- Use security headers like X-Frame-Options and X-Content-Type-Options
- Educate users about URL spoofing and verify domain names before entering credentials
- Consider using canonical links and server-side session tokens for redirect validation

## Variant hunting
Search for other 'redir' or 'redirect' endpoints across the application and subdomains
Test similar parameter names: 'url', 'return', 'returnUrl', 'redirect', 'next', 'goto', 'continue'
Check for encoded bypass variants: %00, double encoding, Unicode encoding, case variation
Test with different URL schemes: javascript:, data:, file://, and protocol-relative URLs //
Look for parameter pollution attacks combining multiple redirect parameters
Test on different endpoints (logout, login flows, password reset)
Check for stored open redirects in user profiles or settings

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1598.001 - Phishing: Spearphishing Attachment
- T1608.005 - Stage Capabilities: Link Target
- T1583.001 - Acquire Infrastructure: Domains

## Notes
Report lacks critical details: program name, bounty amount, affected system host, and suggested remediation are redacted or missing. The POC is clear but the report could be strengthened with: severity justification, business impact assessment, screenshots, actual exploitation evidence, and specific remediation code examples. The vulnerability is straightforward and low-effort to validate, suggesting it may have been overlooked during development code review or security testing.

## Full report
<details><summary>Expand</summary>

Open Redirect on https://███

User can be redirect to malicious site
POC: ████████/texis/search/redir.html?query=1234&pr=External+Meta&prox=page&rorder=500&rprox=500&rdfreq=500&rwfreq=250&rlead=500&rdepth=62&sufs=3&order=r&u=http://evil.com&m=0&p=2

I hope you know the impact of open redirect and more info refer

https://cwe.mitre.org/data/definitions/601.html

## Impact

User can be redirect to malicious site.

## System Host(s)
███████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Just open:  █████/texis/search/redir.html?query=1234&pr=External+Meta&prox=page&rorder=500&rprox=500&rdfreq=500&rwfreq=250&rlead=500&rdepth=62&sufs=3&order=r&u=http://evil.com&m=0&p=2

Vulnerable parameter: u=

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
