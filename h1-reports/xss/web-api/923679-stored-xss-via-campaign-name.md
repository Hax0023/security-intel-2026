# stored xss via Campaign Name.

## Metadata
- **Source:** HackerOne
- **Report:** 923679 | https://hackerone.com/reports/923679
- **Submitted:** 2020-07-14
- **Reporter:** omarelfarsaoui
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi,
I found a stored  xss https://app.lemlist.com

## Steps To Reproduce:
1. go to https://app.lemlist.com/.
2. create or edit campaigns.
3. set the payload `/><svg src=x onload=confirm(document.domain);>` in the **Campaign Name**.
4. visit Buddies-to-Be tab .
5. click Add one on the right Top . or click on one of the list of  **Contact**
6. you will see pop-up.

## Poc
{F907302}

## I

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
Hi,
I found a stored  xss https://app.lemlist.com

## Steps To Reproduce:
1. go to https://app.lemlist.com/.
2. create or edit campaigns.
3. set the payload `/><svg src=x onload=confirm(document.domain);>` in the **Campaign Name**.
4. visit Buddies-to-Be tab .
5. click Add one on the right Top . or click on one of the list of  **Contact**
6. you will see pop-up.

## Poc
{F907302}

## Impact

Stealing cookies

</details>

---
*Analysed by Claude on 2026-05-24*
