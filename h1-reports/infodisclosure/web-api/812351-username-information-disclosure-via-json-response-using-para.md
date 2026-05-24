# Username Information Disclosure via Json response - Using parameter number Intruder

## Metadata
- **Source:** HackerOne
- **Report:** 812351 | https://hackerone.com/reports/812351
- **Submitted:** 2020-03-06
- **Reporter:** 0xrobot
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi , Brave Team we found vulnerability's in your websites , I Found  all username disclosed using Json Response ``{parameter-number}``.

Platform(s) Affected: [website]
*. https://community.brave.com/c/brave-feature-requests.json
*. https://community.brave.com/c/beta-builds/38.json

## Steps To Reproduce:
  - Repreat URL ``.json`` to Burp Suite
  - Sent to Parameter **Burp-Intruder**
 

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
Hi , Brave Team we found vulnerability's in your websites , I Found  all username disclosed using Json Response ``{parameter-number}``.

Platform(s) Affected: [website]
*. https://community.brave.com/c/brave-feature-requests.json
*. https://community.brave.com/c/beta-builds/38.json

## Steps To Reproduce:
  - Repreat URL ``.json`` to Burp Suite
  - Sent to Parameter **Burp-Intruder**
  - Set parameter , ``§random-number§`` , and start request
  - You can see **Sensitive Information** in Responsive Header ``Number-Parameter``

**Request**
```
GET /c/beta-builds/§38§.json HTTP/1.1
Host: community.brave.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1
```
  - You can see Information Disclosure in Responsive Header ```200 OK.```

##POC Supporting Material/References (Screenshots)
  - F739659
  - F739660
  - F739661
  - F739658

## Impact

Information Disclousure

</details>

---
*Analysed by Claude on 2026-05-24*
