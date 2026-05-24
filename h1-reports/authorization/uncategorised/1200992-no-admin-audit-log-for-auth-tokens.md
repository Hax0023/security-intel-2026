# Missing Admin Audit Log for Authentication Token Operations

## Metadata
- **Source:** HackerOne
- **Report:** 1200992 | https://hackerone.com/reports/1200992
- **Submitted:** 2021-05-18
- **Reporter:** rtod
- **Program:** HackerOne (inferred from URL pattern)
- **Bounty:** Not specified in provided content
- **Severity:** medium
- **Vuln:** Insufficient Logging, Audit Trail Deficiency, Lack of Accountability
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application fails to maintain audit logs for critical authentication token operations including creation, revocation, scope modifications, renaming, and wiping. This absence of audit trails prevents administrators from tracking token lifecycle changes and identifying potential security incidents or unauthorized access.

## Attack scenario
1. Attacker gains temporary access to a user account with token creation privileges
2. Attacker creates multiple authentication tokens with broad scopes to establish persistence
3. Attacker exfiltrates data using the created tokens
4. Administrator detects unusual data access but cannot determine token creation timeline or creator
5. Without audit logs, administrator cannot correlate token creation with the compromise timeframe
6. Investigation is severely hampered, allowing attacker to maintain undetected access through additional tokens

## Root cause
The application architecture does not implement comprehensive audit logging for token lifecycle management operations, creating a blind spot in administrative visibility and incident response capabilities.

## Attacker mindset
An attacker with compromised credentials or insider threat capability would intentionally exploit the lack of audit trails to create backdoor access tokens while remaining undetected. The absence of logging prevents attribution and forensic analysis.

## Defensive takeaways
- Implement comprehensive audit logging for all authentication token operations (create, revoke, modify, delete)
- Log token metadata including creator identity, timestamp, scope/permissions, and operation type
- Ensure audit logs are immutable and stored separately from application logs
- Provide administrators with searchable audit dashboards filtered by operation type, user, timeframe, and token
- Integrate token audit logs with SIEM systems for real-time anomaly detection
- Set alerts for suspicious token patterns (bulk creation, high-privilege scopes, unusual access patterns)
- Retain audit logs for extended periods (minimum 90 days, ideally 1+ years) for forensic investigation

## Variant hunting
Check for missing audit logs on API key management operations
Verify OAuth/OIDC token grant and revocation are logged with sufficient context
Examine session management for missing lifecycle audit trails
Investigate whether privilege escalation or permission changes are logged
Review MFA/2FA configuration changes for audit trail completeness
Check service account and technical token management audit coverage

## MITRE ATT&CK
- T1098 - Account Manipulation (token creation without audit)
- T1556 - Modify Authentication Process (token scope changes unlogged)
- T1078 - Valid Accounts (use of created tokens undetected)
- T1562 - Impair Defenses (disabling or avoiding audit logging)

## Notes
The reporter references a related report (1193321) suggesting this audit log gap exacerbates another security incident. This is a compliance and governance issue as much as a security one, affecting ability to meet regulatory requirements (SOC2, ISO27001, HIPAA) that mandate audit trails for privileged operations. Medium severity is appropriate as it's a detective/forensic control gap rather than direct exploitation vector.

## Full report
<details><summary>Expand</summary>

There seems to be no audit trail for auth tokens.

* Creating tokens
* Revoking tokens
* Scope changes
* Renames
* Marking the token to be wiped

## Impact

As auth tokens are used to access your data having a track record when they are created helps a lot.
If you also take https://hackerone.com/reports/1193321 into account this would have been good information to track down what happened and by who.

</details>

---
*Analysed by Claude on 2026-05-24*
