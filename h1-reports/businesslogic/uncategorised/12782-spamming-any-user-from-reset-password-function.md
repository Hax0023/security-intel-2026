# Spamming any user from Reset Password Function

## Metadata
- **Source:** HackerOne
- **Report:** 12782 | https://hackerone.com/reports/12782
- **Submitted:** 2014-05-22
- **Reporter:** coolboss
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
It is possible to spam any user whose email-id is known.

This can be combined with csrf attack i.e automated to send 50 emails with a click.

This is reset password form --->

<form accept-charset="UTF-8" action="https://hackerone.com/users/password" class="new_user" id="new_user" method="post"><div style=""><input name="utf8" value="✓" type="hidden"><input name="authenticity_token" value="

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

It is possible to spam any user whose email-id is known.

This can be combined with csrf attack i.e automated to send 50 emails with a click.

This is reset password form --->

<form accept-charset="UTF-8" action="https://hackerone.com/users/password" class="new_user" id="new_user" method="post"><div style=""><input name="utf8" value="✓" type="hidden"><input name="authenticity_token" value="AjjZNIMzdX598CXInx9CMbovtHbiqL+ziw4qTJ7RFnZQh/oub+mYFKjjNb1TXyITVCpkFPJ21ViG4IQz72KbMQ==" type="hidden"></div>

  <h1 class="narrow-title">Forgot password</h1>

  <div class="narrow-container">
    <p>To retrieve your password enter the email address you used to sign up.</p>

    <div class="input-wrapper-small">
      <input autofocus="autofocus" class="input" id="user_email" name="user[email]" placeholder="Email address" type="email">
    </div>

    <input class="button success is-full-width" data-disable-with="Sending..." name="commit" value="Send" type="submit">
  </div>
</form>

Here,
<input name="authenticity_token" value="AjjZNIMzdX598CXInx9CMbovtHbiqL+ziw4qTJ7RFnZQh/oub+mYFKjjNb1TXyITVCpkFPJ21ViG4IQz72KbMQ==" type="hidden">

authencity token can be used more than one.
Users can be spammed heavily by just simple coding a script.
Only email-id should be known.

I tried it on my own account. I was able to use the token for more than 5 attempts.
This is not best practice.
Only one try must be allowed.

</details>

---
*Analysed by Claude on 2026-05-24*
