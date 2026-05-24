# XSS in Widget Review Form Preview in settings

## Metadata
- **Source:** HackerOne
- **Report:** 1595905 | https://hackerone.com/reports/1595905
- **Submitted:** 2022-06-09
- **Reporter:** penguinshelp
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi team,

I found a XSS vulenrability in the widget review form preview. The payload is added in the success message and triggers when you preview the form

## Steps To Reproduce:

  1. Login to your Shopify account and open Judge.Me App
  1. Go to 'Settings' -> 'Review Widget' -> 'Widget Form'
  1. Go the the success message and add this XSS payload to the text: "><img src=x onerror=a

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

I found a XSS vulenrability in the widget review form preview. The payload is added in the success message and triggers when you preview the form

## Steps To Reproduce:

  1. Login to your Shopify account and open Judge.Me App
  1. Go to 'Settings' -> 'Review Widget' -> 'Widget Form'
  1. Go the the success message and add this XSS payload to the text: "><img src=x onerror=alert(document.domain)>
  1. Click Preview to trigger the XSS
  1. Save the changes and now every time someone preview the form XSS would trigger

{F1763124}

## Supporting Material/References:
{F1763127}

Admin can invite Staff user with limited permission, that staff can then add the payload and perform scripts to other users like the Admin.

If there's anything I can help with please let me know.

Have a great day!

Cheers,
PenguinsHelp

## Impact

Stored XSS

</details>

---
*Analysed by Claude on 2026-05-24*
