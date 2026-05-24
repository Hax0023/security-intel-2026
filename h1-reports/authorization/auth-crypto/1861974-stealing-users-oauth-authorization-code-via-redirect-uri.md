# Stealing Users OAuth Authorization Code via Redirect URI Path Traversal

## Metadata
- **Source:** HackerOne
- **Report:** 1861974 | https://hackerone.com/reports/1861974
- **Submitted:** 2023-02-04
- **Reporter:** kuzu7shiki
- **Program:** Pixiv/Booth
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Path Traversal, OAuth Redirect URI Validation Bypass, Credential Leakage, Insufficient URL Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A path traversal vulnerability in the OAuth redirect_uri parameter allows attackers to bypass redirect validation and redirect authenticated users to attacker-controlled product pages. By leveraging Google Analytics, attackers can capture OAuth authorization codes from query strings, enabling account takeover attacks.

## Attack scenario
1. Attacker creates a public shop on Booth and registers a product with Google Analytics tracking enabled
2. Attacker crafts a malicious OAuth authorization link with path traversal payload in redirect_uri parameter (using ../../../../ traversal)
3. Attacker tricks victim into clicking the malicious link, which initiates OAuth login flow with Pixiv
4. Victim authenticates with their Pixiv credentials and grants permissions
5. OAuth provider redirects victim to attacker's product page with authorization code in query string instead of legitimate callback endpoint
6. Attacker extracts authorization code from Google Analytics real-time reports and exchanges it for access token to hijack victim's account

## Root cause
Insufficient validation of the redirect_uri parameter in OAuth flow. The application failed to properly validate that the redirect_uri resolves to the legitimate callback endpoint and allowed path traversal sequences (../) to bypass URL matching logic, enabling redirects to arbitrary internal paths controlled by attacker-created shop items.

## Attacker mindset
Opportunistic threat actor exploiting OAuth implementation flaws to harvest sensitive authentication credentials. The attacker recognizes that redirect_uri validation is often overlooked and that legitimate-looking product pages serve as credible redirect destinations, especially when combined with analytics tools to passively collect credentials.

## Defensive takeaways
- Implement strict whitelist validation for redirect_uri - compare against registered callback URLs after URL decoding and normalization
- Reject redirect_uri parameters containing path traversal sequences (../, .., %2e%2e, etc.) before validation
- Normalize URLs (decode, resolve relative paths) before validation to prevent encoding bypasses
- Use exact string matching for redirect_uri validation rather than pattern matching
- Never allow redirect_uri to point to user-controlled content (product pages, profile pages, etc.)
- Implement strict Content Security Policy to prevent query string leakage to third-party analytics
- Log and alert on suspicious redirect_uri values including those with path traversal attempts
- Use authorization code rotation and implement short expiration times (60 seconds) for codes
- Educate users to verify they're being redirected to expected callback domains

## Variant hunting
Test other OAuth flows (implicit, hybrid) for similar redirect_uri bypasses
Check if other user-controlled redirect destinations exist (error pages, confirmation pages, user uploads)
Test double-encoding variations (%252e%252e%252f) against normalization
Attempt Unicode normalization bypasses (e.g., %ef%bc%8e for fullwidth period)
Test case sensitivity variations on redirect_uri validation
Check for null byte injection in redirect_uri (%00)
Probe for fragment-based bypasses (#@legitimate.com@attacker.com)
Test backslash escaping (..\ on Windows implementations)
Examine other parameters that might influence redirect behavior (return_to, callback, etc.)
Test with different URL schemes (javascript:, data:, etc.)

## MITRE ATT&CK
- T1190
- T1598
- T1187
- T1556

## Notes
This is a high-impact OAuth vulnerability that combines path traversal with credential theft. The use of Google Analytics as an exfiltration vector is creative and demonstrates how legitimate monitoring tools can be weaponized. The vulnerability is particularly dangerous because it doesn't require victims to notice the redirect to an unexpected domain - product pages appear legitimate. This report highlights the importance of treating redirect_uri as a critical security boundary in OAuth implementations.

## Full report
<details><summary>Expand</summary>

## Summary:
Path traversal in OAuth `redirect_uri` which can lead to users authorization code being leaked to any malicious user.

The following authorization code flow request is generated at booth login.
```
https://oauth.secure.pixiv.net/v2/auth/authorize?client_id=a1Z7w6JssUQkw5Hid0uIDeuesue9&redirect_uri=https%3A%2F%2Fbooth.pm%2Fusers%2Fauth%2Fpixiv%2Fcallback&response_type=code&scope=read-works+read-favorite-users+read-friends+read-profile+read-email+write-profile&state=%3A1a38b53563599621ce25094661b1c4458ddb52d79d771149
```

Path traversal vulnerability in this `redirect_uri` parameter allows the attacker to direct the user to the product page created by the attacker.
```
redirect_uri=https%3A%2F%2Fbooth.pm%2Fusers%2Fauth%2Fpixiv%2Fcallback/../../../../ja/items/4503924
```
-> redirected to https://booth.pm/ja/items/4503924

If the attacker had Google Analytics enabled, the query string could be exposed when the victim is redirected to the product page, so the unused authorization code is leaked.

## Steps To Reproduce:

  1. The attacker makes his shop public. Register his products and set up his Google Analytics tracking ID.
  2. Have the victim click on the following link; the value of the state parameter can be anything.
```
https://oauth.secure.pixiv.net/v2/auth/authorize?client_id=a1Z7w6JssUQkw5Hid0uIDeuesue9&redirect_uri=https%3A%2F%2Fbooth.pm%2Fusers%2Fauth%2Fpixiv%2Fcallback/../../../../ja/items/[attacker's product id]&response_type=code&scope=read-works+read-favorite-users+read-friends+read-profile+read-email+write-profile&state=%3A1a38b53563599621ce25094661b1c4458ddb52d79d771149
```

  3. When the victim clicks on the above link and proceeds with the login process, he is redirected to the attacker's product page.

  4. The attacker can steal victims' authorizaiton code from Google Analytics real-time reports.

## Impact

Due to path traversal in `redirect_uri` parameter in OAuth flow, its possible to redirect authenticated users to attacker's product page with their OAuth credentials from which its possible to takeover their account.

</details>

---
*Analysed by Claude on 2026-05-24*
