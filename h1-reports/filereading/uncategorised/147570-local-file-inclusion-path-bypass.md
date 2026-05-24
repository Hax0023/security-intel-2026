# Local File Inclusion Path Bypass via Mixed Path Separators

## Metadata
- **Source:** HackerOne
- **Report:** 147570 | https://hackerone.com/reports/147570
- **Submitted:** 2016-06-27
- **Reporter:** paulos__
- **Program:** Concrete5
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Local File Inclusion (LFI), Path Traversal, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The LFI fix using strpos() to block '../' sequences was incomplete, failing to account for mixed forward slash and backslash path separators. Attackers could bypass the protection using patterns like '../\', '..\/', '/\..', and '\/..' which normalize to directory traversal on Unix-like systems, allowing arbitrary file inclusion.

## Attack scenario
1. Attacker identifies that Concrete5's path validation only checks for '../', '..\', and similar patterns
2. Attacker crafts a request with mixed separators (e.g., '../\' or '..\/')
3. Operating system path parser normalizes the mixed separators to valid traversal sequences
4. Validation function fails to match the obfuscated patterns and allows the request
5. Attacker traverses directory structure using the bypassed validation
6. Attacker includes and executes arbitrary local files

## Root cause
The developers implemented a blacklist-based defense using strpos() to detect directory traversal patterns, but only checked the canonical forms ('/../', '/..\', etc.). They failed to account for mixed path separator normalization where backslashes on Unix systems are converted to forward slashes by the OS path parser, allowing traversal patterns to evade the filter.

## Attacker mindset
An observant security researcher noticed incomplete path traversal protections after previous fixes were committed. Rather than reporting only what was blocked, they identified the underlying assumption (canonical separator forms) and demonstrated how OS-level path normalization could be weaponized to bypass the fix with alternative separator combinations.

## Defensive takeaways
- Avoid blacklist-based path validation; use whitelist approach with realpath() and canonical path comparison
- Normalize all path separators to a single form before validation across all OS targets
- Use realpath() or similar canonicalization before any file operations to resolve .. sequences
- Consider that different operating systems may parse and normalize paths differently
- Test path filters against mixed separator patterns, URL-encoded variations, and OS-specific behaviors
- Implement defense-in-depth with multiple validation layers rather than relying on single filter
- Use framework-provided secure path handling rather than manual string comparisons

## Variant hunting
Search for other instances of strpos()-based path validation checking only forward slashes. Look for path filters that don't normalize input before validation. Check for rawurldecode() usage without subsequent normalization. Examine other directory traversal filters that may overlook backslash handling on mixed-OS codebases. Test authentication bypasses using similar mixed-separator techniques on any path-based access controls.

## MITRE ATT&CK
- T1190
- T1083
- T1027

## Notes
This is a follow-up to concrete5 issue #59665. The vulnerability demonstrates how OS path normalization features can be exploited when developers assume canonical input forms. The fix required acknowledging that '../\' and '..\/' are equivalent to '../' on Unix systems. The researcher provided constructive suggestions for completing the fix rather than just reporting the bypass.

## Full report
<details><summary>Expand</summary>

Hey,

After reading egix's report #59665 and seeing your fix at https://github.com/concrete5/concrete5/commit/19d0cc81c7cd485b856289ac71ebc0389ea7c3da & https://github.com/concrete5/concrete5/commit/c646dd0defcfa79ef119dca8ba1beba2c5bc91ea I think the fixes are insufficient to stop lfi.

If you are going to stick with the `strpos()` trick, you missed something. 
```php
$path = $request->getPathInfo();
$path = rawurldecode($request->getPathInfo());
 if (substr($path, 0, 3) == '../' || substr($path, -3) == '/..' || strpos($path, '/../') ||
     substr($path, 0, 3) == '..\\' || substr($path, -3) == '\\..' || strpos($path, '\\..\\')) {
``` 
while that is one way to go. you forgot about "../\", " ..\/", "/\.." & "\/.." this works because some oses (unix like) parse the backslash to forward slash and proceed. add those and I think you should be fine. :)

Thanks,
P

</details>

---
*Analysed by Claude on 2026-05-24*
