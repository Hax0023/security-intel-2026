# Pre-Auth Blind NoSQL Injection leading to Remote Code Execution in Rocket.Chat

## Metadata
- **Source:** HackerOne
- **Report:** 1130721 | https://hackerone.com/reports/1130721
- **Submitted:** 2021-03-19
- **Reporter:** sonarsource
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** NoSQL Injection, Information Disclosure, Authentication Bypass, Account Takeover, Remote Code Execution
- **CVEs:** CVE-2021-22911
- **Category:** memory-binary

## Summary
The getPasswordPolicy method in Rocket.Chat versions 3.8.0+ fails to sanitize the token parameter, allowing unauthenticated attackers to perform blind NoSQL injection attacks using MongoDB's $regex operator. By leaking password reset tokens character-by-character, attackers can take over any user account (particularly admin accounts) and subsequently achieve Remote Code Execution through webhook script execution.

## Attack scenario
1. Attacker requests a password reset for target user's account (requires knowing email address)
2. Attacker performs blind NoSQL injection using $regex operator on token parameter to leak reset token character-by-character via getPasswordPolicy method
3. Attacker resets target user's password using leaked token (works if 2FA/email verification disabled)
4. Attacker logs in as takeover account; if admin, gains administrative privileges
5. Attacker creates incoming webhook with malicious script payload through admin panel
6. Attacker triggers webhook execution to achieve Remote Code Execution on server

## Root cause
The getPasswordPolicy method accepts user-controlled token parameter without validation/sanitization and passes it directly to MongoDB query operations. The parameter is not type-checked as a string, allowing injection of MongoDB operators like $regex. The endpoint is callable without authentication via /api/v1/method.callAnon.

## Attacker mindset
An attacker would recognize that password reset tokens are high-value targets for account takeover, and the blind NoSQL injection technique allows systematic extraction without triggering obvious security alerts. Targeting admin accounts specifically maximizes impact by leveraging legitimate admin features (webhooks) for code execution.

## Defensive takeaways
- Implement strict input validation: enforce that token parameter is exactly a string type, reject objects/operators
- Apply allowlist validation for token format (e.g., regex matching expected token pattern)
- Require authentication or implement rate limiting on password reset operations
- Enforce 2FA (email verification + TOTP) on all accounts, especially admin accounts
- Sanitize all user inputs before using in database queries; use parameterized queries/schema validation
- Implement query depth limiting and operator filtering at query layer
- Restrict webhook script execution contexts with sandboxing or disable arbitrary script execution
- Log and alert on suspicious password reset patterns or repeated token validation attempts

## Variant hunting
Search for other unauthenticated endpoints accepting user input for database queries (especially with callAnon)
Review all password reset/token validation flows for similar injection patterns
Audit other NoSQL database operations for missing input sanitization
Check for similar issues in other Meteor.js methods that process complex objects
Investigate webhook execution contexts for other code execution vectors
Test other parameters in getPasswordPolicy and related auth methods for injection

## MITRE ATT&CK
- T1190
- T1190
- T1586
- T1110
- T1059
- T1098
- T1199
- T1021

## Notes
Vulnerability introduced in commit b950f17 and present since version 3.8.0. Proof-of-concept exploit provided. The attack chain demonstrates critical severity: unauthenticated token leak + account takeover + RCE. Mitigation suggestion of type-checking is oversimplified; comprehensive input validation and authentication enforcement needed. Video demonstration of full exploitation provided with report.

## Full report
<details><summary>Expand</summary>

**Summary:**
The `getPasswordPolicy` method is vulnerable to NoSQL injection attacks and does not require authentication/authorization. It can be used to take over accounts by leaking password reset tokens. Taking over an admin account leads to Remote Code Execution.

**Description:**
The `getPasswordPolicy` method does not properly validate or sanitize the `token` parameter and can thus be used to perform a blind NoSQL injection. It can be called without authentication (which seems intended), e.g. by using the `/api/v1/method.callAnon` API endpoint

