# Cross-Site Scripting via 'currentImage' parameter

## Metadata
- **Source:** HackerOne
- **Report:** 3136746 | https://hackerone.com/reports/3136746
- **Submitted:** 2025-05-09
- **Reporter:** jonasdiasrebelo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**
Hi, team!
I discovered a Cross-Site Scripting (XSS) vulnerability on ████ , specifically through the GET method, via 'currentImage' parameter. This vulnerability allows an attacker to inject malicious scripts that could be executed, potentially leading to cookie theft, session hijacking, and other malicious actions.

PoC: ███

When you open the link, will apear one alert(1) pop-up

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

**Description:**
Hi, team!
I discovered a Cross-Site Scripting (XSS) vulnerability on ████ , specifically through the GET method, via 'currentImage' parameter. This vulnerability allows an attacker to inject malicious scripts that could be executed, potentially leading to cookie theft, session hijacking, and other malicious actions.

PoC: ███

When you open the link, will apear one alert(1) pop-up to you. And after you close the pop-up, the "-alert(1)-" will disappear in the URL, but the XSS works.

It's a official website from U.S. Navy:

█████████

## References

████

## Impact

Exploitation of this vulnerability can lead to severe consequences, including but not limited:
Session Hijacking: Attackers can steal cookies and impersonate legitimate users.

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Open the link.

## Suggested Mitigation/Remediation Actions
Apply context-dependent encoding and/or validation to user input rendered on a page.



</details>

---
*Analysed by Claude on 2026-05-24*
