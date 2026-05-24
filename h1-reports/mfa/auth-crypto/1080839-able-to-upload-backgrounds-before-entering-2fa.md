# Unauthorized Background Upload and Access Before 2FA Completion

## Metadata
- **Source:** HackerOne
- **Report:** 1080839 | https://hackerone.com/reports/1080839
- **Submitted:** 2021-01-18
- **Reporter:** mr_vrush
- **Program:** CS.Money (csgo/cs2 trading platform)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authentication Bypass, Broken Authentication, Premature Session Access, Insufficient Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Users can upload and view custom backgrounds on the 3d.cs.money subdomain before completing 2FA authentication, allowing unauthorized access to premium features. The application grants access to protected functionality immediately after password login without waiting for 2FA verification completion. This authentication bypass affects Prime subscriber-exclusive features and previously uploaded content.

## Attack scenario
1. Attacker logs into victim's account with valid credentials on primary domain
2. During login flow, attacker skips or dismisses 2FA prompt without entering code
3. Attacker navigates to 3d.cs.money subdomain which does not enforce 2FA re-authentication
4. Attacker accesses Prime-exclusive background upload feature via Ctrl+V shortcut
5. Attacker successfully uploads malicious or unauthorized custom backgrounds
6. Attacker views previously uploaded backgrounds, confirming unauthorized access to premium account features

## Root cause
The 3d.cs.money subdomain implements independent or insufficient authentication verification that does not validate 2FA completion status. Session tokens are likely issued after password authentication without conditional gates based on 2FA completion. The subdomain may not properly validate authentication state or may trust parent domain session cookies without re-checking 2FA requirements.

## Attacker mindset
An attacker with credentials (through phishing, credential stuffing, or social engineering) can bypass multi-factor authentication by exploiting cross-subdomain session management weaknesses. They can access restricted premium features and manipulate user content without completing the full authentication challenge, creating both immediate and downstream account compromise risks.

## Defensive takeaways
- Implement 2FA completion verification before granting access to any protected subdomains or resources
- Use explicit authentication tokens that include 2FA verification status rather than relying on session cookies alone
- Enforce 2FA challenges at subdomain boundaries when subdomains handle sensitive operations
- Require re-authentication for premium/restricted features regardless of existing sessions
- Implement server-side session state validation that verifies 2FA completion for each protected endpoint
- Add monitoring and alerts for authentication state mismatches or incomplete 2FA flows
- Use HTTP-only, secure, SameSite cookies with domain-specific scoping to prevent cross-subdomain session reuse

## Variant hunting
Check other subdomains (api.cs.money, inventory.cs.money, etc.) for similar 2FA bypass vulnerabilities
Test uploading other user content types (profiles, avatars, trade settings) before 2FA completion
Attempt to access account settings, billing, or withdrawal features before 2FA verification
Check if user-specific data (trade history, wallets) is accessible on secondary domains post-password-auth
Test with fresh sessions after password change but before 2FA to identify session lifecycle issues
Examine API endpoints called by 3d.cs.money for 2FA state validation in headers/parameters
Test alternative authentication flows (OAuth, SSO) for similar incomplete verification bypasses

## MITRE ATT&CK
- T1190
- T1556
- T1098
- T1199

## Notes
Reporter references previous report #993786 suggesting this may be a re-disclosure of related authentication bypass issues. The reliance on premium subscriber status for exploit confirmation indicates the vulnerability gates access to monetized features. Cross-subdomain authentication handling is a common vulnerability class when applications delegate authentication to parent domains or use shared sessions without proper state validation.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi Team, 
I am able to see and use uploaded backgrounds and able to upload new ones without proper authentication of 2FA. I hope you remember this report #993786.

## Steps To Reproduce:

  1. Login with a steam account and enable 2FA.
  1. Now logout your account. Clear all the cookies.
  1. Now again login into your account now don't enter the 2FA code.
  1. Go to the 3d.cs.money
  1. If you are a Prime subscriber you are able to upload the custom backgrounds by pressing the "ctrl+v" combination. If you have already uploaded some backgrounds you are able to see those too.

## Supporting Material/References:
Please check the attachment F1162263.

## Impact

Able to access subdomain without proper authentication.
It should be accessible after the proper authentication.
Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
