# ████████ portal is open to enumeration once authenticated.  Session ID's appear static.  All PII available once a valid session ID is found.

## Metadata
- **Source:** HackerOne
- **Report:** 1150573 | https://hackerone.com/reports/1150573
- **Submitted:** 2021-04-05
- **Reporter:** gentlemenhacker
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Session Fixation
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Description:**
Once Authenticated to █████████ portal with valid credentials you can type in another members session id and you can see any service members data as if you were authenticated as them.

https://█████████

I did not see if there was a way to dump all session id's, but wouldn't be too surprised if it was vulnerable to this.

## References

Replacing that string above with valid sessi

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

**Description:**
Once Authenticated to █████████ portal with valid credentials you can type in another members session id and you can see any service members data as if you were authenticated as them.

https://█████████

I did not see if there was a way to dump all session id's, but wouldn't be too surprised if it was vulnerable to this.

## References

Replacing that string above with valid session ID's let me see ██████ info

## Impact

All PII held in ██████████ portal exposed.  █████████.  
If website doesn't stop me, I could either dump the list of id's or utilize a tool to brute force a range.

## System Host(s)
█████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Step 1: Authenticate to █████████ portal with valid credentials. 
Step 2:  navigate straight to this page with a valid session id
https://████████
If you have a valid session id, you can see any service members data as if you were authenticated as them.

## Suggested Mitigation/Remediation Actions
random session ids.  better authorization to data.



</details>

---
*Analysed by Claude on 2026-05-24*
