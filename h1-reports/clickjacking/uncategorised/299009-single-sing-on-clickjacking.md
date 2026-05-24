# Clickjacking Vulnerability on Semrush Single Sign On Page

## Metadata
- **Source:** HackerOne
- **Report:** 299009 | https://hackerone.com/reports/299009
- **Submitted:** 2017-12-18
- **Reporter:** r0p3
- **Program:** Semrush
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Clickjacking, UI Redress Attack, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Semrush SSO login page at sso.semrush.com is vulnerable to clickjacking attacks due to missing frame-busting protections. An attacker can embed the SSO page in an invisible iframe and trick users into performing unintended actions such as account takeover or credential disclosure.

## Attack scenario
1. Attacker creates a malicious website with the SSO login page embedded in a transparent iframe positioned over legitimate-looking content
2. User visits the attacker's website believing they are interacting with legitimate content
3. Attacker uses CSS styling to overlay fake buttons or content that visually appears as normal page elements
4. User clicks on what they perceive as innocuous elements (e.g., 'Click to play video'), but actually clicks on SSO login buttons
5. User credentials or sensitive account actions are performed without their knowledge or consent
6. Attacker gains unauthorized access to user's Semrush account or captures sensitive information

## Root cause
The Semrush SSO page lacks proper frame-busting mechanisms. Specifically, it is missing the X-Frame-Options HTTP header (or equivalent Content-Security-Policy frame-ancestors directive) that would prevent the page from being embedded in iframes on external domains.

## Attacker mindset
An attacker would recognize that SSO pages are high-value targets since they protect account credentials and access to multiple services. By combining clickjacking with the framing vulnerability, they can perform credential harvesting or account takeover at scale with minimal technical effort, targeting users who trust the Semrush brand.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all authentication pages
- Use Content-Security-Policy header with frame-ancestors directive as a modern alternative
- Implement frame-busting JavaScript code as defense-in-depth (check window.top !== window.self)
- Apply clickjacking protections to all sensitive pages, not just login pages
- Conduct regular security audits and vulnerability scanning to identify missing security headers
- Consider implementing user interaction verification for critical operations
- Use visual indicators or challenges to prevent transparent overlay attacks

## Variant hunting
Look for other Semrush subdomains lacking frame protection (accounts, profile, settings pages). Check other authentication providers for similar missing X-Frame-Options headers. Test for combinations with CSRF vulnerabilities where clickjacking could bypass CSRF tokens.

## MITRE ATT&CK
- T1189 - Service Exploitation
- T1583.001 - Acquire Infrastructure: Domains
- T1598.004 - Phishing for Information: Credential Phishing

## Notes
This is a straightforward but impactful vulnerability. The POC is simple (basic iframe), making it easily exploitable. SSO/authentication pages are critical infrastructure and should have multiple layers of framing protection. The 'Any' browser specification indicates no browser-specific mitigations were effective, confirming lack of server-side protections.

## Full report
<details><summary>Expand</summary>

**Description:** 
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on.
**Browsers Verified In:**
Any

**Steps To Reproduce:** 
Create HTML file containg following code:
` <iframe src="https://sso.semrush.com/"></iframe> `
Execute the HTML file & you will see Single Sing On login page present trough the iframe.


**Supporting Material/References:**

## Impact

Revealing confidential information(credentials) AND/OR taking control of their computer/account while clicking on seemingly innocuous web pages.

</details>

---
*Analysed by Claude on 2026-05-24*
