# Clickjacking Vulnerability on Mobile Website

## Metadata
- **Source:** HackerOne
- **Report:** 21110 | https://hackerone.com/reports/21110
- **Submitted:** 2014-07-22
- **Reporter:** cliantech
- **Program:** Mavenlink
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The mobile version of Mavenlink (m.mavenlink.com) lacks clickjacking protections, allowing an attacker to frame the site in an iframe and overlay malicious UI elements. The application does not implement the X-Frame-Options HTTP header to prevent framing, making it vulnerable to UI redressing attacks.

## Attack scenario
1. Attacker creates a malicious webpage that loads the Mavenlink mobile site in a hidden iframe
2. Attacker overlays transparent buttons or interactive elements on top of the framed content
3. Victim visits the attacker's webpage, unaware of the hidden iframe beneath
4. When victim clicks on what appears to be legitimate content, they unknowingly interact with Mavenlink (e.g., creating workspaces, modifying settings)
5. Attacker can trick users into performing sensitive actions like workspace creation or data manipulation
6. Session-based CSRF-like attacks can be executed if the victim is already authenticated to Mavenlink

## Root cause
The application server does not set the X-Frame-Options HTTP response header, which is the standard defense against clickjacking. Without this header, browsers allow the page to be embedded in iframes on any origin, enabling UI redressing attacks.

## Attacker mindset
The attacker recognized that mobile interfaces are often overlooked in security reviews and tested a simple framing attack. They provided a clear proof-of-concept and actionable remediation advice, demonstrating security research rather than malicious intent.

## Defensive takeaways
- Implement X-Frame-Options: DENY header on all pages, or use SAMEORIGIN if legitimate framing is required
- Alternatively, use Content-Security-Policy frame-ancestors directive for modern browsers
- Apply clickjacking protections consistently across desktop and mobile versions
- Implement frame-busting JavaScript as a secondary defense: if (self !== top) { top.location = self.location; }
- Test both desktop and mobile versions during security reviews
- Consider SameSite cookie attributes to limit session hijacking via clickjacking

## Variant hunting
Check for X-Frame-Options and CSP frame-ancestors headers on all subdomains (www., m., api., etc.). Test other mobile endpoints, API endpoints, and any user-accessible pages. Verify that the header is present on redirects and error pages. Check if the header is properly set for different user roles (authenticated vs. unauthenticated).

## MITRE ATT&CK
- T1189 - Service Exploitation
- T1557 - Man-in-the-Middle
- T1598 - Phishing

## Notes
This is a straightforward, well-documented clickjacking report. The researcher clearly demonstrated understanding by using a user agent switcher to test the mobile version specifically. The PoC is simple but effective. The recommendation for X-Frame-Options is the standard mitigation. No indication of actual exploitation or data compromise, suggesting responsible disclosure.

## Full report
<details><summary>Expand</summary>

Hi,

You have no implementation of Clickjacking attacks on your mobile version. I have set up a user agent switcher and tried to support my claim with regards to the mobile website.

For proof of concept: <iframe src="https://m.mavenlink.com/#/workspaces/new"></iframe>

For mitigation, you may want to add the HTTP header XFRAMEOPTIONS and set it to DENY.

Attached below is a screenshot. Thanks!


</details>

---
*Analysed by Claude on 2026-05-24*
