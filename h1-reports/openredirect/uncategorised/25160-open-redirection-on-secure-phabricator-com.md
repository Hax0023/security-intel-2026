# Open Redirection on secure.phabricator.com

## Metadata
- **Source:** HackerOne
- **Report:** 25160 | https://hackerone.com/reports/25160
- **Submitted:** 2014-08-18
- **Reporter:** anandpingsafe
- **Program:** Phabricator
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Open Redirect, Token Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirection vulnerability exists on secure.phabricator.com that allows attackers to redirect users to malicious websites. The vulnerability can be exploited to steal Disqus access tokens during the OAuth flow, though Facebook tokens are protected by additional security measures.

## Attack scenario
1. Attacker crafts a malicious URL on secure.phabricator.com with an open redirect parameter pointing to attacker-controlled domain
2. Attacker sends link to victim via phishing email or social engineering
3. Victim clicks link and is redirected through legitimate Phabricator domain, appearing trustworthy
4. Victim is redirected to attacker's website during OAuth callback from Disqus
5. Attacker's website captures the Disqus access token from the redirect URL
6. Attacker uses stolen token to impersonate victim or access Disqus account

## Root cause
Insufficient validation of redirect URL parameters in the OAuth callback handler. The application does not properly validate that redirect destinations are on the same origin or in a whitelist before performing the redirect.

## Attacker mindset
Social engineering and credential theft. The attacker aims to leverage user trust in Phabricator's legitimate domain to intercept OAuth tokens during authentication flows, enabling account takeover.

## Defensive takeaways
- Implement strict whitelist-based URL validation for all redirect parameters
- Use relative URL redirects instead of absolute URLs when possible
- Validate that redirect URLs belong to same origin or pre-approved domains
- Implement URL parsing safely to prevent bypasses (e.g., protocol-relative URLs, unicode encoding)
- Log and monitor suspicious redirect attempts
- Consider using HTTP 307/308 instead of 302 to prevent downgrade attacks
- Implement Content-Security-Policy headers to restrict redirect destinations

## Variant hunting
Check all OAuth callback handlers (Facebook, GitHub, Google, etc.) for similar redirect validation issues
Test other authentication-related redirect parameters
Search for any user-controllable parameters in redirect chains
Test for filter bypass techniques: double encoding, case variation, protocol schemes (javascript:, data:)
Check for reflected open redirects in error pages and password reset flows

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1188 - Man in the Middle
- T1539 - Steal Web Session Cookie
- T1056.004 - Phishing for Information

## Notes
The vulnerability specifically affects Disqus token exposure but not Facebook tokens, suggesting Facebook may have implemented additional protections like CSRF tokens or stricter redirect validation. The POC is referenced as a video but not fully detailed in the text. This is a classic open redirect vulnerability combined with OAuth token exposure.

## Full report
<details><summary>Expand</summary>

Hi,

It is possible to redirect users to malicious websites and steal their Disqus access token (not possible in case of Facebook).

Please have a look at POC video: 
https://www.dropbox.com/s/41qm7lbj6rg53td/phabricator.mov

Please fix this and let me know if you need any information.  It would be great if you can please copy the vulnerable link from the video.

Best Regards,
Anand Prakash


</details>

---
*Analysed by Claude on 2026-05-24*
