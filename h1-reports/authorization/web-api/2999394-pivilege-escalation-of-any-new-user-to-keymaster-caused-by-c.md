# Privilege Escalation to Keymaster Role via CSRF in bbPress User Registration

## Metadata
- **Source:** HackerOne
- **Report:** 2999394 | https://hackerone.com/reports/2999394
- **Submitted:** 2025-02-18
- **Reporter:** br3n
- **Program:** bbPress
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Request Forgery (CSRF), Privilege Escalation, Insecure Direct Object References (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
bbPress fails to implement CSRF protections on user registration, allowing attackers to craft malicious requests that automatically assign the bbp_keymaster role to newly registered users. When an authenticated admin visits an attacker-controlled link, a new user account is created with elevated forum privileges, granting complete control over the bbPress forum without proper authorization.

## Attack scenario
1. Attacker creates a malicious HTML page containing a hidden form that auto-submits to the WordPress registration endpoint with user_login, user_email, and bbp-forums-role=bbp_keymaster parameters
2. Attacker sends the link to an authenticated administrator or forum moderator
3. When the admin visits the link, their authenticated session is leveraged to submit the form
4. The registration endpoint processes the request without validating CSRF tokens, creating a new user account controlled by the attacker
5. The bbp_user_add_role_on_register function assigns bbp_keymaster role based on the unvalidated POST parameter
6. Attacker receives login credentials via email and gains full control over forum functionality

## Root cause
The bbp_user_add_role_on_register function processes user role assignment from the bbp-forums-role POST parameter without implementing CSRF token validation. The registration endpoint lacks nonce verification and relies entirely on the user being authenticated, without checking the legitimate intent of the request.

## Attacker mindset
Seek to gain persistent administrative control over community-managed spaces by exploiting trust relationships. Target authenticated administrators with elevated privileges to amplify attack impact. Leverage email delivery to ensure account takeover persistence. View CSRF as an opportunity to perform privileged actions without direct authentication.

## Defensive takeaways
- Implement WordPress nonce verification on all state-changing operations, particularly user registration and role assignment endpoints
- Validate and sanitize all user-supplied parameters controlling role assignments; never trust POST parameters for privilege escalation decisions
- Separate user registration from role assignment and require explicit, authenticated confirmation for elevated role grants
- Implement capability checks using current_user_can() to verify the acting user has explicit permission to assign roles
- Add logging and monitoring for suspicious role assignments, particularly to admin/keymaster roles during registration
- Restrict role assignment parameters to authenticated, authorized users only; consider removing from standard registration flow
- Use security headers (SameSite cookies) to provide defense-in-depth against CSRF attacks

## Variant hunting
Check other WordPress plugins for similar unprotected role assignment during registration or user creation flows
Audit any POST endpoints that accept user-supplied role or capability parameters without nonce validation
Review other bbPress endpoints for missing CSRF protections on administrative actions (topic deletion, user bans, etc.)
Examine custom user meta or capability assignment hooks that might be exploitable via CSRF during registration
Test whether similar attacks work on membership/subscription plugins that assign roles based on POST parameters

## MITRE ATT&CK
- T1190
- T1499
- T1548
- T1133
- T1098

## Notes
This vulnerability is particularly dangerous because it bridges unauthenticated account creation with authenticated privilege escalation. The attacker gains both account access and administrative forum control simultaneously. The reliance on admin visitation reduces exploit reliability but is still practical in targeted attacks. Email credential delivery ensures persistence even if the initial link is detected. The issue represents a fundamental design flaw where registration logic trusts user-supplied role parameters without authorization verification.

## Full report
<details><summary>Expand</summary>

An attacker can escalate a newly registered user's forum role to bbp_keymaster without proper authentication. This occurs because bbPress fails to implement adequate CSRF protections when assigning forum roles, allowing an attacker to craft a malicious request that upgrades a targeted user’s forum privileges upon registration.

When an authenticated admin user visits the link, an new user is registered with the attacker's details, they receive an email containing login credentials.

Root Cause
The bbp_user_add_role_on_register function assigns a user role based on a user-controlled POST parameter (bbp-forums-role). 

## Steps To Reproduce:
1. Install and activate the bbpress plugin.
1. Here is my CSRF form for the PoC.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loading...</title>
</head>
<body onload="document.getElementById('csrf-form').submit();">

    <form id="csrf-form" action="http://localhost/victim/wp-login.php" method="POST">
        <input type="hidden" name="user_login" value="evilpen">
        <input type="hidden" name="user_email" value="attacker@email.com">
        <input type="hidden" name="action" value="register">
        <input type="hidden" name="bbp-forums-role" value="bbp_keymaster">
    </form>

</body>
</html>
```
3. Set up your wordpress instance to send emails, in my case I used the plugin wp-smtp mail.
3. Send a link to an authenticated admin user, when the user opens the link, the forum role of the new user is "Keymaster".
## Recommendations

Implement CSRF Protection

## Impact

While the compromised user remains a WordPress subscriber and does not obtain full site-wide administrative privileges, the bbp_keymaster role grants complete control over the bbPress forum, including managing topics, users, and settings, an attacker could modify discussions, delete content, or manipulate user roles within bbPress.

</details>

---
*Analysed by Claude on 2026-05-24*
