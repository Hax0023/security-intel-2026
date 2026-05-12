# HTML Injection and Possible XSS in sms-be-vip.twitter.com via Unencoded Path Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 150179 | https://hackerone.com/reports/150179
- **Submitted:** 2016-07-09
- **Reporter:** secgeek
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** HTML Injection, Cross-Site Scripting (XSS), Reflected XSS
- **CVEs:** None
- **Category:** web-api

## Summary
The sms-be-vip.twitter.com 404 error page fails to properly encode user-supplied input in the URL path, allowing HTML injection and potential XSS attacks. The vulnerability is particularly exploitable in Internet Explorer 7-11 when combined with HTTP 302 redirects to bypass URL encoding mechanisms. By bypassing IE's friendly error message threshold (512 bytes for 404 errors), attackers can inject malicious JavaScript that executes in the domain context.

## Attack scenario
1. Attacker creates a malicious PHP redirect page that accepts a URL parameter and issues a 302 redirect without URL encoding
2. Attacker crafts a URL containing HTML/JavaScript payload in the path of sms-be-vip.twitter.com (e.g., <h1>TEST</h1> or script tags)
3. Attacker sends victim a link to the redirect page with the crafted sms-be-vip.twitter.com URL as parameter
4. Internet Explorer processes the 302 redirect and sends the request without URL encoding due to browser behavior
5. The 404 error page reflects the unencoded HTML/JavaScript payload in the response
6. Attacker adds padding data to exceed the 512-byte threshold, forcing IE to render the injected content instead of the friendly error page

## Root cause
The application reflects URL path parameters in the 404 error page without HTML entity encoding or output sanitization. Additionally, the error page response is short enough to trigger IE's friendly error message suppression, preventing payload execution unless padding is added.

## Attacker mindset
An attacker would recognize that reflected XSS in error pages is a common oversight, and would specifically target Internet Explorer due to its unique URL encoding behavior with redirects. The attacker would exploit browser-specific quirks and the friendly error message mechanism to deliver a working exploit despite modern browsers' URL encoding defaults.

## Defensive takeaways
- Always HTML-encode user-supplied input before reflecting it in HTTP responses, including URL paths
- Implement Content Security Policy (CSP) headers to restrict script execution
- Use a templating engine that auto-escapes output by default
- Validate and sanitize all user input at the point of use, not just at entry
- Ensure error pages do not reflect untrusted data directly
- Test error handling paths with various payloads, including on legacy browsers
- Consider using X-XSS-Protection header (defense in depth, not primary defense)
- Implement input validation to reject or sanitize HTML special characters in URL paths

## Variant hunting
Search for other Twitter subdomains with similar 404 error page implementations
Test other error status codes (400, 403, 405, 500, 501, 505) mentioned in the threshold criteria
Investigate other endpoints that reflect request parameters in error messages
Check for similar patterns in other properties/endpoints that display user-controlled data
Test if the vulnerability exists in other browsers or via other bypass techniques (POST requests, unusual HTTP methods)

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.001
- T1203

## Notes
This report demonstrates sophisticated exploitation technique leveraging Internet Explorer's URL encoding behavior with HTTP 302 redirects and the friendly error message bypass mechanism. The vulnerability is browser-specific and requires specific conditions (IE 7-11, XSS Auditor disabled) but represents a real attack vector against legacy browsers. The POC methodology of using external redirect pages is valuable for bypassing client-side encoding. Report appears to be from 2016 timeframe based on IE version references.

## Full report
<details><summary>Expand</summary>

Hi,
I would like to report HTML Injection and possible cross site scripting (XSS) vulnerability in **sms-be-vip.twitter.com**

##Overview

The **sms-be-vip.twitter.com** 404 error page appears to be vulnerable to XSS and HTML Injection as it doesn't encode the HTML tags in the path name such as ```https://sms-be-vip.twitter.com/<h1>TEST</h1>```.

But the HTML tags have to be send without URL encoding. Most of the modern web browsers will encode the HTML tags in the request before it being sent to the webserver. However In Internet Explorer 11 and lower versions it's possible to make the browser send the request without any URL encoding.

### How to make MSIE 7 - 11 send the request without URL encoding ?

Internet Explorer won't encode the URL if it was sent from a 302 Redirect.

So you can use a simple PHP page like the following:

```php
<?php
$url = $_GET['x'];
header("Location: $url");
?> 
```

Then use the  page and perform a redirection to the endpoint which is vulenrable to XSS.

``` http://secgeek.net/POC/redir.php?x=https://sms-be-vip.twitter.com/<h1>TEST</h1> ```


Now you could notice that the friendly HTTP error messages in Internet Explorer will appear instead of showing the **<h1>TEST</h1>** in the error page.

There is a simple workaround for this issue. 
According to Microsoft the HTTP friendly error message will appears if it meets two criteria

1.The HTTP Status code must be [400, 403, 404, 405, 406, 408, 409, 410, 500, 501, 505]
2.The HTTP Response body’s byte length must be shorter than a threshold value

```Ruby
 The default threshold value for 404 errors is 512 bytes.
```
So we can add more data in the request to be returned in the server response that will overcome this issue.

```http://secgeek.net/POC/redir.php?x=https://sms-be-vip.twitter.com/<h1>TEST</h1>.................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................... ```

##Techincal Details

##Impact:

The vulnerability allow a malicious user to inject html tags and execute Javascript in the same context of sms-be-vip.twitter.com domain which could lead to steal user's session, peform CSRF attacks or open a phishing page.

##Affected Domain:
sms-be-vip.twitter.com

##Affected Insertion point:
The path name in the url ```https://sms-be-vip.twitter.com/<XSS Injection here>```

##HTML Injection POC
http://secgeek.net/POC/Twitter-HTML-POC.php

##XSS POC
http://secgeek.net/POC/Twitter-XSS-POC.php

**Note:** This XSS POC will work only if the XSS Auditor is disabled in Internet Explorer. 

I've Attached Sreenshots for the two POCs.

Kindly check and review the issue.
Thanks in advance!






</details>

---
*Analysed by Claude on 2026-05-12*
