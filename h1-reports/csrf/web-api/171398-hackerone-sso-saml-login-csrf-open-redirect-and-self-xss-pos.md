# (HackerOne SSO-SAML) Login CSRF, Open Redirect, and Self-XSS Possible Exploitation

## Metadata
- **Source:** HackerOne
- **Report:** 171398 | https://hackerone.com/reports/171398
- **Submitted:** 2016-09-23
- **Reporter:** whhackersbr
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
###Summary:###

Login CSRF, Open Redirect, and Self-XSS Possible Exploitation through HackerOne SSO-SAML

###PoC###

- Go to █████;

Use a browser window with clear cookies.

Source-code:

```
<html>
<body>
	<iframe id="login_csrf_frame" src="████████" style="width:0;height:0;border:0;border:none;"></iframe>
	<script>
		setTimeout(function(){document.location.href = "https://hackerone.com/users/sa

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

###Summary:###

Login CSRF, Open Redirect, and Self-XSS Possible Exploitation through HackerOne SSO-SAML

###PoC###

- Go to █████;

Use a browser window with clear cookies.

Source-code:

```
<html>
<body>
	<iframe id="login_csrf_frame" src="████████" style="width:0;height:0;border:0;border:none;"></iframe>
	<script>
		setTimeout(function(){document.location.href = "https://hackerone.com/users/saml/sign_in?email=████&remember_me=true";}, 5000);
	</script>
</body>
</html>
```

###Impact:###

1) Information Leak

An attacker can use Logout CSRF + Login CSRF against a victim to steal all information sent by the victim to the HackerOne website while using the malicious session, including confidential bug reports.

2) Open Redirect

Since the SSO-SAML l​ogin flow can be started automatically (`GET https://hackerone.com/users/saml/sign_in?email=███`) by an attacker and it redirects to external URLs, the attacker can redirect the user to anywhere.

3) Self-XSS Possible Exploitation​

Some stored Self-XSS's (internal areas accessed just by the victim, etc.) can be exploited through Login CSRF.

```
Malicious page -> HackerOne Login CSRF -> Self-XSS triggers -> Logout -> Wait user actions
```

If the user interacts with the page (sign in with his account, etc.), the attacker can exploit the Self-XSS.

P.S.:

An attacker can add extra dots to the SAML Email Domain in the config dialog.
I didn't test all the implications, but registering a very similar domain could be a bad thing, like `hackerone..com`, `hackerone.com.`, `.hackerone.com` or even `gmail..com` because of typing mistakes (`victim@hackerone..com would redirect the victim to the attacker external login flow`).

</details>

---
*Analysed by Claude on 2026-05-24*
