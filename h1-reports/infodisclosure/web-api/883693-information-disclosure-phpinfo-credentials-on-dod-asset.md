# Information Disclosure (PHPINFO/Credentials) on DoD Asset

## Metadata
- **Source:** HackerOne
- **Report:** 883693 | https://hackerone.com/reports/883693
- **Submitted:** 2020-05-27
- **Reporter:** atbabers
- **Program:** Department of Defense (DoD)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Information Disclosure, Credential Exposure, Sensitive Data Exposure, Improper Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
A publicly accessible phpinfo() page on a DoD asset leaks sensitive system information and domain credentials including USERDOMAIN, USERNAME, and PASSWORD environment variables. The exposure allows unauthenticated attackers to gather detailed system configuration and authentication material.

## Attack scenario
1. Attacker discovers publicly accessible phpinfo() page through reconnaissance or directory enumeration
2. Attacker accesses the page without authentication and retrieves full PHP environment details
3. Attacker extracts domain credentials (USERDOMAIN, USERNAME, PASSWORD) from the phpinfo() output
4. Attacker uses harvested credentials for lateral movement or privilege escalation within the DoD network
5. Attacker leverages system configuration details (PHP version, extensions, paths) to identify additional attack vectors
6. Attacker establishes persistent access using compromised credentials

## Root cause
Development/debugging phpinfo() page was deployed to production without authentication controls or removal, exposing sensitive environment variables and system configuration.

## Attacker mindset
An attacker conducting reconnaissance on DoD assets would actively search for information disclosure vulnerabilities. phpinfo() pages are high-value targets as they immediately yield system details and, when misconfigured, credential material. This is often the result of developers leaving debugging tools accessible, providing a low-effort path to system compromise.

## Defensive takeaways
- Never deploy phpinfo() or similar diagnostic pages to production environments
- Implement strict access controls and authentication for any diagnostic/debug endpoints that must exist
- Conduct regular audits to identify and remove development/debugging code from production
- Use environment variable management tools; never embed credentials in application code or accessible configuration
- Implement network segmentation and Web Application Firewalls to block access to suspicious paths
- Enable logging and alerting for access to sensitive diagnostic pages
- Perform regular source code reviews to catch debugging code before deployment

## Variant hunting
Search for other diagnostic pages: phpversion(), phptest.php, info.php, test.php, debug.php
Enumerate common paths: /admin/, /debug/, /test/, /backup/, /.env, /config.php
Check for other information disclosure mechanisms: error pages, directory listings, git repositories, backup files
Look for environment variable exposure in other contexts: error messages, logs, API responses
Search for similar credential leakage: hardcoded passwords in comments, logs, or configuration files

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1592 - Gather Victim Host Information
- T1526 - Enumerate External Targets
- T1580 - Obtain Capabilities
- T1589 - Gather Victim Identity Information

## Notes
This is a common misconfiguration in DoD and government systems where development/testing environments are not properly separated from production. The exposure of domain credentials is particularly critical in enterprise environments where lateral movement is a concern. The vulnerability requires no authentication and can be discovered through basic reconnaissance, making it a high-risk configuration despite being technically straightforward to remediate.

## Full report
<details><summary>Expand</summary>

**Summary:**
A DoD leaks credentials on a phpinfo() page.

**Description:**
https://███ publicly displays a phpinfo() page that leaks system information and credentials.

## Impact
The impact is medium not only due to information leakage of numerous different details such as system information but also the leakage of domain credentials.
USERDOMAIN	███████
USERNAME	██████
█████████PASSWORD']	████████

## Step-by-step Reproduction Instructions

1. Visit: https://████/████
2. Information Disclosed

## Suggested Mitigation/Remediation Actions
████████ BAT  suggests removing the ███ page or requiring authentication before making it accessible.

## Impact

The impact is medium not only due to information leakage of numerous different details such as system information but also the leakage of domain credentials.

</details>

---
*Analysed by Claude on 2026-05-24*
