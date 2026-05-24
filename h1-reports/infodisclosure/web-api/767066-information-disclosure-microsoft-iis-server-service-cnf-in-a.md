# Information Disclosure Microsoft IIS Server service.cnf in a mtn website

## Metadata
- **Source:** HackerOne
- **Report:** 767066 | https://hackerone.com/reports/767066
- **Submitted:** 2020-01-02
- **Reporter:** miguel_santareno
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there i found a information disclosure Microsoft IIS Server service.cnf file in the website https://www.mtn.co.za/ using firefox.

In the following steps i will demonstrate how to reproduce the vulnerability.

POC:
1ºGo to the following url:
https://www.mtn.co.za/_vti_pvt/service.cnf

you will see:
vti_encoding:SR|utf8-nl
vti_extenderversion:SR|15.0.0.5179

service.jpg

Remediation:
Remove the 

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

Hi there i found a information disclosure Microsoft IIS Server service.cnf file in the website https://www.mtn.co.za/ using firefox.

In the following steps i will demonstrate how to reproduce the vulnerability.

POC:
1ºGo to the following url:
https://www.mtn.co.za/_vti_pvt/service.cnf

you will see:
vti_encoding:SR|utf8-nl
vti_extenderversion:SR|15.0.0.5179

service.jpg

Remediation:
Remove the service.cnf file from the web server or restrict access to this file.

Example:
For more detailed information please check the References section first link.

References:
https://www.acunetix.com/vulnerabilities/web/vulnerability/microsoft-iis-server-service-cnf-file-found/
https://blogs.msdn.microsoft.com/fabdulwahab/2015/08/15/security-protecting-sharepoint-server-applications/

Best Regards Miguel Santareno

## Impact

Attackers can read /_vti_pvt/service.cnf and gather more information about the system

</details>

---
*Analysed by Claude on 2026-05-24*
