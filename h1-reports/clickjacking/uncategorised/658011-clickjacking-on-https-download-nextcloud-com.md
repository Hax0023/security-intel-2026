# Clickjacking Vulnerability on download.nextcloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 658011 | https://hackerone.com/reports/658011
- **Submitted:** 2019-07-24
- **Reporter:** bibek1
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The download.nextcloud.com domain is vulnerable to clickjacking attacks because it lacks the X-Frame-Options HTTP security header. An attacker can embed the page in an iframe on a malicious website and overlay transparent or disguised elements to trick users into performing unintended actions like downloading files.

## Attack scenario
1. Attacker creates a malicious webpage that embeds download.nextcloud.com in a hidden or transparent iframe
2. Attacker overlays fake UI elements (buttons, links) on top of the framed content to trick users
3. Victim visits the attacker's webpage, believing they are interacting with legitimate content
4. Victim clicks on what they think is a harmless button, but actually triggers a click on the framed Nextcloud download page
5. Victim unknowingly initiates file downloads or performs other unintended actions on the Nextcloud site
6. Attacker achieves malicious objectives such as distributing malware or causing reputational damage

## Root cause
The server hosting download.nextcloud.com does not set the X-Frame-Options HTTP response header (or Content-Security-Policy frame-ancestors directive) to prevent the page from being embedded in iframes on external domains.

## Attacker mindset
An attacker would exploit this to conduct phishing campaigns, drive unwanted downloads, trick users into performing sensitive actions, or damage Nextcloud's reputation by associating it with malware distribution.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all pages
- Use Content-Security-Policy with frame-ancestors directive as a modern alternative or supplement
- Apply frame-busting JavaScript as a fallback defense mechanism
- Regularly audit all domains and subdomains for missing security headers
- Implement a security header scanning tool in CI/CD pipeline to catch regressions
- Educate users about verifying the URL bar and being cautious with unexpected downloads

## Variant hunting
Check other Nextcloud subdomains (cloud.nextcloud.com, talk.nextcloud.com, etc.) for the same vulnerability
Test if other HTTP security headers are missing (CSP, X-Content-Type-Options, etc.)
Verify if the vulnerability exists on different endpoints within download.nextcloud.com
Check if any authentication mechanisms can be bypassed through clickjacking on login pages
Test for UI-based redressing attacks that could lead to account takeover or data exfiltration

## MITRE ATT&CK
- T1189 - Drive-by Compromise
- T1566 - Phishing
- T1598 - Phishing for Information

## Notes
This is a straightforward clickjacking vulnerability with clear reproducible steps. The fix is simple (add X-Frame-Options header) but the impact is moderate as it can be used as a vector for social engineering and malware distribution. The report demonstrates good security practice by providing clear reproduction steps and a legitimate POC.

## Full report
<details><summary>Expand</summary>

This page is vulnerable to clickjacking https://download.nextcloud.com

Steps to Reproduce:

1. Copy the following code and save it as clickjacking.html
<html>
   <head>
     <title>Clickjack test page</title>
   </head>
   <body>
     <p>Website is vulnerable to clickjacking!</p>
     <iframe src="https://download.nextcloud.com" width="500" height="500"></iframe>
   </body>
</html>

2. Open it in browser

You can see the website is vulnerable to clickjacking

## Impact

Anyone can be tricked to download files without their intention

</details>

---
*Analysed by Claude on 2026-05-24*
