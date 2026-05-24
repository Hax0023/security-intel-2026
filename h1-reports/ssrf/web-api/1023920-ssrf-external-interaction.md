# SSRF external interaction

## Metadata
- **Source:** HackerOne
- **Report:** 1023920 | https://hackerone.com/reports/1023920
- **Submitted:** 2020-11-01
- **Reporter:** 0xcharan
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
hi team,

i found ssrf external interaction on your website which is https://my.stripo.email/cabinet/#/login?guid=&tn=&locale=en on chatbox 

description:- the attacker might cause the server to make connection back to it self
or to other web services within the organization infrastructure or to external third party systems

steps to reproduce:-

1)navigate to this website  https://my.stripo.email

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

hi team,

i found ssrf external interaction on your website which is https://my.stripo.email/cabinet/#/login?guid=&tn=&locale=en on chatbox 

description:- the attacker might cause the server to make connection back to it self
or to other web services within the organization infrastructure or to external third party systems

steps to reproduce:-

1)navigate to this website  https://my.stripo.email/cabinet/#/login?guid=&tn=&locale=en 
2))there you can find chat box
3)paste burp collaborator URL or http://pingb.in
4)you will get HTTP request to your server

note:-i previously submitted this issues in bug crowd it marked as p4 so i set severity to low and i tested many chat application not all are vulnerable example bug crowd chat system.

## Impact

by this vulnerability attacker can map out attack surface

</details>

---
*Analysed by Claude on 2026-05-24*
