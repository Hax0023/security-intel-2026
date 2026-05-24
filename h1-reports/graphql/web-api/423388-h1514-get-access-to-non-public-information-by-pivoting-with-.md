# H1514 Get access to non public information by pivoting with graphql queries

## Metadata
- **Source:** HackerOne
- **Report:** 423388 | https://hackerone.com/reports/423388
- **Submitted:** 2018-10-13
- **Reporter:** emitrani
- **Program:** Unknown
- **Bounty:** $1,500
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hi security team,

**Summary:** It is possible to pivot with queries to get access to information you shouldn't have access to according to docs located at https://help.shopify.com/en/api/graphql-admin-api/reference/queryroot

**Description:** I will try to write up all the ones I can find related to information disclosure where a user with only access to Apps can get from other parts of the store

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

Hi security team,

**Summary:** It is possible to pivot with queries to get access to information you shouldn't have access to according to docs located at https://help.shopify.com/en/api/graphql-admin-api/reference/queryroot

**Description:** I will try to write up all the ones I can find related to information disclosure where a user with only access to Apps can get from other parts of the store using the graphiql app.

* Example 1:
User with no home access can use locations query to find out store locations and address
{F360024}
It is also possible to use inventoryLevel(inventoryItemId) to get access to inventory without access

* Example 2:
Marketing activities with no marketing access
{F360044}
even though it is possible to ask for more this is the basic query I used. Note it doesn't say access denied.
`query{marketingActivities(first:100){edges{node{id,title, createdAt, budget{total{amount}}}}}}`

* Example 3:
Publications and api keys(I suspect app access makes you see api keys but still)
{F360060}
Query I used:
`query{publications(first: 100){edges{node{name, id, supportsFuturePublishing, app{apiKey}}}}}`

## Impact

This means the graphql can be used to disclose information about other parts of the store that a low permissions user shouldn't have access to.

Best,
Eray

</details>

---
*Analysed by Claude on 2026-05-24*
