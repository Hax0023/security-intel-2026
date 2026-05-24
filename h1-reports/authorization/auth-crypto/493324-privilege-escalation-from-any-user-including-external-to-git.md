# Privilege Escalation to GitLab Admin via Session Hijacking During Impersonation

## Metadata
- **Source:** HackerOne
- **Report:** 493324 | https://hackerone.com/reports/493324
- **Submitted:** 2019-02-09
- **Reporter:** skavans
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Privilege Escalation, Session Hijacking, Improper Session Management, Inadequate Access Controls
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An authenticated attacker can escalate privileges to GitLab administrator by hijacking the admin's impersonation session. When an admin impersonates a user, the impersonated user can view the admin's session in their active sessions list, copy the session ID, and use it to take control of the admin account by clicking 'Stop impersonating'.

## Attack scenario
1. Attacker logs into GitLab as a regular user and revokes all other active sessions
2. Attacker requests or tricks a GitLab administrator into impersonating their account
3. Administrator impersonates the attacker, creating a new admin session visible in the attacker's active sessions list
4. Attacker extracts the admin's session ID from the active sessions page
5. Attacker manually sets their browser cookie to the admin's session ID via browser console
6. Attacker clicks 'Stop impersonating' button, which logs them into the admin account with elevated privileges

## Root cause
GitLab's session management failed to properly isolate impersonation sessions. The system displayed the admin's session details to the impersonated user without restricting their ability to interact with or hijack that session. The 'Stop impersonating' functionality did not verify that the requester was the original admin account holder.

## Attacker mindset
An insider threat or compromised low-privilege account holder could systematically request impersonation from administrators under false pretenses (troubleshooting issues, permission problems, etc.) to trigger this attack chain. The attack requires minimal technical skill once an admin agrees to impersonate.

## Defensive takeaways
- Never display impersonation session details (session IDs) to the impersonated user
- Implement strict session isolation—impersonated sessions should be inaccessible to the impersonated user's normal session context
- Require re-authentication or admin verification before allowing 'Stop impersonating' operations
- Log all impersonation attempts and require legitimate business justification
- Implement session pinning and device binding to prevent session hijacking
- Use secure, opaque session identifiers that cannot be easily copied or manipulated
- Add rate limiting and alerts on impersonation requests to detect abuse
- Consider implementing passwordless admin operations or hardware token requirements for sensitive actions

## Variant hunting
Check if similar session hijacking is possible during other privilege transitions (role changes, temporary access grants)
Investigate whether session IDs are exposed in other administrative functions or audit logs
Test if the vulnerability applies to API sessions or OAuth tokens during impersonation
Examine if other 'Stop X' operations (Stop 2FA, Stop VPN) have similar isolation failures
Check if impersonation can be chained—impersonating an admin to gain higher privileges
Test whether the vulnerability exists in GitLab's container registry, package registry, or other integrated services

## MITRE ATT&CK
- T1078.003
- T1556
- T1550.001
- T1528

## Notes
This is a critical design flaw in GitLab's impersonation feature. The vulnerability requires admin cooperation (unwitting or otherwise) but results in complete account takeover with administrative privileges. The low barrier to exploitation makes it particularly dangerous in organizations with permissive admin policies. GitLab should implement session encryption, isolation, and stricter verification for privileged operations.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hey team,
I have discovered a way for any logged in user (attacker) to escalate his privileges to gitlab administrator if the real gitlab administrator impersonates attacker's account.

**Description:**
When the gitlab admin impersonates some user, he gets new `_gitlab_session` cookie and then clicking at `Stop impersonating` he gets his own admin's cookie back. The vulnerability is that the impersonated user (attacker in our case) can see impersonated session at the `Active sessions` so he can switch to it (manually setting it in cookie) and click `Stop impersonating` by himself. This is a way how he can become gitlab administrator.

## Steps To Reproduce:

1. Sign into gitlab app as some user (`attacker`)
1. Go to the active sessions settings tab and revoke all the sessions besides the current active one
1. Sign into gitlab app in other browser as administrator (`admin`)
1. Go to users admin section and impersonate `attacker` user
1. Update the active sessions tab as `attacker` and make sure the second session appeared there (this is the admin logged into your account)
{F420971}
1. Inspect the `Revoke` button and make sure you see the session ID there. Copy it.
████
1. Go to index page of gitlab as `attacker` (http://gitlab.bb/ in my case), I do not know why, but it is important step
1. Clear `attacker` browser's cookie
1. Open the developer console as `attacker` and manually set `_gitlab_session` to the copied one with:

```javascript
document.cookie = "_gitlab_session=█████";
```
9. Refresh the attacker's page and make sure you are now inside the impersonated session
{F420978}
10. Click `Stop impersonating` at the top-right corner as `attacker` and make sure you are now logged in as gitlab admin.
███

## Impact

Every gitlab authenticated user can escalate his privileges to admin ones and give complete access to all gitlab services, projects and abilities. Only he needs to do is ask admin to impersonate his account because of something works bad there.

</details>

---
*Analysed by Claude on 2026-05-24*
