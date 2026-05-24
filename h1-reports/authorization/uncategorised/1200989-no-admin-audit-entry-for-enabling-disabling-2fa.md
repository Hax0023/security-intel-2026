# No Admin Audit Entry for Enabling/Disabling 2FA

## Metadata
- **Source:** HackerOne
- **Report:** 1200989 | https://hackerone.com/reports/1200989
- **Submitted:** 2021-05-18
- **Reporter:** rtod
- **Program:** HackerOne
- **Bounty:** Unknown
- **Severity:** medium
- **Vuln:** Insufficient Logging, Audit Log Bypass, Account Security Monitoring Gap
- **CVEs:** None
- **Category:** uncategorised

## Summary
Critical account security events such as enabling or disabling two-factor authentication are not logged in the admin audit log, preventing administrators from monitoring and detecting unauthorized account modifications. This creates a blind spot in security monitoring, particularly for 2FA disablement which could indicate account compromise.

## Attack scenario
1. Attacker gains unauthorized access to user account through credential compromise or social engineering
2. Attacker disables 2FA to prevent account recovery and secure further access
3. Admin audit log shows no entry for 2FA modification, making the compromise invisible to security team
4. Account remains compromised undetected as there is no alerting mechanism for this critical change
5. Attacker maintains persistent access and performs malicious actions with legitimate-appearing account

## Root cause
The 2FA enable/disable functionality does not trigger audit log entry creation, likely because audit logging was not implemented for this security-critical operation during development

## Attacker mindset
An attacker who gains account access would immediately disable 2FA to maintain persistence and prevent the legitimate owner from regaining control via second factor recovery, while avoiding detection by exploiting the lack of audit logging

## Defensive takeaways
- Implement mandatory audit logging for all account security modifications, especially 2FA changes
- Create real-time alerting for 2FA disablement events to enable rapid incident response
- Establish security event logging as part of the security development lifecycle for any authentication/authorization changes
- Conduct audit log completeness review across all sensitive account operations
- Require multi-factor approval or confirmation for 2FA disablement from admin/privileged users

## Variant hunting
Search for other missing audit entries in: password changes, email/recovery address modifications, API token generation/revocation, permission elevation, SSH key additions, backup code generation, security question updates, device/browser trust settings, and session management operations

## MITRE ATT&CK
- T1531 - Account Access Removal
- T1556 - Modify Authentication Process
- T1562.002 - Impair Defenses: Disable or Modify Log Files and Event Reporting

## Notes
This is a security hygiene issue rather than direct exploitation vulnerability. The impact is amplified in multi-tenant or corporate environments where admin oversight is critical. Related to previous report #1177353 suggesting this may be part of broader audit logging gaps.

## Full report
<details><summary>Expand</summary>

Related to https://hackerone.com/reports/1177353
When a user enables or disables 2FA there is no entry in the audit log.

## Impact

Especially for disabling it should probably be logged there. But account security related things should be in there.

</details>

---
*Analysed by Claude on 2026-05-24*
