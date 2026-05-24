# 2FA Requirement Bypass When Claiming Bounty

## Metadata
- **Source:** HackerOne
- **Report:** 2528919 | https://hackerone.com/reports/2528919
- **Submitted:** 2024-05-31
- **Reporter:** raymatp
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** medium
- **Vuln:** Authentication Bypass, Authorization Bypass, Insufficient Access Control
- **CVEs:** None
- **Category:** business-logic

## Summary
HackerOne fails to enforce 2FA requirements when users claim bounties, despite enforcing them in other submission flows. An account with reward privileges can claim bounties on behalf of users without 2FA enabled, bypassing program-mandated security controls.

## Attack scenario
1. Program administrator enables 2FA requirement in submission_requirements settings
2. Attacker creates or obtains API token with reward privilege
3. Attacker identifies target account without 2FA enabled but eligible for bounty
4. Attacker uses API/account to claim/reward bounty to target account
5. System approves bounty claim without verifying 2FA status
6. 2FA requirement intended by program is successfully bypassed

## Root cause
Inconsistent validation logic - 2FA enforcement is implemented in embedded submission flows but missing from the bounty claiming/rewarding endpoint. The authorization check validates program requirements but does not verify 2FA status before allowing bounty claims.

## Attacker mindset
Opportunistic privilege escalation; attacker with reward privileges seeks to bypass intended security controls to compromise accounts or exfiltrate funds without enabling 2FA protections that would create audit trails or additional friction.

## Defensive takeaways
- Implement centralized 2FA requirement validation that applies consistently across all relevant endpoints (submissions, claims, rewards)
- Audit all endpoints that accept user actions for missing security requirement checks
- Add integration tests verifying 2FA enforcement across all sensitive operations
- Use middleware/decorators to enforce security policies consistently rather than per-endpoint implementations
- Validate security requirements before state-changing operations, not just during initial submission
- Log and monitor bounty claim operations for users without required 2FA

## Variant hunting
Check if other sensitive operations (payment methods, account settings changes) also bypass 2FA requirements
Test API endpoints vs UI flows for inconsistent 2FA enforcement
Verify if 2FA bypass affects only bounty claims or extends to report acceptance/closure
Check if program-specific security requirements are enforced consistently across all features
Test interaction between different user roles (hacker, program, admin) and 2FA validation

## MITRE ATT&CK
- T1190
- T1556
- T1078

## Notes
This is a classic case of incomplete security control implementation. The vulnerability exists because validation logic was added to one code path (embedded submission) but not others (bounty claiming). The use of API tokens with reward privileges increases severity as it enables programmatic exploitation. The writeup could be strengthened with specific API endpoint details and clearer impact explanation (e.g., unauthorized fund transfer, account takeover risk).

## Full report
<details><summary>Expand</summary>

**Summary:**
When claiming bounty, hackerone doesnt check if the user have enabled 2FA even if the program requires that user enabled 2FA

**Description:**
Programs can enable 2FA requirement for users to force users to enable 2FA before they can submit report to the program. At some instance like submitting via embedded submission, hackerone would enforce the 2FA requirement before user can claim the report. However, the requirement isnt enforced if the user is claiming bounty thus bypassing the 2fa requirement


### Steps To Reproduce

1. Using your sandbox program, enable 2fa requirement in https://hackerone.com/{program_handle}/submission_requirements
2. create an API token with reward privilege
3. reward your dummy account with no 2fa enabled
4. using your dummy account, claim the bounty. Notice that you can claim the bounty even without enabling 2fa


### Optional: Supporting Material/References (Screenshots)

{F3315849}{F3315851}{F3315852}

## Impact

bypassing 2fa requirement by the program

</details>

---
*Analysed by Claude on 2026-05-24*
