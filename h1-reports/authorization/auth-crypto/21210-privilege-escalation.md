# Privilege Escalation via Race Condition in Project Invitation System

## Metadata
- **Source:** HackerOne
- **Report:** 21210 | https://hackerone.com/reports/21210
- **Submitted:** 2014-07-23
- **Reporter:** niks
- **Program:** Mavenlink
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Privilege Escalation, Race Condition, Insufficient Access Control, Authorization Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A race condition in Mavenlink's project invitation system allows a user to invite other users to projects even after their invitation privileges have been revoked. By exploiting timing between permission checks and action execution across multiple browser sessions, an attacker can bypass authorization controls and complete privileged actions with revoked permissions.

## Attack scenario
1. Attacker (User B) logs into Mavenlink in one browser and is granted Team Lead privileges on a project by the project owner (User A)
2. Attacker initiates the invite flow by clicking the invite button, triggering a form/dialog but does not submit it yet
3. Project owner (User A) simultaneously downgrades attacker's privileges from Team Lead to Collaboration and removes invitation rights
4. Attacker submits the pending invite request with a target email address while the privilege change is being processed
5. Due to insufficient synchronization, the server validates the invitation request using cached or stale permission data before the privilege revocation takes effect
6. The invitation succeeds despite the user no longer having authorization to perform this action

## Root cause
The application lacks proper transaction isolation and real-time permission synchronization between the privilege modification endpoint and the invitation submission endpoint. The permission check occurs at request initiation rather than execution, allowing a time-of-check-time-of-use (TOCTOU) vulnerability where permissions can change between validation and action completion.

## Attacker mindset
An insider threat or disgruntled team member with initial legitimate access seeks to invite unauthorized users to projects after being stripped of invite privileges. The attacker exploits the assumption that UI-level permission revocation immediately prevents backend action execution, counting on asynchronous processing delays.

## Defensive takeaways
- Implement per-request permission re-validation at action execution time, not just at UI interaction start
- Use session-based permission tokens with short TTLs rather than relying on user roles fetched mid-request
- Enforce pessimistic locking on privilege-sensitive operations to prevent concurrent modifications during critical workflows
- Implement server-side request deduplication and idempotency checks for invitation operations
- Add real-time permission synchronization or use WebSocket/event-driven updates to notify clients of privilege changes
- Log all invitation attempts with timestamp and permission state at time of request for audit trails
- Implement rate limiting and anomaly detection for bulk invitation attempts
- Use atomic database transactions to ensure privilege checks and action execution are indivisible

## Variant hunting
Look for similar race conditions in other multi-step workflows involving privilege changes: file sharing permissions, document collaboration access, team member role changes, API key generation, webhook creation, and SSO configuration. Check for any features where user permissions are cached in session state rather than queried per-request.

## MITRE ATT&CK
- T1548.001
- T1550
- T1071

## Notes
This is a classic TOCTOU (Time-Of-Check-Time-Of-Use) vulnerability amplified by the multi-browser, multi-user scenario which masks the race condition. The vulnerability demonstrates why privilege checks must be re-validated immediately before executing privileged actions, not merely at the start of a user interaction. The bug report lacks bounty amount information and proof of exploitation screenshots mentioned in the narrative.

## Full report
<details><summary>Expand</summary>

1. Consider Two browsers say X and Y, also consider two users say A and B.
2. Sign in to https://app.mavenlink.com using user A through browser X, same as login with user B through browser Y.
3. Now create a project through user A, and add user B as a consultant with Team Lead privilege.
4. Now access this project through user B, and click on invite. A console will open asking for email id. Leave it as it is here and move to user A.
5.  Access the user A console through browser X, and set the privilege of user B to Collaboration and also remove the invite privilege just corresponding to that user, as shown in image below.Now save it.
6. Now move to user B again from where we left in step 4. Enter any email id and submit the request. You will see request will get completed successfully and given user will be invited, while this user doesn't having any privilege to do so..

</details>

---
*Analysed by Claude on 2026-05-24*
