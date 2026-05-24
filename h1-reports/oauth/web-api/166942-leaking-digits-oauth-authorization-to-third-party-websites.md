# leaking Digits OAuth authorization to third party websites

## Metadata
- **Source:** HackerOne
- **Report:** 166942 | https://hackerone.com/reports/166942
- **Submitted:** 2016-09-08
- **Reporter:** akhil-reni
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
**Hi,**

While authenticating digits to my Fabric account i have noticed that the callback_url is not solid i.e. any sub domain or any path is accepted as callback_url with host as fabric.io.
This issue can be exploited by leaking the authorization token to third party websites (websites mentioned on kit's page)

**Steps to reproduce:**
- Go to https://www.digits.com/login?consumer_key=YlNgs6zwm4Q

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

**Hi,**

While authenticating digits to my Fabric account i have noticed that the callback_url is not solid i.e. any sub domain or any path is accepted as callback_url with host as fabric.io.
This issue can be exploited by leaking the authorization token to third party websites (websites mentioned on kit's page)

**Steps to reproduce:**
- Go to https://www.digits.com/login?consumer_key=YlNgs6zwm4QLmrzJBwRK3FcR5&callback_url=https://fabric.io/kits/ios/stripe&host=https://fabric.io
- Give access to Digits
- Now you will be redirected to https://fabric.io/kits/ios/stripe
- While on stripe kits page click on the stripe website URL (https://stripe.com)
- The authorization token will be leaked to stripe.com 
{F118436}

This issue can also be exploited on our organization member by actually leaking the consumer secret to our domain. 

**Steps to reproduce**
- Add the victim to your organization
- Create an crash issue under fabric
- add a note to that issue for ex: https://wesecureapp.com
- Note down the issue URL
{F118437}
Ex: https://fabric.io/img-srcx-onerrorprompt15/android/apps/app.myapplication/issues/56207e21f5d3a7f76bd5c20c
- Change the call back URL to issue url
https://www.digits.com/login?consumer_key=YlNgs6zwm4QLmrzJBwRK3FcR5&callback_url=https://fabric.io/img-srcx-onerrorprompt15/android/apps/app.myapplication/issues/56207e21f5d3a7f76bd5c20c&host=https://fabric.io
- Give digits permission
- You will be redirected to issue
- Now click the link in the notes and the OAuth token will be leaked to the attacker controlled domain.
{F118438}

**Regards,
Akhil**

</details>

---
*Analysed by Claude on 2026-05-24*
