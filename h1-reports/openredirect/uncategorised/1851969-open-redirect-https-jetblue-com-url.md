# Open Redirect Vulnerability in JetBlue Redirect Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1851969 | https://hackerone.com/reports/1851969
- **Submitted:** 2023-01-30
- **Reporter:** theendisnear
- **Program:** JetBlue Airways (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
A JetBlue subdomain contains an unvalidated redirect parameter that allows attackers to redirect users to arbitrary external URLs. By crafting a malicious link with a url parameter pointing to an attacker-controlled domain, users can be redirected away from JetBlue to phishing or malicious sites.

## Attack scenario
1. Attacker identifies JetBlue subdomain with redirect functionality accepting url parameter
2. Attacker crafts malicious URL: https://[jetblue-subdomain]/[path]?url=http://malicious-site.com
3. Attacker sends crafted link via phishing email or social engineering to JetBlue users
4. Victim clicks link believing it originates from JetBlue domain
5. User is silently redirected to attacker's malicious domain (credential harvesting, malware distribution)
6. Victim may be unaware they've left JetBlue domain due to initial legitimate domain in URL bar

## Root cause
The redirect parameter is not properly validated or whitelisted before being used in a redirect operation. The application fails to enforce a whitelist of allowed redirect destinations or validate that URLs stay within JetBlue's domain.

## Attacker mindset
Leveraging trusted brand authority to conduct phishing attacks. Since the initial URL appears legitimate (jetblue.com), users are more likely to trust the redirect and enter credentials on the destination site. Useful for credential harvesting, credential stuffing, or malware distribution while maintaining social engineering plausibility.

## Defensive takeaways
- Implement URL whitelisting - only allow redirects to approved internal domains
- Validate redirect destinations using URL parsing; reject any non-JetBlue domains
- Use allowlist pattern matching (e.g., only allow *.jetblue.com domains)
- Implement a redirect confirmation page warning users they're leaving the site
- Use relative URLs and avoid accepting external URLs in redirect parameters
- Implement Content Security Policy (CSP) headers to restrict navigation
- Conduct security code review of all redirect implementations across application
- Add automated testing for open redirect patterns in URL parameters

## Variant hunting
Search for similar redirect parameters across JetBlue ecosystem: redirect_url, return_url, target, destination, goto, link, forward_url, next, continue, ref, referrer. Test mobile apps, different subdomains (checkout, mobile, api), and POST-based redirects. Check for double-encoding bypass (url=%25http) and protocol bypass attempts (javascript:, data:).

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1598.001 - Phishing: Malicious Link

## Notes
Report appears minimal with limited technical detail - only describes basic POC without demonstrating impact chain. URL parameter name and vulnerable endpoint path are redacted. HackerOne report ID suggests this was accepted and processed by JetBlue security team. Open redirects are often chained with social engineering for maximum effectiveness and can be combined with credential harvesting sites.

## Full report
<details><summary>Expand</summary>

Open the url https://██████████.jetblue.com/████?url=http://www.dakshineswarkalitemple.org/ this as a result we see Open redirect issue

POC video :  ██████

## Impact

Open redirect

</details>

---
*Analysed by Claude on 2026-05-24*
