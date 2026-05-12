# Authenticated RCE via .htaccess Blacklist Bypass in Federated Share Copy

## Metadata
- **Source:** HackerOne
- **Report:** 228825 | https://hackerone.com/reports/228825
- **Submitted:** 2017-05-16
- **Reporter:** icewind1991
- **Program:** Nextcloud/Owncloud
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Arbitrary File Upload, Access Control Bypass, Configuration Bypass
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Storage::copyFromStorage function fails to validate blacklisted files (.htaccess) when copying folders from external or federated storage sources. An authenticated attacker can exploit federated sharing to move a malicious .htaccess file and PHP payload from a compromised instance to the target instance's web-accessible data directory, achieving RCE.

## Attack scenario
1. Attacker controls or compromises a Nextcloud instance (nc1) with disabled file blacklist checks
2. Attacker creates a folder structure with .htaccess (configured to allow execution) and malicious PHP file (attack.php)
3. Attacker initiates federated share of the folder from nc1 to target instance (nc2)
4. Authenticated user on nc2 receives and accepts the federated share
5. User moves the shared folder outside the share mount point to the root of their files directory using copyFromStorage
6. Attacker navigates to /data/userid/files/attack/attack.php and executes arbitrary code with web server privileges

## Root cause
The Storage::copyFromStorage function does not apply the blacklist validation (Filesystem.php line 616) to files being copied from external storage sources. The blacklist check exists for direct uploads but is bypassed during cross-storage copy operations, allowing blacklisted extensions like .htaccess to be transferred to protected directories.

## Attacker mindset
Exploit the trust model of federated sharing and the assumption that blacklist enforcement applies uniformly across all file operations. Target the gap between upload restrictions and inter-storage operations by leveraging a compromised or attacker-controlled federated instance.

## Defensive takeaways
- Apply blacklist validation consistently across all file operations (upload, copy, move) regardless of source
- Validate content of copied folders recursively, not just direct uploads
- Implement additional .htaccess protections (read-only, integrity checks) in data directories
- Restrict or sanitize federated share acceptance policies
- Ensure data directory is outside webroot or properly restricted via web server config
- Disable Apache handler directives in data directories via centralized .htaccess
- Implement mandatory file type validation on copied files from external sources
- Log and monitor inter-storage copy operations for suspicious patterns

## Variant hunting
Check if blacklist bypass exists in move/rename operations within same storage
Test if other dangerous files (.htpasswd, .php, .phtml) bypass checks in copy operations
Verify if symlink following in copyFromStorage allows traversal to protected areas
Test if SFTP/S3/external storage copy operations bypass blacklist checks differently
Check if archive extraction (zip/tar) operations apply blacklist validation
Investigate if the fix was applied to all storage backends uniformly

## MITRE ATT&CK
- T1190
- T1190
- T1570
- T1190
- T1574
- T1547

## Notes
This vulnerability requires authentication but assumes attacker controls or can compromise a federated instance. The default Nextcloud/Owncloud setup with webroot-exposed data directory is vulnerable. The bug is in the architecture assumption that external storage sources are trusted; federated sharing breaks this assumption. Severity elevated due to automatic PHP execution in data directory when .htaccess allows it.

## Full report
<details><summary>Expand</summary>

`Storage::copyFromStorage` doesn't check the content of a folder it copies against the list of blacklisted files.
Meaning that if a user has access to an external storage (inc. fed. shares) that contains a .htaccess file, he can move the .htaccess file to the local data directory.

The attack works on any nextcloud/owncloud since federated sharing was introduced that uses apache and has the data directory inside the webroot (as is default)

Steps to reproduce:
- Setup an evil instance (nc1) that has the file blacklist disabled (Filesystem.php line 616)
- create a folder 'sharefolder/attack' in nc1 with the following files
  - .htaccess configured to "allow from all"
  - attack.php with the desired attack
- Setup a non-evil instance (nc2) (or pick an existing nc instance that you want to attack)
- Federated share 'sharefolder' from nc1 to nc2
- In nc2, move 'sharefolder/attack' to 'attack' (outside the share)
- navigate to http://nc2/data/userid/files/attack/attack.php

</details>

---
*Analysed by Claude on 2026-05-12*
