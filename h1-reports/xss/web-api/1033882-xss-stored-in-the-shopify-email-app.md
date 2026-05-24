# XSS stored in the Shopify Email app

## Metadata
- **Source:** HackerOne
- **Report:** 1033882 | https://hackerone.com/reports/1033882
- **Submitted:** 2020-11-13
- **Reporter:** tomorrow_future
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
step:

1、install app `Shopify Email`
{F1076928}

2、Click `General` under `Settings`

3、Change phone number to `1234567"><img src=a onerror=alert(1)>`
{F1076939}

4、Open shopify email app and create an email

5、Show phone number
{F1076940}

6、watch the vedio poc for more information

## Impact

store xss

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

step:

1、install app `Shopify Email`
{F1076928}

2、Click `General` under `Settings`

3、Change phone number to `1234567"><img src=a onerror=alert(1)>`
{F1076939}

4、Open shopify email app and create an email

5、Show phone number
{F1076940}

6、watch the vedio poc for more information

## Impact

store xss

</details>

---
*Analysed by Claude on 2026-05-24*
