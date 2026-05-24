# Clickjacking to Change Email Address via Missing X-FRAME-OPTIONS Header

## Metadata
- **Source:** HackerOne
- **Report:** 783191 | https://hackerone.com/reports/783191
- **Submitted:** 2020-01-25
- **Reporter:** paramdham
- **Program:** gener8ads.com
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
The gener8ads.com dashboard lacks X-FRAME-OPTIONS headers, allowing attackers to embed the application in an iframe and perform clickjacking attacks. An attacker can trick users into performing unintended actions such as changing email addresses by overlaying invisible frames on malicious websites.

## Attack scenario
1. Attacker creates a malicious HTML page that embeds the vulnerable gener8ads.com dashboard in an invisible or semi-transparent iframe
2. Attacker hosts this malicious page and tricks users (via phishing, social engineering, or ads) into visiting it
3. User believes they are interacting with benign content on the attacker's page
4. Attacker uses CSS positioning and opacity tricks to align the email change form with visible clickable elements
5. User clicks what appears to be a legitimate button but actually clicks the hidden email change button
6. Account email is changed to attacker-controlled address, compromising account security

## Root cause
The application fails to implement X-FRAME-OPTIONS HTTP response header, which would prevent the page from being embedded in iframes on unauthorized origins. Additionally, the absence of Content-Security-Policy (frame-ancestors) directive leaves the application vulnerable to frame-based attacks.

## Attacker mindset
The attacker seeks to compromise user accounts by leveraging the principle of user trust and cognitive misdirection. By framing the vulnerable application without the user's knowledge, they can perform sensitive actions (email changes, potentially account takeover) without explicit user consent.

## Defensive takeaways
- Implement X-FRAME-OPTIONS: SAMEORIGIN or X-FRAME-OPTIONS: DENY header on all responses
- Use Content-Security-Policy header with frame-ancestors directive as defense-in-depth
- Apply anti-clickjacking measures: use frame-busting JavaScript, token validation on state-changing actions
- Implement SameSite cookie attribute to prevent cross-site request forgery in clickjacking scenarios
- Add user interaction confirmation dialogs for sensitive actions like email changes
- Implement rate limiting on email change requests
- Consider using Content-Security-Policy with sandbox attribute directives

## Variant hunting
Check all other sensitive endpoints (password change, 2FA settings, payment methods) for identical vulnerability
Test other endpoints for missing X-FRAME-OPTIONS to identify scope of clickjacking exposure
Verify if X-FRAME-OPTIONS bypass techniques work (via older browser versions or edge cases)
Assess whether other security headers (CSP, Referrer-Policy) are missing
Check if sensitive actions lack CSRF tokens or have weak CSRF protection
Test if account takeover can be achieved by combining clickjacking with password reset endpoints

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
The PoC provided demonstrates basic clickjacking capability. The actual impact depends on what actions the attacker can induce users to perform. Given the title mentions 'change email address', this is a high-value target as email changes often lead to account takeover. The vulnerability is particularly concerning for financial or sensitive account types. The fix is straightforward and should be prioritized for immediate remediation.

## Full report
<details><summary>Expand</summary>

##Summary



Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

It allows remote attackers to do some clickjacking which can be used for adding arbitrary tasks . Why? Almost all of your page has missing X-FRAME-OPTIONS header.

Websites are at risk of a clickjacking attack when they allow content to be embedded within a frame.





##Proof of concept code :- 

Copy the above code and paste it in notepad and save it with .html extention
and open it in browser


<html> 
<head> 
<title>Clickjack test page</title> 
</head> 
<body> 
<p>Website is vulnerable to clickjacking!</p>

<iframe src="https://gener8ads.com/dashboard/account"  sandbox="allow-top-navigation allow-same-origin allow-scripts" width="500" height="500"></iframe> 

</body> 
</html>


Copy and paste above given code and  save it with hack.html and  open it in browser



------------------------------------------------------------------->

Recommendation :- 

Add X-FRAME-OPTIONS header to mitigate the issue

## Impact

An attacker may use this risk to invisibly load the target website into their own site and trick users into clicking on links which they never intended to. An "X-Frame-Options" header should be sent by the server to either deny framing of content, only allow it from the same origin or allow it from a trusted URIs.

</details>

---
*Analysed by Claude on 2026-05-24*
