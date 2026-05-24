# Internal GET SSRF via CSRF with Press This scan feature

## Metadata
- **Source:** HackerOne
- **Report:** 110801 | https://hackerone.com/reports/110801
- **Submitted:** 2016-01-14
- **Reporter:** skansing
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Description
-----------------------------------
The url `http://xxx.xxx.xxx.xxx/wp-admin/press-this.php?u=URL_TO_SCRAPE&url-scan-submit=Scan` does not validate that user intends to send a scrape request.
The filter does not validate for `0.0.0.0:PORT` and allows the attacker to make the victim send GET request to servers priate127.0.0.1:PORT, localhost:PORT or anything which can be accessed via 0.

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

Description
-----------------------------------
The url `http://xxx.xxx.xxx.xxx/wp-admin/press-this.php?u=URL_TO_SCRAPE&url-scan-submit=Scan` does not validate that user intends to send a scrape request.
The filter does not validate for `0.0.0.0:PORT` and allows the attacker to make the victim send GET request to servers priate127.0.0.1:PORT, localhost:PORT or anything which can be accessed via 0.0.0.0

So basicly a wordpress installations can send unwanted scrape/scan requests on behalf of their user invoked by the attacker. Including private connections via 0.0.0.0


Example
--------------------------------------- 
Victim is owner of myWordpress.com

- Victim is logged into Wordpress.
- Victim visits bad site with a content of`<img src="//myWordpress.com/wp-admin/press-this.php?u=htto://0.0.0.0:8080&url-scan-submit=Scan" /> 
-  Victim sends a unwanted request to their server requesting a internal server address to be hit.
- Server sends get request to 0.0.0.0:8080
- Servers private 127.0.0.1 answers back.

This example is with a private address, but it could also be a public. address

  
Fix
----------------------------------------
The scan/scrape should be a POST request using a csrf token or etc. 
The address 0.0.0.0 should not be allowd for scanning/scraping.

</details>

---
*Analysed by Claude on 2026-05-24*
