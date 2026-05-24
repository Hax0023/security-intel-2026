# Removed Staff Members Can Indefinitely Modify Flow App Connections via Timestamp Refresh Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 698708 | https://hackerone.com/reports/698708
- **Submitted:** 2019-09-20
- **Reporter:** mariogh
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Authentication, Authorization Bypass, Session Management Flaw, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Removed staff members with prior 'Apps' permission can indefinitely maintain unauthorized access to Shopify Flow app connections by continuously refreshing signed URLs before they expire. The vulnerability allows attackers to manipulate the timestamp and path_hmac parameters to generate new valid URLs every 60 minutes, bypassing the intended one-hour expiration mechanism. A malicious removed staff member can persistently reconnect third-party services (Google Sheets, Trello, Asana) to exfiltrate store data.

## Attack scenario
1. Attacker is added as staff member with 'Apps' permission and connects Google Sheets/Trello/Asana to Shopify Flow, capturing the signed URL containing timestamp and path_hmac parameters
2. Store owner removes the attacker from staff, expecting access revocation after 60 minutes
3. Attacker navigates to saved URL before 60-minute window closes and manually disconnects the connected service
4. Upon reconnecting with any Google account, attacker receives fresh timestamp and path_hmac parameters, resetting the 60-minute expiration clock
5. Attacker automates this refresh process every 45 minutes to maintain perpetual unauthorized access to Flow connectors
6. Attacker redirects workflow data to their own external accounts, exfiltrating sensitive store information

## Root cause
Signed URLs use only a timestamp-based expiration without invalidating tokens when user permissions are revoked. The application generates new valid signatures for the same user actions without verifying current authorization status. No authorization check is performed on the backend when processing reconnection requests; the HMAC validation alone is insufficient because new legitimate actions (disconnect/reconnect) generate fresh valid HMACs.

## Attacker mindset
A disgruntled employee or contractor seeks to maintain persistent access to store data after removal. The attacker recognizes that the application's authorization model relies solely on token expiration rather than permission verification, enabling indefinite access through a simple refresh loop. This represents a targeted insider threat exploiting poor session invalidation.

## Defensive takeaways
- Implement server-side authorization checks on every request, not just HMAC validation - verify the user's current staff status and permissions
- Invalidate all issued tokens immediately when user permissions are revoked or staff member is removed
- Store association between generated signatures and the user/permission set, revoke signatures in bulk when permissions change
- Use short-lived tokens with additional contextual validation (user ID, session ID, request fingerprint) rather than relying solely on timestamp-based expiration
- Implement rate limiting and anomaly detection for repeated connector modification attempts
- Add audit logging for all Flow connector modifications with user context for forensic analysis
- Consider requiring re-authentication for sensitive actions like reconnecting third-party services

## Variant hunting
Similar authorization bypass patterns likely exist in other Shopify apps using signed URLs (private apps, custom apps, embedded apps). Look for: 1) Time-based token expiration without revocation lists, 2) Client-side timestamp/signature refresh mechanisms, 3) Missing backend permission validation on sensitive operations, 4) Apps with service account impersonation features allowing indefinite access refresh, 5) Integration URLs that regenerate credentials without re-validating authorization

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (signed URL manipulation)
- T1078 - Valid Accounts (abuse of previously valid app integration)
- T1556 - Modify Authentication Process (bypass signature expiration)
- T1098 - Account Manipulation (maintain access after removal)
- T1087 - Account Discovery (via reconnected third-party accounts)

## Notes
This is a follow-up to report #416983, indicating a bypass of a previously patched authorization issue. The reporter demonstrates sophisticated understanding by automating the refresh loop. The vulnerability has business impact beyond confidentiality - compromised accounts can be used to modify workflows, potentially affecting business operations. The fact that admin-generated new credentials don't invalidate attacker's old credentials suggests cryptographic material is not properly scoped to the authorization context.

## Full report
<details><summary>Expand</summary>

The following report intends to disclose a bypass for #416983.

>It's been found that removed staff members who had "Apps" permission can still modify flow app connection settings due to improper authorization.

**Description**

Signed URLs generated by Shopify Flow (https://apps.shopify.com/flow) use a timestamp so it remains valid only during a period of one hour.

After that period of time, a removed staff member that previously had Apps permissions should not be able to get unauthorized access to store data, or to connect and disconnect Google Sheets, Trello and Asana accounts from Flow.

With that said, it's possible for a removed staff member to keep refreshing the `timestamp` and `path_hmac` parameters again and again to get unauthorized access to Flow app connections, forever.

Steps To Reproduce:
=====================
1. Login to your shop as the shop owner and add a staff member with only "Apps" permission.
{F587389}
2. Install flow app: (https://apps.shopify.com/flow)
3. Login with the new user you added and navigate to `https://[Your-Shop].myshopify.com/admin/apps/flow/connectors`
{F587390}
4. Click and connect Google Sheets, Trello and Asana.
5. With the user you added go to `https://[Your-Shop].myshopify.com/admin/apps/flow/connectors`, click `Google Sheets` and you will be redirected to:
{F587391}
**Jorge Perez Hilton** is my personal Google Account, I link it to the store to create this report. You can verify this by sending me an email to ███████. 
6. Grab the URL you are visiting. It will look like `https://flow-connectors.shopifycloud.com/gsheet/connect?shop_domain=victim-store-mariogh.myshopify.com&shop_id=10361503766&timestamp=[TIMESTAMP]&path_hmac=[PATH_HMAC]`.
7. Login with the shop owner and remove the user you added
8. You can now use the links you saved to modify connectors settings for 60 minutes even if you are not a Staff member anymore. To reset the timestamp, go to the link you grabbed before the 60 minutes time-frame ends and disconnect the Google Account by clicking `Disconnect`. You will see now something like:
{F587394}
9. Now, click on `Connect` and use any Google Account. The account will successfully connect, a new `timestamp` and a new `path_hmac` will be generated, and they will give you unauthorized access to Flow connectors for an extra 60 mins. 
10. Save the updated URL and repeat the *step 8* and *step 9* every ~45 min. This can be done manually or by automating the browser actions.

I tried to login with the Admin account, Disconnect and Reconnect a new Google Account, thinking that after a new `timestamp` and a new `path_hmac` is generated, the hacker's URL and `path_hmac` will be "blocked" but it doesn't work this way.

When the Admin generates a new `timestamp` and a new `path_hmac`, is like "both URL's are valid to get access". The hacker's (which is a removed staff member) URL still allows him to get unauthorized access to Flow app connections and to refresh the `timestamp` and `path_hmac` again and again.

## Impact

Through this vulnerability a removed staff member will be able to modify google spread sheet, trello and asana connections to connect his own accounts so that workflow actions regarding the connections go to his accounts and therefore he can still access the shop data.

</details>

---
*Analysed by Claude on 2026-05-24*
