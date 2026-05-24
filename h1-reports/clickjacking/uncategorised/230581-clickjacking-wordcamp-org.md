# Clickjacking vulnerability - Missing X-Frame-Options header on wordcamp.org

## Metadata
- **Source:** HackerOne
- **Report:** 230581 | https://hackerone.com/reports/230581
- **Submitted:** 2017-05-22
- **Reporter:** hasanexpert
- **Program:** wordcamp.org
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
wordcamp.org is vulnerable to clickjacking attacks due to the absence of the X-Frame-Options HTTP response header. This allows attackers to embed the site within an iframe on malicious pages and trick users into performing unintended actions. The vulnerability could be exploited for credential theft, CSRF attacks, or phishing campaigns.

## Attack scenario
1. Attacker creates a malicious webpage and embeds wordcamp.org within an iframe using HTML
2. Attacker overlays transparent or disguised clickable elements on top of the framed content
3. Victim visits the attacker's malicious page believing it to be a legitimate site or content
4. Victim performs actions on the framed wordcamp.org content (e.g., clicks login button, submits form)
5. Attacker captures the victim's actions or credentials through JavaScript event handlers
6. Attacker redirects victim to phishing page or uses stolen credentials for account takeover

## Root cause
The web server is not returning the X-Frame-Options HTTP response header, which would normally restrict whether the page can be framed by other origins. This misconfiguration leaves the application vulnerable to UI redress attacks.

## Attacker mindset
An attacker recognizes that missing frame protection headers allow them to weaponize the legitimate site's trust. They can leverage this to create convincing phishing experiences by overlaying malicious UI elements on the legitimate framed content, tricking users into revealing sensitive information or performing unauthorized actions.

## Defensive takeaways
- Implement X-Frame-Options header with value 'DENY' or 'SAMEORIGIN' to prevent framing from external origins
- Use Content-Security-Policy (CSP) frame-ancestors directive as a modern alternative/complement to X-Frame-Options
- Implement frame-busting JavaScript code as defense-in-depth measure
- Regularly audit HTTP security headers using automated scanning tools
- Apply security headers consistently across all pages and endpoints
- Test for clickjacking vulnerabilities during security assessments

## Variant hunting
Check for missing X-Frame-Options on all subdomains of wordcamp.org
Verify if Content-Security-Policy frame-ancestors directive is properly set
Test if frame-busting JavaScript is present but can be bypassed
Audit other wordcamp sites and WordPress-related domains for the same issue
Check if the vulnerability exists on redirect or error pages
Examine if dynamically generated pages also lack the header

## MITRE ATT&CK
- T1189
- T1598.004

## Notes
The POC in the report incorrectly references blockchain.com instead of wordcamp.org, suggesting potential copy-paste error. The vulnerability is straightforward and easily remediable. The report conflates clickjacking with CSRF and phishing but these are distinct attack vectors. Medium severity is appropriate as exploitation requires user interaction and the impact depends on what actions are available on the framed page.

## Full report
<details><summary>Expand</summary>

Hello Security,
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.
The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
This vulnerability affects Web Server.
IMPACT:
An attacker can host this domain in other evil site by using iframe and if a user fill the given filed it can directly redirect as logs to attacker and after its redirect to your web server.. its lead to steal user information too and use that host site as phishing of your site its CSRF and Clickjacking
POC:
1.Open URL :https://www.blockchain.com/
2.put the url in the below code of iframe
<!DOCTYPE HTML>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<title>i Frame</title>
</head>
<body>
<h3>This is clickjacking vulnerable</h3>
<iframe src="https://www.blockchain.com/" frameborder="2 px" height="500px" width="500px"></iframe>
</body>
</html>

3.Observe that site is getting displayed in Iframe

Impact:
By using Clickjacking technique, an attacker hijack's click's
meant for one page and route them to another page, most likely
for another application, domain, or both.

Remediation:
Frame busting technique is the better framing protection
technique.
Sending the proper X-Frame-Options HTTP response headers
that instruct the browser to not allow framing from other
domains

</details>

---
*Analysed by Claude on 2026-05-24*
