# Stored XSS in Contact Form

## Metadata
- **Source:** HackerOne
- **Report:** 50564 | https://hackerone.com/reports/50564
- **Submitted:** 2015-03-08
- **Reporter:** ishahriyar
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
In Contact form there is an option to display Message  when completed.
There I have put the payload
payload: "><img src=x onerror=alert(1)>

and the payload executed and saved permanently.

 

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

In Contact form there is an option to display Message  when completed.
There I have put the payload
payload: "><img src=x onerror=alert(1)>

and the payload executed and saved permanently.

 

</details>

---
*Analysed by Claude on 2026-05-24*
