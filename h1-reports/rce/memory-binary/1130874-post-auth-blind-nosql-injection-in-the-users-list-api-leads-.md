# Post-Auth Blind NoSQL Injection in users.list API leads to Remote Code Execution

## Metadata
- **Source:** HackerOne
- **Report:** 1130874 | https://hackerone.com/reports/1130874
- **Submitted:** 2021-03-19
- **Reporter:** sonarsource
- **Program:** Rocket.Chat
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** NoSQL Injection, Information Disclosure, Account Takeover, Remote Code Execution, Authentication Bypass
- **CVEs:** CVE-2021-22910
- **Category:** memory-binary

## Summary
The users.list API endpoint in Rocket.Chat fails to properly sanitize the 'query' parameter, allowing authenticated attackers to perform blind NoSQL injection attacks using MongoDB's $where operator. By leaking password reset tokens and 2FA secrets from admin accounts, attackers can gain complete account takeover and subsequently achieve Remote Code Execution through admin webhook script execution.

## Attack scenario
1. Attacker authenticates as a low-privilege user to access the users.list endpoint
2. Attacker crafts NoSQL injection payloads using $where operator to leak admin user email and password hash
3. Attacker requests password reset for the targeted admin account via legitimate mechanism
4. Attacker performs blind NoSQL injection to leak the password reset token character-by-character using regex matching oracles
5. Attacker leaks TOTP 2FA secret or email 2FA token hash through similar injection techniques
6. Attacker resets admin password using leaked token and 2FA secrets, then creates malicious webhook with server-side script execution to achieve RCE

## Root cause
The users.list API endpoint at users.js:230 accepts a user-controlled 'query' parameter that is passed directly to MongoDB queries without validation or parameterization. The $where operator is enabled, allowing arbitrary JavaScript execution in query context. Output field restrictions do not prevent exploitation since the injection occurs in the query logic itself, not the projection.

## Attacker mindset
An authenticated attacker with minimal privileges can systematically extract sensitive authentication credentials through time-based/response-based blind injection techniques. The attacker recognizes that MongoDB's $where operator provides a powerful oracle for character-by-character data exfiltration, and understands the privilege escalation chain from user account takeover to admin RCE through webhook functionality.

## Defensive takeaways
- Never pass user-controlled input directly to database query builders; use parameterized queries and schema validation frameworks
- Disable dangerous MongoDB operators like $where in production unless absolutely necessary, as they enable arbitrary code execution
- Implement strict allowlist-based query parameter validation using JSON schema or similar mechanisms
- Enforce input type checking and reject unexpected data structures (e.g., objects when strings expected)
- Restrict webhook and scripting functionality with sandboxing, capability limits, and code review requirements
- Apply principle of least privilege to webhook execution context - do not run webhooks with application-level permissions
- Implement rate limiting and anomaly detection on API endpoints that could be used for data exfiltration
- Use ORM/ODM libraries with built-in protection against injection attacks rather than raw query construction
- Require re-authentication or additional authorization for sensitive operations like password reset
- Audit and log all query parameter usage, especially in security-sensitive endpoints

## Variant hunting
Look for similar patterns in other API endpoints accepting 'query' or 'filter' parameters that may pass input to MongoDB operators. Check for other uses of $where, $function, or eval-like operators. Examine webhook/script execution features in other applications for insufficient sandboxing. Hunt for blind injection vulnerabilities in other POST-auth endpoints using time-based or content-based oracles. Review password reset token generation and validation logic for similar weaknesses in other applications.

## MITRE ATT&CK
- T1190
- T1190
- T1557
- T1111
- T1555
- T1110
- T1078
- T1059
- T1046
- T1595

## Notes
This vulnerability requires prior authentication, limiting initial attack surface but enabling privilege escalation from low-privilege accounts. The blind injection technique using regex matching is particularly effective against MongoDB. The vulnerability existed since commit 3112d22 (version 0.49.0), indicating long-term exposure. The attack chain elegantly demonstrates how authentication bypass plus authorization escalation leads to RCE. The webhook RCE component suggests insufficient separation between administrative functionality and untrusted script execution contexts.

## Full report
<details><summary>Expand</summary>

**Summary:**
The `users.list` API endpoint is vulnerable to NoSQL injection attacks. It can be used to take over accounts by leaking password reset tokens and 2FA secrets. Taking over an admin account leads to Remote Code Execution.

**Description:**
The `users.list` API endpoint takes a custom query via the `query` URL query parameter. Although the returned fields are restricted, the query is not validated or sanitized properly and can thus be used to perform a blind NoSQL injection that can leak any field's value of any document in the `users` collection.

