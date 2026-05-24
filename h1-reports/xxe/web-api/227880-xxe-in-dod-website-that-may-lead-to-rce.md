# XXE in DoD website that may lead to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 227880 | https://hackerone.com/reports/227880
- **Submitted:** 2017-05-12
- **Reporter:** jin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** XML External Entities (XXE)
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
XXE in https://█████

**Description:**
A malicious user can modify an XML-based request to include XML content that is then parsed locally.

## Impact
An attacker can use an XML external entity vulnerability to send specially crafted unauthorized XML requests, which will be processed by the XML parser. The attacker can use an XML external entity vulnerability for getting unauthorised 

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

**Summary:**
XXE in https://█████

**Description:**
A malicious user can modify an XML-based request to include XML content that is then parsed locally.

## Impact
An attacker can use an XML external entity vulnerability to send specially crafted unauthorized XML requests, which will be processed by the XML parser. The attacker can use an XML external entity vulnerability for getting unauthorised access to the OS file system.

## PoC

```
POST /PSIGW/PeopleSoftServiceListeningConnector HTTP/1.1
Host: https://███
Content-type: text/xml
Content-Length: 50

<!DOCTYPE a PUBLIC "-//B/A/EN" "HELLO_XXE"><a></a>
```

</details>

---
*Analysed by Claude on 2026-05-24*
