# Nextcloud 10.0 Session Management Bypass - Desktop and Android Clients

## Metadata
- **Source:** HackerOne
- **Report:** 165353 | https://hackerone.com/reports/165353
- **Submitted:** 2016-09-02
- **Reporter:** egrep
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Session Management Flaw, Authentication Bypass, Insufficient Session Invalidation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Nextcloud 10.0 fails to properly invalidate sessions when terminated via the user session management interface. Desktop and Android client sessions persist after being killed, allowing continued file synchronization and access without re-authentication. Additionally, session tracking for mobile clients is incomplete.

## Attack scenario
1. Attacker gains access to a user's Nextcloud account and logs in via web browser
2. Attacker installs Nextcloud desktop and Android clients and authenticates with the compromised credentials
3. User detects suspicious activity and terminates desktop/Android sessions from Personal > Sessions panel
4. Attacker continues to sync files and access data via previously-logged-in desktop client without authentication prompts
5. Attacker's Android client remains active and functional despite being terminated from session management
6. Session logs fail to reflect mobile client activity, preventing audit trail detection of the breach

## Root cause
Session invalidation logic does not properly revoke authentication tokens across all client types. Desktop and Android clients maintain cached credentials or persistent tokens that are not invalidated when sessions are terminated server-side. Session tracking mechanism lacks comprehensive client-type coverage.

## Attacker mindset
After credential compromise, maintaining persistent access through multiple vectors while evading detection by killing less-used sessions in the UI while preserving active desktop/mobile client access for data exfiltration and continued monitoring.

## Defensive takeaways
- Implement token-based authentication (JWT/OAuth) with server-side token revocation lists (TRL) or Redis caching
- Force immediate re-authentication across all client types when a session is terminated
- Standardize session tracking to capture all authenticated clients (web, desktop, mobile) with consistent metadata
- Clear cached credentials and local tokens on all connected clients when server-side session termination occurs
- Log session termination events and ensure mobile clients respect server-side session state changes
- Implement session affinity binding (IP, device ID, user agent) to detect anomalous client behavior
- Add real-time session synchronization across clients to prevent orphaned sessions

## Variant hunting
Test other desktop sync clients (Seafile, OwnCloud, Synology) for similar session bypass
Investigate if other token revocation endpoints (API, WebDAV) properly invalidate all client sessions
Check if app-specific passwords bypass the session termination mechanism
Test simultaneous login from many clients and bulk session termination effectiveness
Verify if session timeout policies are enforced equally across client types

## MITRE ATT&CK
- T1078.001
- T1550.001
- T1098.004
- T1556

## Notes
Severity correctly marked as 'minor' by reporter but actually represents a medium-risk authentication persistence flaw. The incomplete session tracking on mobile clients creates audit blindness. This is a common weakness in multi-client sync applications where backend session management doesn't properly cascade termination to native clients with local caching.

## Full report
<details><summary>Expand</summary>

Scenario:
***********
--> Installed nextcloud 10.0 locally and created "admin" account
--> Installed nextcloud desktop client and andoid client

I found session related vulnerability in nextcloud 10.0 where killing session in User(admin) --> Personal --> Sessions not actually killing sessions in desktop client

Steps:
1) Logged into admin account in browser
2) Logged into admin account in desktop client and android client. Currently admin account is having 3 sessions : browser, desktop, andoid
3) Goto User(admin) --> Personal --> Sessions --> kill desktop client session --> upload new file using browser --> Still dekstop client is syncing files without asking any password prompt (issue1)
4) Though android client is still  active, sessions are not capturing in personal --> sessions tab

Hope these are minor issues

</details>

---
*Analysed by Claude on 2026-05-24*
