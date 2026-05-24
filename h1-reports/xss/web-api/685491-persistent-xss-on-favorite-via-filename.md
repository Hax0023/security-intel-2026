# Persistent XSS on favorite via filename

## Metadata
- **Source:** HackerOne
- **Report:** 685491 | https://hackerone.com/reports/685491
- **Submitted:** 2019-08-31
- **Reporter:** foobar7
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
CVSS
----

Medium 6.4 [CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:N](https://www.first.org/cvss/calculator/3.0#CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:N)

Description
-----------

The name of a file is echoed without encoding when favoring the file, leading to persistent XSS. 

POC
---

To place the payload:

- Create a file called `test'"><img src=x onerror=alert(document.location)>.pdf` and u

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

CVSS
----

Medium 6.4 [CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:N](https://www.first.org/cvss/calculator/3.0#CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:N)

Description
-----------

The name of a file is echoed without encoding when favoring the file, leading to persistent XSS. 

POC
---

To place the payload:

- Create a file called `test'"><img src=x onerror=alert(document.location)>.pdf` and upload it. 

To trigger the payload:

- click on ... next to the file followed by "add to favorites". The payload will trigger here.

## Impact

With a successful attack, an attacker can access all data the attacked user has access to, as well as perform arbitrary requests in the name of the attacked user.

</details>

---
*Analysed by Claude on 2026-05-24*
