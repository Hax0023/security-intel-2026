# Directory Traversal at staging.jsdelivr.net via Double URL Encoding

## Metadata
- **Source:** HackerOne
- **Report:** 18371 | https://hackerone.com/reports/18371
- **Submitted:** 2014-06-29
- **Reporter:** vineet
- **Program:** jsDelivr
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Directory Traversal, Path Traversal, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A directory traversal vulnerability existed on staging.jsdelivr.net that allowed attackers to bypass path restrictions using double URL-encoded Unicode characters (%25c0%25af representing encoded slash). By chaining multiple encoded traversal sequences, attackers could access arbitrary files outside the intended web root, such as /etc/passwd.

## Attack scenario
1. Attacker identifies that the staging server uses URL decoding to process file requests
2. Attacker discovers that single URL decoding bypass filters aren't sufficient to prevent traversal
3. Attacker crafts a payload using double URL encoding: %25c0%25af (first decoding yields %c0%af, second decoding yields a path separator)
4. Attacker repeats the encoded traversal sequence multiple times to traverse up directory levels
5. Attacker appends target file path (/etc/passwd) after traversal sequences
6. Server processes the request, decodes it, and returns sensitive system files

## Root cause
Insufficient input validation and incomplete filtering of path traversal sequences. The application likely decoded user input once but failed to validate after decoding or didn't account for double-encoded Unicode equivalents of path separators.

## Attacker mindset
An attacker would systematically test encoding variations after discovering basic traversal is blocked. Recognizing that %c0%af is a UTF-8 encoded forward slash, they would apply double encoding to bypass single-pass decoding mechanisms, iterating the payload to traverse multiple directory levels.

## Defensive takeaways
- Implement recursive or iterative decoding validation: decode, validate, repeat until no further decoding occurs
- Use canonical path resolution (realpath/Path.resolve) to normalize paths after decoding
- Implement strict whitelist-based path validation rather than blacklist filtering
- Avoid using user-supplied input directly in file system operations
- Apply path canonicalization before any security checks
- Monitor staging environments with the same security rigor as production
- Use security libraries designed for path validation instead of custom implementations

## Variant hunting
Test alternate Unicode encodings for path separators (%c0%ae for dots, %e0%80%ae)
Attempt triple URL encoding in environments with multiple decoding layers
Combine double encoding with other bypass techniques (backslash variants, null bytes)
Test with normalized Unicode forms (NFC, NFD, NFKC, NFKD)
Check for other jsdelivr subdomains or mirrors with similar vulnerabilities
Attempt case variation bypasses on Windows systems (..%2f vs ..%5c)

## MITRE ATT&CK
- T1083
- T1190
- T1499

## Notes
This vulnerability demonstrates the danger of insufficient input validation in staging environments and the importance of understanding encoding/decoding edge cases. The use of double URL encoding as a bypass technique is a well-known pattern that should be tested whenever path traversal protections are in place. The staging server exposure indicates a gap between production and non-production security controls.

## Full report
<details><summary>Expand</summary>

hi, 

Directory Traversal is a vulnerability which allows attackers to access restricted directories and execute commands outside of the web server's root directory.

POC: go this link ->  

http://staging.jsdelivr.net//..%25c0%25af..%25c0%25af..%25c0%25af..%25c0%25af..%25c0%25af..%25c0%25af..%25c0%25af..%25c0%25af/etc/passwd



</details>

---
*Analysed by Claude on 2026-05-24*
