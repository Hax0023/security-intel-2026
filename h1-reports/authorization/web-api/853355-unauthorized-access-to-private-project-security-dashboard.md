# Unauthorized Access to Private Project Security Dashboard via Permission Downgrade

## Metadata
- **Source:** HackerOne
- **Report:** 853355 | https://hackerone.com/reports/853355
- **Submitted:** 2020-04-19
- **Reporter:** vaib25vicky
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Access Control, Privilege Escalation, Authorization Bypass, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A user with previously elevated permissions (maintainer) could retain access to a private project's security dashboard even after their permissions were downgraded to guest level. The vulnerability allows viewing new and old security vulnerabilities, dependencies, and internal project structure through the personal security dashboard despite lacking direct project access.

## Attack scenario
1. Attacker gains maintainer access to a private project (legitimate or through social engineering)
2. Attacker adds the project to their personal security dashboard while maintaining elevated privileges
3. Attacker's access level is revoked or downgraded to guest by the project owner
4. Attacker accesses their personal security dashboard and discovers project still appears with full vulnerability details
5. Attacker reviews newly discovered security issues, dependencies, and code structure without authorization
6. Attacker leverages disclosed vulnerabilities and architectural information to exploit the target application

## Root cause
Permission revocation logic failed to invalidate cached or materialized security dashboard entries when user role was downgraded. The system checked direct project access permissions for the project view but did not validate permissions for dashboard-aggregated security findings, creating a permission escalation path through the dashboard cache/view.

## Attacker mindset
An insider threat or former trusted contributor seeks to retain visibility into security posture after access is removed. The attacker recognizes that dashboard features may have weaker permission enforcement than direct project access, exploiting this inconsistency to maintain competitive or malicious intelligence about the codebase.

## Defensive takeaways
- Implement synchronous permission invalidation across all features when user roles change, not just primary views
- Audit all aggregated views (dashboards, reports, search results) for permission enforcement consistency
- Use event-driven architecture to cascade permission changes to all dependent features and caches
- Implement real-time permission checks rather than relying on cached or materialized views
- Add audit logging for security dashboard access attempts and permission-state mismatches
- Conduct cross-feature permission testing when modifying access control for any resource
- Consider time-bounded caching or eventual consistency models for sensitive security data

## Variant hunting
Check if other aggregated views (reports, insights, activity feeds) have similar permission bypass vulnerabilities
Test if starred projects retain visibility after permission downgrade
Verify if project search/discovery functions filter results based on current permissions
Examine if API endpoints used by security dashboard respect current user permissions
Test permission changes from other roles (reporter, developer, maintainer) to guest
Verify if removing user entirely vs downgrading permissions behaves consistently
Check if project export/sharing features validate current permissions

## MITRE ATT&CK
- T1190
- T1078
- T1552
- T1526
- T1087

## Notes
This is a permission enforcement bug affecting GitLab's security scanning features. The vulnerability demonstrates a common architectural flaw where permission checks are applied at the primary feature level but overlooked in secondary/aggregated features. The bug allows information disclosure of security posture and internal code structure to unauthorized parties. Reporter provided clear reproduction steps and referenced a public example project for validation.

## Full report
<details><summary>Expand</summary>

### Summary

User with guest permissions can't view security dashboard of the private project. However, this is not applied when user permission changes from maintainer to guest. 

As a result, if user was previously a maintainer in the project he/she can add the project to their security dashboard and when their access levels decreases to guest, they can still view new security vulnerabilities result found in the project through their security dashboard. New security issues found in the project are reflecting back to the guest user security dashboard.


### Steps to reproduce

*  User A create a private project and add user B with maintainer access
* User B will add the project in his security dashboard.
* User A reduced the user B access level to guest. Now, user B can't view any old and new security issues in the project directly
* User B access the project new as well as old security issues through his security dashboard and also the specific new files where the issues lies
* Done

### Impact

The impact of this vulnerability is actually very high. A malicious user can take advantage of the security issues found and can use it to exploit the owner application.  **More info** will also disclose newly added files, dependencies and new internal structure of the project/application to the unauthorized user.


### What is the current *bug* behavior?

Unauthorized user (guest) can view security dashboard of the private project

### What is the expected *correct* behavior?

Project should be removed from the user security dashboard when his/her permission changes to lower.

### Relevant logs and/or screenshots

When permission changes to guest, user can't view the security dashboard directly, they are treated with this message.

{F794811}

But user can access the private project security issues through his own security dashboard.

{F794812}

### Output of checks

This bug happens on GitLab.com

**NOTE** : I'm using one of the example project provided by Gitlab named "yarn-vulnerabilities" for security testing.  
If you want to quickly validate my report, please consider using it.  https://gitlab.com/gitlab-examples/security/yarn-vulnerabilities. 



Thanks,
Vaibhav Singh

## Impact

Unauthorized access to private project security dashboard which allows a malicious user to exploit the owner application and also disclose application newly added files/dependencies and internal structure.

</details>

---
*Analysed by Claude on 2026-05-24*
