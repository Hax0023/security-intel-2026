# Path Traversal Vulnerability in resolve-path via Windows Drive Letters

## Metadata
- **Source:** HackerOne
- **Report:** 315760 | https://hackerone.com/reports/315760
- **Submitted:** 2018-02-13
- **Reporter:** orange
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Improper Input Validation
- **CVEs:** CVE-2018-3732
- **Category:** uncategorised

## Summary
The resolve-path npm module fails to properly validate paths containing Windows drive letters (e.g., 'C:') combined with relative path traversal sequences (../../), allowing attackers to escape the intended root directory. This vulnerability affects popular downstream libraries like KoaJS that depend on resolve-path for security boundary enforcement.

## Attack scenario
1. Attacker identifies an application using resolve-path for file access validation, such as a web server using KoaJS
2. Attacker crafts a malicious path containing a Windows drive letter followed by traversal sequences: 'C:../../'
3. The resolve-path module fails to properly parse the drive letter prefix and sanitize the traversal sequences
4. The validation bypass allows the path to reference files outside the intended root directory
5. Attacker gains unauthorized access to sensitive files on the Windows system (e.g., system files, configuration files)
6. Application serves or processes restricted files that should have been protected by the root path boundary

## Root cause
The resolve-path module does not correctly handle Windows drive letter syntax when combined with relative path traversal sequences. The parser likely fails to normalize paths that begin with drive letters (C:, D:, etc.) before validating traversal sequences, allowing relative components like ../../ to escape the intended security boundary.

## Attacker mindset
An attacker would recognize that path validation libraries often have platform-specific edge cases. By testing Windows-specific path formats (drive letters) combined with common traversal techniques, the attacker discovered that the library doesn't properly normalize these paths before validation, enabling directory escape attacks on Windows systems.

## Defensive takeaways
- Always canonicalize and normalize paths before validation using language-native functions (e.g., path.resolve() in Node.js)
- Test path traversal validation on all supported platforms (Windows, Linux, macOS) with platform-specific path formats
- Validate paths after normalization, not before, to prevent bypasses using alternative path representations
- Implement comprehensive test cases covering drive letters, UNC paths, relative references, and symlinks
- For libraries providing security boundaries, conduct threat modeling specifically for path handling edge cases
- Regular security audits of widely-used dependencies, especially those handling file access validation

## Variant hunting
Search for similar bypasses in other path validation libraries using: Windows drive letter prefixes (C:, D:), UNC paths (\\server\share), mixed separators (/\ combinations), case sensitivity variations, and null byte injection. Test path normalization functions in resolve-path alternatives like path-to-regexp, normalize-path, and custom implementations in web frameworks.

## MITRE ATT&CK
- T1190
- T1083
- T1566

## Notes
The vulnerability was already patched by the maintainer before public disclosure. The high download statistics (2.5M+ annually) indicate widespread potential exposure. Windows drive letter handling represents a critical blind spot in cross-platform path validation libraries. KoaJS and other frameworks depending on resolve-path were potentially vulnerable to arbitrary file access attacks through this bypass.

## Full report
<details><summary>Expand</summary>

The author of `resolve-path` told me that I can submit this to here. The vulnerability already reported to the author and got a fixed!

## Module

**module name:** resolve-path
**version:** 1.3.3
**npm page:** `https://www.npmjs.com/package/resolve-path`

### Description

Resolve a relative path against a root path with validation.

This module would protect against commons attacks like GET /../file.js which reaches outside the root folder.

### Module Stats

Stats
[8264] downloads in the last day
[48226] downloads in the last week
[210556] downloads in the last month

~[2526672] estimated downloads per year

## Description

The library failed to process path like `C:../../` on Windows

## Steps To Reproduce:

```js
require('resolve-path')("C:/windows/temp/", "C:../../")
```

## Supporting Material/References:

- Windows 10
- Node v8.9.4
- NPM 5.6.0

## Wrap up

- [Y] I contacted the maintainer to let him know
- [N] I opened an issue in the related repository

## Impact

This is a high-dependency library, for example: [KoaJS](https://github.com/koajs/koa) is suffered from this vulnerability

[21086] downloads in the last day
[113573] downloads in the last week
[462543] downloads in the last month
~[5550516] estimated downloads per year

</details>

---
*Analysed by Claude on 2026-05-24*
