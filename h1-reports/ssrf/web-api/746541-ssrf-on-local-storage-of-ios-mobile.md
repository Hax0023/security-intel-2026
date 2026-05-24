# SSRF on local storage of iOS mobile

## Metadata
- **Source:** HackerOne
- **Report:** 746541 | https://hackerone.com/reports/746541
- **Submitted:** 2019-11-26
- **Reporter:** l0l1ch3ng
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
1. The tester uploaded the text file, containing "test ssrf" message, in order to proof SSRF attack.
2. Next, the tester uploaded the common file and then manipulate the content and extension file to html format in order to find the application path: <svg/onload=document.write(document.location)> 
3. The tester access that file and found the application path to use for SSRF local file disclosure.


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

1. The tester uploaded the text file, containing "test ssrf" message, in order to proof SSRF attack.
2. Next, the tester uploaded the common file and then manipulate the content and extension file to html format in order to find the application path: <svg/onload=document.write(document.location)> 
3. The tester access that file and found the application path to use for SSRF local file disclosure.
4. Then, the tester uploaded the common file and then manipulate the content and extension file to html format in order to view the local file via SSRF attack: <iframe src="file://.../ssrfpoc.txt" width="400" height="400"></iframe> 
5. The tester access that file and found that this application allow you to access and read the local file successfully.

## Impact

This allow anyone to use other URLs such as that can access documents on the system/application (using file://) a.k.a Sensitive Data Exposure.

</details>

---
*Analysed by Claude on 2026-05-24*
