# Clickjacking on cas.acronis.com Login Page

## Metadata
- **Source:** HackerOne
- **Report:** 971234 | https://hackerone.com/reports/971234
- **Submitted:** 2020-08-31
- **Reporter:** dgirlwhohacks
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header, Insufficient CSP Configuration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The cas.acronis.com login page lacks clickjacking protections, allowing attackers to embed the page in an iframe and overlay transparent UI elements to trick users into performing unintended actions. An attacker could deceive users into deactivating accounts or performing other sensitive actions without their knowledge by combining this vulnerability with social engineering.

## Attack scenario
1. Attacker creates a malicious HTML page embedding cas.acronis.com in a hidden iframe using frameborder=0 and opacity tricks
2. Attacker overlays transparent buttons or clickable elements on top of the framed login page aligned with legitimate UI controls
3. Attacker sends the malicious page link to target users via email, chat, or social media with enticing pretext (e.g., 'Check your account status')
4. User clicks what appears to be a normal button on the attacker's page, but actually clicks a hidden login button or account settings option within the iframe
5. User unknowingly interacts with the Acronis application within the iframe context, potentially deactivating account, changing settings, or authorizing actions
6. Attack succeeds silently as user believes they clicked on attacker's content while actually interacting with legitimate Acronis functionality

## Root cause
Missing HTTP security headers (X-Frame-Options and/or Content-Security-Policy frame-ancestors directive) that would prevent the page from being embedded in iframes on external domains. The application did not implement clickjacking defenses.

## Attacker mindset
An attacker seeks to perform account takeover or sabotage by leveraging the legitimate authentication context of Acronis. By disguising malicious actions as normal page interactions, they bypass user skepticism. The low technical barrier to exploitation (simple HTML iframe) combined with high impact makes this attractive for social engineering campaigns targeting Acronis users.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all sensitive pages
- Add Content-Security-Policy with frame-ancestors 'self' directive to prevent framing from external origins
- Use additional clickjacking protections: frame-busting JavaScript (though deprecated, can layer defense)
- Implement UI-level protections: confirmation modals for sensitive actions, require explicit user interaction patterns
- Consider SameSite cookie attributes to reduce session hijacking risk from clickjacking exploits
- Conduct security awareness training emphasizing dangers of clicking links from untrusted sources
- Implement regular security scanning to detect missing security headers across all endpoints

## Variant hunting
Check if other Acronis subdomains (account.acronis.com, my.acronis.com, etc.) have same vulnerability
Test for similar clickjacking on password reset, payment processing, and API management pages
Verify if CSP is properly enforced (check for 'unsafe-allow-same-origin' or report-uri bypass)
Test polyglot attack: clickjacking combined with CSRF to amplify impact on state-changing operations
Check for parent framing detection bypasses using nested iframes or same-origin policy exceptions
Audit other single sign-on (SSO) providers that Acronis integrates with for identical vulnerabilities

## MITRE ATT&CK
- T1189
- T1566
- T1204

## Notes
This is a straightforward clickjacking vulnerability with clear business impact (account deactivation). The fix is well-documented but appears not to have been implemented at the time of report. The vulnerability's simplicity to exploit and reliance on social engineering makes it practically dangerous despite medium severity classification. The reference to report #591432 suggests this may be a recurring issue across Acronis properties.

## Full report
<details><summary>Expand</summary>

Steps To Reproduce:

    Create a new HTML file
Source code:
<!DOCTYPE HTML>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<title>I Frame</title>
</head>
<body>
<h2>Clickjacking Vulnerability</h2>
<iframe src="https://cas.acronis.com/" frameborder="0" height="700px" width="850px"></iframe>
</body>
</html>
 
    Save the file as whatever.html
    Open document in browser 

Reference: https://hackerone.com/reports/591432

FIX-
The vulnerability can be fixed by adding "frame-ancestors 'self';" to the CSP (Content-Security-Policy) header.
NOTE

Best Regards,
Dgirl

## Impact

Attacker may tricked user, sending them malicious link then user open it clicked some image and their account unconsciously has been deactivated

</details>

---
*Analysed by Claude on 2026-05-24*