By using [MongoDB's `$where` operator](https://docs.mongodb.com/manual/reference/operator/query/where/), an attacker can build arbitrary oracles that can leak the value of any field of any user document. The query can be tailored to leak only the values of a specific account which makes it easy to target an admin account. Most notably an attacker can leak password reset tokens and 2FA secrets.

Example: in order to check if the password reset token of an admin user begins with a specific letter, e.g. `A`, the attacker would send the JSON object `{"$where":"this.roles.includes('admin') && /^A/.test(this.services.password.reset.token)"}` as the `query` parameter. The response contains the matching admin user when the guess was correct, or no users otherwise. This can be repeated for all possible characters and for each position in the token, until the whole token is known. See the `users_nosqli_blind_leak` function in the attached exploit for an implementation of this.

In order to take over another account, an attacker would perform the following high-level steps:
1. Leak the user's email address
1. Request a password reset for the target user's account
1. Leak the password reset token
1. Leak the TOTP 2FA secret or email 2FA token hash if necessary
1. Reset the target user's password to an attacker known one using the password reset token and any leaked 2FA tokens/secrets if necessary

To gain Remote Code Execution capabilities on the server, an attacker can follow these steps to take over an admin account. The attacker can then use the newly gained admin privileges to create an incoming web hook that has a script. This allows them  to execute commands or get a shell on the server, because the script is executed on the server without a security boundary in place (which seems to be intended).

The vulnerable code can be found here: [users.js:230](https://github.com/RocketChat/Rocket.Chat/blob/eba1e9b3146e5102baed000953c2cb51930c345c/app/api/server/v1/users.js#L230-L237)

See `post_auth_nosqli.py` for a reference exploit and the attached video for a demonstration of it.

## Releases Affected:
- Tested on 3.12.1
- Seems to be affected since 0.49.0 as the vulnerability was introduced in [commit 3112d22](https://github.com/RocketChat/Rocket.Chat/commit/3112d225fe1533dd77cfad7fff085d53d78c19f2#diff-84949efc4b8041a5ac51e7bcd0f2cd38b8fd3690f059235769ab437b453feab8R120)

## Steps To Reproduce (from initial installation to vulnerability):
1. Install Python3 (required by the exploit)
1. Install the Python dependencies required by the exploit: `pip3 install requests bcrypt`
1. Set up an instance of RocketChat 3.12.1, e.g. by cloning the repo and using Docker Compose:
  1. `git clone git@github.com:RocketChat/Rocket.Chat.git`
  1. `cd Rocket.Chat`
  1. `git checkout tags/3.12.1`
  1. `docker-compose up -d`
1. Configure the instance with default settings
1. Create a normal (non-admin) user with username `attacker` and password `attacker`
1. Run the reference exploit against the instance: `python3 post_auth_nosqli.py -u attacker -p attacker 'http://localhost:3000'`
1. The exploit should provide an interactive shell on the the server, use it to verify that you can execute commands as the rocketchat user: `whoami`

## Supporting Material/References:
The attached proof-of-concept video shows the setup and exploitation of a fresh Rocket.Chat instance.
**Please note:** The unsuccessful login at the end of the video does not mean that the exploit did not work, it just shows that the original admin password was restored (as stated in the exploits output). The exploit was successful, which can be seen by the output of the shell commands at the end of the exploit.

This is the exploit's output:
```
 ___  ___  _ __   __ _ _ __ ___  ___  _   _ _ __ ___ ___ 
/ __|/ _ \| '_ \ / _` | '__/ __|/ _ \| | | | '__/ __/ _ \
\__ \ (_) | | | | (_| | |  \__ \ (_) | |_| | | | (_|  __/
|___/\___/|_| |_|\__,_|_|  |___/\___/ \__,_|_|  \___\___|

[+] Found admin: username=admin id=56gyPQKt8Ff3Weowk
[*] Leaking email...
[+] Leaked email: admin@rocketchat.local
[*] Leaking password hash...
[+] Leaked password hash: $2b$10$ubhEIM/j6qLFNINHVbP.B.CJFCXagK7V5zD0Q8BYzs6UBlbBpiECa
[+] Requesting password reset...
[*] Leaking password reset token...
[+] Leaked password reset token: ET4sx905cF9pTZOsHFu6eRad7MwpYmqs-iTMWQIXAhv
[+] Resetting password to "DEbCf2b0A2BE79bBcDf1"...
[+] Admin account takeover successful!
[+] Creating hook "backdoor-9Fbd6E5A" with secret "AbE217B9d9e7Dd0CB2EB8dd30d26edfe"...
[*] Hook: 7bgxdkGHQYdBwtHWA/2S3EGB2ywWHM3aeYKu2q7akGF6TEjXEKMGK2Smggw7LpSLHc
[+] Restoring admin password...
[+] Dropping into shell:
$ whoami
rocketchat
$ id
uid=65533(rocketchat) gid=65533(rocketchat) groups=65533(rocketchat)
$ 
```

## Suggested mitigation
- Properly validate the `query` parameter:
  - Restrict the usage of MongoDB operators using an allowlist, especially top level operators like `$where`
  - Restrict the set of query-able fields using an allowlist (like the restriction on the returned fields)
- Check every API endpoint that uses the `parseJsonQuery()` function for similar vulnerabilities

## Disclosure Policy
All reported issues are subject to a 90 day disclosure deadline. 
After 90 days elapse, parts of the bug report will become visible to the public.

Don't hesitate to ask if you have any questions or need further help with this issue.

## Impact

An attacker can use this vulnerability to target an admin user and take over their account, which is already a high impact. The attacker can then use certain features that are available to admins in order to gain Remote Code Execution capabilities. This is demonstrated in the reference exploit by creating an incoming web hook that executes the attacker's payload in the context of the server process.

This gives them complete control over the Rocket.Chat instance and exposes all attached components, e.g. the database or any external system whose credentials are stored within Rocket.Chat settings. An attacker can read, change, or delete all items in the database, impacting confidentiality, integrity, and availability.

</details>

---
*Analysed by Claude on 2026-05-12*
