# Open Redirect Via X-Forwarded-Host Header

## Metadata
- **Source:** HackerOne
- **Report:** 1479889 | https://hackerone.com/reports/1479889
- **Submitted:** 2022-02-13
- **Reporter:** ndizon_
- **Program:** Omise
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Host Header Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in https://link.omise.co due to improper handling of the X-Forwarded-Host header. An attacker can inject a malicious domain via this header to redirect users to arbitrary external websites, enabling phishing and credential theft attacks.

## Attack scenario
1. Attacker crafts a request to https://link.omise.co with X-Forwarded-Host: attacker.com header injected
2. The application processes the X-Forwarded-Host header and uses it to construct redirect URLs instead of using the legitimate Host header
3. Attacker sends victim a crafted URL or intercepts legitimate traffic to inject the malicious header
4. Victim's browser receives a redirect response pointing to attacker.com with the same URL path structure
5. User is redirected to attacker's domain which mimics the legitimate Omise site for credential harvesting
6. Attacker captures sensitive information such as login credentials or session tokens

## Root cause
The application trusts the X-Forwarded-Host header without proper validation when constructing redirect URLs. This header is commonly used by reverse proxies and load balancers, but the application failed to validate it against a whitelist of trusted hosts or implement proper canonicalization of URLs before using them in redirects.

## Attacker mindset
An attacker would leverage this to create convincing phishing campaigns by redirecting users from legitimate Omise domains to lookalike attacker-controlled sites. The attack is low-effort with high impact since users trust the initial domain.

## Defensive takeaways
- Never blindly trust the X-Forwarded-Host header; validate it against a whitelist of known legitimate hosts
- Prefer using the standard Host header for redirect decisions; only use X-Forwarded-Host when explicitly needed and in controlled proxy environments
- Implement strict URL validation and canonicalization before using any user-influenced input in redirects
- Use relative redirects instead of absolute redirects when possible to prevent host injection
- Configure proxy headers only on trusted reverse proxies and strip them at the edge if not expected
- Log and monitor unusual Host/X-Forwarded-Host mismatches as potential attack indicators

## Variant hunting
Search for similar patterns in other Omise subdomains (.co, .io, .co.th); check for other proxy headers like X-Forwarded-Proto, X-Original-Host being misused; test redirect endpoints across dashboard, admin, api subdomains; investigate if Content-Security-Policy or Referer headers reveal redirect patterns

## MITRE ATT&CK
- T1598.003
- T1598.002
- T1583.005
- T1566.002

## Notes
The researcher discovered this vulnerability on February 8, 2022 and reported it twice (reports 1470535 and 1479889) due to lack of initial response. The duplicate report suggests potential triage/response issues. The vulnerability is straightforward to exploit and has clear phishing/social engineering implications. X-Forwarded-Host header injection is a known attack vector that should be part of standard security testing for any application behind a reverse proxy.

## Full report
<details><summary>Expand</summary>

## Summary:
I have found this bug since feb. 8,2022, when my open redirect in https://dashboard.omise.co got duplicated
here where I first bug report my bug( https://hackerone.com/reports/1470535 ) since nobody response that's why I made new report for it.

## Steps To Reproduce:
[add details for how we can reproduce the 
  1. Open https://link.omise.co
  2. Capture the request of the site
  3.  Add this `X-Forwarded-Host: example.com` below Host
  4. Now you will get redirected in the site

## Supporting Material/References:


  * [attachment / reference]

## Impact

An attacker can use this to make the user go to malicious website.

</details>

---
*Analysed by Claude on 2026-05-24*
