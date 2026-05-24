# Privilege escalation allows to use iframe functionality w/o upgrade

## Metadata
- **Source:** HackerOne
- **Report:** 594080 | https://hackerone.com/reports/594080
- **Submitted:** 2019-06-02
- **Reporter:** muon4
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hello team!

I've found a privilege escalation issue which allows to set iframes to the projects w/o upgrading.

### Steps to reproduce
- Login
- Navigate to the project
- Choose `integrations` and click the `IFrame`
- See that you'll get `upgrade now` notification
{F501019}
- Inspect the page with developer tool and choose the `upgrade` from `IFrame` icon
- Delete the `data-upgrade="true"` part
{

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

Hello team!

I've found a privilege escalation issue which allows to set iframes to the projects w/o upgrading.

### Steps to reproduce
- Login
- Navigate to the project
- Choose `integrations` and click the `IFrame`
- See that you'll get `upgrade now` notification
{F501019}
- Inspect the page with developer tool and choose the `upgrade` from `IFrame` icon
- Delete the `data-upgrade="true"` part
{F501023}
- Click the `IFrame` and see that you are able to add iframe to the page w/o upgrade
{F501024}


If you need any information please let me know.

Cheers!

## Impact

Users can use functionalities without paying

</details>

---
*Analysed by Claude on 2026-05-24*
