# No admin audit entry for enabling/disabling 2FA

## Metadata
- **Source:** HackerOne
- **Report:** 1200989 | https://hackerone.com/reports/1200989
- **Submitted:** 2021-05-18
- **Reporter:** rtod
- **Program:** Unknown (HackerOne Report #1200989)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Insufficient Logging, Audit Log Bypass, Account Security Event Logging
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The application fails to create audit log entries when users enable or disable two-factor authentication (2FA), a critical account security event. This logging gap prevents administrators from detecting unauthorized changes to user account security settings and tracking security posture changes.

## Attack scenario
1. Attacker gains access to a user account through credential compromise or social engineering
2. Attacker disables 2FA on the compromised account to maintain persistent access
3. No audit log entry is created for the 2FA disablement action
4. Administrator reviews audit logs but finds no indication of the security modification
5. Administrator is unable to detect the attack or trace when account security was degraded
6. Attacker maintains long-term access while evading detection through lack of logging

## Root cause
The application's 2FA enable/disable functionality does not trigger audit log creation, likely due to missing logging hooks in the authentication or account security code paths.

## Attacker mindset
An attacker with compromised credentials would disable 2FA to reduce detection risk and ensure persistent access even if the original compromise method is patched. The lack of audit logging makes this evasion technique viable.

## Defensive takeaways
- Implement comprehensive audit logging for all account security modifications including 2FA changes
- Log both 2FA enablement and disablement actions with timestamp, user, and source IP
- Generate alerts for sensitive security events like 2FA disablement for immediate detection
- Establish retention policies for audit logs and ensure immutability
- Regularly review audit logs during security investigations and incident response
- Include 2FA status changes in user activity monitoring and SIEM systems

## Variant hunting
Check for missing audit entries on other security-sensitive operations (password changes, permission escalations, session management)
Verify that 2FA changes via API endpoints are also logged
Test if admin-initiated 2FA resets on user accounts generate audit entries
Investigate whether backup code generation or recovery options are logged
Check if 2FA method changes (SMS to TOTP, etc.) create audit entries

## MITRE ATT&CK
- T1098 - Account Manipulation
- T1556 - Modify Authentication Process
- T1562.002 - Impair Defenses: Disable or Modify System Firewall
- T1562.008 - Impair Defenses: Disable or Modify Logging

## Notes
This is a related/duplicate of report #1177353. The vulnerability is classified as an audit/logging control bypass rather than a direct authentication bypass, making it an indirect security issue with impact on detection and incident response capabilities. The severity assessment depends on whether the organization relies on audit logs for compliance (SOC2, ISO27001) or incident investigation.

## Full report
<details><summary>Expand</summary>

Related to https://hackerone.com/reports/1177353
When a user enables or disables 2FA there is no entry in the audit log.

## Impact

Especially for disabling it should probably be logged there. But account security related things should be in there.

</details>

---
*Analysed by Claude on 2026-05-24*
