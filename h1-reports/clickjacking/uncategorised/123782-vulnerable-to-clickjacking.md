# Clickjacking Vulnerability on grtp.co

## Metadata
- **Source:** HackerOne
- **Report:** 123782 | https://hackerone.com/reports/123782
- **Submitted:** 2016-03-17
- **Reporter:** trabajoduro
- **Program:** GRTP (grtp.co)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The grtp.co website lacks proper clickjacking protections and can be embedded in an iframe on attacker-controlled domains. This allows attackers to overlay transparent UI elements and redirect user clicks to malicious actions without their knowledge.

## Attack scenario
1. Attacker creates a malicious webpage with an iframe embedding grtp.co
2. Attacker overlays transparent buttons or clickable elements on top of the iframe targeting legitimate user interactions (e.g., login, submit forms, account changes)
3. Victim visits the attacker's webpage and interacts with what appears to be normal content
4. Victim's clicks are captured and processed by the underlying grtp.co application within the iframe
5. Attacker performs unauthorized actions on behalf of the victim (e.g., changing settings, transferring funds, deleting data)
6. Victim remains unaware their clicks were hijacked and actions were performed on grtp.co

## Root cause
The application does not implement X-Frame-Options HTTP response headers (or implements them incorrectly with ALLOW-FROM) that would prevent the page from being framed by external domains. The absence of frame-busting JavaScript code provides an additional layer of missing protection.

## Attacker mindset
Attackers recognize that users inherently trust legitimate domains and will click on familiar UI elements. By invisible framing, attackers can chain this vulnerability with social engineering to perform account takeovers, unauthorized transactions, or data manipulation without requiring the user to authenticate separately on the attacker's domain.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all HTTP responses
- Add Content-Security-Policy frame-ancestors directive as modern defense-in-depth (CSP: frame-ancestors 'none' or 'self')
- Implement frame-busting JavaScript code as defense-in-depth for older browser support
- Validate referer headers for sensitive operations, though this is not a complete solution
- Apply SameSite cookie flags to prevent CSRF attacks that may be chained with clickjacking
- Conduct regular security headers audits across all application endpoints
- Educate users about clickjacking risks and suspicious iframe behavior

## Variant hunting
Search for other endpoints on grtp.co and subdomains lacking X-Frame-Options headers; test for partial frame busting bypasses; check if sensitive operations (authentication, account changes) have additional clickjacking protections; verify CSP implementation; test cross-origin form submissions that might be vulnerable to clickjacking combined with CSRF.

## MITRE ATT&CK
- T1189
- T1204

## Notes
This is a straightforward clickjacking vulnerability with clear reproduction steps. The fix is well-documented and standard across the industry. The vulnerability is particularly dangerous when combined with CSRF or when targeting high-value user actions. The reporter correctly cited CWE-693 and provided practical remediation guidance. No CVE was assigned as this appears to be a private vulnerability disclosure.

## Full report
<details><summary>Expand</summary>

Reproduction steps:

1.Open URL :https://grtp.co/
2.put the url in the below code of iframe
<html>
   <head>
     <title>Clickjacking GRTP</title>
   </head>
   <body>
     <p>Website is vulnerable to clickjacking!</p>
     <iframe src="https://grtp.co/" width="500" height="500"></iframe>
   </body>
</html>
3.Observe that site is getting displayed in Iframe

Impact:
By using Clickjacking technique, an attacker hijack's click's
meant for one page and route them to another page, most likely
for another application, domain, or both.

Standard:
SANS CWE-693

Remediation:
Frame busting technique is the better framing protection
technique.
Sending the proper X-Frame-Options HTTP response headers
that instruct the browser to not allow framing from other
domains


</details>

---
*Analysed by Claude on 2026-05-24*
