# Path Traversal via Symlink in http_server NPM Package

## Metadata
- **Source:** HackerOne
- **Report:** 692262 | https://hackerone.com/reports/692262
- **Submitted:** 2019-09-11
- **Reporter:** vineetpandey
- **Program:** HackerOne
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Path Traversal, Symlink Following, Information Disclosure
- **CVEs:** CVE-2019-15600
- **Category:** uncategorised

## Summary
The http_server NPM package (v1.0.12) fails to validate symbolic links, allowing attackers to read arbitrary files outside the web root directory. By creating a symlink to sensitive system files within the served directory, an attacker can access restricted content like /etc/shadow through HTTP requests.

## Attack scenario
1. Attacker gains local access to the server or can influence files in the web root directory
2. Attacker creates a symbolic link pointing to a sensitive system file (e.g., ln -s /etc/shadow test_shadow)
3. Attacker makes an HTTP request to the symlinked file via the web server (e.g., http://localhost:8888/test_shadow)
4. The http_server follows the symlink without validation and returns the contents of the target file
5. Attacker reads sensitive data such as shadow file, private keys, or configuration files
6. Attacker uses disclosed information for further exploitation or lateral movement

## Root cause
The http_server application does not validate whether files are symbolic links before serving them. It follows symlinks without checking if they point outside the intended web root directory, violating the principle of least privilege and directory boundary enforcement.

## Attacker mindset
An attacker with local file system access or ability to place files in the web root would exploit this to exfiltrate sensitive system files. The low attack complexity makes this an attractive vector for privilege escalation or information gathering during post-exploitation.

## Defensive takeaways
- Implement symlink detection and rejection; reject requests for symbolic links or validate target paths are within web root
- Use realpath() or equivalent to resolve canonical paths and verify they remain within the web root directory
- Apply principle of least privilege: run web server with minimal necessary permissions
- Implement strict file access controls; prevent users from creating symlinks in web-served directories
- Regular security audits of file serving logic, especially for directory traversal and symlink vulnerabilities
- Update dependencies regularly and monitor security advisories for NPM packages

## Variant hunting
Check other Node.js static file servers (express.static, serve, http-server) for symlink handling
Test hard links and other file system tricks to bypass symlink checks
Investigate if path normalization is properly implemented before symlink validation
Review if follow_symlinks or similar configuration options exist and default to safe values
Test with relative symlinks and complex path combinations (../ traversal combined with symlinks)

## MITRE ATT&CK
- T1190
- T1083
- T1526

## Notes
Low weekly downloads (35) suggest limited exposure. Reporter did not contact maintainer or open upstream issue. Patch recommendation is clear: implement symlink rejection. This is a classic path traversal variant that affects any file server not properly validating symlinks. The vulnerability requires some level of local access or ability to create files in the web root, limiting remote-only exploitation scenarios.

## Full report
<details><summary>Expand</summary>

I would like to report Path traversal in http_server
It allows an attacker to read arbitrary system files.

# Module

**module name:** http_server
**version:** 1.0.12
**npm page:** `https://www.npmjs.com/package/http_server`

## Module Description

> Copy description from npm page

## Module Stats

Weekly downloads: 35

# Vulnerability

## Vulnerability Description

With a symbolically linked file in the working directory, it is possible to read arbitrary files outside of the web root directory.

## Steps To Reproduce:

1. Install the http_server: npm install http_server -g

2. Create a symlink file within the directory
ln -s /etc/shadow test_shadow

3. Request the file within browser
http://localhost:8888/test_shadow

## Patch

Reject the symbolically linked path files.

## Supporting Material/References:

> State all technical information about the stack where the vulnerability was found

- Kali Linux
- Node.js v12.8.0
- NPM v6.11.3
- Firefox 60.8.0esr

# Wrap up

> Select Y or N for the following statements:

- I contacted the maintainer to let them know: N
- I opened an issue in the related repository: N

> Hunter's comments and funny memes goes here

## Impact

It allows attacker to read content of arbitrary file on remote server and could leverage attacks like remote code execution.

</details>

---
*Analysed by Claude on 2026-05-24*
