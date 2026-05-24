# 2FA Requirement Bypass via Client-Side Response Manipulation During Team Member Invitation

## Metadata
- **Source:** HackerOne
- **Report:** 3356149 | https://hackerone.com/reports/3356149
- **Submitted:** 2025-09-24
- **Reporter:** 0x7ashish
- **Program:** Unknown
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insufficient Server-Side Validation, Client-Side Security Enforcement, Business Logic Flaw, Security Control Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application enforces 2FA requirement for team invitations but only validates this check on the client-side. An attacker can intercept and modify the client-side response (changing a boolean flag from false to true) to bypass the 2FA requirement entirely. This allows unauthorized users to send team invitations without enabling 2FA, circumventing a critical security control.

## Attack scenario
1. Attacker creates account and logs in without enabling 2FA
2. Attacker navigates to Team section and attempts to invite a new member
3. Application blocks the request on client-side with message requiring 2FA
4. Attacker uses Burp Suite Match and Replace to intercept response and modify boolean flag from false to true
5. Attacker refreshes page or resends invitation request with modified response
6. Application processes invitation successfully, bypassing 2FA requirement entirely

## Root cause
Security-critical validation logic (2FA requirement check) is performed exclusively on the client-side rather than being verified server-side. The server trusts the client-provided boolean flag indicating 2FA status without re-validating the actual 2FA state of the user account.

## Attacker mindset
An attacker with basic proxy interception knowledge recognizes that client-side security controls are inherently bypassable. They use simple match-and-replace techniques to flip a boolean value, exploiting trust in client-provided data to circumvent mandatory security controls and gain unauthorized team management capabilities.

## Defensive takeaways
- Always validate security-critical controls on the server-side, never rely solely on client-side enforcement
- Implement server-side checks to verify 2FA status before processing sensitive operations like team invitations
- Use server sessions/tokens to maintain authoritative 2FA state rather than trusting client assertions
- Implement rate limiting and audit logging for team invitation actions
- Add user notifications when team members are invited (to detect unauthorized invitations)
- Separate authentication (login) from authorization (performing actions) - verify both server-side
- Conduct security code review specifically targeting all client-side conditional logic that affects security decisions

## Variant hunting
Check other privileged operations (project creation, member removal, permission changes) for similar client-side 2FA bypass
Test if MFA requirement can be bypassed for other sensitive actions (payments, password changes, API token generation)
Investigate if other security flags/settings can be similarly manipulated through client-side response modification
Check if WebAuthn or other advanced 2FA methods are subject to the same client-side validation flaw
Test if 2FA can be bypassed during account creation, password reset, or permission elevation flows
Examine API endpoints to determine if the same 2FA check exists server-side but is redundantly checked client-side

## MITRE ATT&CK
- T1190
- T1566
- T1199
- T1556
- T1021

## Notes
This is a classic example of security theater - implementing a control that appears to work but is entirely bypassable due to client-side enforcement. The vulnerability demonstrates why the principle of 'never trust the client' is fundamental to security. The fix is straightforward but critical: move validation to server-side. The report correctly identifies the root cause and provides clear reproduction steps, making it actionable for developers.

## Full report
<details><summary>Expand</summary>

## Summary:
The application requires users to enable 2FA before sending team invitations. However, this restriction can be bypassed by modifying client-side responses (match and replace from false to true). This allows invitations to be sent without enabling 2FA, defeating the security requirement.

## Steps To Reproduce:
1. Sign up / log in to the application.

2. Go to the Team section.

3. Try to invite a new member → the application blocks the request, requiring 2FA.
{F4819623}
4. Use a Burp extension ( Match and Replace) to change the client-side flag `false → true`.
{F4819627}
5. Refresh the page then attempt to send an invitation again.

6. The invitation is sent successfully without enabling 2FA.
{F4819634}

## Impact

1. This bypass allows attackers to ignore the enforced security policy.

2. Reduces the effectiveness of 2FA enforcement.

3. Could allow compromised accounts to invite unauthorized users without 2FA protection.

##Recommendation

Ensure 2FA requirement is validated on the server-side before processing any team invitation requests, instead of relying only on client-side checks.

</details>

---
*Analysed by Claude on 2026-05-24*
