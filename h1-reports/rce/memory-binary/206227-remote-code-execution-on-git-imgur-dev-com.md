# Remote Code Execution on Git.imgur-dev.com via Unpatched GitHub Enterprise Server

## Metadata
- **Source:** HackerOne
- **Report:** 206227 | https://hackerone.com/reports/206227
- **Submitted:** 2017-02-14
- **Reporter:** orange
- **Program:** Imgur
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Remote Code Execution, Use of Hard-coded Cryptographic Key, Insecure Deserialization, Unpatched Software
- **CVEs:** None
- **Category:** memory-binary

## Summary
Imgur's GitHub Enterprise Server instance at git.imgur-dev.com was running an unpatched version (prior to 2.8.7) vulnerable to RCE via a static Rails secret key. The vulnerability stems from hardcoded cryptographic credentials that could be exploited to achieve arbitrary code execution.

## Attack scenario
1. Attacker identifies Imgur's GHE instance at git.imgur-dev.com through reconnaissance
2. Attacker determines the server version is prior to 2.8.7, which is vulnerable to the static key vulnerability
3. Attacker extracts or predicts the static Rails secret key used by the application
4. Attacker crafts a malicious serialized Ruby object using the known secret key
5. Attacker delivers the payload via Rails session cookie or other entry point that processes deserialized objects
6. The unpatched application deserializes the malicious object, achieving remote code execution

## Root cause
GitHub Enterprise Server version prior to 2.8.7 contained a vulnerability related to static/hardcoded Rails secret keys that enabled insecure deserialization attacks. The lack of timely patching left the vulnerability exposed in production.

## Attacker mindset
Opportunistic threat actor performing routine reconnaissance on technology assets. Discovered an internal development server with a known, publicly documented vulnerability in a specific software version. Likely motivated by accessing internal development infrastructure for code theft, lateral movement, or supply chain attacks.

## Defensive takeaways
- Implement automated patch management and version tracking for all GitHub Enterprise Server instances
- Enforce regular security assessments and vulnerability scanning for internal-facing development tools
- Rotate cryptographic keys from default/static values; generate unique keys per deployment
- Restrict network access to development infrastructure (git.imgur-dev.com) to authorized networks/VPN
- Monitor GHE logs for suspicious deserialization attempts and session anomalies
- Implement Web Application Firewall (WAF) rules to detect serialized object injection patterns
- Establish rapid patching SLAs for critical infrastructure software, especially development platforms

## Variant hunting
Search for other Imgur subdomains running outdated GHE versions
Identify other organizations using vulnerable GHE versions with exposed management interfaces
Hunt for Rails applications using hardcoded or predictable secret keys across cloud infrastructure
Check for similar insecure deserialization vulnerabilities in other GitHub Enterprise Server versions
Scan for other Imgur development infrastructure exposed on *.imgur-dev.com domains

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1192 - Spearphishing Link
- T1021 - Remote Services (lateral movement post-compromise)
- T1555 - Credentials from Password Stores (if GHE contains stored credentials)

## Notes
This report demonstrates the critical importance of patch management for development infrastructure. GHE instances often contain sensitive source code and credentials, making them high-value targets. The researcher provided PoC screenshots but full technical details are limited in the provided writeup. Version 2.8.7 was the patched version, suggesting the vulnerability was in 2.8.6 or earlier. This appears to be related to Rails deserialization vulnerabilities present in certain GHE releases.

## Full report
<details><summary>Expand</summary>

Hi, Imgur Security Team:

I just found that your GitHub Enterprise Server(https://git.imgur-dev.com/) didn't patch to the latest version(2.8.7). And there is a Rails static key leads to RCE vulnerability!

You can see the PoC from my screenshots :)

</details>

---
*Analysed by Claude on 2026-05-11*
