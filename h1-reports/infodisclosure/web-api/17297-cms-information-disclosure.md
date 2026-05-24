# Drupal Version Disclosure via CHANGELOG.txt

## Metadata
- **Source:** HackerOne
- **Report:** 17297 | https://hackerone.com/reports/17297
- **Submitted:** 2014-06-23
- **Reporter:** gangw4n
- **Program:** Uzbey
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Sensitive Information Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
The CHANGELOG.txt file is publicly accessible and discloses the exact Drupal version running on the staging server. This information can be leveraged by attackers during reconnaissance to identify known vulnerabilities affecting that specific version.

## Attack scenario
1. Attacker discovers the target is running Drupal via banner grabbing or web technology detection
2. Attacker accesses /CHANGELOG.txt to confirm exact version number
3. Attacker cross-references disclosed version against public vulnerability databases (CVE databases, Drupal security advisories)
4. Attacker identifies applicable exploits for that specific version
5. Attacker develops targeted attack using identified vulnerabilities
6. Attacker gains unauthorized access or executes malicious code

## Root cause
Sensitive version information stored in publicly accessible default installation files without access restrictions

## Attacker mindset
Reconnaissance and enumeration phase optimization - reducing reconnaissance time by directly obtaining version details instead of inferring them through fingerprinting techniques

## Defensive takeaways
- Remove or restrict access to CHANGELOG.txt and other version-disclosing files (.git, README files, etc.)
- Implement .htaccess rules or web server configuration to deny access to sensitive metadata files
- Use security headers and robots.txt to prevent indexing of sensitive paths
- Apply principle of least privilege - only expose necessary files on production systems
- Implement web application firewall rules to block requests for common reconnaissance files
- Regularly audit server for unintended information disclosure

## Variant hunting
Check for other version-disclosing files: README.txt, INSTALL.txt, VERSION.txt, composer.json, package.json, .git directories, SVN metadata, admin interface footers, HTTP headers (Server, X-Powered-By), source code comments, sitemap.xml patterns, or any CMS-specific version disclosure mechanisms

## MITRE ATT&CK
- T1592
- T1592.004
- T1538

## Notes
Low severity vulnerability on its own but valuable in multi-stage attack chains. Version disclosure is standard reconnaissance; impact depends on availability of exploits for disclosed version. Staging server exposure is particularly problematic as staging environments often have weaker security controls.

## Full report
<details><summary>Expand</summary>

Hi,

I noticed that the CHANGELOG.txt disclose Drupal vesion. It might help an attacker to perform information gathering and help an attacker to find the vulnerabilties from the version.


PoC:
https://staging.uzbey.com/CHANGELOG.txt

</details>

---
*Analysed by Claude on 2026-05-24*
