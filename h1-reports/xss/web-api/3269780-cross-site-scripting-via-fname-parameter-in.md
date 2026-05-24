# Cross-Site Scripting via 'fname' parameter in ███

## Metadata
- **Source:** HackerOne
- **Report:** 3269780 | https://hackerone.com/reports/3269780
- **Submitted:** 2025-07-24
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
I discovered a Cross-Site Scripting (XSS) vulnerability on ███ , specifically through the GET method. This vulnerability allows an attacker to inject malicious scripts that could be executed, potentially leading to cookie theft, session hijacking, and other malicious actions.

Vulnerable parameter: fname
Payload: "'><A HRef=\" AutoFocus OnFocus=;1^(print)``^1>"

## Refer

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
I discovered a Cross-Site Scripting (XSS) vulnerability on ███ , specifically through the GET method. This vulnerability allows an attacker to inject malicious scripts that could be executed, potentially leading to cookie theft, session hijacking, and other malicious actions.

Vulnerable parameter: fname
Payload: "'><A HRef=\" AutoFocus OnFocus=;1^(print)``^1>"

## References

████████

## Impact

Exploitation of this vulnerability can lead to severe consequences, including but not limited:
Session Hijacking: Attackers can steal cookies and impersonate legitimate users.

## System Host(s)
███████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Open the link:

███?ReqType=news&fname=2013.026.jpg%22%27%3E%3CA%20HRef%3d\%22%20AutoFocus%20OnFocus=;1^(print)``^1%3E%22&title=%E2%80%9CCandy%20Bomber%E2%80%9D%20passes%20away%20at%20101

I used the 'print' function to bypass the firewall.

## Suggested Mitigation/Remediation Actions
Apply context-dependent encoding and/or validation to user input rendered on a page.



</details>

---
*Analysed by Claude on 2026-05-24*
