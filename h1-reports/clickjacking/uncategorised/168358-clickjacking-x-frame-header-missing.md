# Clickjacking: X-Frame-Options Header Missing

## Metadata
- **Source:** HackerOne
- **Report:** 168358 | https://hackerone.com/reports/168358
- **Submitted:** 2016-09-14
- **Reporter:** vaxo
- **Program:** Yelp
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Yelp application is vulnerable to clickjacking attacks due to the absence of the X-Frame-Options HTTP security header. An attacker can embed the vulnerable application within an iframe on a malicious webpage and overlay transparent UI elements to trick users into performing unintended actions.

## Attack scenario
1. Attacker creates a malicious webpage that embeds Yelp in a hidden iframe
2. Attacker overlays deceptive UI elements (buttons, links) on top of the iframe content
3. User visits the attacker's webpage believing it to be legitimate
4. User clicks on what appears to be a benign element (e.g., 'Click here for prize')
5. The click actually interacts with the hidden Yelp iframe, triggering unintended actions like review manipulation or account changes
6. Attacker harvests sensitive user data or performs unauthorized actions on behalf of the victim

## Root cause
The application fails to implement the X-Frame-Options HTTP response header (or equivalent Content-Security-Policy frame-ancestors directive), allowing the page to be framed by any third-party domain without restriction.

## Attacker mindset
An attacker seeks to exploit user trust by creating convincing phishing pages or deceptive sites that perform hidden actions on behalf of legitimate services. This could include manipulating reviews, changing account settings, or harvesting credentials through overlay attacks.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN HTTP header on all pages
- Use Content-Security-Policy frame-ancestors directive as a modern alternative: frame-ancestors 'none' or frame-ancestors 'self'
- Apply frame-busting JavaScript code as a secondary defense layer
- Implement SameSite cookie attributes to prevent CSRF-like clickjacking variants
- Use anti-clickjacking headers consistently across all endpoints and content types
- Regularly audit security headers using automated scanning tools

## Variant hunting
Search for other endpoints lacking X-Frame-Options headers; test API endpoints and file download handlers; check for inconsistent header application across subdomains; test older or legacy endpoints that may have been overlooked; verify headers are present on error pages and redirects.

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a classic security header vulnerability. While clickjacking severity is sometimes disputed, it can facilitate credential theft, unauthorized transactions, and social engineering. The PoC demonstrates the basic concept effectively. Remediation is straightforward but requires consistent application across all application endpoints.

## Full report
<details><summary>Expand</summary>

Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.

CODE:
<html>
   <head>
     <title>Clickjack test page</title>
   </head>
   <body>
     <p>Website is vulnerable to clickjacking!</p>
     <iframe src="http://yelp.com" width="500" height="500"></iframe>
   </body>
</html>


For More :  https://www.owasp.org/index.php/Testing_for_Clickjacking_(OWASP-CS-004) 

Proof attatched !

</details>

---
*Analysed by Claude on 2026-05-24*
