# IDOR - Delete all Licenses and certifications from users account using CreateOrUpdateHackerCertification GraphQL query

## Metadata
- **Source:** HackerOne
- **Report:** 2122671 | https://hackerone.com/reports/2122671
- **Submitted:** 2023-08-24
- **Reporter:** harshdranjan
- **Program:** Unknown
- **Bounty:** $12,500
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Hey team,

While editing our **Licenses and certifications** if we change the ID number we can delete other users **Licenses and certifications**. it simply can be done by editing the ID number in our graphql query.
If change the ID from 1 to X possible range then we can delete all the **Licenses and certifications** present between these.


### Steps To Reproduce

1. Log in to your o

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
Hey team,

While editing our **Licenses and certifications** if we change the ID number we can delete other users **Licenses and certifications**. it simply can be done by editing the ID number in our graphql query.
If change the ID from 1 to X possible range then we can delete all the **Licenses and certifications** present between these.


### Steps To Reproduce

1. Log in to your own account in two browsers A and B with User A and User B
2. Create your own **Licenses and certifications* in both the account
3. Now edit your own **Licenses and certifications* and Intercept this using a Burp Proxy 
4. Now In the body change the **ID** number and you will be able to delete all the **Licenses and certifications** present in HackerOne 
5. For now change the ID to the **Licenses and certifications** ID of the Other account and it will be deleted.

PoC Video: ████

## Impact

Able to delete all the **Licenses and certifications** present in HackerOne

</details>

---
*Analysed by Claude on 2026-05-24*
