# Open Redirect in WordPress Login Redirect Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 765227 | https://hackerone.com/reports/765227
- **Submitted:** 2019-12-27
- **Reporter:** damn007
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Phishing Vector
- **CVEs:** None
- **Category:** uncategorised

## Summary
The WordPress login page's redirect_to parameter accepts arbitrary URLs without proper validation, allowing attackers to redirect authenticated users to malicious sites. An attacker can craft a login link pointing to an external domain, and after a user authenticates, they are redirected without warning, enabling phishing attacks.

## Attack scenario
1. Attacker identifies the redirect_to parameter in wp-login.php accepts unvalidated URLs
2. Attacker URL-encodes a malicious redirect URL (e.g., https://vul-example.com) and crafts a login link: wp-login.php?redirect_to=[encoded_malicious_url]
3. Attacker distributes the crafted link via email, forum posts, or social engineering, making it appear legitimate
4. Victim clicks the link and sees the legitimate WordPress login page, building trust
5. Victim enters credentials and authenticates successfully
6. WordPress redirects victim to attacker's malicious site where credential harvesting, malware, or further social engineering occurs

## Root cause
The redirect_to parameter in wp-login.php lacks URL validation to ensure redirects remain within the WordPress application domain. The parameter is processed without checking if the destination is an external URL.

## Attacker mindset
An attacker leverages the trust users place in legitimate login flows to achieve seamless redirection to phishing sites. By combining a real login page with an unexpected redirect, the attacker exploits cognitive biases where users are less suspicious after successful authentication.

## Defensive takeaways
- Implement whitelist validation for redirect destinations—only allow relative URLs or URLs matching the application domain
- Use URL parsing to extract and validate the host component against allowed domains
- Store approved redirect locations server-side rather than accepting user input
- Add user-visible warnings before redirecting to external domains
- Implement security headers like X-Frame-Options to prevent framing in phishing contexts
- Log and monitor unusual redirect patterns for security analytics
- Educate users to inspect URL bars after login and verify they're on expected domains

## Variant hunting
Check other authentication pages (password reset, account recovery) for similar redirect parameters
Test multisite WordPress installations for cross-site redirect validation bypasses
Look for redirect parameters with different names (return_url, callback, next, back)
Test referer header-based redirects without validation
Check for double-encoding bypasses (redirect_to=%25%32%35... to bypass URL decoding filters)
Test fragment-based redirects (#/../../malicious-site) that might bypass path validation
Examine plugin authentication hooks that might introduce custom redirect logic
Test for Unicode/IDN homograph attacks in redirect validation

## MITRE ATT&CK
- T1598.003
- T1598.004
- T1566.002
- T1589.001

## Notes
This is a classic open redirect vulnerability in an authentication context, making it particularly dangerous for phishing. The requirement to URL-encode the payload suggests some minimal parsing exists but insufficient validation. The vulnerability affects user trust in the login mechanism itself, making it a high-risk social engineering vector despite medium severity classification.

## Full report
<details><summary>Expand</summary>

Steps To Reproduce:
=====================
>1_ visit : [Normal Link](https://iandunn.name/wordpress/wp-login.php?redirect_to=https%3A%2F%2Fiandunn.name%2Fwordpress%2Fwp-admin%2F&reauth=1).
>2_ Sign-in with your wordpress account and you will directed to [This](https://iandunn.name/wordpress/wp-admin/)
>3_Change the value of the **Parameter** : redirect_to .. To the attacker website let's say : (https://vul-example.com)
>4_**NOTE THAT** : you must URL-encode the vulnerable link first

## Impact

**Phishing** attacks to get Users to visit malicious sites without realizing it.

</details>

---
*Analysed by Claude on 2026-05-24*
