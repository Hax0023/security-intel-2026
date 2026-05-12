# Login CSRF, Open Redirect, and Self-XSS in HackerOne SSO-SAML Authentication

## Metadata
- **Source:** HackerOne
- **Report:** 171398 | https://hackerone.com/reports/171398
- **Submitted:** 2016-09-23
- **Reporter:** whhackersbr
- **Program:** HackerOne
- **Bounty:** Undisclosed
- **Severity:** High
- **Vuln:** Cross-Site Request Forgery (CSRF), Open Redirect, Self-XSS, Authentication Bypass, Session Fixation
- **CVEs:** None
- **Category:** web-api

## Summary
HackerOne's SSO-SAML login flow is vulnerable to login CSRF attacks that can force authentication without user consent, combined with open redirect vulnerabilities in the authentication flow. These vulnerabilities can be chained with stored self-XSS to execute arbitrary JavaScript in a victim's authenticated session, potentially exposing sensitive bug reports and confidential information.

## Attack scenario
1. Attacker crafts a malicious HTML page containing an invisible iframe triggering logout CSRF on HackerOne
2. Page redirects victim to SSO-SAML login with attacker-controlled email parameter after 5 seconds
3. Victim's browser automatically submits SAML login request, creating authenticated session under attacker's control
4. Attacker uses open redirect in SAML flow to redirect victim to external malicious site or stored self-XSS payload
5. Stored self-XSS executes in victim's authenticated context, exfiltrating session cookies or sensitive data
6. Victim logs out unknowingly, and attacker accesses victim's account or retains session for information theft

## Root cause
SAML authentication endpoint lacks CSRF tokens on login initialization, allows email parameter manipulation without validation, and redirects to user-controlled URLs without proper validation. Session management does not prevent forced re-authentication with different credentials.

## Attacker mindset
An attacker seeks to perform account takeover and data exfiltration by exploiting authentication flow weaknesses. By chaining multiple vulnerabilities (CSRF + open redirect + self-XSS), they can trick users into authenticated sessions and steal sensitive information from bug reports without direct access to credentials.

## Defensive takeaways
- Implement CSRF tokens on all authentication state-changing endpoints, including SAML login initiation
- Validate and whitelist redirect URLs in SAML flows; reject external redirects or use explicit confirmation
- Enforce strict email domain validation in SAML configuration to prevent homograph attacks (hackerone..com, etc.)
- Implement SameSite cookie attribute (Strict) to prevent CSRF in authentication flows
- Add rate limiting and anomaly detection on login CSRF attempts from multiple IPs
- Sanitize all user-controlled input used in authentication flows, even internal parameters
- Use secure session binding and re-authentication challenges for sensitive operations
- Audit SAML service provider configuration for insecure redirect patterns

## Variant hunting
Test other SSO providers (OAuth, OpenID Connect) for similar CSRF and redirect vulnerabilities
Check for CSRF on password reset and account recovery flows
Investigate if logout CSRF can be chained with forced re-login on other platforms
Search for self-XSS in user profile fields that persist across sessions
Test email validation bypass using internationalized domain names or special characters
Examine SAML assertion validation for signature bypass or modification attacks
Check if open redirect can be chained with stored XSS on redirect landing pages

## MITRE ATT&CK
- T1190
- T1598
- T1200
- T1185
- T1556

## Notes
Report references potential domain confusion attacks via malformed SAML email domain configuration (extra dots, trailing dots). Severity amplified by ability to chain multiple low-severity issues into high-impact account compromise and data theft. Researcher demonstrated understanding of SAML flow internals and session management weaknesses.

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
*Analysed by Claude on 2026-05-12*
