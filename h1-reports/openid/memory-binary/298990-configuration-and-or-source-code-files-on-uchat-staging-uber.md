# Unauthenticated Access to Configuration and Source Code Files on uchat-staging.uberinternal.com

## Metadata
- **Source:** HackerOne
- **Report:** 298990 | https://hackerone.com/reports/298990
- **Submitted:** 2017-12-17
- **Reporter:** gregoryvperry
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Information Disclosure, Misconfiguration, Insecure Direct Object References, Exposure of Sensitive Information
- **CVEs:** CVE-2005-2169, CVE-2005-0202
- **Category:** memory-binary

## Summary
A staging server (uchat-staging.uberinternal.com) exposed sensitive configuration and source code files via direct URL access without requiring OneLogin SSO authentication. Attackers could retrieve compiled JavaScript bundles and potentially other sensitive assets that contained internal system information and credentials.

## Attack scenario
1. Attacker discovers or guesses the staging domain uchat-staging.uberinternal.com
2. Attacker accesses the static asset path /static/main.740f5a0b92c00e72e2e1.js without any authentication
3. Server returns the JavaScript file containing source code, configuration details, and internal references
4. Attacker analyzes the downloaded file to extract API endpoints, internal service names, and system architecture details
5. Attacker uses extracted information to conduct further reconnaissance or targeted attacks against internal systems
6. If credentials or tokens are embedded, attacker gains unauthorized access to additional services

## Root cause
Misconfigured web server that failed to enforce OneLogin SSO authentication on static asset routes. The staging server likely had overly permissive access controls or missing authentication middleware for the /static directory, treating all content as publicly accessible.

## Attacker mindset
An attacker performing reconnaissance on Uber's infrastructure would systematically probe staging/development domains. Finding unauthenticated access to source code is a goldmine for information gathering, allowing them to understand system architecture, identify potential vulnerabilities, and locate sensitive hardcoded values.

## Defensive takeaways
- Enforce authentication and authorization on ALL internal/staging domains, including static assets
- Never serve production or internal source code/bundles via unprotected paths
- Minify and obfuscate JavaScript before deployment; avoid source maps in production/staging
- Use environment-specific configuration that never embeds secrets in static assets
- Implement network-level access controls to restrict staging domains to authorized networks/IPs
- Regularly scan staging environments for unprotected endpoints and misconfigured access controls
- Apply same security standards to staging as production; don't assume staging is low-risk
- Use Content Security Policy headers to restrict asset loading
- Implement authentication middleware that applies to all routes, not just API endpoints

## Variant hunting
Scan other Uber staging domains for similar unauthenticated static asset exposure
Check for exposed .env files, config.js, or settings files at common paths
Look for source maps (.js.map files) that would provide direct source code access
Test other static directories (/assets, /build, /dist) for authentication bypass
Check backup or legacy paths like /static.old, /static_v2, /previous versions
Search for exposed API documentation or Swagger/OpenAPI JSON files
Test for directory listing on static directories
Look for git repositories (.git/config) exposed in static paths
Check for compression-related bypasses (encoded paths, double encoding)

## MITRE ATT&CK
- T1526 - Gather Victim Identity Information
- T1592 - Gather Victim Host Information
- T1040 - Network Sniffing
- T1526.004 - Gather Victim Identity Information: Search for vendors
- T1598 - Phishing for Information

## Notes
This is a classic case of staging environment misconfiguration. The fact that a staging domain was directly accessible without internal network requirements made it a low-hanging fruit for reconnaissance. The report references older CVEs (2005-era) related to local file inclusion, suggesting the fundamental issue of unprotected file access has existed for decades. The specific JavaScript bundle name (main.740f5a0b92c00e72e2e1.js with hash) indicates a modern build pipeline, but proper authentication controls were missing.

## Full report
<details><summary>Expand</summary>

## Summary
Configuration file and/or source code information leakage without Uber OneLogin SSO authentication.

## Security Impact
Misconfiguration on the server results in information leakage without authentication.

## Reproduction Steps
https://uchat-staging.uberinternal.com/static/main.740f5a0b92c00e72e2e1.js

## Specifics
* http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2005-2169
* http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2005-0202
* https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion

## Impact

Access to internal configuration files, system names, and source code.

</details>

---
*Analysed by Claude on 2026-05-24*
