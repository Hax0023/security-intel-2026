# SSRF on testing endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 128685 | https://hackerone.com/reports/128685
- **Submitted:** 2016-04-06
- **Reporter:** agarri_fr
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
# Synopsis

The form at https://www.apitest.io/request accepts (among others) the "url" parameter. This feature allows to reach internal services (like the OpenStack metadata server) or services running on loopback.

# Identified services

http://0x7f.1/ (nginx) => "If you see this page, the nginx web server is successfully installed and
working. Further configuration is required."

http://169.254

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

# Synopsis

The form at https://www.apitest.io/request accepts (among others) the "url" parameter. This feature allows to reach internal services (like the OpenStack metadata server) or services running on loopback.

# Identified services

http://0x7f.1/ (nginx) => "If you see this page, the nginx web server is successfully installed and
working. Further configuration is required."

http://169.254.169.254/meta-data (OpenStack metada) => directoty listing (instance-id, mac, local-ipv4, public-ipv4, network_config/content_path, SUBID, ipv6-addr, ipv6-prefix)

http://0x7f.1:8081/ (vestacp admin panel) => <a href="http://vestacp.com/">Powered by VESTA</a>

# Impacts

The metadata server does't seem to host any sensitive data. However, access to port 8081 may allow to reconfigure the OS or services (untested). Additional services may exist, but it seems that my IP address (81.56.184.117) was just blacklisted on your side.

</details>

---
*Analysed by Claude on 2026-05-24*
