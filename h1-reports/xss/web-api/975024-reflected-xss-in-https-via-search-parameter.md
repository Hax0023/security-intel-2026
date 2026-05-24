# Reflected XSS in https://███████ via search parameter

## Metadata
- **Source:** HackerOne
- **Report:** 975024 | https://hackerone.com/reports/975024
- **Submitted:** 2020-09-05
- **Reporter:** kegn
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Reflected XSS in https://█████████

**Description:**
I noticed I got an error when visiting https://███.mil stating
```The provided hostname is not valid for this server```

I pinged the site to see that it resolves to https://██████

 ██████

Based on the content of the site I believe this asset is a DOD asset due to the logos and verbiage. The staff page has all @mail.mil email cont

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
Reflected XSS in https://█████████

**Description:**
I noticed I got an error when visiting https://███.mil stating
```The provided hostname is not valid for this server```

I pinged the site to see that it resolves to https://██████

 ██████

Based on the content of the site I believe this asset is a DOD asset due to the logos and verbiage. The staff page has all @mail.mil email contacts. If I should report this to https://www.us-cert.gov/report instead, please allow me to self close this as the owner/operator on this one is tough to determine.

 ██████████

The search parameter is subject to Reflected XSS

 - Visit https://█████/search?search_text=%3Cscript%3Ealert%28document.domain%29%3C%2Fscript%3E
 - See the response in browser

 ████

## Impact

Reflected XSS allows an attacker to send seemingly legitimate links to a victim, potentially stealing cookies or other sensitive session data via unwanted javascript execution

</details>

---
*Analysed by Claude on 2026-05-24*
