# Path Traversal via Unsanitized CLI Argument to io.ioutil.ReadFile

## Metadata
- **Source:** HackerOne
- **Report:** 1664244 | https://hackerone.com/reports/1664244
- **Submitted:** 2022-08-09
- **Reporter:** bhaskar_ram
- **Program:** Hyperledger Fabric
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Arbitrary File Read, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A path traversal vulnerability exists in Hyperledger Fabric where unsanitized CLI arguments are directly passed to io.ioutil.ReadFile(), allowing attackers to read arbitrary files on the system. The vulnerability stems from insufficient input validation before file operations, enabling directory traversal using relative path sequences.

## Attack scenario
1. Attacker identifies a CLI command that accepts a file path argument without validation
2. Attacker crafts a malicious CLI argument using path traversal sequences (e.g., '../../../etc/passwd')
3. The unsanitized argument is passed directly to io.ioutil.ReadFile() function
4. The file operation resolves the traversal sequence and reads the target file outside intended directories
5. Attacker exfiltrates sensitive files such as configuration files, credentials, or source code
6. If file contents are echoed or logged, attacker gains direct access to arbitrary file data

## Root cause
Insufficient input validation and sanitization of CLI arguments before passing them to file I/O operations. The code fails to implement path canonicalization, allowlisting, or blocking of traversal sequences like '..' and symbolic links.

## Attacker mindset
An attacker would leverage this vulnerability to perform reconnaissance, extract sensitive configuration data, steal credentials, or access private keys. The vulnerability is particularly dangerous in containerized deployments where Fabric processes have access to sensitive cluster data.

## Defensive takeaways
- Always validate and sanitize user-supplied file paths before file operations
- Use filepath.Clean() and filepath.Abs() to normalize and resolve paths
- Implement allowlist validation to restrict file access to intended directories
- Use filepath.HasPrefix() to ensure resolved path is within allowed base directory
- Reject paths containing '..', '~', or symbolic link traversal attempts
- Apply principle of least privilege to file system access permissions
- Implement comprehensive input validation for all CLI arguments
- Use static analysis tools to detect unsafe file path handling patterns

## Variant hunting
Search for other io.ioutil.ReadFile() calls with user-supplied arguments throughout codebase
Audit all CLI argument parsing code for path parameters without validation
Review os.Open(), os.OpenFile(), ioutil.WriteFile() for similar vulnerabilities
Check for symbolic link following without validation
Examine any file path operations that accept external input in Fabric components
Look for path concatenation operations (filepath.Join) without prior validation
Review configuration file loading mechanisms for path traversal exposure

## MITRE ATT&CK
- T1190
- T1083
- T1087
- T1041
- T1005

## Notes
This is a critical finding in Hyperledger Fabric (enterprise blockchain platform). The fix is available in PR #3573. Path traversal vulnerabilities are particularly dangerous in server/daemon applications where elevated privileges may grant access to sensitive system files. The use of deprecated io.ioutil package functions should also be replaced with modern alternatives from os package.

## Full report
<details><summary>Expand</summary>

Unsanitized input from CLI argument flows into `io.ioutil.ReadFile`, where it is used as a path. This may result in a Path Traversal vulnerability and allow an attacker to read arbitrary files.

See this fix : https://github.com/hyperledger/fabric/pull/3573

## Impact

There is a path traversal vulnerability in the source code of fabric

</details>

---
*Analysed by Claude on 2026-05-24*
