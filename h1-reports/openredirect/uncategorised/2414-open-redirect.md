# Open Redirect via retURL Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2414 | https://hackerone.com/reports/2414
- **Submitted:** 2014-02-28
- **Reporter:** niks
- **Program:** RelateIQ
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
The sign-up endpoint at relateiq.com/sign-up contains an unvalidated redirect vulnerability in the 'retURL' parameter. An attacker can modify this parameter to redirect users to arbitrary external URLs after form submission, enabling phishing and credential theft attacks.

## Attack scenario
1. Attacker identifies the sign-up flow at https://www.relateiq.com/sign-up contains a 'retURL' redirect parameter
2. Attacker crafts a malicious URL pointing to a phishing site and sets retURL parameter to redirect there
3. Attacker tricks victim into clicking a link to the legitimate sign-up page with malicious retURL parameter
4. Victim completes the sign-up form and submits the request
5. Application processes the request and redirects victim to attacker-controlled phishing URL
6. Victim is deceived into entering credentials or sensitive information on the phishing page

## Root cause
The application fails to validate the 'retURL' parameter against a whitelist of allowed redirect destinations. The parameter is directly used in a redirect response without proper sanitization or domain validation, allowing arbitrary external URLs.

## Attacker mindset
An attacker leverages the trust users place in legitimate sign-up flows to redirect them to phishing pages. By embedding the redirect in the legitimate registration process, the attack appears credible and users are less likely to notice the domain change, making it effective for credential harvesting.

## Defensive takeaways
- Implement strict whitelist validation for all redirect parameters, only allowing known internal URLs or approved domains
- Use relative URLs instead of absolute URLs where possible to prevent external redirects
- Validate redirect destinations against a hardcoded list of safe URLs before performing the redirect
- Implement Content Security Policy (CSP) headers to restrict redirect targets
- Log and monitor redirect activities for suspicious patterns
- Use framework-provided redirect functions that include built-in validation
- Educate users to verify URLs before and after redirect operations

## Variant hunting
Search for other parameters with similar names (returnUrl, redirect, url, next, continue, target, destination)
Test all authentication flows (login, password reset, logout, OAuth callbacks) for redirect parameters
Check for multiple redirect parameters that can be chained or bypassed
Test URL encoding bypasses (e.g., //google.com, /\google.com, javascript: protocol)
Examine API endpoints that may accept redirect parameters in POST/JSON bodies
Look for regex-based validation that can be bypassed with encoded characters or protocol handlers

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (leveraging trusted domain with redirect)
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1056 - Phishing for Information

## Notes
This is a classic open redirect vulnerability. While often considered low severity due to requiring user interaction, it significantly amplifies phishing attacks by using legitimate domains as redirect sources, increasing success rates. The vulnerability is straightforward to exploit and patch, making it a good candidate for bug bounty programs.

## Full report
<details><summary>Expand</summary>

1. go to https://www.relateiq.com/sign-up
2. Fill the form and click on signup free button.
3. Intercept the request using tamper data and change the 'retURL' parameter to any value like https://google.com (any evil url) and submit the request.
4. The web app redirect to any evil website.

</details>

---
*Analysed by Claude on 2026-05-24*
