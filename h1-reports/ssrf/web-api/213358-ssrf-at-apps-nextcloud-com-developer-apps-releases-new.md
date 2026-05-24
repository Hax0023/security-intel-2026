# SSRF at apps.nextcloud.com/developer/apps/releases/new

## Metadata
- **Source:** HackerOne
- **Report:** 213358 | https://hackerone.com/reports/213358
- **Submitted:** 2017-03-14
- **Reporter:** t-pwn
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
***Hi,***

***I've found SSRF vulnerability at https://apps.nextcloud.com/developer/apps/releases/new***

##Description##

Server Side Request Forgery (SSRF) is a vulnerability that appears when an attacker has the ability to create requests from the vulnerable server.

Usually, Server Side Request Forgery (SSRF) attacks target internal systems behind the firewall that are normally inaccessible fr

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

***Hi,***

***I've found SSRF vulnerability at https://apps.nextcloud.com/developer/apps/releases/new***

##Description##

Server Side Request Forgery (SSRF) is a vulnerability that appears when an attacker has the ability to create requests from the vulnerable server.

Usually, Server Side Request Forgery (SSRF) attacks target internal systems behind the firewall that are normally inaccessible from the outside world (but using SSRF it’s possible to access these systems). With SSRF it’s also possible to access services from the same server that is listening on the loopback interface.
Using Server Side Request Forgery attacks it’s possible to:

+ Scan and attack systems from the internal network that are not normally accessible
+ Enumerate and attack services that are running on these hosts
+ Exploit host-based authentication services

##Steps to reproduce##

+ Navigate to https://apps.nextcloud.com/developer/apps/releases/new
+ Enter https://127.0.0.1:22 (SSH) or https://127.0.0.1:80 (HTTP) (Download Link area) 
+ You will get this error
{F168743}
         means the 22 port is opened, the same with 80
+ but if you entered https://127.0.0.1:21 (Telnet) you will get this error 
{F168742}
         means the 21 port isn't opened

***Thanks.***


</details>

---
*Analysed by Claude on 2026-05-24*
