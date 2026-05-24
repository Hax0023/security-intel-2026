# Open Redirection in Login - Korean Starbucks

## Metadata
- **Source:** HackerOne
- **Report:** 380939 | https://hackerone.com/reports/380939
- **Submitted:** 2018-07-12
- **Reporter:** jtjisgod
- **Program:** Starbucks Korea (istarbucks.co.kr)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirection, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Korean Starbucks login page contains an open redirection vulnerability in the redirect_url parameter that allows attackers to redirect authenticated users to arbitrary external domains. An attacker can craft a malicious login link that redirects victims to a phishing site after successful authentication.

## Attack scenario
1. Attacker crafts a malicious URL: https://www.istarbucks.co.kr/login/login.do?redirect_url=//phishing-site.com
2. Attacker sends this URL to victims via email, social media, or advertising
3. Victim clicks the link and arrives at the legitimate Starbucks login page
4. Victim enters their credentials and authenticates successfully
5. Application redirects victim to the attacker's phishing domain without validation
6. Attacker harvests additional credentials or sensitive information from the spoofed site

## Root cause
The application accepts user-supplied redirect_url parameter without proper validation or whitelisting. The parameter is used directly in a redirect without checking if the destination is part of an approved domain list.

## Attacker mindset
An attacker would exploit the trust users have in the legitimate Starbucks domain to conduct phishing attacks. By leveraging the trusted login flow, the attack appears more credible to victims, increasing success rates for credential harvesting or malware distribution.

## Defensive takeaways
- Implement strict whitelist validation for all redirect parameters - only allow redirects to trusted internal URLs or a pre-approved list of domains
- Use relative URLs instead of absolute URLs when possible
- Validate that the redirect URL belongs to the same domain or approved domains before processing
- Implement Content Security Policy (CSP) headers to restrict redirect destinations
- Log and monitor redirect attempts for suspicious patterns
- Use secure redirect libraries that enforce validation automatically
- Educate users about verifying they are on the correct domain after login

## Variant hunting
Check other query parameters for similar redirect functionality (callback, return_url, next, goto, target)
Test other authentication flows: password reset, logout, account recovery pages
Attempt protocol-based bypasses: javascript://, data://, vbscript://
Test encoding variations: %2f%2f, url encoding, double encoding
Check POST parameters and request bodies for hidden redirect mechanisms
Test if redirect validation can be bypassed using whitespace, null bytes, or special characters
Examine other Starbucks regional sites for the same pattern

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1598.002

## Notes
Open redirection vulnerabilities are commonly found in authentication flows and are frequently chained with phishing attacks. The use of protocol-relative URLs (//domain.com) rather than http:// or https:// can sometimes bypass basic validation. This vulnerability is relatively simple to exploit and has high impact when combined with social engineering.

## Full report
<details><summary>Expand</summary>

Summary:
Open Redirection is performed in Korean Starbucks login page.
An attacker can redirect victim to other site such as fishing.

Description:
When victim visit https://www.istarbucks.co.kr/login/login.do?redirect_url=//www.bughunting.net this site, and login, he/she is redirected to www.bughunting.net page.

PoC 
https://www.istarbucks.co.kr/login/login.do?redirect_url=//www.bughunting.net

Etc
I attached a PoC video.

## Impact

Fishing

</details>

---
*Analysed by Claude on 2026-05-24*
