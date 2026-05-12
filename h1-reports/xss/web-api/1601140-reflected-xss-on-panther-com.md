# Reflected XSS on panther.com Search Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1601140 | https://hackerone.com/reports/1601140
- **Submitted:** 2022-06-15
- **Reporter:** ibrahimatix0x01
- **Program:** Panther
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, HTML Injection, Input Validation Failure
- **CVEs:** None
- **Category:** web-api

## Summary
The search functionality on panther.com fails to sanitize user input, allowing attackers to inject arbitrary HTML tags and potentially execute JavaScript code. An attacker can craft malicious URLs with embedded HTML/JS payloads in the search parameter that execute in the victim's browser context.

## Attack scenario
1. Attacker crafts a malicious URL containing HTML/JavaScript payload in the search parameter: https://panther.com/search/[PAYLOAD]
2. Attacker shares the URL via phishing email, social engineering, or posts it on social media
3. Victim clicks the link while authenticated to panther.com
4. Browser receives unsanitized user input reflected in the HTML response without encoding
5. HTML tags and potentially JavaScript execute in victim's browser with their session context
6. Attacker can steal session cookies, perform actions on behalf of user, or redirect to phishing page

## Root cause
The search parameter value is reflected directly into the HTML response without proper output encoding or input validation. The application fails to sanitize or escape special HTML characters (<, >, quotes) before rendering user-supplied input in the response.

## Attacker mindset
An attacker identifies that search functionality is a common vector for reflected XSS since user input is often echoed back. They test with simple HTML tags to verify lack of sanitization, then escalate to JavaScript payloads. They recognize the value of session theft and craft URLs for phishing campaigns targeting authenticated users.

## Defensive takeaways
- Implement strict output encoding for all user-supplied data reflected in HTML context (use context-appropriate encoding: HTML entity encoding for HTML content)
- Apply input validation to reject or neutralize potentially dangerous characters in search parameters
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if injection occurs
- Use security-focused templating engines that auto-escape output by default
- Conduct security code review of all user input handling, particularly in search/filter functionality
- Implement automated security testing (SAST/DAST) to detect reflected XSS vulnerabilities
- Consider using a Web Application Firewall (WAF) as defense-in-depth, though not as primary control

## Variant hunting
Test other search/filter parameters across the application for similar XSS vulnerabilities
Check URL parameters used in redirects (runpanther.io → panther.com redirect chain)
Test error messages and 404 pages that may reflect user input
Examine API endpoints that may accept search queries and return unsanitized responses
Check autocomplete/suggestion features that echo user input
Test with different payload encodings (URL encoding, double encoding, mixed case, Unicode) to bypass filters

## MITRE ATT&CK
- T1598 - Phishing: Attackers send malicious URLs in phishing emails
- T1566 - Phishing: Phishing messages with malicious links
- T1592 - Gather Victim Identity Information: Through credential theft via XSS
- T1187 - Forced Authentication: Potential for credential harvesting
- T1539 - Steal Web Session Cookie: Session theft through XSS

## Notes
The report demonstrates successful HTML injection with h1 and font tags. The 'possible XSS' qualifier in the impact suggests JavaScript execution may be blocked by WAF, but HTML injection alone is dangerous. The redirect from runpanther.io to panther.com may indicate infrastructure changes that should be reviewed for security implications. Reporter demonstrates proof-of-concept but does not include JavaScript payload testing, possibly due to responsible disclosure practices or WAF detection avoidance.

## Full report
<details><summary>Expand</summary>

## Summary:
When visiting  runpanther.io I got redirected to panther.com and the application failed to sanitise user's input resulting into HTML injection and possible XSS.

## Steps To Reproduce:

{F1774502}
  1. Go to https://panther.com/search/Users%3Ch1%3EHello,%20I%20am%3C/h1%3E%3Cfont%20color=red%3E%20Ibrahimatix0x01%3C/font%3E
  1. You will notice that HTML codes in the search form are executed by the browser.
  

## Supporting Material/References:
{F1774497}

## Impact

The vulnerability allow a malicious user to inject html tags and could possibly execute Javascript (if WAF is successfully bypassed)which could lead to steal user's session

</details>

---
*Analysed by Claude on 2026-05-12*
