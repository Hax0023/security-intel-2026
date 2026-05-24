# Clickjacking vulnerability on aspen.io due to missing X-Frame-Options header

## Metadata
- **Source:** HackerOne
- **Report:** 272387 | https://hackerone.com/reports/272387
- **Submitted:** 2017-09-27
- **Reporter:** sadhu16
- **Program:** Aspen
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The domain django.aspen.io is vulnerable to clickjacking attacks due to the absence of the X-Frame-Options HTTP response header. An attacker can embed the vulnerable page in an iframe and trick users into clicking on hidden elements, potentially leading to unauthorized actions or information disclosure. The vulnerability was demonstrated with a simple HTML proof-of-concept that loads the target site in an iframe.

## Attack scenario
1. Attacker creates a malicious HTML page containing an invisible or deceptive overlay with an iframe embedding django.aspen.io
2. Attacker hosts the malicious page on their own server or injects it into a compromised website
3. Victim visits the attacker's malicious page believing it to be a legitimate site
4. Victim perceives they are clicking on buttons or links on the visible page (e.g., 'Click here to win a prize')
5. Clicks actually target hidden interactive elements within the embedded Aspen iframe (e.g., account settings, fund transfers)
6. Victim unknowingly performs sensitive actions on Aspen while logged in, compromising their account security

## Root cause
The web server hosting django.aspen.io fails to include the X-Frame-Options HTTP response header in its responses, allowing the page to be embedded in iframes on arbitrary domains without restriction.

## Attacker mindset
Attacker recognizes a common security misconfiguration and demonstrates it with a straightforward POC. The attacker appears to follow responsible disclosure practices by reporting to the vendor and providing educational resources (OWASP references) alongside the vulnerability report.

## Defensive takeaways
- Implement X-Frame-Options header with value 'DENY' or 'SAMEORIGIN' on all responses to prevent framing
- Alternatively or additionally, implement Content-Security-Policy header with frame-ancestors directive
- Conduct regular security audits to identify missing HTTP security headers across all web applications
- Use automated scanning tools to detect clickjacking vulnerabilities during development and deployment
- Implement frame-busting JavaScript as a secondary defense mechanism for critical pages
- Test that security headers are correctly applied across all subdomains and environments

## Variant hunting
Check all subdomains of aspen.io for similar missing X-Frame-Options headers
Verify if Content-Security-Policy header is also missing or improperly configured
Test other Aspen properties and APIs for clickjacking vulnerabilities
Investigate if the vulnerability persists across different URL paths and endpoints
Examine if the header is missing only on specific pages or globally across the application

## MITRE ATT&CK
- T1566.002
- T1204.1
- T1656

## Notes
This is a well-documented, straightforward vulnerability report. The reporter provided clear POC code, referenced OWASP standards, and offered remediation guidance. While clickjacking severity can vary depending on the sensitivity of actions the embedded site allows, it typically warrants medium severity classification. The vulnerability is easily exploitable but requires social engineering to be effective. The fix is simple and should be applied immediately across all domains.

## Full report
<details><summary>Expand</summary>

Hi Team,

Found vulnerability of clickjacking on the domain "aspen.io".

Please refer the below attached screenshot as POC.

<html>
<head>
<title>Clickjack test page</title>
</head>
<body>
<p>Website is vulnerable to clickjacking!</p>
<iframe src="http://django.aspen.io/en/latest/" height="500"></iframe>
</body>
</html>

2.save it as <anyname>.html eg cj.html
3.and just simply open that in browser

Issue Details :Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.

This vulnerability affects Web Server.

As far as i know this data is enough to prove that your site is vulberable to Clickjacking..
according to OWASP its more than enough..
https://www.owasp.org/index.php/Testing_for_Clickjacking_(OWASP-CS-004)

Solution

https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet
check this out..here is the solution for that.

Refer the attached screenshot for issue details.


</details>

---
*Analysed by Claude on 2026-05-24*
