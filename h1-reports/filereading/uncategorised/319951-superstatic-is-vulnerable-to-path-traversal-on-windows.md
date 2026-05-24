# superstatic Path Traversal Vulnerability on Windows via Backslash Encoding

## Metadata
- **Source:** HackerOne
- **Report:** 319951 | https://hackerone.com/reports/319951
- **Submitted:** 2018-02-26
- **Reporter:** chalker
- **Program:** superstatic (npm package)
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Path Traversal, Directory Traversal, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
superstatic version 5.0.1 is vulnerable to path traversal on Windows platforms due to incomplete path validation. The application blocks forward-slash based traversal attempts (../) but fails to block backslash-based traversal (..\ ), allowing attackers to read arbitrary files outside the intended directory.

## Attack scenario
1. Attacker discovers superstatic is running as a static file server on Windows
2. Attacker identifies the document root directory (e.g., C:\Users\User\tmp)
3. Attacker crafts a URL with URL-encoded backslashes (..\ becomes ..%5c)
4. Attacker requests http://localhost:3474/..%5c..%5c..%5cWindows/notepad.exe
5. Browser decodes the path to ..\..\..\Windows/notepad.exe
6. Application fails to detect the backslash traversal and serves arbitrary files from the filesystem

## Root cause
The path validation logic at lib/providers/fs.js line 71 only checks for the forward-slash variant of directory traversal (../). On Windows systems, the backslash character (\) is equally valid for path traversal but is not validated. The incomplete check fails to account for platform-specific path separators.

## Attacker mindset
An attacker would recognize that Windows systems use backslashes in file paths and exploit the developer's assumption that only forward-slashes need to be blocked. This represents a common pitfall in cross-platform security—assuming Unix-centric threat models apply universally.

## Defensive takeaways
- Use platform-agnostic path normalization functions (e.g., path.normalize() or path.resolve()) before validation
- Validate against both forward-slash and backslash traversal patterns
- Use proper path resolution libraries rather than string matching for security controls
- Implement canonicalization of paths before any access control checks
- Test security controls on multiple operating systems (Windows, Linux, macOS)
- Reject or normalize all path separators to a single canonical form before validation

## Variant hunting
Look for other path manipulation bypasses: URL double-encoding, Unicode normalization bypasses, mixed separators (../, ..\, ..\/), case sensitivity issues on case-insensitive filesystems, symlink attacks, and extended-length path prefixes (\\?\ on Windows).

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery

## Notes
The vulnerability has significant reach (1.6M+ estimated annual downloads). The reporter did not contact the maintainer before disclosure. This is a classic example of incomplete security implementation that fails to account for platform-specific filesystem semantics. The use of .%5c URL encoding to bypass browser normalization is a practical demonstration of encoding evasion techniques.

## Full report
<details><summary>Expand</summary>

I would like to report path traversal vulnerability in `superstatic`
It allows to read arbitrary out-of-dir files when running on the Windows platform

# Module

**module name:** `superstatic`
**version:** 5.0.1
**npm page:** `https://www.npmjs.com/package/superstatic`

## Module Description

> Superstatic is an enhanced static web server that was built to power. It has fantastic support for HTML5 pushState applications, clean URLs, caching, and many other goodies.

## Module Stats

2 196 downloads in the last day
33 588 downloads in the last week
139 118 downloads in the last month

~1 669 416 estimated downloads per year

# Vulnerability

## Vulnerability Description

`superstatic` verifies that current dir is not evaded by checking the presense of `../` in the decoded path, but on Windows, `..\` works.
Code: https://github.com/firebase/superstatic/blob/v5.0.1/lib/providers/fs.js#L71

## Steps To Reproduce:

Install and run superstatic (`npx superstatic` in any dir). It could be also used as a Node.js lib.

Go to `http://localhost:3474/..%5c..%5c..%5c/Windows/notepad.exe` (adjust the path accordingly, that's for `C:\Users\User\tmp`).

*Note: don't use Edge for that, it decodes the path itself. Use e.g. Chromium.*

## Supporting Material/References:

- OS: Windows 10
- Node.js v8.9.4
- npm v5.6.0
- Chromium

# Wrap up

- I contacted the maintainer to let him know: N
- I opened an issue in the related repository: N

## Impact

Read any accessible files outside of the restricted directory.

</details>

---
*Analysed by Claude on 2026-05-24*
