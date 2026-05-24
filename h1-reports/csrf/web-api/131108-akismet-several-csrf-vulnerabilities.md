# Akismet Several CSRF vulnerabilities

## Metadata
- **Source:** HackerOne
- **Report:** 131108 | https://hackerone.com/reports/131108
- **Submitted:** 2016-04-15
- **Reporter:** eboda
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Summary
-----------

Akismet is vulnerable to CSRF allowing an attacker to cancel accounts of victims, add sites, remove subscriptions, etc.


Steps to reproduce *Account cancelation*
-----------

1. Login to your Akismet account, which has a subscription activated.
2. The following POST request will cancel the subscription and the account:

    `https://akismet.com/api/account/1/cancel`

The `1` 

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

Summary
-----------

Akismet is vulnerable to CSRF allowing an attacker to cancel accounts of victims, add sites, remove subscriptions, etc.


Steps to reproduce *Account cancelation*
-----------

1. Login to your Akismet account, which has a subscription activated.
2. The following POST request will cancel the subscription and the account:

    `https://akismet.com/api/account/1/cancel`

The `1` can be replaced with any number. The userid was originally there, but I noticed that it actually just gets ignored.


Steps to reproduce other CSRF
--------------------
Basically all actions on Akismet are vulnerable to CSRF. Here are some further examples (`1` can be replaced with 2, 3, etc):

### Adding a site to a subscription:

```
POST /api/activation/create

subscriptionId=1&site_url=foo.bar
```
*foo.bar* is now added to subscription *1*

### Cancel specific subscription:

```POST /api/subscription/1/cancel```
   
Subscription *1* is now canceled.



</details>

---
*Analysed by Claude on 2026-05-24*
