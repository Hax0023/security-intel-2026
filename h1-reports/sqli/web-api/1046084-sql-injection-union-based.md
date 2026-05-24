# SQL Injection Union Based

## Metadata
- **Source:** HackerOne
- **Report:** 1046084 | https://hackerone.com/reports/1046084
- **Submitted:** 2020-11-28
- **Reporter:** fuzzme
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** sqli
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:

Hello, 

I have found a SQL Injection Union Based on `https://intensedebate.com/commenthistory/$YourSiteId `
The `$YourSiteId` into the url is vulnerable to SQL Injection.

## Steps to reproduce

1.  Logging into `https://intensedebate.com`

2. After create your own site on `https://intensedebate.com/install` and follow all steps

3. Now you need to know your site id, to get then you 

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

## Summary:

Hello, 

I have found a SQL Injection Union Based on `https://intensedebate.com/commenthistory/$YourSiteId `
The `$YourSiteId` into the url is vulnerable to SQL Injection.

## Steps to reproduce

1.  Logging into `https://intensedebate.com`

2. After create your own site on `https://intensedebate.com/install` and follow all steps

3. Now you need to know your site id, to get then you need go to `https://intensedebate.com/user-dashboard` and you can see on the right side of the page your site list, choice your site and click to the link `Overview`.
You will be redirected to `https://intensedebate.com/dash/$YourSiteId`.

4. Now you have your site id,  go to the vulnerable URL with your site id `https://intensedebate.com/commenthistory/$YourSiteId`.
 
5. Now Trigger the SQL Injection with this following link `https://intensedebate.com/commenthistory/$YourSiteId%20union%20select%201,2,@@VERSION%23` (!) You need to do this with your own site id (!)

6. Now you can see `10.1.32-MariaDB` on the page.

## POC 

@@VERSION

{F1096977}

current_user()

{F1096976}

Video POC

## IMPORTANT
Can you see my comment into [#1044698](https://hackerone.com/reports/1044698) ??
 And I no longer want to put all SQL Injection issues on into my initial report [#1042746](https://hackerone.com/reports/1042746), because i don't win any reputations 

Thank you,

Fuzzme.

## Impact

Full database access holding private user information and Reflected Cross-Site-Scripting

</details>

---
*Analysed by Claude on 2026-05-24*
