# Improper Access Control on MediaWiki Installation Configuration Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1804174 | https://hackerone.com/reports/1804174
- **Submitted:** 2022-12-14
- **Reporter:** miguel_santareno
- **Program:** U.S. Department of Defense
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Improper Access Control, Missing Authentication, Information Disclosure, Denial of Service
- **CVEs:** None
- **Category:** uncategorised

## Summary
The MediaWiki installation configuration directory (/mw-config/index.php) was accessible without authentication, allowing unauthenticated attackers to restart the application installation process. This represents a critical access control failure on a DoD asset that could lead to application disruption or data compromise.

## Attack scenario
1. Attacker discovers a DoD-hosted MediaWiki instance through reconnaissance
2. Attacker navigates directly to the /mw-config/index.php endpoint without any credentials
3. The endpoint loads the MediaWiki installation interface without authentication checks
4. Attacker accesses the restart installation button exposed in the configuration interface
5. Attacker triggers the installation restart, disrupting application availability
6. Attacker potentially modifies database settings, user credentials, or other critical configuration during reinstallation

## Root cause
The MediaWiki installation configuration directory was not properly restricted after initial setup. The web server (Apache) did not have access control rules preventing unauthorized access to /mw-config/, leaving this administrative interface exposed to unauthenticated requests.

## Attacker mindset
An attacker would recognize that installation/configuration interfaces are high-value targets as they often provide administrative functionality without proper authentication checks. Accessing such endpoints on government systems could enable configuration tampering, service disruption, or preparation for further exploitation.

## Defensive takeaways
- Remove or delete installation/configuration directories after successful application deployment
- Implement web server-level access controls (e.g., Apache RedirectMatch, nginx location blocks) to block access to sensitive administrative paths
- Enforce authentication and authorization checks at both web server and application levels for any administrative endpoints
- Conduct regular security audits to identify exposed installation, config, or backup directories
- Use Web Application Firewalls (WAF) to detect and block access attempts to known installation/config paths
- Implement proper file permissions and directory restrictions on the hosting server
- Monitor access logs for reconnaissance attempts targeting configuration endpoints

## Variant hunting
Check for other common exposed paths: /install/, /setup/, /admin/, /config/, /installer/, /wizard/
Look for backup files in web root: .bak, .backup, .old, config.php~, settings.php.bak
Identify similar issues in other web applications on the same asset (WordPress, Drupal, Joomla, etc.)
Test for information disclosure through directory listing on parent directories
Verify if other installation files are accessible: install.php, setup.php, README files containing version/config info
Check if configuration files are readable via web: wp-config.php, LocalSettings.php, database configuration files

## MITRE ATT&CK
- T1190
- T1526
- T1562
- T1105
- T1098

## Notes
This is a critical finding on a DoD asset indicating incomplete security hardening post-deployment. The fix applied (RedirectMatch 404 /mw-config) is a server-level access control measure. Best practice would be to completely remove the mw-config directory after installation or implement authentication within the application itself. The lack of basic access controls on administrative interfaces suggests potential gaps in the organization's deployment security procedures.

## Full report
<details><summary>Expand</summary>

Hello,

I notice that is possible to restart installation on this media wiki website due to the fact that /mw-config/index.php is available without authentication

Poc:
https://█████████/mw-config/index.php

Regards

## Impact

Attackers can restart the application.

## System Host(s)
███████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Go directly to https://██████████/mw-config/index.php and you should see the restart installation button.

## Suggested Mitigation/Remediation Actions
Block all access to your mw-config folder.

We fixed this by adding:

RedirectMatch 404 /\mw-config



</details>

---
*Analysed by Claude on 2026-05-24*
