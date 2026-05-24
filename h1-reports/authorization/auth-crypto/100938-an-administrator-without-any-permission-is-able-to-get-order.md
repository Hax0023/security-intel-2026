# Unprivileged Administrator Can Register Mobile Device for Order Notifications via Mobile Devices Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 100938 | https://hackerone.com/reports/100938
- **Submitted:** 2015-11-22
- **Reporter:** rms
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Authorization Bypass, Privilege Escalation, Access Control Flaw
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An administrator lacking the 'Settings' permission can bypass UI restrictions and register a mobile device for order notifications by directly calling the /admin/mobile_devices.json endpoint. This allows unprivileged users to receive sensitive order notifications despite lacking the required permissions.

## Attack scenario
1. Attacker logs in to Shopify admin with an account that has full access initially
2. Attacker registers a mobile device via the mobile app, triggering a POST to /admin/mobile_devices.json and capturing the APNS token
3. Attacker's account permissions are revoked, specifically removing 'Settings' permission
4. Attacker removes the mobile device registration through legitimate means
5. Attacker replays the original /admin/mobile_devices.json request with the captured APNS token
6. The endpoint accepts the request despite lacking permissions, registering the device for order notifications which now appear in /admin/settings/notifications

## Root cause
The /admin/mobile_devices.json endpoint does not properly validate the 'Settings' permission before allowing a user to register a mobile device for notifications. The permission check exists in the UI layer but is absent or improperly implemented in the API endpoint itself, creating a classic authorization bypass vulnerability.

## Attacker mindset
An internal threat actor or disgruntled employee with revoked permissions seeks to maintain visibility into business-critical information (orders) despite administrative access being restricted. The attacker recognizes the permission model is only enforced at the UI level and probes APIs for inconsistent validation.

## Defensive takeaways
- Implement consistent permission validation across all endpoints, not just UI forms
- Validate 'Settings' permission on the server-side before allowing mobile device registration or notification subscriptions
- Apply principle of least privilege: ensure API endpoints are protected with the same authorization checks as UI components
- Audit all administrative endpoints for permission mismatches between UI and API layers
- Implement request signing or CSRF tokens that cannot be replayed across different permission states
- Log and monitor device registration attempts, especially from accounts with recently revoked permissions
- Use capability-based security: tie notification subscriptions to explicit permission grants rather than implicit access

## Variant hunting
Check other /admin/* endpoints for permission validation bypasses (mobile_devices, webhooks, api_credentials, etc.)
Test if replaying requests from different endpoints works after permission revocation
Investigate whether other sensitive operations (data exports, API key generation) also lack server-side permission checks
Examine if permission changes are reflected immediately across all APIs or if there are race conditions
Test cross-account token reuse scenarios with the APNS token
Check if the vulnerability extends to other notification channels (email, SMS, webhooks)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process
- T1222 - File and Directory Permissions Modification

## Notes
This is a classic example of authorization bypass through API endpoint mishandling. The vulnerability is straightforward to exploit and demonstrates the importance of implementing permission checks at the API layer rather than relying solely on UI-level restrictions. The ability to replay requests across permission state changes is particularly concerning in administrative interfaces.

## Full report
<details><summary>Expand</summary>

**Description**
----
An administrator who lacks the 'Settings' permission is not able to add notifications through the UI. But the endpoint `shop.myshopify.com/admin/mobile_devices.json` does allow the unprivileged user to add his own device.



**PoC**
----
This PoC simply show how to get & re-use the mobile APNS Token.

. Log in the Shopify phone app with a full access account
. Intercept the request to `POST /admin/mobile_devices.json`
. Remove all permissions of that account.
. Remove the mobile notification added.
. Replay the request to `POST /admin/mobile_devices.json`

The order notification has been added in `/admin/settings/notifications`
Make an order, and the mobile will get the notification.

</details>

---
*Analysed by Claude on 2026-05-24*
