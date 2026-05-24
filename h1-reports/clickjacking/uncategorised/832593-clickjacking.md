# Clickjacking Vulnerability - Missing X-Frame-Options Header

## Metadata
- **Source:** HackerOne
- **Report:** 832593 | https://hackerone.com/reports/832593
- **Submitted:** 2020-03-27
- **Reporter:** hackerboy404
- **Program:** Kubernetes
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Kubernetes.io website lacks the X-Frame-Options HTTP response header, making it vulnerable to clickjacking attacks. An attacker could frame the website in a malicious context to trick users into performing unintended actions or revealing sensitive information.

## Attack scenario
1. Attacker creates a malicious HTML page that embeds kubernetes.io in an invisible or transparent iframe
2. Attacker overlays their own UI elements on top of the framed content to disguise the true target
3. Attacker tricks users into clicking what appears to be a legitimate button (e.g., 'Download', 'Sign Up')
4. User's click actually activates a hidden element within the kubernetes.io iframe instead
5. This could trigger unintended actions on the legitimate site or expose sensitive information
6. Attack is particularly effective when combined with social engineering to maximize click likelihood

## Root cause
The web server does not set the X-Frame-Options HTTP response header to prevent embedding the page in frames or iframes, leaving the application vulnerable to UI redressing attacks.

## Attacker mindset
An attacker would target high-trust websites like kubernetes.io to leverage user trust and trick them into performing actions they didn't intend. Even without login functionality, the attacker could manipulate users into revealing credentials or redirecting them to phishing pages.

## Defensive takeaways
- Implement X-Frame-Options header with DENY or SAMEORIGIN directive on all pages
- Use Content-Security-Policy (CSP) frame-ancestors directive as modern alternative/complement
- Apply framing protections to all sensitive pages, not just login pages
- Consider implementing UI-based protections like frame-busting JavaScript
- Regularly audit HTTP response headers for security configurations
- Document and enforce security header requirements in development guidelines

## Variant hunting
Search for other kubernetes.io subdomains and related infrastructure lacking X-Frame-Options headers. Test other Cloud Native Computing Foundation projects and open-source documentation sites for similar framing vulnerabilities. Check for partial implementations that only protect certain endpoints.

## MITRE ATT&CK
- T1566.002
- T1187

## Notes
This is a relatively straightforward security header misconfiguration. While the report acknowledges most clickjacking attacks target login pages, the vulnerability still exists for potential credential theft through phishing-style overlays. The severity is medium rather than high due to limited immediate impact on the documentation site itself, though it could be used as a vector for broader attacks. Modern browsers and CSP provide additional protections that may reduce real-world risk.

## Full report
<details><summary>Expand</summary>

Report Submission Form

## Summary:
Clickjacking is an attack that tricks a user into clicking a webpage element which is invisible or disguised as another element
##Description:
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
##Steps to Reproduce:
1. Go to https://kubernetes.io/
2. Generate a HTML code for testing 

<!DOCTYPE HTML>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<title>I Frame</title>
</head>
<body>
<h3>clickjacking vulnerability</h3>
<iframe src="https://kubernetes.io/" height="550px" width="700px"></iframe>
</body>
</html>

Note :- Mostly clickjacking is work on login pages but site dosent have any login page but attacker can steal user credential by manipulating user

## Impact

The hacker selected the UI Redressing (Clickjacking) weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers

</details>

---
*Analysed by Claude on 2026-05-24*
