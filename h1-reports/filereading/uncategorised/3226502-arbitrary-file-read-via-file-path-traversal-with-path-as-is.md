# Arbitrary File Read via file:// Path Traversal with --path-as-is

## Metadata
- **Source:** HackerOne
- **Report:** 3226502 | https://hackerone.com/reports/3226502
- **Submitted:** 2025-06-27
- **Reporter:** demsese
- **Program:** curl
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Improper Input Validation, Directory Traversal
- **CVEs:** None
- **Category:** uncategorised

## Summary
curl's --path-as-is flag bypasses path normalization for file:// URLs, allowing attackers to use .. segments to traverse directories and read arbitrary files accessible to the process. This vulnerability affects curl 8.15.0-DEV and potentially other versions, enabling disclosure of sensitive files like /etc/passwd and private keys.

## Attack scenario
1. Attacker crafts a malicious file:// URL containing ../ path traversal sequences
2. Attacker invokes curl with the --path-as-is flag to prevent path normalization
3. The file:// handler processes the URL without sanitizing .. segments due to the flag being set
4. Path normalization that would typically resolve .. to parent directories is skipped
5. curl traverses up the directory tree and accesses files outside intended scope (e.g., /etc/passwd)
6. Attacker obtains contents of arbitrary world-readable files or files accessible to the curl process

## Root cause
The --path-as-is flag was designed to skip URL path normalization to preserve literal paths, but this safety feature was not properly restricted to the file:// protocol handler. The file:// handler failed to apply path canonicalization logic even when --path-as-is is enabled, trusting user input for local filesystem access without validation.

## Attacker mindset
An attacker would use this to perform reconnaissance on a target system, extract sensitive configuration files, read private SSH keys, or access other confidential files. The attack is trivial to execute with simple command-line manipulation and requires no special privileges beyond what the curl process already has.

## Defensive takeaways
- Always sanitize and normalize path inputs regardless of user-supplied flags or options
- Implement separate validation logic for local filesystem operations that cannot be bypassed by flags
- Use allowlists for path resolution rather than blacklists when dealing with directory traversal risks
- Apply principle of least privilege - restrict file:// protocol handler access to specific directories
- Test security-critical code paths with both normal and edge-case inputs (path traversal patterns)
- Document security implications clearly when providing options like --path-as-is that affect validation
- Consider disallowing --path-as-is on local file:// URLs entirely if the use case doesn't require it

## Variant hunting
Search for similar path normalization bypasses in other curl protocol handlers (ftp://, sftp://, etc.) when --path-as-is is used. Examine how other tools (wget, tools using libcurl) handle path traversal with similar options. Test whether relative paths with ../ work in other URL schemes when path normalization is disabled.

## MITRE ATT&CK
- T1190
- T1083
- T1005

## Notes
The vulnerability is in curl's URL processing logic where the --path-as-is flag creates a security bypass. The fix should either: (1) always normalize .. segments in file:// URLs regardless of flags, or (2) explicitly disallow --path-as-is with file:// protocol. This is a logic error in security-critical code where user-supplied flags were allowed to override safety mechanisms.

## Full report
<details><summary>Expand</summary>

## Summary:
Using `--path-as-is` with a `file://` URL skips normalization of `..` segments allowing reading of any local file the process can access

## Affected version
`* curl 8.15.0-DEV (commit 2a9dfe275, June 27, 2025) on Kali Linux 2024.3, x86_64`

## Steps To Reproduce:

  1. bulild curl with debug and ASan:
```
git clone https://github.com/curl/curl.git && cd curl  
autoreconf -fi  
CFLAGS="-fsanitize=address -g" ./configure --enable-debug --with-openssl  
make -j$(nproc)
```
  2. read `/etc/passwd`:
```
./src/curl --path-as-is file:///../../../../../../../../etc/passwd
```
  3. read `/etc/hosts`:
```
./src/curl --path-as-is file:///../../../../../../../../etc/hosts
```

## Mitigation:
Normalize and sanitize `..` segments in the file-URL handler even when `--path-as-is` is used, or disallow its use on local paths.

## Impact

## Summary:
Disclosure of any world-readable file e.g. `/etc/passwd`, `/etc/hosts`, private keys

</details>

---
*Analysed by Claude on 2026-05-24*
