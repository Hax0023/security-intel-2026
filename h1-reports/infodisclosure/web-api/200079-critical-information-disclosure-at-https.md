# Critical information disclosure at https://█████████

## Metadata
- **Source:** HackerOne
- **Report:** 200079 | https://hackerone.com/reports/200079
- **Submitted:** 2017-01-21
- **Reporter:** juliocesar
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**

There is a critical information disclosure at https://████████/rserver/rdPage.aspx?rdReport=db_Dashboard&rdShowModes=

**Description:**

As you can see in the video the  https://████████/rserver/rdPage.aspx?rdReport=db_Dashboard&rdShowModes= loads a page with a debug this page functions enabled, which gives the user access to server side information such some sql structure, the path 

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

**Summary:**

There is a critical information disclosure at https://████████/rserver/rdPage.aspx?rdReport=db_Dashboard&rdShowModes=

**Description:**

As you can see in the video the  https://████████/rserver/rdPage.aspx?rdReport=db_Dashboard&rdShowModes= loads a page with a debug this page functions enabled, which gives the user access to server side information such some sql structure, the path to the webroot  plus some other information.

POC video : 
https://█████


## Impact

The impact here can be great, since the user have access to sql structure.

## Step-by-step Reproduction Instructions

1. Log in to the application and open the following link:  https://██████/rserver/rdPage.aspx?rdReport=db_Dashboard&rdShowModes=

## Product, Version, and Configuration (If applicable)

Tested on firefox latest version

## Suggested Mitigation/Remediation Actions

Reference: https://www.owasp.org/index.php/Full_Path_Disclosure

**Mitigation**

Turn of the debugger trace report or limit the access only to administrator

</details>

---
*Analysed by Claude on 2026-05-24*
