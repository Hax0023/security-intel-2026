# Ability to View Partial Other Users' Notifications

## Metadata
- **Source:** HackerOne
- **Report:** 2584 | https://hackerone.com/reports/2584
- **Submitted:** 2014-03-01
- **Reporter:** wcypierre
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Information Disclosure, Improper Access Control, Cross-User Data Leakage
- **CVEs:** None
- **Category:** uncategorised

## Summary
A user discovered they could view partial notification content from other users' bug reports without proper authorization. The vulnerability appears to be intermittent and was not fully reproducible at the time of submission. This information disclosure affects user privacy by exposing details about other users' bug reporting activities.

## Attack scenario
1. Attacker browses through HackerOne notification pages
2. Due to a caching or session management issue, notifications from other users are displayed
3. Attacker views partial content of other users' bug reports (e.g., Yahoo bug notifications)
4. Attacker may repeat browsing actions to trigger the condition intermittently
5. Attacker documents the leaked information (report titles, associated programs)
6. Attacker reports the issue or uses gathered intelligence about other researchers

## Root cause
Improper access control or caching mechanism in the notification system that fails to properly validate user ownership before displaying notification content. Likely causes include: shared cache without proper key scoping, session-level data pollution, or race condition in database queries filtering notifications by user ID.

## Attacker mindset
Opportunistic reconnaissance attacker seeking to gather competitive intelligence about other bug hunters' activities and report targets. The intermittent nature suggests the attacker probed the system multiple times to understand when the vulnerability manifests, indicating methodical investigation.

## Defensive takeaways
- Implement strict server-side access control validating user authentication and authorization before serving any notification content
- Use properly scoped cache keys including user ID and session tokens to prevent cross-user data leakage
- Implement database query filters with explicit WHERE clauses binding notifications to authenticated user ID
- Add logging and monitoring for anomalous notification access patterns (multiple users accessing same notification ID)
- Use row-level security (RLS) in database layer to prevent queries from returning unauthorized records
- Implement API response sanitization to strip sensitive user data from error messages and partial responses
- Conduct security code review of notification retrieval logic focusing on authorization checks

## Variant hunting
Check if other personal data endpoints (messages, profile, report history) have similar cross-user visibility issues
Test if direct API calls with modified user IDs return unauthorized notifications
Investigate caching headers (Cache-Control, ETag) for improper shared caching configuration
Probe notification endpoint during high concurrency to trigger race conditions
Test with timing attacks between simultaneous requests from different accounts
Examine if pagination parameters can be manipulated to access other users' notification windows
Test if notification IDs are sequential and guessable to enumerate other users' data

## MITRE ATT&CK
- T1040 - Network Sniffing (observing cross-user data)
- T1526 - Reconnaissance/Enumerate sensitive data
- T1213 - Data from Information Repositories (HackerOne platform data)
- T1087 - Account Discovery (identifying other researchers' activities)

## Notes
The intermittent reproducibility suggests a race condition, caching bug, or state management issue rather than a consistent authorization bypass. The partial nature of the leak indicates the system may have partial controls in place that fail under specific conditions. Lack of reproducible steps limited impact assessment but information disclosure was confirmed.

## Full report
<details><summary>Expand</summary>

I was browsing through the pages and suddenly I saw this at my notification: 

Screenshot: ███

The two yahoo bug notification are definitely not mine as I've not reported any bugs to Yahoo, while the Slack's report is mine. I can't really explain what happened as I do not know it myself. I seem to be able to replicate it from time to time but I don't know what is the factor that causes the bug.

</details>

---
*Analysed by Claude on 2026-05-24*
