# Clickjacking on https://nextcloud.com/

## Metadata
- **Source:** HackerOne
- **Report:** 661768 | https://hackerone.com/reports/661768
- **Submitted:** 2019-07-27
- **Reporter:** j4tayu
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Nextcloud.com website is vulnerable to clickjacking attacks due to the absence of proper X-Frame-Options HTTP headers, allowing the site to be embedded in iframes on attacker-controlled pages. An attacker can overlay transparent or disguised UI elements to trick users into performing unintended actions.

## Attack scenario
1. Attacker creates a malicious HTML page and embeds nextcloud.com in a transparent iframe
2. Attacker overlays deceptive UI elements (buttons, links) on top of the iframe content
3. Victim visits the attacker's page and sees what appears to be legitimate content
4. Victim clicks on what they think is a normal button/link, but actually interacts with the hidden Nextcloud page
5. Unintended actions execute in the victim's Nextcloud account (credential changes, file deletion, account modifications)
6. Attacker gains unauthorized access or causes damage to victim's Nextcloud instance

## Root cause
The Nextcloud.com website lacks the X-Frame-Options HTTP response header (or it is not properly configured) that would prevent the page from being embedded in iframes on external domains. The Content-Security-Policy frame-ancestors directive is also likely missing or misconfigured.

## Attacker mindset
An attacker recognizes that users trust legitimate domains and can exploit that trust by creating convincing phishing pages. By embedding the legitimate site invisibly, the attacker leverages visual deception to bypass user awareness of the actual target domain they're interacting with.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all responses
- Add Content-Security-Policy frame-ancestors 'none' or 'self' directive
- Consider frame-busting JavaScript code as an additional layer (though headers are preferred)
- Regularly audit HTTP security headers using tools like OWASP ZAP or Mozilla Observatory
- Educate users about visual indicators of legitimate sites and phishing techniques
- Test websites for clickjacking vulnerabilities as part of security assessment routine

## Variant hunting
Test other Nextcloud subdomains for clickjacking vulnerabilities
Check if admin panels, login pages, or sensitive endpoints have additional protections
Verify whether CSP headers are implemented but configured incorrectly (frame-ancestors * or unsafe values)
Test if the vulnerability exists across different browsers/versions
Check if certain user agent headers affect the security posture
Attempt to bypass with HTML5 object embedding or other frame alternatives

## MITRE ATT&CK
- T1566.002
- T1199
- T1598.004

## Notes
This is a straightforward clickjacking vulnerability report. The PoC is simple but effective. The reporter's English language barrier didn't prevent the vulnerability from being clearly demonstrated. The absence of X-Frame-Options is a common misconfiguration that can lead to serious phishing and account compromise scenarios, particularly for productivity platforms like Nextcloud where users authenticate and perform sensitive operations.

## Full report
<details><summary>Expand</summary>

the vulnerability is Clickjacking

Steps for Reproduce:
1. Create a script like this

<title> Clickjacking! </ title>
<p> The Site is Vulnerability Clickjacking </ p>
<iframe src = "https://www.nextcloud.com" height = "700px" width = "700px"> </ iframe>

2. Enter a file name after saving it in the .html format

Then the web is Vuln Clickjacking

Sorry bad english (im indonesian)

## Impact

By using Clickjacking technique, an attacker hijack's click's
meant for one page and route them to another page, most likely
for another application, domain, or both.

</details>

---
*Analysed by Claude on 2026-05-24*
