# Open Redirect via redirect_to Parameter in tumblr.com

## Metadata
- **Source:** HackerOne
- **Report:** 2812583 | https://hackerone.com/reports/2812583
- **Submitted:** 2024-10-30
- **Reporter:** shivangmauryaa
- **Program:** Tumblr (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, URL Redirection to Untrusted Site
- **CVEs:** None
- **Category:** uncategorised

## Summary
Tumblr's logout endpoint fails to properly validate the redirect_to parameter, allowing attackers to redirect authenticated users to arbitrary external domains. The vulnerability can be exploited using a backslash bypass technique to evade URL validation checks, enabling phishing and malware distribution attacks.

## Attack scenario
1. Attacker crafts a malicious URL with redirect_to parameter pointing to attacker-controlled domain using backslash bypass
2. Attacker tricks user into clicking the logout link (via phishing email, social media, etc.)
3. User visits https://www.tumblr.com/logout?redirect_to=https://evil.com%5C%40www.tumblr.com
4. Tumblr's redirect validation is bypassed due to improper parsing of the backslash character
5. User is redirected to attacker's domain (evil.com) after logout
6. Attacker's phishing page mimics Tumblr login to harvest credentials or distributes malware

## Root cause
Insufficient input validation on the redirect_to parameter in the logout endpoint. The application likely uses a validation scheme that does not properly handle URL encoding bypass techniques, specifically the backslash (%5C) character which can be interpreted differently across parsing layers.

## Attacker mindset
Leverage trust established between user and legitimate Tumblr domain to conduct credential harvesting or malware distribution. The logout context is particularly effective as users may be less suspicious when redirected during session termination.

## Defensive takeaways
- Implement strict whitelist-based validation for redirect URLs (only allow internal paths or pre-approved domains)
- Use URL parsing libraries consistently across all validation layers to prevent encoding bypasses
- Validate redirect_to parameter against a list of safe destinations rather than blacklisting dangerous patterns
- Ensure redirect validation occurs on the server-side and cannot be bypassed through encoding tricks (URL-decode before validation)
- Implement Content-Security-Policy headers to prevent redirects to untrusted origins
- Add user warning/confirmation page for external redirects instead of silent redirects
- Test redirect handling with various encoding techniques (double encoding, backslash, null bytes, etc.)

## Variant hunting
Check other endpoints with redirect parameters (login, password reset, OAuth callbacks)
Test alternative encoding bypass techniques: double URL encoding, Unicode encoding, mixed case protocols
Examine other redirect parameters by name: return_to, next, goto, url, continue, returnUrl
Test protocol-relative URLs (//evil.com) and data URIs
Check if redirect validation differs between authenticated and unauthenticated contexts
Test with different character encodings and BOM markers
Verify if backslash is properly handled in redirect context across different browsers

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1598.002 - Phishing: Spearphishing Attachment
- T1566 - Phishing
- T1071 - Application Layer Protocol

## Notes
The use of backslash (%5C) followed by @-symbol is a known URL parsing bypass technique that exploits differences between RFC specifications and browser implementations. The vulnerability is particularly impactful on logout pages since users naturally expect to be redirected away from the application. No bounty amount was disclosed in the report submission.

## Full report
<details><summary>Expand</summary>

## Summary:
URL redirection is sometimes used as a part of phishing attacks that confuse visitors about which web site they are visiting.

## Platform(s) Affected:
Website 

## Steps To Reproduce:
1. open any browser 
2. enter https://www.tumblr.com/logout?redirect_to=https://evil.com%5C%40www.tumblr.com

## Supporting Material/References:
video attached

## Impact

A remote attacker can redirect users from your website to a specified URL. This problem may assist an attacker to conduct phishing attacks, trojan distribution, spammers.

</details>

---
*Analysed by Claude on 2026-05-24*
