# HackerOne SSO-SAML Login CSRF, Open Redirect, and Self-XSS Exploitation Chain

## Metadata
- **Source:** HackerOne
- **Report:** 171398 | https://hackerone.com/reports/171398
- **Submitted:** 2016-09-23
- **Reporter:** whhackersbr
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Request Forgery (CSRF), Open Redirect, Cross-Site Scripting (Self-XSS), Authentication Bypass, SAML Misconfiguration
- **CVEs:** None
- **Category:** web-api

## Summary
Multiple authentication flaws in HackerOne's SSO-SAML implementation allow attackers to perform login CSRF attacks, exploit open redirects, and chain self-XSS vulnerabilities. An attacker can force a victim to log in with an attacker-controlled session, redirect users to arbitrary external sites, and exploit stored XSS through authentication hijacking.

## Attack scenario
1. Attacker crafts malicious HTML page with hidden iframe that initiates logout CSRF against victim's existing session
2. Attacker's JavaScript automatically triggers login CSRF by navigating to SSO-SAML endpoint with attacker-controlled email parameter
3. Victim's browser processes the login request without user consent, establishing session under attacker's SAML identity
4. Victim unknowingly accesses HackerOne under attacker's session, and any self-XSS payloads stored in victim's profile trigger
5. Attacker can steal sensitive information from victim's account (bug reports, communications) or redirect victim to phishing site via open redirect
6. Self-XSS combined with login CSRF allows session hijacking and credential theft when victim interacts with malicious page

## Root cause
SSO-SAML login endpoint lacks CSRF tokens and state validation parameters. Email parameter is user-controllable without proper anti-CSRF mechanisms. SAML domain validation accepts malformed domains (extra dots, trailing dots). No sameSite cookie attributes or proper redirect URL whitelisting.

## Attacker mindset
Attacker recognizes that SSO flows are often overlooked in security testing due to complexity. By chaining multiple medium-severity vulnerabilities (CSRF + open redirect + self-XSS), they create a critical exploitation path. Discovering SAML domain validation bypass shows attention to configuration logic. Targeting information theft and account compromise maximizes impact.

## Defensive takeaways
- Implement CSRF tokens (state parameter) on all SSO/SAML login initiation endpoints, verified on callback
- Add sameSite=Strict cookie attributes to session cookies to prevent CSRF attacks
- Validate and whitelist redirect URLs in SAML flows; reject open redirects to arbitrary domains
- Implement strict SAML domain validation using exact matching (no extra dots, trailing dots, or typo domains)
- Require user action confirmation before login with pre-filled email addresses
- Sanitize and validate all SAML assertion data before processing
- Implement logout CSRF protection with token validation
- Monitor for unusual SAML assertions or domain mismatches
- Add Content Security Policy headers to prevent self-XSS exploitation

## Variant hunting
Test other SSO providers (OAuth2, OpenID Connect) for similar CSRF vulnerabilities in login flows
Check for state parameter bypass or reuse in SAML callbacks
Hunt for SAML signature validation bypasses (unsigned assertions)
Test XML External Entity (XXE) attacks in SAML processing
Investigate SAML replay attacks by intercepting and reusing assertions
Search for subdomain takeover opportunities using malformed domain variants
Test for SAML attribute injection to escalate privileges
Examine other authentication endpoints for logout CSRF protection gaps
Check for email enumeration through SAML error messages

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1187
- T1556
- T1556.003

## Notes
Report demonstrates sophisticated chaining of multiple authentication vulnerabilities. The SAML domain validation bypass (accepting `hackerone..com`, `gmail..com`) is particularly concerning as it could enable account takeover via homograph attacks. The logout CSRF component is critical because it strips authentication before forced re-login. Self-XSS exploitation through CSRF shows understanding of session context in payload execution. Lack of bounty amount suggests potential resolution or policy issue.

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
