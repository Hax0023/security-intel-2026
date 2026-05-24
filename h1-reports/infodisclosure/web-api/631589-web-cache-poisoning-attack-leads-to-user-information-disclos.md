# Web Cache poisoning attack leads to User information Disclosure and more

## Metadata
- **Source:** HackerOne
- **Report:** 631589 | https://hackerone.com/reports/631589
- **Submitted:** 2019-06-28
- **Reporter:** deksterh11
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** web-api

## Summary
Hello

Your Web-Server is vulnerable to web cache poisoning attacks.
This means, that the attacker are able to get another user Information.

If you are logged in and visit this website (For example):
https://www.lyst.com/shop/trends/mens-dress-shoes/blahblah.css

Then the server will store the information in the cache, BUT with the logged in user information.
A non-logged-in user can then visit t

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

Hello

Your Web-Server is vulnerable to web cache poisoning attacks.
This means, that the attacker are able to get another user Information.

If you are logged in and visit this website (For example):
https://www.lyst.com/shop/trends/mens-dress-shoes/blahblah.css

Then the server will store the information in the cache, BUT with the logged in user information.
A non-logged-in user can then visit this website and see the information contained therein.

In that case, this url: https://www.lyst.com/shop/trends/mens-dress-shoes/blahblah.css can be visited in Private Mode and still you will be shown as "LOGGED IN" and then check the Source code you will get your email, member id ,etc..


Some informations about the attack:
https://www.blackhat.com/docs/us-17/wednesday/us-17-Gil-Web-Cache-Deception-Attack.pdf

The screenshots with the steps are in the attachments.

## Impact

Web cache poisoning attack can be used to steal user informations like email, name and member id which is important for the login security feature.

</details>

---
*Analysed by Claude on 2026-05-24*
