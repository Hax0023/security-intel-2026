# Clickjacking - Missing X-Frame-Options Header on mercantile.wordpress.org

## Metadata
- **Source:** HackerOne
- **Report:** 258283 | https://hackerone.com/reports/258283
- **Submitted:** 2017-08-09
- **Reporter:** giantfire
- **Program:** WordPress Mercantile
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
The mercantile.wordpress.org website lacks the X-Frame-Options HTTP response header, allowing the site to be embedded in iframes on attacker-controlled pages. This enables clickjacking attacks where users can be tricked into performing unintended actions while believing they are interacting with legitimate content.

## Attack scenario
1. Attacker creates a malicious webpage containing an iframe that embeds mercantile.wordpress.org
2. Attacker overlays transparent or deceptive UI elements on top of the framed content using CSS styling
3. Victim visits the attacker's webpage believing it contains innocent content
4. Victim clicks on what appears to be a button or link on the attacker's page
5. The click actually targets a hidden element within the embedded iframe (e.g., 'Delete Account', 'Authorize Action', 'Transfer Funds')
6. Unintended action is performed on the victim's account at mercantile.wordpress.org without their knowledge

## Root cause
The web server is not sending the X-Frame-Options HTTP response header, which allows the browser to render the page within iframe elements. Without this security header, the server provides no protection against frame-based attacks.

## Attacker mindset
An attacker would recognize that unprotected framing enables social engineering attacks through UI redressing. They would craft convincing decoy pages that trick users into interacting with hidden framed content, potentially compromising accounts or performing unauthorized transactions.

## Defensive takeaways
- Implement X-Frame-Options header with DENY or SAMEORIGIN value on all responses
- Use Content-Security-Policy (CSP) with frame-ancestors directive as modern alternative
- Implement frame-busting JavaScript code as defense-in-depth measure
- Educate users about potential phishing and social engineering risks
- Monitor for suspicious framing patterns in access logs
- Consider implementing SameSite cookie attributes to limit session hijacking via clickjacking

## Variant hunting
Search for other WordPress installations and plugins lacking X-Frame-Options headers. Test other subdomains of wordpress.org. Verify if the vulnerability persists across different endpoints and HTTP methods. Check if CSP headers are also missing as a complementary defense layer.

## MITRE ATT&CK
- T1189 - Service Exploitation
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link

## Notes
This is a straightforward clickjacking vulnerability report with clear POC. The fix is trivial (add one HTTP header) but the impact can be significant depending on actions available within the framed context. WordPress.org properties should prioritize this remediation. The reporter demonstrated good vulnerability disclosure practices with clear explanation and reproducible steps.

## Full report
<details><summary>Expand</summary>

Hi team,

While performing security testing of your website i have found the vulnerability called Clickjacking.

What is Clickjacking ?
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.
The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
This vulnerability affects Web Server.

>> Steps to Reproduce / POC
1. Please Open URL: https://mercantile.wordpress.org/
2. Put the url in the code of iframe, which is given below

<!DOCTYPE HTML>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<title>I Frame</title>
</head>
<body>
<h3>clickjacking vulnerability</h3>
<iframe src="https://mercantile.wordpress.org/" frameborder="5 px" height="550px" width="700px"></iframe>
</body>
</html>

3. Notice that site is visible in the Iframe

POC is in the attachments. Thanks, waiting for your response.

Regards
giantfire

</details>

---
*Analysed by Claude on 2026-05-24*
