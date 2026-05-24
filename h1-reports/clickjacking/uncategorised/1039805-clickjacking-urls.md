# Clickjacking Vulnerability - Missing X-Frame-Options Header

## Metadata
- **Source:** HackerOne
- **Report:** 1039805 | https://hackerone.com/reports/1039805
- **Submitted:** 2020-11-20
- **Reporter:** tinkerermaruthu
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple Nextcloud subdomains lack the X-Frame-Options HTTP header, making them vulnerable to clickjacking attacks where malicious sites can embed pages in invisible iframes to trick users into unintended actions. An attacker can overlay transparent iframes over legitimate content to hijack user interactions including clicks and keystrokes.

## Attack scenario
1. Attacker creates a malicious webpage containing an invisible iframe pointing to a Nextcloud subdomain (e.g., auth.nextcloud.com)
2. The iframe is positioned over visible decoy content (fake login form, file download button, etc.) using CSS styling with opacity near zero
3. User visits the malicious page and perceives legitimate-looking content with call-to-action buttons
4. When user clicks the visible button, they unknowingly interact with the hidden Nextcloud iframe beneath
5. Attacker captures credentials, approves sensitive actions, or transfers files through the hidden frame
6. User remains unaware their actions were performed on the Nextcloud application rather than the decoy content

## Root cause
The web server does not include the X-Frame-Options response header in HTTP responses, leaving the application defenseless against iframe-based embedding. This missing security header fails to restrict where the application can be framed.

## Attacker mindset
An attacker would identify high-value Nextcloud endpoints (authentication, file management, account settings) and craft targeted phishing pages with overlaid invisible iframes to harvest credentials or perform unauthorized actions on behalf of legitimate users.

## Defensive takeaways
- Implement X-Frame-Options header with value 'DENY' or 'SAMEORIGIN' across all application domains
- Deploy Content Security Policy (CSP) with frame-ancestors directive to prevent framing
- Add clickjacking protection JavaScript to break out of frames
- Implement frame-busting code: if (self !== top) { top.location = self.location; }
- Audit all subdomains and internal applications for consistent security header implementation
- Use automated security header scanning to prevent regression
- Consider additional UI security measures for sensitive operations (user confirmation, gesture-based verification)

## Variant hunting
Check for missing X-Frame-Options on internal/admin portals
Test for bypassable frame-busting JavaScript using sandbox attributes
Look for subdomains with inconsistent header implementation
Identify high-privilege endpoints that could be targeted (payment, account deletion, admin panels)
Test hybrid scenarios combining clickjacking with CSRF for amplified impact
Search for legacy endpoints that may have been overlooked in security updates

## MITRE ATT&CK
- T1189
- T1566.002

## Notes
This report demonstrates a widespread vulnerability pattern affecting multiple Nextcloud subdomains. While individual clickjacking risk is often rated as medium, the scale (13+ affected URLs) and potential for credential theft elevate concern. The reporter provided clear reproduction steps but lacked specific impact demonstration. No bounty information was included, suggesting possible duplicate or low-priority classification by the program.

## Full report
<details><summary>Expand</summary>

Hey Team
While performing security testing of your websites i have found the vulnerability called Clickjacking.
Many URLS are in scope and vulnerable to Clickjacking.


The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
This vulnerability affects Web Server.



##Steps to Reproduce

Vulnerable Urls:
 1.https://nextcloud.com
 2.https://download.nextcloud.com
 3.https://help.nextcloud.com
 4.https://apps.nextcloud.com/
 5.https://docs.nextcloud.com
 6.https://crm.nextcloud.com
 7.https://support.nextcloud.com
 8.https://scan.nextcloud.com/
 9.https://lists.nextcloud.com
10.https://portal.nextcloud.com
11.https://auth.nextcloud.com
12.https://pushfeed.nextcloud.com
13.https://newsletter.nextcloud.com



URL one by one into iframe src value  ..
this is the HTML code

<html>
<style>
   iframe {
       position:relative;
       width:500px;
       height:700px;
       opacity:0.0001;
       z-index:2;
   }
   div {
       position:absolute;
       top:500px;
       left:550px;
       z-index:1;
   }
</style>
<iframe src="url"></iframe>
</html>


The Site Is Fully Loaded

## Impact

This  technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email  account, but are instead typing into an invisible frame controlled by the attacker.

I attached a Screenshots
thank you

</details>

---
*Analysed by Claude on 2026-05-24*
