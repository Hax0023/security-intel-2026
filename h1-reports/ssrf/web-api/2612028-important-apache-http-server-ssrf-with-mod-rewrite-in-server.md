# important: Apache HTTP Server: SSRF with mod_rewrite in server/vhost context on Windows (CVE-2024-40898)

## Metadata
- **Source:** HackerOne
- **Report:** 2612028 | https://hackerone.com/reports/2612028
- **Submitted:** 2024-07-19
- **Reporter:** xi4o7unj1e
- **Program:** Unknown
- **Bounty:** $4,263
- **Severity:** high
- **Vuln:** ssrf
- **CVEs:** CVE-2024-40898
- **Category:** web-api

## Summary
I reported this vulnerability through the official Apache HTTP Server security email on 2024-07-12, and received a CVE number on 2024-07-17. You can check detailed information from here:
https://httpd.apache.org/security/vulnerabilities_24.html

## Impact

SSRF in Apache HTTP Server on Windows with mod_rewrite in server/vhost context, allows to potentially leak NTLM hashes to a malicious server vi

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

I reported this vulnerability through the official Apache HTTP Server security email on 2024-07-12, and received a CVE number on 2024-07-17. You can check detailed information from here:
https://httpd.apache.org/security/vulnerabilities_24.html

## Impact

SSRF in Apache HTTP Server on Windows with mod_rewrite in server/vhost context, allows to potentially leak NTLM hashes to a malicious server via SSRF and malicious requests.

</details>

---
*Analysed by Claude on 2026-05-24*
