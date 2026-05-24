# Clickjacking and CSRF vulnerability at Mavenlink login page

## Metadata
- **Source:** HackerOne
- **Report:** 14494 | https://hackerone.com/reports/14494
- **Submitted:** 2014-06-02
- **Reporter:** vineet
- **Program:** Mavenlink
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Clickjacking, Cross-Site Request Forgery (CSRF), Missing X-Frame-Options header, Missing CSRF tokens
- **CVEs:** None
- **Category:** web-api

## Summary
The Mavenlink login page at https://app.mavenlink.com/login is vulnerable to clickjacking attacks due to missing X-Frame-Options HTTP header, allowing the page to be embedded in iframes on attacker-controlled domains. This vulnerability can be combined with CSRF attacks to trick users into performing unintended actions such as account creation or credential submission.

## Attack scenario
1. Attacker creates a malicious webpage with an invisible or semi-transparent iframe embedding the Mavenlink login page
2. Attacker hosts this webpage on an external domain and shares it via phishing email or social engineering
3. Victim visits the attacker's webpage believing it to be legitimate content
4. Attacker uses clickjacking techniques to overlay fake UI elements, tricking the victim into clicking on login fields or buttons
5. Victim's credentials or sensitive information is captured by the attacker through form hijacking or keystroke logging
6. Attacker can impersonate the user or redirect credentials to their own server for credential harvesting

## Root cause
The application fails to implement the X-Frame-Options HTTP response header (e.g., 'X-Frame-Options: DENY' or 'SAMEORIGIN') which prevents browsers from rendering the page within iframes on cross-origin domains. Additionally, absence of robust CSRF token validation on sensitive endpoints enables cross-site request forgery attacks.

## Attacker mindset
An attacker would leverage this vulnerability to conduct credential harvesting campaigns, phishing attacks, or unauthorized account access. By embedding the login page in a controlled iframe, they can manipulate user interaction patterns and capture sensitive authentication data without the victim's knowledge of the actual origin.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN HTTP header on all pages, especially authentication pages
- Implement Content-Security-Policy (CSP) header with frame-ancestors directive to control framing contexts
- Add CSRF tokens to all state-changing requests and validate them server-side
- Use SameSite cookie attribute (Strict or Lax) on session cookies to prevent cross-site cookie transmission
- Implement frame-busting JavaScript as a secondary defense mechanism
- Apply anti-clickjacking protections such as visual challenge tokens or user verification on sensitive actions
- Regularly security test authentication and sensitive endpoints for framing vulnerabilities

## Variant hunting
Test other authentication endpoints (password reset, account recovery, MFA setup) for identical framing vulnerabilities
Check for CSRF token validation on account modification endpoints, password changes, and administrative functions
Examine API endpoints for CSRF protection and SameSite cookie configuration
Test for double-submit cookie CSRF patterns and their bypass methods
Verify CSP policy effectiveness and potential bypasses through injection points
Check if clickjacking protections can be bypassed via CSS overlays or pointer events manipulation
Test whether sensitive actions implement additional verification steps (re-authentication, CAPTCHA, OTP)

## MITRE ATT&CK
- T1189
- T1566
- T1598
- T1187
- T1056

## Notes
This report demonstrates a basic but critical vulnerability in a production authentication system. The researcher provided clear POC code and exploitation methodology. The writeup lacks specific technical depth regarding CSRF token validation status and CSP configuration, but the core finding is valid and exploitable. The report was filed on HackerOne's responsible disclosure platform. Modern browsers provide some protection via SameSite cookies (default Lax since Chrome 80+), but this does not eliminate the clickjacking risk or fully mitigate CSRF on older browsers.

## Full report
<details><summary>Expand</summary>

Hello,
My name is Vineet bhardwaj. i am security researcher and i pen test your website( https://app.mavenlink.com/login) and i found there is click jacking attack and CSRF attack can be done.

POC:

<html><head>
<title> CSRF testing </title>
<style>

frame {

opacity: 0.5;
border: none;
position: absolute;
top: 0px;
left: 0px;
z-index: 1000;
}
</style>
</head>
<body>
<script>
window.onbeforeunload = function()
{
return " Do you want to leave ?";
}
</script>
<p> site is vulnerable for CSRF! by Vineet bhardwaj</p>
<iframe id="frame" width="100%" height="100%" src="https://app.mavenlink.com/login"></iframe>
</body>
</html>

Procedure: 1. for test your website is vulnerable to clickjacking or CSRF or not ......
open pen-test-for-CSRF.html (in attachment)

2. in iframe tag give link to https://app.mavenlink.com/login (already given in .html file)

save "pen-test-for-CSRF.html" open in your browser if your website open with the text "site is vulnerable " and given below with your whole site than your domain is vulnerable to clickjacking attack & CSRF.

Impact: An attacker can host this domain in other evil site by using iframe and if a user fill the given filed it can directly redirect as logs to attacker and after its redirect to your web server.. its lead to steal user information too and use that host site as phishing of your site its CSRF and Clickjacking

Note : check the attachment.;- 1. pent-test-for-CSRF.html
2. image for proof

waiting for positive response ........

Thanks,
Vineet

</details>

---
*Analysed by Claude on 2026-05-24*
