# Open Redirection while saving User account Settings

## Metadata
- **Source:** HackerOne
- **Report:** 288219 | https://hackerone.com/reports/288219
- **Submitted:** 2017-11-07
- **Reporter:** 0xprial
- **Program:** Moneybird
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirection vulnerability exists in the user account settings page where the 'return_to' parameter is not properly validated before redirecting users after saving settings. Attackers can craft malicious URLs to redirect authenticated users to attacker-controlled domains, facilitating phishing attacks and credential harvesting.

## Attack scenario
1. Attacker crafts a malicious URL containing the open redirect: https://moneybird.com/user/edit?return_to=//attacker.com/fake-login
2. Attacker distributes this URL via phishing email or social engineering to target Moneybird users
3. Victim clicks the link while authenticated to Moneybird and lands on the account settings page
4. Victim modifies and saves account settings
5. Application redirects user to attacker's fake login page via the unsanitized return_to parameter
6. Victim re-enters credentials or sensitive information on the attacker-controlled page

## Root cause
The application fails to validate or sanitize the 'return_to' parameter before using it in a redirect operation. The parameter accepts arbitrary URLs (including protocol-relative URLs like //evil.com) without whitelist validation or URL parsing to ensure the redirect target is legitimate.

## Attacker mindset
Leverage the trust users have in the legitimate Moneybird domain to socially engineer them into visiting malicious links. After performing an account-related action (which appears legitimate), redirect to a phishing page while trust is high, increasing likelihood of credential compromise.

## Defensive takeaways
- Implement strict whitelist validation for redirect parameters - only allow relative URLs or known safe domains
- Use URL parsing to validate the scheme and hostname of redirect targets
- Avoid accepting protocol-relative URLs (//example.com) which inherit the attacker's scheme
- Implement a redirect allowlist rather than a blocklist approach
- Add user-visible warning when redirects are about to occur to external domains
- Log all redirect parameters for security monitoring and incident detection
- Use framework-provided safe redirect functions rather than manual URL concatenation

## Variant hunting
Check all authentication flow endpoints (login, logout, password reset, email verification) for similar redirect parameters
Search for other parameter names that might control redirects: redirect_url, next, continue, target, destination, callback, return_url
Test API endpoints that might have JSON redirect responses with similar validation issues
Check OAuth/SSO callback handlers for open redirect vulnerabilities
Test for post-authentication redirect in admin/account management panels
Look for encoded redirect parameters that might bypass filters (URL encoding, base64, etc.)

## MITRE ATT&CK
- T1598.003
- T1598.004
- T1598.001
- T1598

## Notes
This is a classic open redirect vulnerability with high phishing potential. The use of protocol-relative URLs (//evil.com) bypasses basic scheme validation. The vulnerability is in a sensitive area (account settings) post-authentication, making it effective for MitM-style attacks or credential harvesting. The report lacks specific bounty information and remediation confirmation.

## Full report
<details><summary>Expand</summary>

Hi team ,
I got a Open redirection while saving account setting . This could lead to serious issues .

**Endpoint :-** https://moneybird.com/user/edit?return_to=//evil.com

##Reproduce :-
* Visit https://moneybird.com/user/edit?return_to=//evil.com and click on `Save` .
* You will be take to evil.com .

##Impact :-
Attacker can redirect a user to a fake login page easily to get his login and other sensitive infos .

Thanks .

</details>

---
*Analysed by Claude on 2026-05-24*
