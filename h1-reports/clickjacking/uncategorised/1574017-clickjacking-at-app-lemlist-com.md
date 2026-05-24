# Clickjacking at app.lemlist.com

## Metadata
- **Source:** HackerOne
- **Report:** 1574017 | https://hackerone.com/reports/1574017
- **Submitted:** 2022-05-18
- **Reporter:** scriptsavvy
- **Program:** lemlist
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application fails to implement the X-Frame-Options HTTP response header, allowing the website to be embedded in iframes on attacker-controlled domains. This enables clickjacking attacks where users can be tricked into performing unintended actions while believing they are interacting with legitimate content.

## Attack scenario
1. Attacker creates a malicious website and embeds app.lemlist.com in a hidden or transparent iframe
2. Attacker overlays deceptive content (buttons, links) on top of the iframe to trick users into clicking specific locations
3. User visits attacker's malicious site believing they are accessing legitimate content
4. When user clicks on what appears to be a benign button, the click is actually processed by the hidden iframe on app.lemlist.com
5. User unknowingly performs sensitive actions such as changing settings, transferring data, or approving requests within their lemlist account
6. Attacker can harvest keystroke input if text fields are targeted, potentially capturing credentials or sensitive information

## Root cause
The application does not set the X-Frame-Options HTTP response header to DENY or SAMEORIGIN, failing to prevent the page from being framed by external domains. This is a missing security control rather than a logic flaw.

## Attacker mindset
An attacker would identify this vulnerability as a low-effort, high-impact attack vector requiring no authentication and minimal technical sophistication. The attacker could target users with social engineering to visit a malicious site, then leverage the clickjacking vulnerability to perform unauthorized actions on their lemlist account such as modifying team settings, accessing user data, or escalating privileges.

## Defensive takeaways
- Implement X-Frame-Options header set to 'DENY' or 'SAMEORIGIN' on all responses to prevent framing by external domains
- Consider implementing Content-Security-Policy (CSP) with frame-ancestors directive as an additional layer of protection
- Use JavaScript frame-busting code as a secondary defense mechanism to detect and break out of frames
- Apply UI protections such as requiring user interaction (CAPTCHA, confirmation dialogs) for sensitive operations
- Implement SameSite cookie attributes to mitigate session hijacking through clickjacking
- Conduct regular security testing across all in-scope URLs to identify missing security headers
- Implement automated security header scanning in CI/CD pipeline to prevent regression

## Variant hunting
Search for other endpoints across lemlist subdomains and verify X-Frame-Options header presence on all user-facing pages. Check for endpoints handling sensitive operations (authentication, data deletion, permission changes) that may be particularly attractive clickjacking targets. Test different header values (DENY vs SAMEORIGIN) to identify the most appropriate protection level for different page types.

## MITRE ATT&CK
- T1187
- T1189
- T1566

## Notes
This report demonstrates a common and well-understood vulnerability affecting user authentication and authorization flows. The provided proof-of-concept uses an iframe approach that clearly illustrates the vulnerability. While the bounty amount was not disclosed, clickjacking vulnerabilities on sensitive endpoints typically receive moderate bounties ($500-$2000 range). The vulnerability is particularly impactful on authenticated admin/settings pages as demonstrated in the URL. Remediation is straightforward and should be a quick win for the security team.

## Full report
<details><summary>Expand</summary>

Hi team,

While performing security testing of your website i have found the vulnerability called Clickjacking.
Many URLS are in scope and vulnerable to Clickjacking.

What is Clickjacking ?

Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
This vulnerability affects Web Server.


Vulnerable Urls:
=============

https://app.lemlist.com

Put every above url one by one in the code of iframe, which is given below
```javascript
<html lang="tr-TR">
<kafa>
<meta karakter kümesi="UTF-8">
<title>Çerçeve Yapıyorum</title>
</head>
<body>
<h3>clickjacking güvenlik açığı</h3>
<iframe src="https://app.lemlist.com/teams/tea_sgYr5dZr478x4FQ9K/settings/user/usr_Z3GZ4DDHLLyLyZHj5/users" height="550px" width="700px"></iframe>
</body>
</html>
```

## Impact

Using a similar technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
