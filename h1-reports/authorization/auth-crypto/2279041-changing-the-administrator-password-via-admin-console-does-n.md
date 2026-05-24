# Administrator Password Change Does Not Invalidate Existing Sessions

## Metadata
- **Source:** HackerOne
- **Report:** 2279041 | https://hackerone.com/reports/2279041
- **Submitted:** 2023-12-09
- **Reporter:** osama-hamad
- **Program:** Burp Suite Enterprise
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Improper Session Management, Insufficient Session Invalidation, Authentication Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
When an administrator password is reset via the admin console tool (./resetAdministratorPassword), existing authenticated sessions for that administrator account remain valid instead of being invalidated. This allows an attacker who compromised an admin account to maintain persistent access even after the legitimate administrator changes the password as a remediation step.

## Attack scenario
1. Attacker gains unauthorized access to admin account and authenticates successfully
2. Attacker obtains and maintains a valid session cookie/token
3. Legitimate administrator detects the compromise and attempts password recovery
4. Administrator executes ./resetAdministratorPassword command to change the compromised password
5. Administrator confirms new password is set and believes account is now secure
6. Attacker uses their existing session cookie to maintain full administrative access to the system

## Root cause
The password reset mechanism fails to implement session invalidation logic. When credentials are changed, the application does not revoke existing sessions associated with that user account, allowing old sessions to remain active indefinitely despite the authentication factors being updated.

## Attacker mindset
An attacker who has compromised admin credentials would exploit this to establish persistent backdoor access. Even when detected and the password is changed, the attacker maintains a valid session that bypasses the new password requirement, allowing them to continue malicious activities undetected while the administrator believes the account is secured.

## Defensive takeaways
- Implement automatic session invalidation whenever user credentials (passwords, API keys, etc.) are changed or reset
- Revoke all active tokens/cookies for a user when password reset operations are performed
- Log all session termination events for administrative accounts
- Provide administrators with visibility into active sessions and force-logout capabilities
- Implement session timeout mechanisms as an additional layer of protection
- Require re-authentication for sensitive operations rather than relying on session validity alone
- Consider implementing device/location binding for admin sessions to detect anomalies

## Variant hunting
Test if other credential changes (email, 2FA reset) also fail to invalidate sessions
Check if API tokens/keys remain valid after password reset
Verify if sessions are invalidated across all connected services in an enterprise setup
Test whether forceful password changes via admin tools behave differently than user-initiated changes
Check if logout operations properly terminate all session instances or only the current one
Examine if security-sensitive operations (privilege escalation) require session freshness validation

## MITRE ATT&CK
- T1110
- T1190
- T1556
- T1078.002
- T1190

## Notes
This vulnerability is particularly dangerous in breach response scenarios where incident responders are attempting to regain control of compromised systems. The attack is silent and undetectable to the administrator without proper session monitoring. The issue affects both the admin console tool and potentially the dashboard password change function, requiring investigation of both paths.

## Full report
<details><summary>Expand</summary>

- Login to your admin account from the browser. 
- Change the password of admin account via ``` ./resetAdministratorPassword``` as described in https://portswigger.net/burp/documentation/enterprise/managing-users-and-permissions/reset-admin-password

- Go back to your browser session and confirm the session still valid. 

Screen recording proof of concept attached : ████

## Impact

The impact is minimal but effective, assuming an attacker got in and changed the password and the owner realized that and tried to change the password of its account ( he have 1 option to change it via the admin console since he don't have access to its account via the dashboard ) . The admin will change the password of the account but the attacker will still have access to the administrator account as an administrator since its session didn't got invalidated.

</details>

---
*Analysed by Claude on 2026-05-24*
