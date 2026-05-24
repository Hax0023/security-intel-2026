# Arbitrary file upload and stored XSS via ███ support request

## Metadata
- **Source:** HackerOne
- **Report:** 865354 | https://hackerone.com/reports/865354
- **Submitted:** 2020-05-03
- **Reporter:** z32
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
A malicious user can upload files of any type when submitting a support request. 

## Impact
This would allow the attacker to upload malicious executable files as well as `.html` or `.svg` files which would allow the attacker to execute malicious code on behalf of the ████ customer support representative.

## Step-by-step Reproduction Instructions

1. Browse to████████ and create an a

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
A malicious user can upload files of any type when submitting a support request. 

## Impact
This would allow the attacker to upload malicious executable files as well as `.html` or `.svg` files which would allow the attacker to execute malicious code on behalf of the ████ customer support representative.

## Step-by-step Reproduction Instructions

1. Browse to████████ and create an account or sign in if you already have an account.
2. Click `█████ Faculty/Staff IT Support`.
█████████
3. Click `██████ Support`
██████████
4. Complete the form and upload a file of your choice. Click Submit.
█████████
5. You will see that your request has been created, and your files are readily available for download.
█████████
6. If the customer support representative downloads the executable, their machine could be compromised. This is unlikely, however what is more likely is for the representative to open a malicious `.svg` (or `.xls`/`.doc`/etc.) file.
██████████
7. Opening the `.svg` file in a browser would fire the XSS.
███████
8. Instead of the `alert(XSS)` payload, an attacker could use `window.location` to redirect the user to a malicious website. They could also craft a fake login page that would appear to be the `████████` login page. Once the unsuspecting user submits their credentials, the malicious page would redirect the user to the real login page and the users credentials would be stored on the attackers machine.

## Suggested Mitigation/Remediation Actions
Whitelist allowed file types for upload (`.pdf`, `.jpg`, etc) as needed.

## Impact

This would allow the attacker to upload malicious executable files as well as `.html` or `.svg` files which would allow the attacker to execute malicious code on behalf of the █████ customer support representative.

</details>

---
*Analysed by Claude on 2026-05-24*
