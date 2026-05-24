# Bypass to Defective Fix of Path Traversal in localhost-now

## Metadata
- **Source:** HackerOne
- **Report:** 329837 | https://hackerone.com/reports/329837
- **Submitted:** 2018-03-25
- **Reporter:** caioluders
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Path Traversal, Directory Traversal, Inadequate Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A path traversal vulnerability exists in localhost-now v1.0.2 that allows remote attackers to read arbitrary files on the server. The vulnerability is a bypass of a previous mitigation attempt that simply removed '../' strings without proper encoding/validation, allowing obfuscated payloads like '..././' to bypass the filter.

## Attack scenario
1. Attacker installs and identifies localhost-now running on target server on port 5432
2. Attacker crafts a malicious URL with obfuscated path traversal sequences using '..././' patterns instead of '../'
3. Attacker sends curl request with --path-as-is flag to preserve the URL structure and bypass normalization
4. The vulnerable code's naive string replacement removes all '../' but leaves '..././' intact
5. After the flawed sanitization, '..././' becomes '../' allowing traversal to parent directories
6. Attacker successfully reads sensitive files like /etc/passwd and other arbitrary files outside the web root

## Root cause
The mitigation for the original path traversal vulnerability (issue #312889) used a simplistic approach of removing all '../' substrings via string replacement. This fails against obfuscated variations where the filter itself can be bypassed by inserting characters between the traversal sequences (e.g., '..././' → '../' after removal).

## Attacker mindset
An attacker identifies that the mitigation is incomplete and attempts to craft alternative representations of the path traversal payload. By understanding that simple string removal can be circumvented, the attacker tests variations with extra characters that get stripped away, revealing the path traversal once more.

## Defensive takeaways
- Never use simple string replacement for path traversal mitigation; use canonical path resolution instead
- Validate and normalize file paths using language-native functions (e.g., path.resolve() in Node.js) to resolve symlinks and relative paths
- Implement whitelist-based access controls rather than blacklist-based filtering
- Use security libraries designed for path validation rather than custom regex or string manipulation
- Recursively apply sanitization until no changes occur, or better yet, avoid the need for sanitization through architectural design
- Test security fixes against common bypass techniques including obfuscation and encoding variations
- Implement proper access controls to restrict file serving to intended directories only

## Variant hunting
Look for similar vulnerable npm packages using string-replacement-based path sanitization. Test with variations including: '....///', '..%2e%2e/', '..\..\', double URL encoding, unicode encoding, null bytes, and other separator variations. Check for recursive traversal patterns and check if the code applies sanitization multiple times.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1005 - Data from Local System

## Notes
This is a classic example of security fix bypass through inadequate mitigation. The original vulnerability (issue #312889) was likely discovered previously, but the fix introduced was flawed. The module has minimal adoption (13 downloads/week) limiting real-world impact but demonstrating the dangers of npm packages with inadequate security review. The reporter appropriately demonstrated the issue with a proof-of-concept curl command and identified the exact vulnerable code line.

## Full report
<details><summary>Expand</summary>

I would like to report a Path Traversal vulnerability in localhost-now. It allows to read arbitrary files on the server. This is a bypass on the mitigation of #312889 .

# Module

**module name:** localhost-now
**version:** 1.0.2
**npm page:** `https://www.npmjs.com/package/localhost-now`

## Module Description

>Am I the only one who is lazy to install Apache just for testing some HTML or JavaScript code (like XHR) ?

## Module Stats

[13] downloads in the last week

# Vulnerability

## Vulnerability Description

A path traversal attack aims to access files and directories that are stored outside the web root folder. 

## Steps To Reproduce:

* Install localhost-now
* Run localhost-now on directory
```
ec2-user@kali:~$ localhost 5432
Web Server started on localhost:5432
```
* Execute the curl command 
```
$ curl -v --path-as-is "http://IP:5432/..././..././..././..././..././..././..././..././..././..././etc/passwd"
root:x:0:0:root:/root:/usr/bin/fish
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
...
```

The problem resides on the line [17](https://github.com/DCKT/localhost-now/blob/master/lib/app.js#L17) as the code just delete all the '../' strings , allowing a payload like "..././" to be transformed back in "../" .

## Supporting Material/References:

- OS version :Linux kali 4.13.0
- NodeJS version : v8.10.0
- NPM version : 5.6.0

# Wrap up

- I contacted the maintainer to let them know: No
- I opened an issue in the related repository: No

## Impact

The attacker can read remotely all files on the server.

</details>

---
*Analysed by Claude on 2026-05-24*
