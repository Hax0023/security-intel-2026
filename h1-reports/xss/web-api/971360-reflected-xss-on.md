# Reflected XSS on ███████

## Metadata
- **Source:** HackerOne
- **Report:** 971360 | https://hackerone.com/reports/971360
- **Submitted:** 2020-08-31
- **Reporter:** nagli
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary**:
Reflected Cross site Scripting (XSS) on████leaving.html?url=%22%3E%3Cscript%3Ealert(document.domain)%3C/script%3E

**Steps To Reproduce**:
1. Navigate to███leaving.html?url=
2. Enter a crafted XSS payload like "><script>alert("xss by nagli")</script>
3. Alert will pop :-)

█████████

**How can the system be exploited with this bug?**
The attacker can execute JS code, which could lead 

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

**Summary**:
Reflected Cross site Scripting (XSS) on████leaving.html?url=%22%3E%3Cscript%3Ealert(document.domain)%3C/script%3E

**Steps To Reproduce**:
1. Navigate to███leaving.html?url=
2. Enter a crafted XSS payload like "><script>alert("xss by nagli")</script>
3. Alert will pop :-)

█████████

**How can the system be exploited with this bug?**
The attacker can execute JS code, which could lead to stealing cookies and full account takeover.

**Recommendations for fix**
Content based escaping on the users input, in this case on the redirect parameter.

**Best Regards,**
nagli

## Impact

Attacker can execute JS code on the Victim Behalf.

</details>

---
*Analysed by Claude on 2026-05-24*
