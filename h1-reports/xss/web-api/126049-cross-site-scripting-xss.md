# Cross-site Scripting (XSS)

## Metadata
- **Source:** HackerOne
- **Report:** 126049 | https://hackerone.com/reports/126049
- **Submitted:** 2016-03-25
- **Reporter:** djadmin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The website located at https://login.uber.com/applications suffers from a stored Cross-site Scripting (XSS) vulnerability.

Reproduction Steps:
Create a new application with name as the following vector, and try to delete the same app.

*Vector* : "><img src=x onerror=prompt(1)>

Note that the XSS payload has fired.

Possible Scenarios:
1. Attacker gets added as an admin or developer for an app
2.

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

The website located at https://login.uber.com/applications suffers from a stored Cross-site Scripting (XSS) vulnerability.

Reproduction Steps:
Create a new application with name as the following vector, and try to delete the same app.

*Vector* : "><img src=x onerror=prompt(1)>

Note that the XSS payload has fired.

Possible Scenarios:
1. Attacker gets added as an admin or developer for an app
2. Adds an app with an XSS vector as a name
3. Victim sees the unusual app and attempts to delete it.


Or:

1. Attacker creates an app with XSS-y name
2. Adds victim as an admin
3. Victim joins the app and attempts to delete it

I’ve tested this in the latest Firefox and Chrome. 
Attached to this report is the screenshot of this issue occurring in Chrome.


</details>

---
*Analysed by Claude on 2026-05-24*
