# Reflected XSS on /admin/stats.php

## Metadata
- **Source:** HackerOne
- **Report:** 1187820 | https://hackerone.com/reports/1187820
- **Submitted:** 2021-05-07
- **Reporter:** solov9ev
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** CVE-2021-22948
- **Category:** web-api

## Summary
Hi, Security Team!

Linked to the reports:
- https://hackerone.com/reports/1083376
- https://hackerone.com/reports/1097217

In the past reports, we have corrected Reflected XSS. But recently it turned out that with the parameter `breakdown = affiliates`, this vulnerability still works. (Fixed when parameter `breakdown = history`).

- Go to `http://revive-adserver.loc/admin/stats.php?entity=global&

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

Hi, Security Team!

Linked to the reports:
- https://hackerone.com/reports/1083376
- https://hackerone.com/reports/1097217

In the past reports, we have corrected Reflected XSS. But recently it turned out that with the parameter `breakdown = affiliates`, this vulnerability still works. (Fixed when parameter `breakdown = history`).

- Go to `http://revive-adserver.loc/admin/stats.php?entity=global&breakdown=affiliates&statsBreakdown=day%27%20onclick=alert(document.domain)%20accesskey=X%20`
- For the payload to be executed, the user needs to press the access key combination for the hidden input field (for Firefox, Alt+Shift+X, see [this](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/accesskey) for other browsers).

{F1292520}

{F1292519}

## Impact

With this vulnerability, an attacker can for example steal users cookies or redirect users on malicious website.

</details>

---
*Analysed by Claude on 2026-05-24*
