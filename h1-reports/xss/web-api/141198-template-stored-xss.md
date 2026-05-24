# Template stored XSS

## Metadata
- **Source:** HackerOne
- **Report:** 141198 | https://hackerone.com/reports/141198
- **Submitted:** 2016-05-26
- **Reporter:** s_p_q_r
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The template filed names are not escaped properly, which gives an opportunity to inject HTML tags with javascript there.

1. Log into your account
2. Open the template builder https://%your_domain%.drchrono.com/clinical/advanced_form_builder
3. Create a new template with a field called **<svg onload=alert(document.domain)>**
4. Save the template and share it to the library

I created one such temp

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

The template filed names are not escaped properly, which gives an opportunity to inject HTML tags with javascript there.

1. Log into your account
2. Open the template builder https://%your_domain%.drchrono.com/clinical/advanced_form_builder
3. Create a new template with a field called **<svg onload=alert(document.domain)>**
4. Save the template and share it to the library

I created one such template as a proof of concept:

> https://www.drchrono.com/medical-forms/1460752/aaabbbcccdddeee

The script can also be executed at the search page by onmouseover event:

> https://www.drchrono.com/medical-forms/?query=aaa%22bbb%27ccc%3Cddd%3Eeee

</details>

---
*Analysed by Claude on 2026-05-24*
