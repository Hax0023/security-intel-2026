# Unauthenticated Access to Nexus Repository Manager via Default Credentials

## Metadata
- **Source:** HackerOne
- **Report:** 435457 | https://hackerone.com/reports/435457
- **Submitted:** 2018-11-07
- **Reporter:** sbakhour
- **Program:** Imgur
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Default Credentials, Weak Authentication, Insufficient Access Controls, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Nexus Repository Manager at nexus.imgur.com was exposed with default and anonymous user credentials enabled, allowing unauthenticated users to access sensitive artifact repositories. An attacker could view, manage, and manipulate dependencies, potentially poisoning the supply chain or extracting proprietary artifacts.

## Attack scenario
1. Attacker discovers nexus.imgur.com is publicly accessible
2. Attacker attempts default credentials (admin/admin123) or anonymous/anonymous login
3. Attacker successfully authenticates to Nexus Repository Manager dashboard
4. Attacker enumerates available repositories and stored artifacts/dependencies
5. Attacker can upload malicious components, delete legitimate artifacts, or exfiltrate proprietary code
6. Attacker modifies dependency versions to compromise downstream applications

## Root cause
Nexus Repository Manager instance was deployed with default credentials enabled and anonymous user access permitted without proper network segmentation or credential rotation before production deployment.

## Attacker mindset
Opportunistic reconnaissance - scanning for common internal tools exposed on internet-facing domains. Supply chain attack vector - targeting artifact repositories to poison dependencies consumed by applications. Data exfiltration - accessing proprietary libraries and components.

## Defensive takeaways
- Disable or remove default user accounts (admin, anonymous) before production deployment
- Enforce strong, unique credentials for all service accounts
- Restrict Nexus access via network segmentation, VPN, or IP whitelisting
- Implement authentication mechanisms (LDAP, OAuth, SAML) instead of local accounts
- Monitor and audit all repository access and component modifications
- Use artifact signing and checksums to detect tampering
- Implement supply chain security controls and dependency verification
- Regularly audit exposed internal tools and management interfaces

## Variant hunting
Scan for other exposed Nexus/Artifactory instances on company subdomains
Check for default credentials on other artifact repositories (npm, PyPI proxies)
Look for other administrative interfaces with default credentials (Jenkins, GitLab, Kubernetes dashboards)
Enumerate repositories for unsigned or tampered artifacts
Search for exposed artifact managers on cloud storage endpoints

## MITRE ATT&CK
- T1190
- T1200
- T1199
- T1078
- T1526
- T1213
- T1567

## Notes
This is a critical supply chain attack vector. Default credentials on artifact repositories represent one of the highest-impact security misconfigurations. The anonymous user access suggests insufficient security hardening. The reporter provided clear video evidence and responsible disclosure. This type of exposure could allow dependency injection attacks affecting all downstream consumers of Imgur's internal libraries.

## Full report
<details><summary>Expand</summary>

Hello Imgur Administrators,

I am not sure if this falls in your scope but I wanted to alert you that your Nexus Repository Manager can be accessed through https://nexus.imgur.com/
Usually the default user/pass for the NRM are admin/admin123 but there is an alternative way to login using the below default credentials.
user: anonymous
pass: anonymous

I was able to login and I got access to check all the repositories available. I uploaded the attached video as a proof of traversal.
Kindly arrange to remove the user anonymous or change its password & limit the access to the Nexus Repo Manager site https://nexus.imgur.com/

## Impact

The attacker can manage to proxy, collect, and manage your dependencies (delete components & Analyze applications).

</details>

---
*Analysed by Claude on 2026-05-24*
