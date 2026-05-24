# Clickjacking Vulnerability in demo.nextcloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 222762 | https://hackerone.com/reports/222762
- **Submitted:** 2017-04-21
- **Reporter:** xsszeeshan
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The demo.nextcloud.com domain was vulnerable to clickjacking attacks due to missing X-Frame-Options HTTP security headers. An attacker could embed the Nextcloud interface in an iframe and overlay malicious content to trick users into performing unintended actions.

## Attack scenario
1. Attacker creates a malicious webpage containing an iframe embedding demo.nextcloud.com
2. Attacker overlays transparent buttons or clickable elements on top of the framed Nextcloud interface
3. Victim visits the attacker's malicious page believing it to be legitimate content
4. Victim attempts to click on what appears to be normal content but actually interacts with hidden Nextcloud elements
5. Unintended actions are executed in the Nextcloud context (file operations, permission changes, account modifications)
6. Attacker gains unauthorized access to user data or modifies Nextcloud settings without explicit user consent

## Root cause
The Nextcloud demo server failed to implement the X-Frame-Options HTTP response header or Content-Security-Policy frame-ancestors directive, allowing the application to be embedded in third-party iframes without restriction.

## Attacker mindset
Opportunistic attacker seeking quick wins through low-effort vulnerability discovery. The writeup suggests limited technical depth, focused on identifying low-hanging fruit through basic iframe embedding tests rather than sophisticated exploitation techniques.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all HTTP responses
- Deploy Content-Security-Policy with frame-ancestors 'none' or 'self' directive
- Add additional UI protections such as frame-busting JavaScript for defense-in-depth
- Regularly scan for missing security headers using automated security testing tools
- Test clickjacking vulnerabilities as part of standard security assessment procedures
- Apply fixes to all environments including demo/staging servers, not just production

## Variant hunting
Check for partial frame-options protection (SAMEORIGIN allowing same-origin framing)
Test CSP bypass through frame-ancestors wildcards or subdomain allowlists
Verify if POST-based actions are protected against clickjacking
Test sensitive endpoints like password reset, permission changes, file sharing for clickjacking
Check if admin panels or configuration pages have different framing policies
Analyze if other Nextcloud instances or subdomains have similar issues

## MITRE ATT&CK
- T1189
- T1566.002

## Notes
This is a straightforward clickjacking vulnerability report with minimal technical detail. The writeup lacks sophistication and provides only a basic proof-of-concept. However, it correctly identifies a real security issue affecting the demo environment. Demo/staging environments are often overlooked in security hardening but should maintain equivalent security controls to production systems.

## Full report
<details><summary>Expand</summary>

Hi Nextcloud,

Clickjacking In https://demo.nextcloud.com

This Is Zeeshan,An Ethical Hacker, I Have Found A Security Issue In Your Site

Clickjacking In nextcloud https://demo.nextcloud.com Page

<html>
<head>

<body>
<p>Website is vulnerable to clickjacking!</p>
<iframe src="https://demo.nextcloud.com" width="500" height="500"></iframe>

</body>
</html>

Please Fix It As Soon As Possible

Best Regards,
Zeeshan Waheed
xsszeeshan@gmail.com

</details>

---
*Analysed by Claude on 2026-05-24*
