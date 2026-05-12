# Remote Code Execution via Unauthenticated Apache Solr CVE-2019-0193

## Metadata
- **Source:** HackerOne
- **Report:** 962013 | https://hackerone.com/reports/962013
- **Submitted:** 2020-08-19
- **Reporter:** xy_
- **Program:** Undisclosed
- **Bounty:** Unknown
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Arbitrary Code Execution, Configuration Injection, Authentication Bypass
- **CVEs:** CVE-2019-0192, CVE-2019-0193
- **Category:** memory-binary

## Summary
An unauthenticated Apache Solr instance (version 5.5.1) was exposed without authentication controls, allowing exploitation of CVE-2019-0193 for remote code execution. The attacker was able to access the Core Admin interface, modify configuration files, and execute arbitrary commands on the server.

## Attack scenario
1. Attacker discovers exposed Apache Solr interface at /solr/ endpoint without authentication requirement
2. Attacker identifies vulnerable version 5.5.1 which is susceptible to CVE-2019-0193
3. Attacker accesses Core Admin panel to enumerate available cores and retrieve core configuration paths
4. Attacker crafts malicious configuration update leveraging Solr's Dynamic Configuration feature to inject code
5. Attacker submits configuration request that modifies core settings to include arbitrary code execution payload
6. Malicious code executes with privileges of the Solr process, providing shell access to the server

## Root cause
Multiple security failures: (1) Solr instance exposed without network isolation or access controls, (2) No authentication/authorization mechanisms enabled on Solr endpoints, (3) Outdated version vulnerable to CVE-2019-0193 configuration injection attack, (4) Default Solr configuration allowed dynamic property modifications without validation

## Attacker mindset
Opportunistic attacker scanning for exposed Solr instances (likely through port scanning or service enumeration). Recognized the low-hanging fruit of unauthenticated access and applied known CVE exploits. Minimal sophistication required due to public exploits and detailed vulnerability documentation available.

## Defensive takeaways
- Implement network segmentation and firewall rules to restrict Solr admin interfaces to internal/VPN access only
- Enable Solr authentication and authorization (BasicAuth, Kerberos, or JWT) on all Admin API endpoints
- Keep Apache Solr updated to latest patched versions immediately upon release
- Disable or restrict Core Admin API access if not required for operations
- Implement request filtering to block known malicious configuration payloads
- Deploy Web Application Firewall (WAF) rules to detect Solr exploitation attempts
- Monitor Solr logs for suspicious core administration activities and configuration changes
- Use principle of least privilege for Solr process runtime user account
- Conduct regular vulnerability scanning and penetration testing of search infrastructure
- Implement API rate limiting and disable verbose error messages that leak version information

## Variant hunting
Search for other exposed services using similar patterns: Elasticsearch (CVE-2014-3120), OpenSearch, Splunk, Kibana instances without auth. Look for other Java-based search engines vulnerable to deserialization or expression language injection. Investigate if organization has other Solr deployments at different subdomains or ports. Check for similar authentication bypass issues in related Apache products (Lucene, Derby).

## MITRE ATT&CK
- T1190
- T1200
- T1592
- T1133
- T1021
- T1016

## Notes
Report lacks detailed exploitation steps (heavily redacted), making reproducibility assessment difficult. The CVE-2019-0193 specifically targets Solr's ConfigAPI where dynamic properties can be injected with malicious expressions. Critical that Solr administrative interfaces never be internet-facing. The combination of default credentials/no auth + known CVE is a common pattern in infrastructure reconnaissance and exploitation chains.

## Full report
<details><summary>Expand</summary>

**Summary:**
An unauth solr lead to RCE on ██████████

**Description:**
Hello, I found a solr unauth at https://██████/solr/

This version is 5.5.1, vulnerable with CVE-2019-0192 and CVE-2019-0193, i have try CVE-2019-0193 and successful RCE.

## Impact
Attacker can get shell on server.

## Step-by-step Reproduction Instructions

1. First go to Core Admin and copy path.
██████
2. Update the config.
███████
3. Execute code.
██████████

## Product, Version, and Configuration (If applicable)
Apache Sole 5.5.1
## Suggested Mitigation/Remediation Actions
Update to the latest version and set auth.

## Impact

Attacker can get shell on server.

</details>

---
*Analysed by Claude on 2026-05-12*
