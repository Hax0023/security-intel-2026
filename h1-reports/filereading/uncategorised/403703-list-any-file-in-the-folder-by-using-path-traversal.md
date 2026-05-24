# Path Traversal via Symbolic Links in simplehttpserver

## Metadata
- **Source:** HackerOne
- **Report:** 403703 | https://hackerone.com/reports/403703
- **Submitted:** 2018-09-01
- **Reporter:** vulzzz
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Path Traversal, Symbolic Link Following, Directory Traversal, Information Disclosure
- **CVEs:** CVE-2018-16478
- **Category:** uncategorised

## Summary
simplehttpserver v0.2.1 fails to properly validate symbolic links when serving files, allowing attackers to traverse outside the intended web root directory and access arbitrary files on the system. By creating a symlink pointing to parent directories (e.g., ../../), an attacker can list and potentially access sensitive files outside the web root.

## Attack scenario
1. Attacker identifies a deployment of simplehttpserver running on target system
2. Attacker creates or leverages existing symbolic link in the web root pointing to parent directories (ln -s ../../ symdir)
3. Attacker crafts HTTP request to access the symlink directory (e.g., /symdir/)
4. Server resolves symlink without validation and lists files from parent directories
5. Attacker enumerates sensitive files, credentials, or configuration files outside web root
6. Attacker uses disclosed information for further exploitation (RCE, credential compromise)

## Root cause
The simplehttpserver implementation directly appends the requested path to the web root without validating or rejecting symbolic links. The server fails to implement proper path canonicalization and symlink resolution checks before serving files.

## Attacker mindset
An attacker would leverage this to perform reconnaissance on the target system, discovering file structures and sensitive information outside the intended web-accessible directory. This serves as a stepping stone for further attacks such as credential theft or identifying vectors for remote code execution.

## Defensive takeaways
- Always canonicalize file paths and resolve symlinks before serving content
- Implement strict path validation to ensure requested resources remain within the intended web root
- Disable symbolic link following in web server configurations (use realpath() and validate against base directory)
- Apply chroot jail or containerization to restrict file system access
- Conduct security audits for path traversal vulnerabilities in custom web server implementations
- Use established web servers (Apache, Nginx) instead of custom solutions for production environments
- Implement file access control lists and principle of least privilege

## Variant hunting
Test other Node.js HTTP server packages for similar symlink validation bypasses
Check for hardlinks or bind mounts as alternative traversal vectors
Test double-encoded or URL-encoded traversal sequences
Examine error messages for information disclosure during path resolution
Test with various symlink depths and circular symlink scenarios
Verify behavior with relative vs absolute symlinks

## MITRE ATT&CK
- T1190
- T1083
- T1087
- T1526

## Notes
This vulnerability affects a development/testing tool with only 319 weekly downloads, but demonstrates critical security flaws in custom HTTP server implementations. The maintainer was not notified prior to disclosure. The vulnerability has straightforward exploitation requiring only shell access to create symlinks. Patch recommendation is to disable symlink following entirely in the web server implementation.

## Full report
<details><summary>Expand</summary>

I would like to report Path Traversal in simplehttpserver. It allows to list any file in another folder of web root.

# Module

**module name:** simplehttpserver
**version:** v0.2.1
**npm page:** `https://www.npmjs.com/package/simplehttpserver`

## Module Description

 'simpehttpserver' is an simple imitation of python's SimpleHTTPServer and is intended for testing, development and debugging purposes

## Module Stats

 [319] downloads in the last week

# Vulnerability

## Vulnerability Description

 simpehttpserver is simply get the path name of url and add it to the web root.If there is a symlink file in the directory. You can access files outside the web root directory.

## Steps To Reproduce:
 create symlink file 
$ ln -s ../../ symdir

 install simplehttpserver
$ npm install simplehttpserver -g

start program
$ simplehttpserver ./

{F340863}

## Patch

Disable symlink file access in webserver.

## Supporting Material/References:

Configuration I've used to find this vulnerability:

macos 10.13.6
nodejs v10.9.0
npm 6.4.1
chrome 68.0.3440.106

# Wrap up

- I contacted the maintainer to let them know: [N] 
- I opened an issue in the related repository: [N]

## Impact

This vulnerability allows malicious user to list file in the folder. This might expose vectors to attack system with Remote Code Execution, reveals files with usernames and passwords and many other possibilites.

</details>

---
*Analysed by Claude on 2026-05-24*
