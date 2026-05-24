# Reflected XSS In https://███████

## Metadata
- **Source:** HackerOne
- **Report:** 1094276 | https://hackerone.com/reports/1094276
- **Submitted:** 2021-02-03
- **Reporter:** sleepnotf0und
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hi security team,
According to my report #1092618, The VDP team agreed that ***████*** and it's subdomains is in the scope of the DoD program
So I continue testing that domain

##Vulnerable Website URL:
https://███████████████%3CSvg%20OnLoad=alert(1)%3E

##Description of Security Issue:
Reflected XSS in path parameter (URI)

## Impact

Executing Javascript on behalf of the victim

## System Host(s

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

Hi security team,
According to my report #1092618, The VDP team agreed that ***████*** and it's subdomains is in the scope of the DoD program
So I continue testing that domain

##Vulnerable Website URL:
https://███████████████%3CSvg%20OnLoad=alert(1)%3E

##Description of Security Issue:
Reflected XSS in path parameter (URI)

## Impact

Executing Javascript on behalf of the victim

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1 - Visit https://███
2 - Visit the error page /customerror
3 - Add the URI payload <Svg%20OnLoad=alert(1)>
4 - Final link https://██████████████████%3CSvg%20OnLoad=alert(1)%3E

## Suggested Mitigation/Remediation Actions
Sanitize the URI Path parameter



</details>

---
*Analysed by Claude on 2026-05-24*
