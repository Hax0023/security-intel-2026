# Login Hints on Admin Panel - User Enumeration via Differential Error Messages

## Metadata
- **Source:** HackerOne
- **Report:** 188195 | https://hackerone.com/reports/188195
- **Submitted:** 2016-12-04
- **Reporter:** madhur_bhargava
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** User Enumeration, Information Disclosure, Insufficient Error Handling
- **CVEs:** None
- **Category:** uncategorised

## Summary
The WordPress login panel at wp-login.php returns different error messages based on whether a username exists in the system, allowing attackers to enumerate valid usernames. An attacker receives 'Invalid Username' for non-existent accounts but 'The password you entered for username [X] is incorrect' for valid accounts, effectively revealing which accounts exist.

## Attack scenario
1. Attacker navigates to the WordPress login panel at wp-login.php
2. Attacker attempts login with a random username and password combination
3. System returns 'Invalid Username' error message, indicating the account does not exist
4. Attacker tries with another username and receives error message 'The password you entered for username frank is incorrect'
5. Attacker now knows 'frank' is a valid username and can focus brute force attacks on known accounts
6. Attacker uses the enumerated valid usernames for targeted attacks such as password spraying, phishing, or password reset spam

## Root cause
The login form provides differential error messages that distinguish between invalid usernames and incorrect passwords. This allows attackers to infer account existence based on the specific error message returned, violating the principle of generic error handling.

## Attacker mindset
An attacker would systematically enumerate valid usernames by testing common names or wordlists against the login form, collecting a list of valid accounts to focus further attacks on. This pre-reconnaissance significantly reduces the effort required for brute force or social engineering attacks.

## Defensive takeaways
- Return generic error messages for all authentication failures (e.g., 'Invalid username or password')
- Implement rate limiting and account lockout mechanisms after failed authentication attempts
- Log suspicious authentication attempts and monitor for enumeration patterns
- Disable or restrict access to the WordPress admin panel at /wp-admin/ and /wp-login.php from non-trusted IPs
- Consider implementing CAPTCHA challenges after multiple failed login attempts
- Use security headers and implement Web Application Firewalls (WAF) to detect and block enumeration attacks

## Variant hunting
Search for similar enumeration vulnerabilities in other authentication endpoints: password reset forms (which may reveal account existence when sending reset emails), user registration pages (confirming existing accounts), account recovery features, and API authentication endpoints that provide user-specific error responses.

## MITRE ATT&CK
- T1592
- T1589
- T1590
- T1619

## Notes
This is a classic user enumeration vulnerability commonly found in web applications. While seemingly low-severity, user enumeration is frequently the first step in multi-stage attacks. The vulnerability exists on a public-facing login panel, making it easily discoverable and exploitable at scale. The reporter correctly identified the risk of password reset spam and targeted brute force attacks on enumerated accounts.

## Full report
<details><summary>Expand</summary>

Hi,

Hope you are doing fine.
I wanted to inform you regarding the enabling of the login hints on your wp-admin panel(https://nextcloud.com/wp-login.php).

Vulnerability: The admin panel shows very "specific" hint information if a hacker tries for a bruteforcing attack.

Steps to reproduce:
1. Navigate to: https://nextcloud.com/wp-login.php 

2. Enter username: "charlietango" 
    Enter password: "charlietango"
    A specific error message is shown stating "Invalid Username".(See attachment: xnc_user_err.png)

3. Now enter the following credentials:
    Enter username: "frank" 
    Enter password: "charlietango"
   A specific error message is shown stating "The password you entered for username frank is incorrect".   (See attachment: xnc_user_exist.png)

Why is this important:
As per step 3, Now the attacker knows that "frank" is an existing user in the system and multitude of attacks can be launched. At the very least, the attacker can spam the user's mailbox with several lost password requests. I believe this is not good and should be fixed.

Please do let me know your thoughts on this or if you need any more information.

Thank You,
Madhur 

</details>

---
*Analysed by Claude on 2026-05-24*
