# Authorization bypass allows changing email address of other users

## Metadata
- **Source:** HackerOne
- **Report:** 3398283 | https://hackerone.com/reports/3398283
- **Submitted:** 2025-10-24
- **Reporter:** yoyomiski
- **Program:** Revive Adserver
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Authorization Bypass, Insufficient Authentication, Privilege Escalation, Account Takeover
- **CVEs:** CVE-2025-48986
- **Category:** uncategorised

## Summary
The Revive Adserver admin panel endpoint /admin/agency-user.php accepts POST requests to update user email addresses without requiring password confirmation, despite the UI enforcing this requirement. An authenticated attacker with access to the User Access page can modify any user's email address, including administrators, without authorization.

## Attack scenario
1. Attacker authenticates to Revive Adserver with an account that has access to the User Access management page
2. Attacker navigates to Inventory → User Access and selects the target admin user
3. Attacker intercepts the POST request sent when clicking 'Save changes'
4. Attacker modifies the email_address parameter to an attacker-controlled email address while keeping valid token and userid parameters
5. Attacker forwards the modified POST request to /admin/agency-user.php endpoint
6. Admin user's email is updated without password verification, enabling account takeover through password reset functionality

## Root cause
The backend endpoint /admin/agency-user.php performs insufficient authorization checks when processing email update requests. While the frontend UI correctly requires password confirmation for email changes, the backend fails to enforce this security control, allowing direct API requests to bypass the intended authentication requirement.

## Attacker mindset
An insider threat or attacker with basic user privileges recognizes that UI security controls may not be mirrored on the backend API. By analyzing network requests and discovering the unprotected endpoint, they can escalate privileges to compromise administrative accounts without needing to guess passwords.

## Defensive takeaways
- Always enforce security controls at the backend API level, not just in the UI
- Require re-authentication (password confirmation) for sensitive account changes like email address modifications
- Implement proper authorization checks to verify that users can only modify their own account details or have explicit admin privileges
- Use anti-CSRF tokens that are properly validated and session-specific
- Apply rate limiting on account modification endpoints to detect automated exploitation
- Log and monitor all email address changes with alerting for admin account modifications
- Implement account change confirmations via email verification before applying changes

## Variant hunting
Check if other sensitive account parameters (password, username, phone) can be modified via backend endpoints without re-authentication
Test if the vulnerability affects user-to-user email changes or only admin accounts
Examine other admin panel endpoints (/admin/*.php) for similar authorization bypass patterns
Verify if the token validation is properly checking user identity before allowing modifications
Test if cross-agency user modifications are possible through agencyid parameter manipulation
Check for similar issues in user preference endpoints or profile update mechanisms

## MITRE ATT&CK
- T1190
- T1548
- T1078
- T1566

## Notes
This vulnerability is particularly dangerous as it affects administrative accounts and can lead to complete account takeover through email-based password reset mechanisms. The discrepancy between frontend and backend security controls suggests inadequate security testing of API endpoints. Version affected: Revive Adserver 6.0.0

## Full report
<details><summary>Expand</summary>

==Version: Revive Adserver 6.0.0==

##Summary:
The Change E-mail UI requires the current password, but the admin panel endpoint /admin/agency-user.php accepts a POST that updates a user’s email (including admin) without requiring the account password. The application does not require re-authentication before updating email addresses.

##Step to reproduce:
1. Log in page
2. Go to Preferences → Change E-mail, observe that changing the email normally requires the current password.

██████
3. Navigate to Inventory → User Access, select the admin user, and click Save changes while intercepting the request.
4. Modify and send the following request:
`submit=1&login=admin&token=ba6ff2f70a69a509d5bcc84cb2225517&userid=1&email_address=another-mail@example.com&agencyid=1`

{F4929064}
5. Observe that the admin user’s email is successfully updated without password confirmation.

███████

## Impact

- An authenticated attacker (with access to the User Access page) can change the administrator’s email address without authorization, potentially leading to account takeover or loss of access control integrity.

VIdeo PoC: ██████

</details>

---
*Analysed by Claude on 2026-05-24*
