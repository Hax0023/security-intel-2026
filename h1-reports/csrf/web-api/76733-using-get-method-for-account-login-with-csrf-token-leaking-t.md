# Using GET method for account login with CSRF token leaking to external sites Via Referer.

## Metadata
- **Source:** HackerOne
- **Report:** 76733 | https://hackerone.com/reports/76733
- **Submitted:** 2015-07-19
- **Reporter:** bugs3ra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
HI

At the time of login, the values are present in URL along with the CSRF token.  Also this URL is leaking to external sites in HTTP REFRERER. 

Here are some of those sites:
dxzc9stvaxhhy.cloudfront.net
bam.nr-data.net
ssl.google-analytics.com
usage.trackjs.com
api.mixpanel.com


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

HI

At the time of login, the values are present in URL along with the CSRF token.  Also this URL is leaking to external sites in HTTP REFRERER. 

Here are some of those sites:
dxzc9stvaxhhy.cloudfront.net
bam.nr-data.net
ssl.google-analytics.com
usage.trackjs.com
api.mixpanel.com


</details>

---
*Analysed by Claude on 2026-05-24*
