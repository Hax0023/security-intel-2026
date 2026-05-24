# Local File Inclusion (LFI) via Path Traversal in Grafana Plugin Directory

## Metadata
- **Source:** HackerOne
- **Report:** 1419213 | https://hackerone.com/reports/1419213
- **Submitted:** 2021-12-07
- **Reporter:** tess
- **Program:** MariaDB (Grafana instance)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Local File Inclusion (LFI), Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A path traversal vulnerability exists in Grafana's public plugin serving mechanism that allows unauthenticated attackers to access arbitrary files on the server. By manipulating the URL with traversal sequences (../), an attacker can escape the intended plugin directory and read sensitive files like /etc/passwd.

## Attack scenario
1. Attacker identifies the Grafana instance at grafana.mariadb.org
2. Attacker discovers the public plugin endpoint at /public/plugins/
3. Attacker crafts a URL with path traversal sequences: /public/plugins/alertlist/../../../../../../../etc/passwd
4. The web server fails to properly normalize/validate the path before serving the file
5. Attacker successfully reads /etc/passwd and other sensitive files from the server
6. Attacker maps out system structure and identifies additional targets for exploitation

## Root cause
Grafana's handling of public plugin requests does not properly validate or normalize file paths before serving them. The application fails to implement adequate controls to prevent directory traversal attacks, allowing attackers to use ../ sequences to escape the intended plugin directory context.

## Attacker mindset
An attacker would recognize this as a low-effort, high-impact vulnerability. Public-facing Grafana instances are attractive targets for reconnaissance. The ability to read /etc/passwd provides system information useful for further exploitation, and access to other files (config files, SSH keys, application source code) could lead to complete system compromise.

## Defensive takeaways
- Implement strict path canonicalization and validation for all file serving operations
- Use allowlist-based path validation rather than blacklist approaches for traversal sequences
- Ensure the application resolves symbolic links and normalizes paths before checking against allowed directories
- Apply principle of least privilege to file system access - run Grafana with minimal required permissions
- Implement security headers and restrict access to /public/plugins/ endpoint if not required
- Regularly audit and update Grafana to patch known vulnerabilities
- Use Web Application Firewalls (WAF) to detect and block path traversal patterns

## Variant hunting
Test other plugin endpoints: /public/plugins/[other_plugin_names]/../../../
Attempt access to other sensitive files: /etc/shadow, /etc/hosts, /root/.ssh/id_rsa
Test alternative encoding: %2e%2e%2f, ..%2f, ..\\
Check if vulnerability exists in /api/plugins/ or other plugin-related endpoints
Test on other public Grafana instances or similar applications using plugin architecture
Examine if authenticated users have different path validation rules
Investigate if symlink resolution is properly handled

## MITRE ATT&CK
- T1190
- T1566
- T1583.006

## Notes
This is a straightforward but critical vulnerability in a widely-used monitoring tool. The public nature of the endpoint makes it particularly dangerous as no authentication is required. The report lacks detail on the specific Grafana version and remediation timeline, but path traversal bugs in plugin serving mechanisms are well-understood and should be addressed immediately.

## Full report
<details><summary>Expand</summary>

Hello team,

There is an LFI on `https://grafana.mariadb.org/public/plugins/alertlist/../../../../../../../../../../../../../../../../../../../etc/passwd`


{F1537157}

## Impact

LFI

</details>

---
*Analysed by Claude on 2026-05-24*
