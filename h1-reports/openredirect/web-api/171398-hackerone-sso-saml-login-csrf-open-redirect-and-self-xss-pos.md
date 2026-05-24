# HackerOne SSO-SAML Login CSRF, Open Redirect, and Self-XSS Exploitation Chain

## Metadata
- **Source:** HackerOne
- **Report:** 171398 | https://hackerone.com/reports/171398
- **Submitted:** 2016-09-23
- **Reporter:** whhackersbr
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Request Forgery (CSRF), Open Redirect, Cross-Site Scripting (Self-XSS), Authentication Bypass, Domain Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A SAML SSO implementation on HackerOne contains multiple chained vulnerabilities allowing attackers to forge login requests, redirect users to external sites, and potentially exploit self-XSS vulnerabilities. An attacker can leverage login CSRF to establish a malicious session, then chain this with open redirect and stored XSS to compromise victim accounts and exfiltrate confidential bug reports.

## Attack scenario
1. Attacker creates malicious HTML page containing iframe that triggers logout CSRF to clear victim's session
2. Attacker injects JavaScript to redirect victim to SSO-SAML login endpoint with attacker-controlled email parameter
3. Victim loads malicious page in clean browser; SAML flow initiates automatically without user interaction
4. Attacker controls SAML identity provider and establishes authenticated session under attacker's control on victim's browser
5. Attacker chains with stored self-XSS accessible only to authenticated users to execute JavaScript in victim context
6. Attacker exfiltrates confidential data (bug reports, session tokens) while victim is unaware of active malicious session

## Root cause
SAML SSO implementation lacks CSRF protection on login initiation endpoint (GET /users/saml/sign_in?email=X); automatic redirect to external identity providers without state validation; insufficient email domain validation allowing registration of lookalike domains with extra dots; self-XSS in authenticated areas reachable through login CSRF chain

## Attacker mindset
Exploit authentication flow weaknesses to achieve account takeover without credentials; chain multiple weaknesses (CSRF + open redirect + XSS) to bypass security controls; use lookalike domain registration to intercept legitimate SAML flows; exfiltrate high-value data from bug bounty platform

## Defensive takeaways
- Implement CSRF tokens on all state-changing authentication endpoints, including SSO initiators
- Use POST instead of GET for authentication flow initiation to prevent automatic triggering via iframes
- Validate and whitelist SAML redirect URLs; prevent arbitrary external redirects
- Implement strict domain validation for email-based SAML configuration (reject domains with consecutive dots, trailing dots, leading dots)
- Add SameSite=Strict cookie attribute to authentication cookies to prevent CSRF
- Implement proper state parameter validation in SAML flows (prevent parameter injection)
- Sanitize and encode all user-controlled input in authenticated areas to prevent self-XSS exploitation
- Add anomaly detection for rapid login/logout sequences or session creation from unusual contexts
- Use HTTPS only and implement HSTS to prevent interception
- Implement Content-Security-Policy headers to restrict frame embedding of login flows

## Variant hunting
Check other SSO implementations (OAuth2, OpenID Connect) for similar CSRF-on-login-initiation issues
Test email parameter injection in SAML endpoints for open redirect or domain confusion
Search for other state-changing operations triggered via GET requests in authentication flows
Enumerate self-XSS in authenticated-only features that could be reached via CSRF chains
Test domain validation bypass in other integrations (API keys, webhook configurations, email allowlists)
Check for logout CSRF as precursor to login CSRF attacks on other platforms
Analyze SAML metadata for redirect URI validation gaps
Test parameter pollution in SSO endpoints (email=victim@gmail.com&email=attacker@evildom.com)

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1187
- T1485
- T1528
- T1539

## Notes
Report demonstrates sophisticated attack chaining - individual vulnerabilities (CSRF, open redirect, self-XSS) are well-known but the methodical combination to achieve account compromise and data exfiltration is notable. Domain validation bypass via extra dots is a subtle but critical issue often overlooked in internationalization-aware implementations. The use of iframe-triggered logout CSRF followed by automatic login CSRF is a practical exploitation technique. Self-XSS elevation through CSRF is important security lesson - not all XSS requires network-based interaction. Report lacks explicit PoC confirmation and bounty amount, suggesting responsible disclosure process still ongoing.

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
