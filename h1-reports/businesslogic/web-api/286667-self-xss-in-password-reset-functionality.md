# Self-XSS in password reset functionality

## Metadata
- **Source:** HackerOne
- **Report:** 286667 | https://hackerone.com/reports/286667
- **Submitted:** 2017-11-02
- **Reporter:** zeesek
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
When I opened this domain of yours,
https://accounts.shopify.com/password-reset/new

I just put the following text into email address box,
<h1 style="color:blue;">█████</h1>
it change the colour of the text.

Well my point here is that if you could inject HTML, you might be able to add a <form> tag
to the page.
I also upload the picture as a proof.

Peace.

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
When I opened this domain of yours,
https://accounts.shopify.com/password-reset/new

I just put the following text into email address box,
<h1 style="color:blue;">█████</h1>
it change the colour of the text.

Well my point here is that if you could inject HTML, you might be able to add a <form> tag
to the page.
I also upload the picture as a proof.

Peace.

</details>

---
*Analysed by Claude on 2026-05-24*
