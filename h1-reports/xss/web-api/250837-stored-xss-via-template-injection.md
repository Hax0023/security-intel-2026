# Stored xss via template injection

## Metadata
- **Source:** HackerOne
- **Report:** 250837 | https://hackerone.com/reports/250837
- **Submitted:** 2017-07-18
- **Reporter:** morningstar
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Sir , I found Stored XSS in https://mercantile.wordpress.org/
POC is attached .
Steps to reproduce:
1.Login to your account.
2. Go to https://mercantile.wordpress.org/my-account/edit-address/ & fill details , press save & intercept this request in burp suit.
3.change name to {{constructor.constructor('alert(1)')()}} & forward request. as shown in screenshot.
Xss will popup when you visit you

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

Hello Sir , I found Stored XSS in https://mercantile.wordpress.org/
POC is attached .
Steps to reproduce:
1.Login to your account.
2. Go to https://mercantile.wordpress.org/my-account/edit-address/ & fill details , press save & intercept this request in burp suit.
3.change name to {{constructor.constructor('alert(1)')()}} & forward request. as shown in screenshot.
Xss will popup when you visit your account page.
 
    Although its self XSS. but  following attack  scenario makes it useful.
Anyone can make account on https://mercantile.wordpress.org/ using someone else email id, Its not verifying whether its your email id or not. Lets consider "A" makes account with "B" persons email & by using this technique store XSS payload in its account. After that "B" wants account on mercantile.wordpress.org with same email. so rather creating account with new email, "B" person just do forget password & recover & recover his account. but xss payload is still there in his account so attacker "A" can access victim "B" account anytime.
        One more thing, even after changing name with https://mercantile.wordpress.org/my-account/edit-account/ setting payload is not removed its still there. so its make attack more sophisticated. 
     
Thanks & Regards,
Akshay

</details>

---
*Analysed by Claude on 2026-05-24*
