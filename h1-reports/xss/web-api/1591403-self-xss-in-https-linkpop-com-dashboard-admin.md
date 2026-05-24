# Self XSS in https://linkpop.com/dashboard/admin

## Metadata
- **Source:** HackerOne
- **Report:** 1591403 | https://hackerone.com/reports/1591403
- **Submitted:** 2022-06-04
- **Reporter:** hazemhussien99
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:

Hello Shopify team,
Found a self XSS  https://linkpop.com/dashboard/admin, the steps to reproduce are below

## Steps To Reproduce:
1- Visit https://linkpop.com/dashboard/admin
2- Click on links => add links
3- add in the url  input `javascript:alert(document.cookie)`
{F1757141}
4- Click on the link that appeared on the phone image and the alert will appear
{F1757140}
{F1757142}

In y

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

Hello Shopify team,
Found a self XSS  https://linkpop.com/dashboard/admin, the steps to reproduce are below

## Steps To Reproduce:
1- Visit https://linkpop.com/dashboard/admin
2- Click on links => add links
3- add in the url  input `javascript:alert(document.cookie)`
{F1757141}
4- Click on the link that appeared on the phone image and the alert will appear
{F1757140}
{F1757142}

In your policy page you say that you guys accept self xss as long as its two steps, here its only paste payload in input and click on image so hopefully in scope :)

## Impact

Self XSS.

</details>

---
*Analysed by Claude on 2026-05-24*
