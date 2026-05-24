# Stored XSS triggered by json key during UI generation

## Metadata
- **Source:** HackerOne
- **Report:** 156347 | https://hackerone.com/reports/156347
- **Submitted:** 2016-08-03
- **Reporter:** ctee
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Stored XSS is triggred from **Indices** -> **Generate a UI Demo**. Typing anything in the **Primary, Secondary, Tertiary, Image or URL attributes** for **User Interface** section. These text box have a drop down which displays the json keys during which XSS is triggered. 

Sample json for XSS would be 
``{
  "<img src=1 onerror=alert(document.domain)>": "hello",
}``

Attached: screen shot


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

Stored XSS is triggred from **Indices** -> **Generate a UI Demo**. Typing anything in the **Primary, Secondary, Tertiary, Image or URL attributes** for **User Interface** section. These text box have a drop down which displays the json keys during which XSS is triggered. 

Sample json for XSS would be 
``{
  "<img src=1 onerror=alert(document.domain)>": "hello",
}``

Attached: screen shot


</details>

---
*Analysed by Claude on 2026-05-24*
