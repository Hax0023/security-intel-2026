# Deleted Post and Administrative Function Access in eCommerce Forum

## Metadata
- **Source:** HackerOne
- **Report:** 167846 | https://hackerone.com/reports/167846
- **Submitted:** 2016-09-12
- **Reporter:** ysx
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Hi,

I initially queried the following report as a comment in #165048, in which @juanbroullon confirmed the issue appeared valid and requested I open a new Shopify report.

A selection of privileged information is provided upon appending `/edit` to a user profile URL on the eCommerce forum (as an authenticated user).

As such, it appears that I am able to view the user's entire history of posts as

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

Hi,

I initially queried the following report as a comment in #165048, in which @juanbroullon confirmed the issue appeared valid and requested I open a new Shopify report.

A selection of privileged information is provided upon appending `/edit` to a user profile URL on the eCommerce forum (as an authenticated user).

As such, it appears that I am able to view the user's entire history of posts as an administrator, including those which have been deleted (possibly similar to the case of #135756):

## Proof of Concept URLs

* https://ecommerce.shopify.com/users/1/edit
* https://ecommerce.shopify.com/users/1/posts
* https://ecommerce.shopify.com/users/1/posts?filter=spam

Please let me know if you require any additional details regarding this.

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
