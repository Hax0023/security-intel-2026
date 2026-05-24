# Authentication Bypassing and Sensitive Information Disclosure on Verify Email Address in Registration Flow

## Metadata
- **Source:** HackerOne
- **Report:** 124151 | https://hackerone.com/reports/124151
- **Submitted:** 2016-03-18
- **Reporter:** vivek-p
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The zomato.com web application is vulnerable to authentication bypassing and sensitive information disclosure.

The flaw exist in “Verify Email Address” link which is received in a mail after registration. Once the user enters Full Name, Email Address and Password during registration, he/she is either asked to enter a 4 digit code or directly verify email address by clicking the red button for suc

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

The zomato.com web application is vulnerable to authentication bypassing and sensitive information disclosure.

The flaw exist in “Verify Email Address” link which is received in a mail after registration. Once the user enters Full Name, Email Address and Password during registration, he/she is either asked to enter a 4 digit code or directly verify email address by clicking the red button for successful account activation/creation.
The verify email address link doesn’t expire even after successful user registration/account activation which allows a malicious user to authenticate into the victim’s session without password. When an user clicks on verify email address link, he/she is directly authenticated without a need of password, thereby bypassing authentication. Also, the verify email address link consist of ‘fbcid’ parameter which is just Base64 encoded. It leaks sensitive data like unique user id, 4 digit code and email address of the user. All these three parameter are being passed in URL itself (GET request).The application is authenticating a user using these three parameter without a need of a password. 

The verify email address GET URL consisting of sensitive data like unique user id, 4 digit code and email address gets stored in cache, browser history, web server logs. If the victim has accessed this link or activated his account from a public computer/cyber cafe, any user with malicious intent can access and misuse this url in order to authenticate into the victim session without a need of a password. 


</details>

---
*Analysed by Claude on 2026-05-24*
