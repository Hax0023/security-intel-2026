# Posting to Twitter CSRF on php/post_twitter_authenticate.php

## Metadata
- **Source:** HackerOne
- **Report:** 249234 | https://hackerone.com/reports/249234
- **Submitted:** 2017-07-13
- **Reporter:** kuromatae
- **Program:** Unknown
- **Bounty:** $50
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi !

This time, i found a CSRF who can lead to arbitrary writing on twitter account of victim if they have added it to zomato :)

Coupled with a stored XSS, it could be very troublesome to you.

In the page, it seems there is no token check at all.

You can see in the video the CSRF working and here is the POC i used:

`https://www.zomato.com/php/post_twitter_authenticate.php?type=posttweet&messa

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

Hi !

This time, i found a CSRF who can lead to arbitrary writing on twitter account of victim if they have added it to zomato :)

Coupled with a stored XSS, it could be very troublesome to you.

In the page, it seems there is no token check at all.

You can see in the video the CSRF working and here is the POC i used:

`https://www.zomato.com/php/post_twitter_authenticate.php?type=posttweet&message=Hello Zomato Team :)`

Cordially,

Kuromatae.

</details>

---
*Analysed by Claude on 2026-05-24*
