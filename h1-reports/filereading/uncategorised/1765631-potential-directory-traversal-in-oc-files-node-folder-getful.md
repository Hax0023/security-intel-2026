# Directory Traversal in OC\Files\Node\Folder::getFullPath via Path Normalization Order

## Metadata
- **Source:** HackerOne
- **Report:** 1765631 | https://hackerone.com/reports/1765631
- **Submitted:** 2022-11-08
- **Reporter:** nickvergessen
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Nextcloud's Folder::getFullPath() validates paths before normalizing them, allowing attackers to bypass validation by using backslashes that get converted to forward slashes post-validation. This enables directory traversal sequences like '/../' to be introduced after validation passes, potentially allowing file creation outside intended directories.

## Attack scenario
1. Attacker crafts a malicious path containing backslashes and traversal sequences (e.g., '..\..\') which passes isValidPath() validation
2. The path is then passed to normalizePath() which converts backslashes to forward slashes, reconstructing traversal sequences
3. The reconstructed path now contains valid '/../' traversal sequences that were not present during validation
4. newFile() or newFolder() methods use the malicious getFullPath() result to determine file creation location
5. Files are created outside the attacker's intended directory space, potentially overwriting other users' data
6. Directory traversal succeeds because the traversal sequence only became valid after validation completed

## Root cause
The validation and normalization steps are performed in the wrong order. Path validation occurs before character normalization, allowing validators to miss traversal sequences that only become apparent after normalization (specifically backslash-to-forward-slash conversion that reconstructs '/../' patterns).

## Attacker mindset
Exploiting order-of-operations bugs in security controls. The attacker recognizes that validation against normalized paths can be bypassed by introducing characters that transform during normalization, essentially defeating the validator's assumptions about what characters represent directory traversal.

## Defensive takeaways
- Normalize paths BEFORE validation, not after, to ensure validators inspect the actual form that will be used
- Apply all character normalization and path canonicalization before any security checks
- Validate against the final canonical form that will actually be used in file operations
- Use allowlist-based validation rather than blacklist patterns for path traversal detection
- Consider using language-level path manipulation APIs that handle normalization automatically
- Implement defense-in-depth with multiple independent path boundary checks
- Add integration tests that specifically check validation against normalized forms with various bypass attempts

## Variant hunting
Search for other path validation patterns in the codebase where normalization and validation order is reversed. Look for: (1) Any validation function followed by string normalization, (2) Path checks before realpath() or equivalent canonicalization, (3) Validators that don't account for character encoding or escape sequence transformations, (4) Similar patterns in other file handling libraries and frameworks.

## MITRE ATT&CK
- T1190
- T1083

## Notes
This is a classic validation bypass through operation sequencing. The vulnerability demonstrates why security validations should always operate on the final representation that will be used operationally. The use of backslashes is particularly relevant on Windows systems or when supporting cross-platform paths. The impact extends to multi-user systems where one user could access/modify another user's files.

## Full report
<details><summary>Expand</summary>

https://github.com/nextcloud/server/blob/67551f379f3105d117b9d19095dd381450fe40dd/lib/private/Files/Node/Folder.php#L68-L73
is validating and normalizing the string in the wrong order.

Validation checks for `/../` kind of situations and `normalizePath` later on replaces `\` with `/`, so it would be possible to get `/../` again.

```php
	public function getFullPath($path) {
		if (!$this->isValidPath($path)) {
			throw new NotPermittedException('Invalid path');
		}
		return $this->path . $this->normalizePath($path);
	}
```

## Impact

The function seems to be used in newFile() and newFolder() items, allowing to create paths outside of ones own space and overwriting stuff from others.

</details>

---
*Analysed by Claude on 2026-05-24*
