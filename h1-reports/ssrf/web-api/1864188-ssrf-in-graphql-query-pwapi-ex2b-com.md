# SSRF in graphQL query (pwapi.ex2b.com)

## Metadata
- **Source:** HackerOne
- **Report:** 1864188 | https://hackerone.com/reports/1864188
- **Submitted:** 2023-02-06
- **Reporter:** kirtixs
- **Program:** Unknown
- **Bounty:** $3,000
- **Severity:** medium
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
The query for `allTicks` allows setting the parameter `source` that is used to do `GET` requests,  this can be set arbitrarily .

## Steps to Reproduce:

  1. Use a service like burp collaborator to observer incoming requests. 
  2. Replace my domain with your burp collaborator domain and execute the graphQL request.

{F2158013}
  3. Observer incoming DNS and HTTP requests.

{F2158005}

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

## Summary:
The query for `allTicks` allows setting the parameter `source` that is used to do `GET` requests,  this can be set arbitrarily .

## Steps to Reproduce:

  1. Use a service like burp collaborator to observer incoming requests. 
  2. Replace my domain with your burp collaborator domain and execute the graphQL request.

{F2158013}
  3. Observer incoming DNS and HTTP requests.

{F2158005}{F2158006}

Please note that the `source` parameter in the graphQL request can be a full URL so that any `GET` request is possible.

{F2158024}{F2158025}



## Impact
The SSRF vulnerability can be used to potentially compromise internal services that are exposed to internal network requests. Unfortunately, HTTP responses are not returned,  but an attacker can still gather information about open ports and perform blind HTTP `GET` requests against internal services, potentially help in finding more severe vulnerabilities on internal network services.

## Mitigation
The application must only accept servers on an explicit allow list. This will mitigate SSRF attacks.

## Impact

The SSRF vulnerability can be used to potentially compromise internal services that are exposed to internal network requests. Unfortunately, HTTP responses are not returned,  but an attacker can still gather information about open ports and perform blind HTTP get-reqeusts against services that are running on these ports, potentially help in finding more severe vulnerabilities on internal network services.

</details>

---
*Analysed by Claude on 2026-05-24*
