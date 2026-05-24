# Ability to invite a new member on Sandbox Program

## Metadata
- **Source:** HackerOne
- **Report:** 1088966 | https://hackerone.com/reports/1088966
- **Submitted:** 2021-01-27
- **Reporter:** ex1st3nc3_
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Authorization Bypass, Access Control, Feature Restriction Bypass
- **CVEs:** None
- **Category:** business-logic

## Summary
The HackerOne sandbox environment documentation states that inviting program members to new sandbox programs is not permitted. However, the actual implementation allows users to bypass this restriction and invite team members to sandbox programs by directly navigating to the team members page. This is a mismatch between documented functionality and actual system behavior, allowing unauthorized feature access in the sandbox environment.

## Attack scenario
1. Attacker creates a new sandbox program on HackerOne
2. Attacker navigates to the team_members endpoint for their sandbox program
3. Attacker uses the invite functionality to invite another user as a Security team member
4. System accepts the invitation despite the documented restriction
5. Attacker successfully adds team members to the sandbox program
6. This violates the intended sandbox limitations and allows feature access that should be restricted

## Root cause
Feature flag or authorization check for sandbox program member invitations was not properly implemented at the application level. The UI restriction was documented and likely enforced in the UI layer, but the backend API endpoint lacks proper validation to prevent this action in sandbox environments.

## Attacker mindset
A researcher testing sandbox program functionality discovers that the documented restriction is not enforced, allowing them to invite users contrary to stated limitations. This could be used to expand access beyond intended scope or test features that should be isolated.

## Defensive takeaways
- Implement server-side authorization checks for all sensitive operations, not just UI-level restrictions
- Validate sandbox program status on the backend before allowing team member invitations
- Ensure backend API endpoints enforce the same restrictions as documented features
- Add audit logging for all team member invitations to detect unauthorized access patterns
- Regularly audit sandbox program capabilities to ensure documented restrictions match actual implementation
- Use feature flags consistently across both UI and API layers

## Variant hunting
Check other sandbox-specific features for similar bypasses (e.g., can you modify program settings, change vulnerability scope, or access premium features that should be restricted?). Examine other team management endpoints (remove members, change roles, etc.). Test if this affects program creation limits or other documented sandbox restrictions.

## MITRE ATT&CK
- T1548.001
- T1078
- T1556

## Notes
This is a documentation-implementation mismatch vulnerability. The severity is low as it primarily affects sandbox testing environments. However, it demonstrates a fundamental security principle failure: user-facing restrictions must be enforced at the system level, not just in the UI. The vulnerability would be more critical if this same pattern existed in production environments where feature access is monetized or security-controlled.

## Full report
<details><summary>Expand</summary>

In the description 
> HackerOne offers a sandbox for hackers to help them test program functionality for security vulnerabilities. To create a program, go here. You can select any product edition, giving you access to almost all features HackerOne offers. Hackers can create up to 30 programs in the sandbox. It is currently **not** possible to invite program members to new programs in the sandbox.

However in the Sandbox program the owner allows to invite a new Security member after estabilishing the program

## Steps to produce

1. Create a new sandbox program

2.  Go to [https://hackerone.com/{YOUR-PROGRAM}/team_members](https://hackerone.com/{YOUR-PROGRAM}}/team_members)

3. Invite any user

██████

4. As you can see you can invite a user even though in the description it says 

> It is currently **not** possible to invite program members to new programs in the sandbox.

███

██████████

## Impact

Allows the attacker to invite a ``team_member`` to the sandbox program even though its not permitted.

</details>

---
*Analysed by Claude on 2026-05-24*
