# Complete Server Installation Path Disclosure via /ocs/v1.php/cloud/user Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1690510 | https://hackerone.com/reports/1690510
- **Submitted:** 2022-09-03
- **Reporter:** bohwaz
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak
- **CVEs:** CVE-2023-28834
- **Category:** uncategorised

## Summary
The /ocs/v1.php/cloud/user endpoint returns the full server filesystem path to a user's data directory in the storageLocation field. While the endpoint requires authentication, this sensitive internal infrastructure information should not be exposed to authenticated users as it aids attackers in reconnaissance.

## Attack scenario
1. Attacker creates or gains access to a legitimate Nextcloud account
2. Attacker sends GET request to /ocs/v1.php/cloud/user?format=json with valid authentication credentials
3. Server responds with user profile data including storageLocation field
4. Attacker observes full filesystem path (e.g., /home/bohwaz/www/tmp/nextcloud/data/bohwaz)
5. Attacker uses path information for reconnaissance to identify server structure and potential attack vectors
6. Attacker may combine with other vulnerabilities to target specific directories or conduct privilege escalation

## Root cause
The API endpoint returns sensitive internal filesystem path information without sanitization or filtering, exposing the complete storage directory path to authenticated users unnecessarily.

## Attacker mindset
An authenticated attacker or insider uses this disclosure to understand the server's directory structure for further exploitation, combining this information with other vulnerabilities like directory traversal, symlink attacks, or privilege escalation techniques.

## Defensive takeaways
- Sanitize API responses to exclude unnecessary internal filesystem paths
- Implement principle of least privilege - only return data essential for client functionality
- Never expose absolute filesystem paths in API responses unless absolutely required
- Use abstracted storage references instead of actual filesystem paths in client-facing APIs
- Apply defense in depth - assume authenticated users may be compromised or malicious
- Regularly audit API endpoints for information disclosure vulnerabilities
- Implement logging to detect suspicious API query patterns from authenticated users

## Variant hunting
Search for other /ocs/ API endpoints that return file paths, particularly those related to storage, shares, or user configuration. Check WebDAV endpoints (/remote.php/dav/) and file listing endpoints for similar path disclosures. Examine backup/export features that may reveal filesystem structure.

## MITRE ATT&CK
- T1526
- T1087
- T1087.003

## Notes
Low severity due to authentication requirement, but represents a valid information disclosure that reduces attacker reconnaissance cost. The vulnerability appears present since initial install, suggesting it may be by-design rather than a regression. Consider whether exposing storageLocation serves legitimate client use cases before implementing fix.

## Full report
<details><summary>Expand</summary>

https://github.com/nextcloud/server/issues/33883


When doing a GET request on `/ocs/v1.php/cloud/user?format=json` the server returns user data, including one containing the full local server path:

```
            "storageLocation": "/home/bohwaz/www/tmp/nextcloud/data/bohwaz",
```

This is not a big security issue (as you need to be logged-in to get that response), but this is data that an attacker shouldn't be able to know easily.

This happens on a brand new install after using the web installer.

## Impact

Sensitive internal info

</details>

---
*Analysed by Claude on 2026-05-24*
