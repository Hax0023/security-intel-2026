# Open Redirect in Social Authentication Login Flow

## Metadata
- **Source:** HackerOne
- **Report:** 223718 | https://hackerone.com/reports/223718
- **Submitted:** 2017-04-25
- **Reporter:** rajauzairabdullah
- **Program:** Weblate (hosted.weblate.org)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Insufficient Input Validation, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple social authentication endpoints (Facebook, Google, GitHub, Bitbucket, GitLab) on Weblate are vulnerable to open redirect attacks via the 'next' parameter. An attacker can craft malicious URLs that redirect authenticated users to arbitrary external sites after login completion. The vulnerability affects all five social login providers using the same unvalidated 'next' parameter.

## Attack scenario
1. Attacker crafts a malicious URL such as 'https://hosted.weblate.org/accounts/login/facebook/?next=///evil.com'
2. Attacker sends this link to victim via phishing email, social media, or other channels
3. Victim clicks the link and is redirected to legitimate Weblate login page authenticated by Facebook
4. After successful Facebook authentication, victim is automatically redirected to 'evil.com'
5. Victim, trusting the initial weblate.org domain, may not notice the domain change and enter credentials or download malware
6. Attacker gains access to victim's sensitive data or can perform further attacks from the compromised trust relationship

## Root cause
The 'next' parameter used for post-login redirection is not properly validated before use. The application likely uses a simple string comparison or regex that can be bypassed using protocol-relative URLs (///) or other URL encoding techniques instead of implementing whitelist-based validation or ensuring redirects stay within the application domain.

## Attacker mindset
An attacker recognizes that authentication endpoints are high-value targets for social engineering. By leveraging legitimate login flows, they can maintain the appearance of legitimacy while redirecting users to malicious sites. The multi-provider vulnerability increases attack surface and allows targeting users regardless of their preferred authentication method. This is a low-effort, high-impact phishing vector.

## Defensive takeaways
- Implement strict whitelist-based validation for redirect parameters - only allow relative URLs or URLs matching expected domains
- Validate the 'next' parameter against a list of allowed redirect destinations before performing the redirect
- Use URL parsing libraries to properly parse and validate URLs, avoiding simple string matching
- Reject any redirect URLs containing protocol indicators (//, ://, etc.) or absolute URLs to external domains
- Log and monitor redirect parameters for suspicious patterns indicating exploitation attempts
- Implement Content Security Policy headers to restrict redirect destinations
- Ensure all social authentication providers apply the same validation logic consistently
- Use framework-built-in redirect validation functions rather than custom implementations

## Variant hunting
Search for similar 'next', 'redirect', 'return', 'returnUrl', 'callback', 'goto' parameters across all authentication endpoints. Check OAuth callback URLs, password reset flows, email verification links, and any URL-based navigation parameters. Test with protocol-relative URLs (//evil.com), backslash variations (\\evil.com), unicode encoding, double encoding, and mixed case domain variations.

## MITRE ATT&CK
- T1598.003
- T1598
- T1566.002
- T1566
- T1187

## Notes
This is a classic open redirect vulnerability pattern commonly found in authentication workflows. The use of triple slashes (///) is a known bypass technique for URL validation. The presence of the vulnerability across all five authentication providers suggests framework-level weakness rather than endpoint-specific issues. Weblate uses Django-based authentication, so the fix likely involves using Django's built-in URL validation utilities rather than custom implementations.

## Full report
<details><summary>Expand</summary>

Weak **Authentication** Leads to the **Open redirection** to **_Malicios Sites_** :

### Signing in via Facebook :
+ https://hosted.weblate.org/accounts/login/facebook/?next=///evil.com

### Signing in via Gmail :
+ https://hosted.weblate.org/accounts/login/google-oauth2/?next=///evil.com

### Signing in via Github:

+ https://hosted.weblate.org/accounts/login/github/?next=///evil.com

### Signing in via Bitbucket:

+ https://hosted.weblate.org/accounts/login/bitbucket/?next=///evil.com

### Signing in via Gitlab:

+ https://hosted.weblate.org/accounts/login/gitlab/?next=///evil.com

### Vulnarable Parameter: 

**" next  "**

Greets
**Raja Uzair Abdullah**

</details>

---
*Analysed by Claude on 2026-05-24*
