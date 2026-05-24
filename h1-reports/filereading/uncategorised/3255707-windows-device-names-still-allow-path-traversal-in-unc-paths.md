# Windows Device Names Path Traversal in UNC Paths - CVE-2025-27210 Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 3255707 | https://hackerone.com/reports/3255707
- **Submitted:** 2025-07-16
- **Reporter:** oblivionsage
- **Program:** Node.js
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Path Traversal, Directory Traversal, Incomplete Patch/Fix Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
A path traversal vulnerability exists in Node.js path.join() when processing UNC network paths containing Windows device names (CON, PRN, AUX, etc.), bypassing the CVE-2025-27210 fix. The vulnerability allows attackers to escape intended directories on network shares by leveraging device name handling in UNC path normalization.

## Attack scenario
1. Attacker identifies a Node.js application serving files from a UNC network path (\\server\share\uploads)
2. Attacker crafts a malicious input containing a Windows device name and relative path traversal sequences, such as 'CON:../../../private/passwords.txt'
3. Application passes this input to path.join() to construct the file path, which internally calls normalize()
4. The normalize function processes the UNC path differently than regular paths, failing to apply the CVE-2025-27210 device name prefix protection (the '.\' prefix)
5. Device name is stripped during UNC path processing and traversal sequences are resolved, resulting in access to '../../../private/passwords.txt'
6. Attacker successfully reads sensitive files outside the intended directory on the network share or adjacent shares

## Root cause
The CVE-2025-27210 fix added device name validation for regular local paths by prefixing with '.\', but this mitigation was not applied to UNC path handling within the path.join() and normalize() functions. UNC paths follow a different code path that bypasses the device name detection logic, allowing the vulnerability to persist in network path scenarios.

## Attacker mindset
An attacker recognizing that a previous security fix was incomplete and context-specific would systematically test alternative code paths. By focusing on UNC paths (a legitimate Windows feature for network file access), the attacker bypasses the patch by exploiting the assumption that the fix covered all scenarios. This demonstrates iterative vulnerability discovery and the importance of comprehensive patch validation across all input variations.

## Defensive takeaways
- Apply security fixes uniformly across all code paths handling the same functionality - device name detection must be enforced for both local and UNC paths
- Test security patches against variant inputs and edge cases (UNC paths, relative paths, mixed separators, etc.) during fix validation
- Implement centralized path sanitization that catches device names before any path normalization or joining operations
- Use allowlist-based path validation where possible, restricting access to predefined safe directories rather than relying on traversal prevention alone
- Add comprehensive unit tests covering all path variations (local, UNC, with device names, with traversal sequences) for path manipulation functions
- Consider using path canonicalization followed by strict containment verification rather than prevention-based approaches

## Variant hunting
Test path.join() with: (1) Device names in UNC paths with various traversal depths, (2) Mixed separators (forward and backward slashes), (3) Encoded or case-variation device names (con:, Con:, cOn:), (4) Device names in SMB extended path syntax (\\?\UNC\server\share), (5) Device names in the server or share name component itself, (6) Multiple consecutive device names, (7) Device names combined with symbolic link components in UNC contexts

## MITRE ATT&CK
- T1190
- T1083
- T1057

## Notes
This is a bypass of CVE-2025-27210, indicating the original patch was incomplete. The researcher correctly identified that while the CVE fix addressed normalize() for local paths, it failed to account for UNC path processing which uses different logic. This highlights a common pitfall in security patching: fixing a vulnerability in one context without ensuring the fix applies to all related code paths. The fix requires modifying the UNC-specific path normalization logic to apply the same device name detection and '.\' prefixing strategy used for local paths.

## Full report
<details><summary>Expand</summary>

## Summary:

I found that Windows device names (CON, PRN, AUX, etc.) can still be used for path traversal attacks when working with UNC network paths, even after the CVE-2025-27210 patch. So basically, the fix only covered regular paths but missed the UNC path scenario when using `path.join()`

## Description:

I was testing the recent CVE-2025-27210 fix and noticed something . The patch works fine for regular paths - if I try `path.normalize('CON:../../secret.txt')`, it correctly returns `.\CON:..\..\secret.txt.` Great that's fixed



But then I started testing UNC paths (you know, network paths like `\\server\share`) and found the vulnerability still exists there. The issue is that when you use `path.join()` with a UNC path and a device name, the device name gets stripped and the traversal happens



Here's what I mean:

```javascript
const path = require('path');

// This is fixed (regular path)
console.log(path.normalize('CON:../../secret.txt'));
// Output: .\CON:..\..\secret.txt ✓

// But this is still vulnerable (UNC path)
console.log(path.join('\\\\server\\share\\uploads', 'CON:../../secret.txt'));
// Output: \\server\share\secret.txt ✗
// Should be: \\server\share\uploads\.\CON:..\..\secret.txt
```

{F4574346}


This happens because the normalize function inside `path.join()` handles UNC paths differently than regular paths



## Steps to Reproduce:

1. Use any Node.js version including the latest v24.4.1 (with CVE-2025-27210 fix)

2. Create a simple test file:

```javascript
const path = require('path');

function getNetworkFile(userInput) {
  const basePath = '\\\\\\\\fileserver\\\\public\\\\uploads';
  return path.join(basePath, userInput);
}

console.log(getNetworkFile('CON:../../../private/passwords.txt'));
"
```

3. Run the code

4. Expected result: `\\fileserver\public\uploads\.\CON:..\..\..\private\passwords.txt`

5. Actual result: `\\fileserver\public\private\passwords.txt` (escaped the uploads directory!)


{F4574401}


## Why This is Different from CVE-2025-27210:

So I know what you're thinking - "didn't we just fix this?" Well, kinda. CVE-2025-27210 fixed the issue for regular paths by adding the `.\` prefix when it detects device names. But that fix only applies to direct `normalize()` calls or regular local paths

The difference:

+ CVE-2025-27210: Fixed `path.normalize('CON:../')` for local paths
+ This bug: UNC paths like `\\server\share` + device names still vulnerable when using `path.join()`

It's essentially a bypass of the CVE-2025-27210 fix for network scenarios

## Mitigation:

To fix this, you should apply the same device name validation logic to UNC paths in the `path.join()` function. Specifically, when joining paths that start with `\\,` the code needs to check for device names and add the `.\` prefix just like it does for regular paths

The fix probably needs to go in the normalize function's UNC path handling section, around where it processes paths starting with `\\.`

## Impact

An attacker could read files outside the intended directory on Windows network shares :

+ File sharing applications (escape to other users' folders)
+ Cloud storage systems using UNC paths
+ Corporate network shares (access sensitive documents)
+ Any Node.js app that serves files from network locations

Also, this could lead to lateral movement in corporate networks - imagine escaping from `\\webapp\public` to `\\webapp\C$\Windows\System32\config` or even to other servers like `\\adminserver\C$`.

</details>

---
*Analysed by Claude on 2026-05-24*
