# Admin audit log fails to properly log unsetting of file expiration date

## Metadata
- **Source:** HackerOne
- **Report:** 1200810 | https://hackerone.com/reports/1200810
- **Submitted:** 2021-05-18
- **Reporter:** rtod
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Insufficient Logging, Audit Trail Bypass, Information Disclosure
- **CVEs:** CVE-2021-32680
- **Category:** uncategorised

## Summary
The Nextcloud admin audit log fails to properly record when a file's expiration date is removed/unset, creating gaps in the audit trail. While setting an expiration date is logged correctly, unsetting it generates an uninformative log entry, preventing administrators from obtaining a complete and accurate record of file permission and lifecycle changes.

## Attack scenario
1. Administrator shares a file with an expiration date set
2. Audit log correctly records the file sharing action and expiration date configuration
3. Administrator removes/unsets the expiration date from the shared file
4. Audit log generates a vague or useless log entry that doesn't clearly indicate the expiration date was removed
5. During compliance review or security investigation, auditor cannot determine what changes were made to file expiration
6. This creates a compliance gap and prevents proper forensic analysis of file access policies

## Root cause
The audit logging mechanism in Nextcloud does not properly capture or format the event details when an expiration date attribute is unset/cleared on a shared file, likely because the code only logs meaningful information when a value is SET rather than when it is REMOVED.

## Attacker mindset
A malicious administrator or insider could leverage incomplete audit logging to cover tracks when modifying file expiration policies, extending access to sensitive files without detection in compliance logs.

## Defensive takeaways
- Implement symmetric logging for all state changes - log both SET and UNSET/REMOVE operations with equal detail
- Audit log entries must include both old and new values for modified attributes
- Regular validation that audit logs capture all documented user actions as per security policy
- Test audit logging for both positive actions (adding) and negative actions (removing) during development
- Include field-level change auditing that captures what specific attributes were modified and their values
- Ensure compliance documentation matches actual logging behavior

## Variant hunting
Check if other expiration or permission-related attributes fail to log when unset (e.g., password removal, access level downgrade)
Verify whether deletion of other file metadata (tags, comments, sharing policies) is properly logged
Test unsetting of user attributes or permissions across the platform
Check notification/reminder unsubscription logging
Audit logging of removal actions for access controls, group memberships, or role assignments

## MITRE ATT&CK
- T1578
- T1562.008

## Notes
This is a follow-up to report #1177353 (also appears to be related to audit logging issues). The severity is low because it's a logging/visibility issue rather than a security control bypass, but it undermines audit trail integrity which is critical for compliance and forensics. The issue likely affects other unset/removal operations in the system.

## Full report
<details><summary>Expand</summary>

In relation to https://hackerone.com/reports/1177353

1. Enable the audit log
2. Share a file
3. Set and expiration date

So far all looks good in the log

4. Unset the the expiration date.
5. See a pretty useless log line

## Impact

The audit log is used to get a full trail of the actions which is now incompletely. With possible important information.
It seems to be also listed on https://portal.nextcloud.com/article/using-the-audit-log-44.html

</details>

---
*Analysed by Claude on 2026-05-24*
