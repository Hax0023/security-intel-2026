# Session Not Expire / 2FA Bypass via Stolen Cookies

## Metadata
- **Source:** HackerOne
- **Report:** 2469706 | https://hackerone.com/reports/2469706
- **Submitted:** 2024-04-18
- **Reporter:** blackflyhunter
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Session Management, Insufficient Session Expiration, 2FA Bypass, Cookie Security
- **CVEs:** None
- **Category:** uncategorised

## Summary
The platform fails to properly invalidate stolen session cookies, allowing attackers to maintain unauthorized access to victim accounts indefinitely. Even after victims clear browser history or create new sessions with updated credentials, previously compromised cookies remain valid, effectively bypassing 2FA mechanisms and session management controls.

## Attack scenario
1. Attacker obtains victim's session cookies through phishing, malware, network interception, or other means
2. Victim clears browser history/cookies or logs out, but server does not invalidate existing sessions
3. Attacker imports stolen cookies into their own browser using tools like EditThisCookie
4. Victim logs in again with email/password, creating a new authenticated session on the server
5. Attacker uses the old stolen cookies and successfully accesses the victim's account simultaneously
6. Attacker maintains persistent unauthorized access through the unrevoked legacy session tokens

## Root cause
The application fails to implement proper session invalidation mechanisms. Specifically: (1) No server-side session timeout or expiration logic, (2) No session invalidation on password change or re-authentication, (3) No mechanism to revoke old sessions when new ones are created, (4) 2FA does not invalidate or scope existing cookie-based sessions, (5) Missing logout functionality that terminates all active sessions

## Attacker mindset
An attacker who gains initial cookie access recognizes that persistent session tokens provide long-term account compromise. They understand that victims typically assume clearing cookies removes attacker access, but if the backend never invalidates sessions, the old tokens remain usable indefinitely. This is particularly valuable because it bypasses password resets and 2FA since the session predates those controls.

## Defensive takeaways
- Implement server-side session management with explicit TTL (time-to-live) and periodic expiration checks
- Invalidate all active sessions when user changes password or enables/modifies 2FA
- Store session metadata (IP, User-Agent) and detect anomalous cookie usage patterns
- Implement logout functionality that explicitly invalidates session tokens server-side
- Use short-lived access tokens with refresh token rotation instead of long-lived session cookies
- Require re-authentication for sensitive operations even with valid session cookies
- Implement SameSite cookie attribute and Secure flags to prevent cookie theft
- Add session management UI allowing users to view and terminate active sessions remotely
- Monitor for concurrent sessions from different IPs/User-Agents and alert users
- Ensure 2FA creates a new session or invalidates old ones, not just a flag in existing session
- Log all session creation/termination for forensic analysis

## Variant hunting
Check if JWT tokens or other token formats have proper expiration claims (exp) that are validated
Test if API endpoints validate session state server-side or only check cookie presence
Verify if concurrent session limits are enforced across the platform
Test session behavior after password reset, 2FA enable/disable, and email change
Check if accounts can be accessed simultaneously from multiple geographic locations without alerts
Verify if admins can view user session lists and force session termination
Test if remember-me functionality creates properly scoped, short-lived tokens
Check if OAuth/SSO tokens are properly revoked on logout
Test if API sessions (if separate from web) expire independently
Verify behavior when user agent or IP changes with same session cookie

## MITRE ATT&CK
- T1190
- T1556
- T1187
- T1539
- T1550.001
- T1555.003
- T1021.001

## Notes
This report demonstrates a critical session management failure that compounds into both authentication bypass and 2FA evasion. The POC was redacted in the original report. The vulnerability is particularly severe because it's not just about cookie theft (which is somewhat expected), but the platform's complete failure to invalidate sessions server-side. This suggests the application may lack proper session tables/stores and relies entirely on client-side cookie validation. The 2FA bypass component indicates that 2FA was likely implemented as a flag in the existing session rather than as a session-gating mechanism.

## Full report
<details><summary>Expand</summary>

Hello Security Team,
I hope you are having a good day!

The attacker can use the victim cookie to log in victim's account and if a victim clears her browser history victim can be logged out of her account but the attacker use the victim's previous session cookies and log in multiple times an attacker can still log in the account again and again

## Steps To Reproduce:
1. attacker stole the cookies of victims through any means - https://hackerone.com/ {{attacker perspective}}
2. Victim clears their browser history  {{Victim perspective}}
3. attacker add victim cookies using  http://www.editthiscookie.com addon to own browser {{attacker perspective}}
4. Victim login their browser again using email password (Victim created a new session but the old session has not expired)
5. The attacker could still log in victim's hackerone account again. {{attacker perspective}}


## POC: (Recommended)
███████

## Impact

1. The session does not expire 
2. 2FA Bypass

</details>

---
*Analysed by Claude on 2026-05-24*
