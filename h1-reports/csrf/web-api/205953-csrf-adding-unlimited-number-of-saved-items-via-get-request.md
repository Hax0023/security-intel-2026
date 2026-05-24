# CSRF - Adding unlimited number of saved items via GET request

## Metadata
- **Source:** HackerOne
- **Report:** 205953 | https://hackerone.com/reports/205953
- **Submitted:** 2017-02-13
- **Reporter:** inhibitor181
- **Program:** Unknown
- **Bounty:** $150
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello, I have found a way of potentially adding thousands of items to the saved items list by using a GET request.

POC
-----------
```
GET /email-capture/stock-alert/93543518/?return_url=/email-capture/stock-alert/91703404/?return_url=/email-capture/stock-alert/89201857/ HTTP/1.1
Host: www.lyst.com
```

By adding a stock alert notification to an item, the respective item is automatically added in

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

Hello, I have found a way of potentially adding thousands of items to the saved items list by using a GET request.

POC
-----------
```
GET /email-capture/stock-alert/93543518/?return_url=/email-capture/stock-alert/91703404/?return_url=/email-capture/stock-alert/89201857/ HTTP/1.1
Host: www.lyst.com
```

By adding a stock alert notification to an item, the respective item is automatically added in the saved list and because this is a GET request, there is no CSRF token/protection here.

IMPACT
-------
Because this is done via GET request it is very easy to add thousands of products in the target user account by making one or both of these:
1. Chain your internal redirect requests (shown in POC)
2. Simply embed 1000x 1px image that with the target link (of course different product id per image)

Because of the extreme volume of the added items, the attacker can make the target's save list simply unusable (he must then delete 1000 entries and NO ONE will do that). I think a lot of people are taking advantage of the list, so a CSRF here can have a pretty big/annoying impact and you could loose clients.

Video POC attached.



</details>

---
*Analysed by Claude on 2026-05-24*
