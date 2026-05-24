# Non-Privileged User Can Create Admin Account in Stocky

## Metadata
- **Source:** HackerOne
- **Report:** 1245736 | https://hackerone.com/reports/1245736
- **Submitted:** 2021-06-27
- **Reporter:** stapia
- **Program:** Stocky
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Broken Access Control, Privilege Escalation, Missing Authorization Check
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A non-privileged user in Stocky can create a new admin account by making a direct POST request to the /users/create_admin endpoint, bypassing authorization checks. This allows unauthorized privilege escalation to full administrative access without proper permission validation.

## Attack scenario
1. Attacker creates a non-privileged account in Stocky with limited or no permissions
2. Attacker logs in with the non-privileged account and visits their user profile at /users/me
3. Attacker intercepts the profile update request to capture valid session cookies and CSRF token
4. Attacker crafts a POST request to /users/create_admin endpoint with the intercepted credentials
5. Attacker submits the request with new admin user credentials (first name, last name, email)
6. Attacker logs out, logs in with the newly created admin account, and gains full administrative control

## Root cause
The /users/create_admin endpoint lacks proper authorization checks to verify that only existing admin users can create new admin accounts. The endpoint validates authentication (user is logged in) but not authorization (user has admin role), allowing any authenticated user to invoke admin creation functionality.

## Attacker mindset
An insider threat or compromised non-privileged account holder seeking to escalate privileges without detection. The attack is low-effort, requiring only HTTP interception and a valid session, making it attractive for opportunistic attackers with existing access.

## Defensive takeaways
- Implement role-based access control (RBAC) checks on all sensitive endpoints, especially those that create privileged accounts
- Verify authorization before executing privileged operations, not just authentication
- Audit all endpoints that handle user creation or privilege assignment for authorization gaps
- Use a centralized authorization framework to prevent inconsistent security checks across endpoints
- Implement proper logging and monitoring for admin user creation events
- Add rate limiting to account creation endpoints to detect automated privilege escalation attempts
- Conduct security review of endpoints handling sensitive operations like user management, inventory, and orders

## Variant hunting
Check for similar missing authorization checks on /users/create_user, /users/delete, /users/update_role endpoints
Test if other privileged operations (inventory updates, order placement, vendor management) lack authorization checks
Investigate whether CSRF protection is properly enforced given the use of authenticity_token
Determine if the vulnerability applies to other user roles beyond admin (e.g., creating super-admin or custom roles)
Test if session cookies alone are sufficient or if additional authorization headers are needed

## MITRE ATT&CK
- T1190
- T1078.001
- T1548.002
- T1087

## Notes
The vulnerability is straightforward privilege escalation through broken access control. The attacker only needs valid session credentials (cookies + CSRF token) which are readily obtainable through normal user interaction. The endpoint's presence suggests admin creation was intended, but authorization logic was entirely omitted. This is a critical finding because it requires no exploitation of other vulnerabilities and immediately grants full application control.

## Full report
<details><summary>Expand</summary>

##Summary:
A non-privileged Stocky user (created within Stocky)  may be able to create a new admin user.

##Steps to reproduce:
1.Create a non-privileged user in Stocky, don't give admin privileges to that user.
2.Login with the non-privileged user and go to https://stocky.shopifyapps.com/users/me, update any field and intercept the request.
3. Make a POST request to /users/create_admin with the Cookies and Token that you intercepted from the previous steps.
4. Log out from Stocky and Login with the new user, you will have admin privileges.

```
POST /users/create_admin HTTP/2
Host: stocky.shopifyapps.com
Cookie:[REPLACE COOKIES]
Content-Length: 277
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="91", " Not;A Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Upgrade-Insecure-Requests: 1
Origin: https://stocky.shopifyapps.com
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://stocky.shopifyapps.com/preferences/users
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

utf8=%E2%9C%93&authenticity_token=[REPLACE TOKEN]&user%5Bfirst_name%5D=██████&user%5Blast_name%5D=████████&user%5Bemail%5D=██████████&commit=Create+%26+Login
```

## Impact

A non-privileged Stocky user may get full admin privileges within the app, which would allow that user to update the inventory, stock, vendors, place purchase orders, etc, even if that user doesn't have those privileges within Shopify.

</details>

---
*Analysed by Claude on 2026-05-24*
