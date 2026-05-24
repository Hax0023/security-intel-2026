# Account Takeover via 2FA Linking and Verification Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 810880 | https://hackerone.com/reports/810880
- **Submitted:** 2020-03-04
- **Reporter:** w2w
- **Program:** Helium
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Broken Authentication, Improper Authorization, Insecure Direct Object Reference (IDOR), Missing User Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Two chained vulnerabilities in the 2FA implementation allow unauthenticated account takeover: (1) ability to link 2FA to any account via user ID manipulation, and (2) login without credentials using only a valid 2FA code and target user ID. Together, these enable full account compromise of users without 2FA enabled.

## Attack scenario
1. Attacker discovers or enumerates a target user ID (via /users directory listing or other disclosure method)
2. Attacker initiates 2FA linking on their own account but modifies the user ID parameter to the victim's ID
3. The /api/2fa endpoint fails to validate authorization and links 2FA to the victim's account
4. Attacker generates a valid 2FA code through their own authenticator or intercepts the victim's 2FA secret
5. Attacker calls /api/2fa/verify with victim's user ID and valid 2FA code, bypassing password requirement
6. Attacker gains complete account access without knowing victim's credentials or requiring any user interaction

## Root cause
The /api/2fa endpoint lacks proper authorization checks to verify the requester owns the user ID being modified. Additionally, /api/2fa/verify only validates the 2FA code against the user ID without confirming prior authentication or session ownership, allowing credential-less login.

## Attacker mindset
An opportunistic attacker with knowledge of or ability to enumerate user IDs can systematically compromise accounts. The lack of interaction requirement makes this a highly scalable attack, particularly attractive for account harvesting or targeting high-value users in the Helium ecosystem.

## Defensive takeaways
- Implement strict authorization checks on all endpoints requiring verified session/authentication before allowing modifications to user security settings
- Require multi-step verification for 2FA linking: email confirmation, SMS to registered number, or password re-entry
- Enforce complete authentication (username + password + optional 2FA) before 2FA codes alone can grant access
- Validate that the user initiating 2FA linking matches the user ID in the request via session token verification
- Use opaque tokens instead of predictable UUIDs, or implement rate limiting and anomaly detection for suspicious 2FA verification patterns
- Implement account takeover detection: alert users when 2FA is linked to their account or login occurs from new locations
- Audit all 2FA-related activities and log user ID mismatches in authorization attempts

## Variant hunting
Check for similar IDOR vulnerabilities in other security-critical endpoints: password reset, email change, API key generation
Test whether other authentication factors (backup codes, security questions) can be verified without full authentication
Attempt to enumerate user IDs through directory listings, API responses, or timing attacks on different endpoints
Investigate if 2FA codes can be brute-forced or if rate limiting is applied to /api/2fa/verify
Check whether organization parameter in 2FA linking can be manipulated to link 2FA across organizational boundaries
Test if session fixation or token substitution is possible in the 2FA flow

## MITRE ATT&CK
- T1190
- T1110
- T1556
- T1078
- T1199

## Notes
This is a high-impact finding combining IDOR with broken authentication. The report demonstrates clear proof-of-concept with actual API requests. The vulnerability is particularly dangerous because: (1) it requires only knowledge of user IDs which may be discoverable, (2) it requires zero user interaction, (3) it permanently locks victims out via 2FA, (4) it affects all users with 2FA disabled. The fix requires architectural changes to enforce authorization throughout the 2FA workflow.

## Full report
<details><summary>Expand</summary>

##Description:
Hello, team! I found 2 vulnerabilities in your 2FA implementation:
1) There is a possibility to link 2FA to any other account if it wasn't set up before and user ID is known on the request /api/2fa. In order to do this, after performing a request for 2FA linking, substitute the ID to the victim's ID, organization could be any.

{F737177}

{F737178}

{F737179}

2) We can log in to the account without knowing login and password, using 2FA only, ID should be known. As you can see, in this request, we. don't use tokens/cookie that could be related to the user's ID, we are using only ID a561a2de-b8fe-49f8-8943-fb42229b7b08 and valid code.

Thus, using these 2 bugs we can fully takeover an account that doesn't have 2FA enabled (it was skipped after the first login).

##Steps to reproduce:
1. As a `user1`, register at https://console.helium.com, skip 2FA, copy the ID.
2. Register an account `user2`, register at https://console.helium.com, perform a 2FA request but with ID from `user1`. 2FA is enabled now on the account `user1`!
3. Perform a request /api/2fa/verify with valid code and ID of `user1`.

Result: You've successfully achieved an account takeover. In the future, you'll be able to log in again with this technique in the future, but a victim will have trouble logging in because of 2FA.

## Impact

If a victim's account ID is known, we can fully takeover an account without user interaction. User ID could be disclosed at https://console.helium.com/users (if our user role has access to this directory) or by using other techniques.

</details>

---
*Analysed by Claude on 2026-05-24*