By using [MongoDB's `$regex` operator](https://docs.mongodb.com/manual/reference/operator/query/regex/), a password reset token can be leaked character by character. Example: in order to check if the password reset token begins with a specific letter, e.g. `A`, the attacker would send the JSON object `{"$regex":"^A"}` as the `token` parameter. The response contains the server's password policy when the guess was correct, or an error otherwise. This can be repeated for all possible characters and for each position in the token, until the whole token is known. See the `pwpolicy_leak_token` function in the attached exploit for an implementation of this.

In order to take over an account, an attacker would perform the following high-level steps:
1. Request a password reset for the target user's account. This requires the attacker to know the target user's email address.
1. Leak the password reset token as explained above
1. Reset the target user's password to an attacker known one using the password reset token. The target user cannot have email or TOTP 2FA enabled in order for this step to work.

To gain Remote Code Execution capabilities on the server, an attacker can follow these steps to take over an admin account. The attacker can then use the newly gained admin privileges to create an incoming web hook that has a script. This allows them  to get execute commands or get a shell on the server, because the script is executed on the server without a security boundary in place (which seems to be intended).

See `pre_auth_nosqli.py` for a reference exploit and the attached video for a demonstration of it.

The vulnerable code can be found here: [getPasswordPolicy.js:8](https://github.com/RocketChat/Rocket.Chat/blob/eba1e9b3146e5102baed000953c2cb51930c345c/server/methods/getPasswordPolicy.js#L8)

## Releases Affected:
- Tested on 3.12.1
- Seems to be affected since 3.8.0 as the vulnerability was introduced in [commit b950f17](https://github.com/RocketChat/Rocket.Chat/commit/b950f17e4225efb99b7b80022877f9b2cdf14b64?branch=b950f17e4225efb99b7b80022877f9b2cdf14b64#diff-2fc491cc6f1ca015c2e3f7c36ee12f8d7c7e40907257fd5256d3f39e85c12b88R8)

## Steps To Reproduce (from initial installation to vulnerability):
1. Install Python3 (required by the exploit)
1. Install the Python dependencies required by the exploit: `pip3 install requests`
1. Set up an instance of RocketChat 3.12.1, e.g. by cloning the repo and using Docker Compose:
  1. `git clone git@github.com:RocketChat/Rocket.Chat.git`
  1. `cd Rocket.Chat`
  1. `git checkout tags/3.12.1`
  1. `docker-compose up -d`
1. Configure the instance with default settings, remember the admin's email address (e.g. `admin@rocketchat.local`)
1. Disable all 2FA methods on the admin account
1. Run the reference exploit against the instance, provide the admin's email address: `python3 pre_auth_nosqli.py 'http://localhost:3000' 'admin@rocketchat.local'`
1. The exploit should provide an interactive shell on the the server, use it to verify that you can execute commands as the rocketchat user: `whoami`

## Supporting Material/References:
The attached proof-of-concept video shows the setup and exploitation of a fresh Rocket.Chat instance.
This is the exploit's output:
```
 ___  ___  _ __   __ _ _ __ ___  ___  _   _ _ __ ___ ___ 
/ __|/ _ \| '_ \ / _` | '__/ __|/ _ \| | | | '__/ __/ _ \
\__ \ (_) | | | | (_| | |  \__ \ (_) | |_| | | | (_|  __/
|___/\___/|_| |_|\__,_|_|  |___/\___/ \__,_|_|  \___\___|

[+] Requesting password reset for "admin@rocketchat.local"...
[*] Leaking password reset token...
[+] Leaked password reset token: 0q9oakr3Lc94p3AnUjtQGlBm4bqJF3AndFYOjIg94ld
[+] Resetting password to "f7c87ed1559f2fe101ee"...
[+] Admin account takeover successful!
[+] Creating hook "backdoor-8624225d" with secret "8e2b809f6d1e9c561f9625d362726672"...
[*] Hook: T4nRot8nRvgEDp6rn/6sfs8GYcZCmH7SjKeazsexGmCJjFdLwWMdsqyz9hTcPFYxKF
[+] Dropping into shell:
$ whoami
rocketchat
$ id
uid=65533(rocketchat) gid=65533(rocketchat) groups=65533(rocketchat)
$ 
```

## Suggested mitigation
Ensure that the user-provided `token` parameter is a string.

## Disclosure Policy
All reported issues are subject to a 90 day disclosure deadline. 
After 90 days elapse, parts of the bug report will become visible to the public.

Don't hesitate to ask if you have any questions or need further help with this issue.

## Impact

An attacker can use this vulnerability to target an admin user and take over their account, which is already a high impact. The attacker can then use certain features that are available to admins in order to gain Remote Code Execution capabilities. This is demonstrated in the reference exploit by creating an incoming web hook that executes the attacker's payload in the context of the server process.

This gives them complete control over the Rocket.Chat instance and exposes all attached components, e.g. the database or any external system whose credentials are stored within Rocket.Chat settings. An attacker can read, change, or delete all items in the database, impacting confidentiality, integrity and availability.

</details>

---
*Analysed by Claude on 2026-05-12*
