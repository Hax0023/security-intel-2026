# XSS in Asset name

## Metadata
- **Source:** HackerOne
- **Report:** 133744 | https://hackerone.com/reports/133744
- **Submitted:** 2016-04-22
- **Reporter:** ashish_r_padelkar
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Found one XSS iin asset name

**Steps To Reproduce**

1. Create Any member at `https://sandbox.veris.in/portal/members/`

2. Add that member in any group at `https://sandbox.veris.in/portal/groups/`

3. Create an `Asset` named `<script>alert(1);</script>` at `https://sandbox.veris.in/portal/assets/`

4. Now go back to members  `https://sandbox.veris.in/portal/members/` and click on the symbol show

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

Found one XSS iin asset name

**Steps To Reproduce**

1. Create Any member at `https://sandbox.veris.in/portal/members/`

2. Add that member in any group at `https://sandbox.veris.in/portal/groups/`

3. Create an `Asset` named `<script>alert(1);</script>` at `https://sandbox.veris.in/portal/assets/`

4. Now go back to members  `https://sandbox.veris.in/portal/members/` and click on the symbol shown in screen shot for any of the member
{F88735}

you should see an XSS popup!

Regards
Ashish


</details>

---
*Analysed by Claude on 2026-05-24*
