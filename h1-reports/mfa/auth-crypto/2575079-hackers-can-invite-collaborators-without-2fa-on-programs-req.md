# Hackers can Invite Collaborators Without 2FA on Programs Requiring 2FA

## Metadata
- **Source:** HackerOne
- **Report:** 2575079 | https://hackerone.com/reports/2575079
- **Submitted:** 2024-06-26
- **Reporter:** anish-kosaraju
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authentication Bypass, Access Control, Two-Factor Authentication Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A vulnerability in HackerOne's collaboration system allows users to invite collaborators without 2FA to reports on programs that enforce 2FA requirements. This bypasses the security control entirely, allowing non-2FA authenticated users to access sensitive vulnerability reports.

## Attack scenario
1. Attacker creates account on HackerOne with 2FA enabled to satisfy any profile requirements
2. Attacker submits a vulnerability report to a program with mandatory 2FA enforcement
3. Attacker creates a second account without 2FA enabled
4. Attacker invites the non-2FA account as a collaborator on the report
5. The non-2FA account receives and accepts the collaboration invitation
6. Non-2FA account gains full access to the report, bypassing 2FA requirement

## Root cause
The invitation and access control logic does not validate that collaborators meet the program's 2FA requirement before granting access. The 2FA enforcement is likely only checked at initial program access but not enforced on invited collaborators.

## Attacker mindset
An attacker could exploit this to gain access to sensitive reports using a secondary account while circumventing security controls. This could be used to share reports with co-conspirators or maintain access even if the primary account is suspended.

## Defensive takeaways
- Enforce 2FA requirements at all access points, not just initial login
- Validate that invited collaborators meet program security requirements before granting access
- Implement access control checks on invitation acceptance, not just invitation creation
- Consider blocking invitations to accounts that don't meet the program's security baseline
- Audit collaboration logs for accounts that shouldn't have access based on security policies
- Require collaborator authentication refresh when joining reports with elevated security requirements

## Variant hunting
Check if other security requirements (IP whitelisting, device trust) can be bypassed via collaborator invites
Test if downgrading 2FA after being invited maintains access
Verify if programmatic APIs honor 2FA requirements for collaborator access
Check if other access control policies are enforced on invited parties
Test cross-program collaboration with different security levels

## MITRE ATT&CK
- T1190
- T1548
- T1199

## Notes
This is a logical access control vulnerability where the authorization model fails to properly enforce security policies across all access paths. The vulnerability is particularly critical because it undermines a mandatory security control meant to protect sensitive vulnerability disclosures.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hackers can invite collaborators that don't have 2FA enabled in reports sent to programs that require 2FA.

### Steps To Reproduce

1. Create a new program and enable 2FA.
2. Submit a report to that program. Create a new account without 2FA and invite that account as a collaborator to the report.
3. The new account will be able to accept the invite.

## Impact

This defeats the point of having 2FA enabled as hackers who don't have 2FA can still access the report.

</details>

---
*Analysed by Claude on 2026-05-24*
