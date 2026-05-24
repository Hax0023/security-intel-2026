# Stored 'undefined' Cross-site Scripting

## Metadata
- **Source:** HackerOne
- **Report:** 403793 | https://hackerone.com/reports/403793
- **Submitted:** 2018-09-01
- **Reporter:** rootbakar___
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hello KhanAcademy Security Team,

I'm **rootbakar**, I found an XSS bug on 'BIO' in the profile, I used payload XSS **"/><svg/on<script>load=prompt(document.domain);>"/><svg/on<script>load= prompt (document.cookie);>** after I save it appears there is no trigger from the XSS, but when I try to change one of the values in the profile form and when I save it again an XSS trigger appears but with the

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

Hello KhanAcademy Security Team,

I'm **rootbakar**, I found an XSS bug on 'BIO' in the profile, I used payload XSS **"/><svg/on<script>load=prompt(document.domain);>"/><svg/on<script>load= prompt (document.cookie);>** after I save it appears there is no trigger from the XSS, but when I try to change one of the values in the profile form and when I save it again an XSS trigger appears but with the words '**undefined**'. Every time I want to change both '**REAL NAME**' and '**LOCATION**' and when I press the save button again and after a few seconds an XSS trigger appears with the words '**undefined**'

**PoC**
This is Video Link
https://youtu.be/WGeaclSo_5A
(Not Public Video)

Best Regards,

**RootBakar**

## Impact

**Displayed 'undefined' XSS after user repeated click SAVE button**

</details>

---
*Analysed by Claude on 2026-05-24*
