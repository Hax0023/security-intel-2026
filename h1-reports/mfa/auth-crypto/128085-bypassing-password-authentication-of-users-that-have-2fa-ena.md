# Bypassing Password Authentication for 2FA-Enabled Users via OTP Parameter Injection

## Metadata
- **Source:** HackerOne
- **Report:** 128085 | https://hackerone.com/reports/128085
- **Submitted:** 2016-04-04
- **Reporter:** jobert
- **Program:** GitLab
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Authentication Bypass, Session Fixation, Insecure Direct Object Reference (IDOR), Parameter Injection
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker with 2FA enabled can bypass password authentication and gain unauthorized access to any other 2FA-enabled user account by injecting a login parameter during OTP verification. The vulnerability exists because the find_user method prioritizes the user-supplied login parameter over the session-stored OTP user ID, allowing an attacker to authenticate with their own password but verify the OTP against a victim's account.

## Attack scenario
1. Attacker (Jane) with 2FA enabled navigates to the sign-in page and enters her own credentials
2. Server stores Jane's user ID in session[:otp_user_id] and prompts for her 2FA code
3. Attacker intercepts the OTP verification request that would normally contain only her OTP attempt
4. Attacker adds a login parameter to the request, replacing her username with the target victim's username (e.g., 'john')
5. Attacker either obtains a valid OTP for the victim (via brute force, credential stuffing, or social engineering) or exploits time-drift configurations
6. Server validates the OTP against the victim's account due to parameter precedence, logging attacker in as the victim

## Root cause
The find_user method in SessionsController uses conditional logic that prioritizes user-supplied params[:login] over the trusted session[:otp_user_id]. During OTP verification, this allows an attacker to override the authenticated session context by injecting a login parameter, causing the server to verify credentials against an arbitrary user instead of the one stored in the session.

## Attacker mindset
An attacker recognizes that while 2FA is enabled, the implementation fails to properly bind the OTP verification to the authenticated session. By understanding the parameter precedence logic, they exploit the gap between authentication (password verification) and authorization (OTP verification against a specific user) to impersonate any 2FA-enabled user without knowing their password.

## Defensive takeaways
- Always use session-stored context (session[:otp_user_id]) for security-critical operations like 2FA verification; never allow user-supplied parameters to override authenticated session state
- Implement strict parameter validation: during OTP verification, reject or ignore any login/user identification parameters and use only the session-stored user ID
- Add authentication context binding: ensure the user verifying the OTP is the same user who initiated the login flow
- Implement rate limiting on OTP verification attempts to prevent brute force attacks on OTP codes
- Review all authentication flows to identify similar parameter injection vulnerabilities where user input could override session context
- Conduct security code review focusing on privilege escalation and authentication bypass patterns, particularly in multi-step authentication implementations

## Variant hunting
Check other authentication mechanisms (password reset, email verification) for similar parameter injection vulnerabilities
Audit other endpoints that use session[:otp_user_id] to ensure they don't accept overriding parameters
Test if the vulnerability extends to social login or third-party authentication flows
Investigate whether the login parameter injection works with different encoding methods (URL encoding, case variation, etc.)
Review OAuth/SAML implementations for similar session binding issues in multi-factor authentication
Check if other identity parameters (user_id, email) can be injected to bypass the OTP verification scope

## MITRE ATT&CK
- T1190
- T1110
- T1556
- T1021

## Notes
This is a high-impact authentication bypass vulnerability affecting all 2FA-enabled users. The attack requires minimal complexity: knowledge of a victim's username and either OTP guessing capability or obtaining a valid OTP. The writeup demonstrates responsible disclosure practice by providing proof of concept without executing against production systems. The fix requires removing parameter precedence and strictly using session context for OTP verification decisions.

## Full report
<details><summary>Expand</summary>

# Proof of Concept
When a user has 2FA enabled, it's possible to sign in as that user without the need to know its password. To reproduce this attack, you need two users that both have 2FA enabled. For the sake of this PoC, lets call them Jane and John. Jane is the attacker and wants to get access to John's account. John his username is `john`. Jane knows John's username. Here's how you can reproduce it:

 - as Jane, go to the sign in page and enter your username and password
 - in the background, it sets Jane's user ID in `session[:otp_user_id]`
 - you now need to enter Jane's 2FA code in order to get access to the account
 - now intercept all your network traffic with a tool like Burp Suite and capture the request that is send when you submit the 2FA token - it looks like this:

```
> POST /users/sign_in HTTP/1.1
> Host: 159.xxx.xxx.xxx
> ...

> ----------1881604860
> Content-Disposition: form-data; name="user[otp_attempt]"
> 
> 212421
> ----------1881604860--
```

 - now add the `login` header to the request - the request now looks like:

```
> POST /users/sign_in HTTP/1.1
> Host: 159.xxx.xxx.xxx
> ...

> ----------1881604860
> Content-Disposition: form-data; name="user[otp_attempt]"
> 
> 212421
> ----------1881604860
> Content-Disposition: form-data; name="user[login]"
> 
> john
> ----------1881604860--
```

 - now, instead of `212421`, send a valid OTP code for `john` to the server
 - Jane is now signed in as John by entering her own password and John's OTP code - Jane still doesn't know John's password

# Impact
The OTP codes are 6 numbers that change every 30 seconds. I haven't looked whether the server allows time drift. This would increase the chance that an attacker guesses the right OTP code for the account. As a PoC, I could run a small attack against GitLab.com, but I haven't been able to reach @sytsem to ask for permission. ;)

# Origin of the issue 
This issue originates from the `find_user` method in the `SessionsController`. It returns a `User` object in two different ways: the first returns the object based on `params[:login]` parameter. The second one if `sessions[:otp_user_id]`. The `params[:login]` parameter takes precedence over the ID stored in the session. This means that if the `params[:login]` is specified in the request when the 2FA code needs to be verified, a different user can be selected to verify the code against. Here's the method:

```ruby
# app/controllers/sessions_controller.rb:58
def find_user
  if user_params[:login]
    User.by_login(user_params[:login])
  elsif user_params[:otp_attempt] && session[:otp_user_id]
    User.find(session[:otp_user_id])
  end
end
```

# Fix
Here's a fix (needs specs to proof that it works): F83019.

</details>

---
*Analysed by Claude on 2026-05-24*
