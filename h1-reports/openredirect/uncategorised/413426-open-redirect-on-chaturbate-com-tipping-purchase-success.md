# Open Redirect on chaturbate.com (tipping/purchase_success)

## Metadata
- **Source:** HackerOne
- **Report:** 413426 | https://hackerone.com/reports/413426
- **Submitted:** 2018-09-24
- **Reporter:** glc
- **Program:** Chaturbate
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirects and Forwards
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the tipping/purchase_success endpoint where the `prejoin_data` parameter is not properly validated, allowing attackers to redirect users to arbitrary external domains. This can be exploited for phishing attacks by making malicious links appear to originate from the trusted chaturbate.com domain.

## Attack scenario
1. Attacker identifies the vulnerable `prejoin_data` parameter on the purchase_success endpoint
2. Attacker crafts a malicious URL with `prejoin_data=domain%2Fmalicious-site.com` and shares it via email, social media, or messaging
3. User clicks the link, trusting it because it originates from chaturbate.com
4. Server processes the request and redirects the user to attacker's malicious domain
5. User lands on attacker's phishing page that mimics Chaturbate login or payment form
6. Attacker captures user credentials or sensitive information (payment details, account credentials)

## Root cause
The `prejoin_data` parameter is passed directly to a redirect function without proper validation or sanitization. The application fails to implement whitelist-based validation to ensure redirects only go to trusted internal domains or an explicit list of approved external destinations.

## Attacker mindset
Leverage the trusted domain reputation of Chaturbate to conduct sophisticated phishing attacks. The legitimate-looking URL structure increases likelihood of user trust, making it effective for credential harvesting or financial fraud targeting the platform's user base.

## Defensive takeaways
- Implement whitelist-based redirect validation - only allow redirects to pre-approved internal URLs or trusted domains
- Validate redirect parameters against a strict pattern (e.g., must be relative URLs starting with /)
- Use URL parsing libraries to properly parse and validate redirect destinations
- Implement HTTP security headers like X-Frame-Options to prevent clickjacking on redirect pages
- Log and monitor redirect patterns for unusual activity
- Use Safe Redirect patterns that require explicit acknowledgment from users when redirecting to external domains
- Conduct code review of all endpoints that handle user-supplied redirect parameters

## Variant hunting
Search for other parameters ending in '_url', '_redirect', '_target', '_goto', '_return' on payment/checkout pages
Test all GET/POST parameters on sensitive endpoints (login, registration, payment flows) for redirect functionality
Check for similar issues on related endpoints: `/tipping/`, `/purchase/`, `/checkout/`
Test parameter encoding variations (URL encoding, double encoding, unicode escapes, base64)
Look for similar patterns in other adult content platforms with payment systems
Test 'success_url', 'failure_url', 'return_url' parameters commonly found in payment processors

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1598.002

## Notes
Report demonstrates clear understanding of impact through phishing vector. Researcher provided straightforward PoC. The IP address (64.38.230.2) in the example suggests this may be a staging/testing environment. Chaturbate's payment success page is a high-value target for phishing as users are in transaction completion mindset and may be less skeptical. The vulnerability is relatively easy to exploit but requires user interaction (clicking link), limiting autonomous exploitation potential.

## Full report
<details><summary>Expand</summary>

Hi,

I would like to report an open redirect issue on `https://chaturbate.com/`


## Description

An attacker can redirect a user to any external website using the parameter `prejoin_data`, this parameter seems to miss sanitization.


## Steps to Reproduce

Visit the following url:
https://64.38.230.2/tipping/purchase_success/?product_code=4137&prejoin_data=domain%2Fpoc.10degres.net
This will redirect you to my website `http://poc.10degres.net`

**Browsers Verified In:**
* Firefox 56.0, Ubuntu 16.04


## PoC

{F350390}

## Impact

By modifying untrusted URL input to a malicious site, an attacker may successfully launch a phishing scam and steal user credentials. Because the server name in the modified link is identical to the original site, phishing attempts may have a more trustworthy appearance.


## Remediation

Use a whitelist approach to allow redirection to trusted domains.


## See also

https://www.owasp.org/index.php/Unvalidated_Redirects_and_Forwards_Cheat_Sheet




Best regards,

Gwen

</details>

---
*Analysed by Claude on 2026-05-24*
