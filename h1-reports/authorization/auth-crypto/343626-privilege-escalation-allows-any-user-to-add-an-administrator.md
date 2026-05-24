# Privilege Escalation in express-cart: Unauthenticated Admin User Creation via Referer Header Spoofing

## Metadata
- **Source:** HackerOne
- **Report:** 343626 | https://hackerone.com/reports/343626
- **Submitted:** 2018-04-26
- **Reporter:** patrickrbc
- **Program:** HackerOne (express-cart on npm)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Broken Access Control, Privilege Escalation, Insecure Direct Object References, Header Spoofing
- **CVEs:** CVE-2018-16483
- **Category:** auth-crypto

## Summary
The express-cart npm module contains a critical access control vulnerability in the /admin/user/insert endpoint that allows any authenticated user to create new administrator accounts. The vulnerability exploits weak authorization checks and relies on client-controlled Referer headers to determine admin privileges, bypassing all authentication and authorization mechanisms.

## Attack scenario
1. Attacker creates or obtains a normal user account in an express-cart application
2. Attacker crafts a POST request to /admin/user/insert with user credentials in the body
3. Attacker includes a Referer header containing /admin/setup to trigger admin privilege assignment
4. The vulnerable endpoint processes the request without checking if the user has admin privileges
5. A new administrator account is created under attacker's control
6. Attacker uses the admin credentials to take over the application, modify products, access payment data, or create additional backdoor accounts

## Root cause
The vulnerability stems from two critical security failures: (1) the /admin/user/insert endpoint lacks the common.restrict middleware applied to other admin routes, allowing unauthorized access; (2) admin privilege assignment relies on the client-controlled Referer header rather than server-side session validation. The application incorrectly assumes that only legitimate setup flows will send /admin/setup in the Referer header.

## Attacker mindset
An attacker with basic user access recognizes that admin endpoints are unprotected and that security decisions are based on easily spoofable HTTP headers. The attacker understands that most developers overlook Referer headers as security controls and exploit this oversight to escalate privileges laterally across the application.

## Defensive takeaways
- Never trust HTTP headers (Referer, Origin, User-Agent, etc.) for security decisions; use server-side session state exclusively
- Apply authentication and authorization middleware consistently to all sensitive endpoints, especially admin functions
- Implement explicit role-based access control (RBAC) checks on every privileged operation, not implicit assumptions
- Establish a formal setup/installation flow that is disabled after initial deployment rather than relying on runtime checks
- Use security middleware like express-jwt or passport to enforce authentication on all /admin/* routes at the routing layer
- Implement rate limiting and audit logging on user creation endpoints to detect privilege escalation attempts
- Conduct security code review specifically for access control logic in user management modules

## Variant hunting
Search for similar patterns in Node.js/Express applications: (1) endpoints lacking consistent middleware application; (2) authorization logic based on HTTP headers or request metadata; (3) admin status assignment in user creation flows without explicit permission checks; (4) setup/configuration endpoints that remain accessible after initial installation; (5) any endpoint that checks referer/origin for security decisions

## MITRE ATT&CK
- T1190
- T1078
- T1548
- T1566

## Notes
This is a classic broken access control vulnerability compounded by weak header-based security. The maintainer was not contacted proactively. The vulnerability affects version 1.1.5 with only 10 weekly downloads, but demonstrates critical security flaws in e-commerce software. The fix should involve: (1) adding restrict middleware to all user endpoints; (2) removing Referer-based logic; (3) implementing proper session-based admin checks; (4) adding CSRF protection.

## Full report
<details><summary>Expand</summary>

I would like to report privilege escalation in the npm module express-cart.

It allows a normal user to add another user with administrator privileges.

# Module

**module name:** express-cart
**version:** 1.1.5
**npm page:** `https://www.npmjs.com/package/express-cart`

## Module Description

expressCart is a fully functional shopping cart built in Node.js (Express, MongoDB) with Stripe, PayPal and Authorize.net payments.

## Module Stats

[10] weekly downloads

# Vulnerability

## Vulnerability Description

A deficiency in the access control allows normal users from expressCart to add new users to the application. This behavior by itself might be considered a privilege escalation. However, it was also possible to add the user as administrator.

## Steps To Reproduce:

Firstly, I noticed that all the endpoints located in the *user.js* file are not being restricted by the *common.restrict* middleware, as the other admin routes do.  Also, the endpoint */admin/user/insert* does not check if the user is admin before adding a new user, which I guess it would be a unlikely behavior.

The following code is used to check if it is the first time creating a user:

```
// set the account to admin if using the setup form. Eg: First user account
let urlParts = url.parse(req.header('Referer'));

let isAdmin = false;
if(urlParts.path === '/admin/setup'){
  isAdmin = true;
}
```

As you can see in the above snippet, if you send a request with a Referer containing the string */admin/setup* the user added will be considered an admin. For example:

```
POST /admin/user/insert HTTP/1.1
Host: localhost:1111
Referer: http://localhost:1111/admin/setup
Content-Type: application/x-www-form-urlencoded
Cookie: connect.sid=[NORMAL_USER_COOKIE]

usersName=NEWADMIN&userEmail=new@admin.com&userPassword=password&frm_userPassword_confirm=password
```

# Wrap up

- I contacted the maintainer to let them know: [N] 
- I opened an issue in the related repository: [N]

## Impact

This vulnerability would allow any registered user to create another user with administrator privileges and takeover the application.

</details>

---
*Analysed by Claude on 2026-05-24*
