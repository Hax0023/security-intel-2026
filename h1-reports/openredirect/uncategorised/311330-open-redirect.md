# Open Redirect on Semrush redirect parameter

## Metadata
- **Source:** HackerOne
- **Report:** 311330 | https://hackerone.com/reports/311330
- **Submitted:** 2018-02-01
- **Reporter:** ankit_singh
- **Program:** Semrush
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Improper Input Validation, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on Semrush's redirect endpoint that allows attackers to redirect users to arbitrary external URLs through an unvalidated url parameter. An attacker can craft malicious links to redirect unsuspecting users to phishing sites or malware distribution platforms, leveraging Semrush's trusted domain.

## Attack scenario
1. Attacker discovers the /redirect endpoint on semrush.com accepts an unvalidated url parameter
2. Attacker crafts a malicious URL: https://www.semrush.com/redirect?url=http://attacker-phishing-site.com
3. Attacker distributes the URL via email, social media, or embeds it in phishing campaigns, masking it as legitimate Semrush traffic
4. Victims click the link believing it originates from trusted Semrush domain
5. Users are silently redirected to attacker-controlled malicious site where credentials or sensitive data can be harvested
6. Attacker leverages Semrush's reputation to increase phishing success rates

## Root cause
The /redirect endpoint fails to validate or whitelist the destination URL before performing the redirect. The application accepts arbitrary external URLs without implementing server-side validation, allowlist checking, or protocol restrictions.

## Attacker mindset
An attacker seeks to abuse the trust relationship users have with Semrush. By leveraging the legitimate domain in URLs, they can bypass email filters, security gateways, and user suspicion. This is a classic social engineering vector amplified by domain authority.

## Defensive takeaways
- Implement strict URL validation and whitelist approved redirect destinations
- Use relative URLs or validate against a whitelist of internal paths only
- Enforce HTTPS-only redirects and validate protocol schemes explicitly
- Avoid user-controlled redirect parameters entirely; use opaque identifiers mapped to pre-approved URLs
- Implement Content Security Policy (CSP) headers to prevent unwanted redirects
- Log and monitor redirect requests for anomalies and abuse patterns
- Educate users about verifying URLs in the address bar regardless of referrer

## Variant hunting
Search for other redirect endpoints: /go, /out, /exit, /leave, /external, /link
Test redirect parameters with different names: redirect_url, return_url, next, continue, target, destination
Check for encoded variations: base64, URL-encoded, double-encoded payloads
Test protocol bypass techniques: javascript://, data://, vbscript://
Look for similar patterns across subdomains and partner properties
Test chained redirects and open redirect chains across multiple endpoints

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1204.001

## Notes
This is a straightforward but impactful vulnerability. The PoC is minimal and clearly demonstrates the issue. While individual impact may be medium, the vulnerability's effectiveness in phishing campaigns and credential harvesting at scale makes it a legitimate security concern. The report lacks specific remediation details and bounty information, but the vulnerability is well-documented through CWE references.

## Full report
<details><summary>Expand</summary>

Open Redirect on  https://www.semrush.com/

User can be redirect to malicious site 
POC:  https://www.semrush.com/redirect?url=http://bing.com

I hope you know the impact of open redirect and more info refer

https://cwe.mitre.org/data/definitions/601.html

## Impact

User can be redirect to malicious site.

</details>

---
*Analysed by Claude on 2026-05-24*
