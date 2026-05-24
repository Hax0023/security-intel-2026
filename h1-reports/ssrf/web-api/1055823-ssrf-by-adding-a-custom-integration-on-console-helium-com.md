# SSRF By adding a custom integration on console.helium.com

## Metadata
- **Source:** HackerOne
- **Report:** 1055823 | https://hackerone.com/reports/1055823
- **Submitted:** 2020-12-10
- **Reporter:** th0roid
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** high
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
A Server Side Request Forgery vulnerability was found in the *Add a custom Integration* feature on *console.helium.com*. By creating a custom HTTP integration, and setting the integration endpoint to http://169.254.169.254/latest/meta-data private meta-data from the AWS EC2 instance running can be retrieved.

{F1111768}

{F1111767}

The server makes the HTTP request and sets the response body  as 

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

A Server Side Request Forgery vulnerability was found in the *Add a custom Integration* feature on *console.helium.com*. By creating a custom HTTP integration, and setting the integration endpoint to http://169.254.169.254/latest/meta-data private meta-data from the AWS EC2 instance running can be retrieved.

{F1111768}

{F1111767}

The server makes the HTTP request and sets the response body  as the integration message every time that the device sends a packet. As the endpoint input is not validated, this makes the application vulnerable to a critical SSRF.

{F1111779}

{F1111780}

Endpoint set as: http://169.254.169.254/latest/meta-data/ami-id

{F1111781}

## Impact

By exploiting this vulnerability an attacker can get access to the server internal network and access private and critical information.

</details>

---
*Analysed by Claude on 2026-05-24*
