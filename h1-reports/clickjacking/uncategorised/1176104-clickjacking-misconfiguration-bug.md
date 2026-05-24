# Clickjacking misconfiguration - Missing X-Frame-Options header

## Metadata
- **Source:** HackerOne
- **Report:** 1176104 | https://hackerone.com/reports/1176104
- **Submitted:** 2021-04-27
- **Reporter:** ridoykhan0x1
- **Program:** Sifchain (docs.sifchain.finance)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The target website lacks the X-Frame-Options HTTP response header, allowing the site to be embedded in iframes on attacker-controlled pages. This enables clickjacking attacks where users can be tricked into performing unintended actions on the vulnerable site through UI redressing techniques.

## Attack scenario
1. Attacker creates a malicious website containing an iframe pointing to docs.sifchain.finance
2. Attacker overlays transparent or visually disguised clickable elements on top of the framed content
3. User visits the attacker's website and perceives legitimate content or buttons
4. When user clicks on what they believe is a benign element, they unknowingly interact with the embedded Sifchain page
5. Attacker can harvest sensitive actions like account changes, fund transfers, or credential entry
6. Attack is particularly effective for keystroke hijacking where invisible form fields capture user input

## Root cause
The web server hosting docs.sifchain.finance fails to implement the X-Frame-Options response header or Content-Security-Policy frame-ancestors directive, leaving the application vulnerable to being framed by external domains.

## Attacker mindset
An attacker seeking to perform UI redressing attacks would recognize this misconfiguration as an easy exploitation vector. They could craft sophisticated click-jacking pages to perform account actions, trick users into revealing information, or execute transactions without consent. The lack of framing protection is a low-hanging fruit for social engineering combined with technical exploitation.

## Defensive takeaways
- Implement X-Frame-Options header with value DENY or SAMEORIGIN on all HTTP responses
- Alternatively, use Content-Security-Policy header with frame-ancestors 'none' or 'self'
- Apply headers consistently across all endpoints and applications
- Implement frame-busting JavaScript as secondary defense: if (self !== top) { top.location = self.location; }
- Use SameSite cookie attribute to prevent cookie-based attacks
- Conduct regular security header audits across all domains and subdomains
- Validate that security headers are present in development, staging, and production environments

## Variant hunting
Search for similar misconfiguration across other Sifchain domains (main website, API endpoints, user dashboards). Test all subdomains and paths. Verify whether any sensitive endpoints have been protected while others remain vulnerable. Check for partial implementations (e.g., SAMEORIGIN on some pages but not others). Look for CSP policies that may allow frame-ancestors from trusted but compromised third-party domains.

## MITRE ATT&CK
- T1189 - Drive-by Compromise
- T1566 - Phishing
- T1598 - Phishing for Information
- T1199 - Trusted Relationship

## Notes
This is a straightforward security header misconfiguration. The POC is simple and demonstrates the vulnerability clearly. While clickjacking alone is medium severity, the impact escalates significantly when combined with sensitive operations (fund transfers, permission changes). The researcher properly documented the vulnerability with reference materials and clear reproduction steps. This is a common finding in security audits and should be prioritized for remediation.

## Full report
<details><summary>Expand</summary>

Hi team,

While performing security testing  of your website i have found the vulnerability called Clickjacking.

Many URLS are in scope and vulnerable to Clickjacking.

What is Clickjacking ?

Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.

This vulnerability affects Web Server.

Steps to Reproduce / POC

Vulnerable Urls:https://docs.sifchain.finance

Put every above url one by one in the code of iframe, which  is given below

<!DOCTYPE HTML>

<html lang="en-US">

<head>

<meta charset="UTF-8">

<title>I Frame</title>

</head>

<body>

<h3>clickjacking vulnerability</h3>

<iframe src="https://docs.sifchain.finance"height="550px" width="700px"></iframe>

</body>

</html>

By nil chowdhury

niloychowdhury129@gmail.com

Notice that site is visible in the Iframe

POC is in the attachments. Thanks, waiting for your response.

Reference links: Below are the links which will help you to understand more about this issue including the remediation
https://hackerone.com/reports/8724
https://hackerone.com/reports/289246
https://hackerone.com/reports/1027192
https://hackerone.com/reports/405342
https://hackerone.com/reports/591432

## Impact

Using a similar technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attackers 

</details>

---
*Analysed by Claude on 2026-05-24*
