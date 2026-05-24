# Reporters can upload design to issues using the Move to feature

## Metadata
- **Source:** HackerOne
- **Report:** 1112297 | https://hackerone.com/reports/1112297
- **Submitted:** 2021-02-26
- **Reporter:** maruthi12
- **Program:** GitLab
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Privilege Escalation, Authorization Bypass, Improper Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
GitLab's issue "Move to" feature fails to enforce Design Management upload restrictions, allowing Reporter-role users to upload design files to private projects where they lack Developer privileges. This bypasses the documented permission model that restricts design uploads to Developer roles and above.

## Attack scenario
1. Attacker creates a Reporter account in a target GitLab instance with access to a private project
2. Attacker creates their own public project where they have full permissions as the owner
3. Attacker creates an issue in their own project and uploads a design file to it
4. Attacker uses the issue's "Move" feature to migrate the issue with attached design to the target private project
5. The design file is successfully transferred to the private project despite Reporter role lacking design upload permissions
6. Attacker has now escalated privileges to perform a Developer-restricted action within the private project

## Root cause
The issue move/migration functionality does not re-validate Design Management permissions when transferring issues between projects. The feature copies designs without checking if the user has Developer+ privileges in the destination project, trusting that the designs are already legitimately attached to the source issue.

## Attacker mindset
An opportunistic insider threat or authenticated user seeking to escalate privileges within a GitLab instance. The attacker exploits a logical gap between permission enforcement at upload time and permission validation during issue migration, using their full control of a source project to bypass restrictions in a target project.

## Defensive takeaways
- Implement permission re-validation during issue migration for all permission-sensitive attachments including designs
- Enforce design upload restrictions not only at creation time but also at transfer/migration time
- Audit issue move functionality to identify other features that may bypass permission checks during bulk operations
- Consider preventing design attachment transfers to projects where the user lacks appropriate permissions
- Add logging and alerts for privilege-sensitive operations like design transfers across project boundaries

## Variant hunting
Check if other file attachment types (documents, images outside design management) bypass permissions during issue move
Test if issue cloning/duplication has similar permission bypass vulnerabilities
Verify if moving issues with other restricted content (CI/CD variables, secrets) respects destination permissions
Examine merge request move functionality for similar authorization gaps
Test if bulk issue operations have permission validation gaps

## MITRE ATT&CK
- T1548 - Abuse Elevation Control Mechanism
- T1557 - Adversary-in-the-Middle
- T1078 - Valid Accounts

## Notes
This is a classic authorization bypass in a feature that involves cross-project resource transfer. The vulnerability exists because developers likely assumed designs were pre-validated at upload time and didn't implement additional permission checks during the migration process. The issue particularly affects multi-tenant or multi-project environments where users have varying permission levels across different projects.

## Full report
<details><summary>Expand</summary>

### Summary

 According to the [permission documentation](https://docs.gitlab.com/ee/user/permissions.html), only role of `Developer` or more can upload  [Design Management](https://docs.gitlab.com/ee/user/project/issues/design_management.html) files. However, using the issue "Move to" feature, a reporter can create a issue with designs.

### Steps to reproduce

1. Consider a private project (say **Private Project**) with a member `Reporter`.
2. From Reporter's login, create a new project. (say **Reporter Project**).
3. Create an issue in *Reporter Project*.
4. Once the issue is created, upload a design to it.
5. Now, on the right hand panel bottom, click the *Move* button. 
6. Choose the *Private Project* as the destination project.
7. Now the issue along with the design are migrated to  the *Private Project*.

Let me know if you need anything else to reproduce this issue.

## Impact

Using the vulnerability, a Reporter can escalate his privilege to upload Design Management Files which he is not allowed to perform.

</details>

---
*Analysed by Claude on 2026-05-24*
