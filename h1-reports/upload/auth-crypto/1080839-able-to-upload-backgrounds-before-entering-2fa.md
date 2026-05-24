# Ability to Upload and Access Custom Backgrounds Before 2FA Completion

## Metadata
- **Source:** HackerOne
- **Report:** 1080839 | https://hackerone.com/reports/1080839
- **Submitted:** 2021-01-18
- **Reporter:** mr_vrush
- **Program:** CS.Money
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Authentication Bypass, Broken Authentication, Session Management Flaw, Authorization Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can upload and access custom backgrounds on the 3d.cs.money subdomain without completing two-factor authentication, despite 2FA being enabled on the account. The vulnerability allows authenticated session access to protected features before the second authentication factor is verified, violating the multi-factor authentication security model.

## Attack scenario
1. Attacker compromises or obtains credentials for a Prime subscriber account with 2FA enabled
2. Attacker logs in with the compromised credentials and receives a 2FA prompt
3. Instead of entering the 2FA code, attacker navigates directly to 3d.cs.money subdomain
4. Attacker discovers they can upload custom backgrounds using Ctrl+V keyboard shortcut despite incomplete authentication
5. Attacker accesses previously uploaded backgrounds, confirming full feature access without 2FA completion
6. Attacker can modify account settings or content while 2FA barrier remains bypassed

## Root cause
The subdomain (3d.cs.money) does not properly enforce 2FA verification before granting access to protected features. The application establishes a session upon initial login credentials validation but grants feature access before the secondary authentication factor is validated. Session tokens or cookies are issued without requiring 2FA completion, and the background upload/viewing functionality lacks a 2FA verification check.

## Attacker mindset
An attacker would recognize that session establishment and authentication completion are treated as separate steps, with the application prematurely granting access. The attacker focuses on accessing subdomains that may have weaker authentication controls and tests whether session cookies alone grant feature access before 2FA is satisfied.

## Defensive takeaways
- Implement 2FA verification checks at the application entry point, not just at login - block all authenticated endpoints until 2FA is completed
- Use separate session states: 'partially_authenticated' (pre-2FA) and 'fully_authenticated' (post-2FA) with appropriate access controls for each
- Enforce 2FA verification on all subdomains and cross-origin requests uniformly; avoid relying on domain-level controls alone
- Implement middleware that validates 2FA completion status on every request to protected resources
- Clear sensitive session data and issue new session tokens only after successful 2FA completion
- Add audit logging for all feature access attempts during incomplete authentication states
- Implement rate limiting and alerting on suspicious access patterns during 2FA-pending sessions
- Conduct security review of all subdomains to ensure consistent authentication enforcement

## Variant hunting
Test access to other premium features (inventory, trading, profile editing) during 2FA-pending state
Attempt API calls directly to background upload endpoints with pre-2FA session tokens
Check if WebSocket connections or real-time features bypass 2FA verification
Test whether clearing specific cookies related to 2FA verification allows feature access
Investigate if direct navigation to API endpoints bypasses UI-level 2FA checks
Check if account modification endpoints (password change, email update) are accessible pre-2FA
Test mobile app or alternative client implementations for similar 2FA bypass patterns
Verify whether session fixation or token manipulation can extend pre-2FA access

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1556: Modify Authentication Process
- T1550: Use Alternate Authentication Material
- T1078: Valid Accounts

## Notes
This is a second report on the same issue (references #993786), indicating the vulnerability may not have been fully remediated from a previous disclosure. The vulnerability is particularly concerning for premium/Prime subscribers as it allows unauthorized access to paid features. The use of keyboard shortcuts (Ctrl+V) for uploads suggests client-side feature availability without server-side authentication verification. This is a straightforward authentication bypass that could be exploited with any compromised Prime account credentials, making credential stuffing or phishing attacks on Prime users particularly valuable to attackers.

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
