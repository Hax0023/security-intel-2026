# Site-wide CSRF at Atavist 

## Metadata
- **Source:** HackerOne
- **Report:** 951292 | https://hackerone.com/reports/951292
- **Submitted:** 2020-08-04
- **Reporter:** bugra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** csrf
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi team,
I have a Atavist Magazine account. And there are no CSRF tokens on account settings.

For example ;
- When changing email (there is a user ID but they are sequential) : {F936597}

- Deleting credit card : {F936618}

- Cancelling subscription : https://magazine.atavist.com/cms/ajax/cancel_subscription.php?product_id=com.theatavist.atavist.subscription.membership - this endpoint

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
Hi team,
I have a Atavist Magazine account. And there are no CSRF tokens on account settings.

For example ;
- When changing email (there is a user ID but they are sequential) : {F936597}

- Deleting credit card : {F936618}

- Cancelling subscription : https://magazine.atavist.com/cms/ajax/cancel_subscription.php?product_id=com.theatavist.atavist.subscription.membership - this endpoint sends an email with `We'll Miss You` title, but it doesn't cancel the subscription. (this is not related to CSRF, there is a CSRF but the endpoint is weird :-D)

I didn't want to create report for each endpoint, because this is a site-wide issue. I think you can add a header for root fix.

## Impact

Site-wide CSRF 

Thanks,
Bugra

</details>

---
*Analysed by Claude on 2026-05-24*
