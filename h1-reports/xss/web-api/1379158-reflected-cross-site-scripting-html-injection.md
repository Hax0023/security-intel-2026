# Reflected Cross-Site Scripting/HTML Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1379158 | https://hackerone.com/reports/1379158
- **Submitted:** 2021-10-23
- **Reporter:** jak0_
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
The default ASP page at https://███/redirect/default.asp is vulnerable to reflected Cross-Site Scripting in the "url" parameter. To reproduce the issue just visit the following URL and an alert should pop up:
- https://██████████/redirect/?url=%3Cscript%3Ealert(document.domain)%3C/script%3E

It seems that the redirects subdomain is used to forward users to internal resources, so this vulnerability

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

The default ASP page at https://███/redirect/default.asp is vulnerable to reflected Cross-Site Scripting in the "url" parameter. To reproduce the issue just visit the following URL and an alert should pop up:
- https://██████████/redirect/?url=%3Cscript%3Ealert(document.domain)%3C/script%3E

It seems that the redirects subdomain is used to forward users to internal resources, so this vulnerability could be used to execute JavaScript in the context of an internal user and use the browser as a proxy or steal credentials for internal resources.

In a practical attack scenario, the XSS payload could change the location of the following VPN endpoints to a phishing site and capture VPN credentials:
- https://██████████
- https://██████
- https://███

## Impact

This vulnerability could be used practically in phishing attacks to proxy traffic through internal users' browsers and ultimately lead to internal credential leaks.

</details>

---
*Analysed by Claude on 2026-05-24*
