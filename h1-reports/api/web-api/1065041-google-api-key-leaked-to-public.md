# Google API key leaked to Public

## Metadata
- **Source:** HackerOne
- **Report:** 1065041 | https://hackerone.com/reports/1065041
- **Submitted:** 2020-12-23
- **Reporter:** bb89e4af088379499c73f7d
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hi team,

I found a bunch of endpoints that is leaking you Google Api key.
I tested the key and found it is vulnerable to Geocode Api.

List of vulnerable endpoints
https://ass0.fetlife.com 
https://ass2.fetlife.com
https://app.fetlife.com
https://ass1.fetlife.com 
https://ass3.fetlife.com 
https://fetlife.com
https://ws.fetlife.com 


**POC key:**
`AI████████DM`



**Exploit POC:**
API key is  vu

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

Hi team,

I found a bunch of endpoints that is leaking you Google Api key.
I tested the key and found it is vulnerable to Geocode Api.

List of vulnerable endpoints
https://ass0.fetlife.com 
https://ass2.fetlife.com
https://app.fetlife.com
https://ass1.fetlife.com 
https://ass3.fetlife.com 
https://fetlife.com
https://ws.fetlife.com 


**POC key:**
`AI████████DM`



**Exploit POC:**
API key is  vulnerable  for Geocode API! Here is the PoC link which can be used directly via browser:
https://maps.googleapis.com/maps/api/geocode/json?latlng=40,30&key=AI████████DM

## Impact

costing companies extra money and in some cases DOS.

Identifies cost: $5 per 1000 request

</details>

---
*Analysed by Claude on 2026-05-24*
