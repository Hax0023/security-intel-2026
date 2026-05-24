# Information Disclosure FrontPage Configuration Information

## Metadata
- **Source:** HackerOne
- **Report:** 2180018 | https://hackerone.com/reports/2180018
- **Submitted:** 2023-09-25
- **Reporter:** gu4rdianbyte
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there i found a information disclosure Microsoft FrontPage configuration in the subdomain ██████████hat allows me to see version number and scripting paths off sharepoint using firefox.

POC:
Go to the following url:
https://███████/_vti_inf.html
and you will see the code

<!-- FrontPage Configuration Information 
FPVersion="16.00.0.000"
FPShtmlScriptUrl="_vti_bin/shtml.dll/_vti_rpc"
FPAuthorSc

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

Hi there i found a information disclosure Microsoft FrontPage configuration in the subdomain ██████████hat allows me to see version number and scripting paths off sharepoint using firefox.

POC:
Go to the following url:
https://███████/_vti_inf.html
and you will see the code

<!-- FrontPage Configuration Information 
FPVersion="16.00.0.000"
FPShtmlScriptUrl="_vti_bin/shtml.dll/_vti_rpc"
FPAuthorScriptUrl="_vti_bin/_vti_aut/author.dll"
FPAdminScriptUrl="_vti_bin/_vti_adm/admin.dll"
TPScriptUrl="_vti_bin/owssvr.dll"
-->
██████████

For more detailed information please check the References section first link.

## References
https://fortiguard.com/encyclopedia/ips/103284772
https://blogs.msdn.microsoft.com/fabdulwahab/2015/08/15/security-protecting-sharepoint-server-applications/

## Impact

Attackers can know the version and scripting paths information of Sharepoint FrontPage Configuration.

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Just follow the URL provided

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
