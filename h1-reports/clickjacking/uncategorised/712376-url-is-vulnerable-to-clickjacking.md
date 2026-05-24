# Missing CSP Headers - Clickjacking Vulnerability

## Metadata
- **Source:** HackerOne
- **Report:** 712376 | https://hackerone.com/reports/712376
- **Submitted:** 2019-10-11
- **Reporter:** whitehacker18
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, Missing Security Headers, Insufficient CSP Configuration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The target URL is vulnerable to clickjacking attacks due to missing Content Security Policy (CSP) headers and X-Frame-Options directives. An attacker can embed the vulnerable page within a malicious iframe to trick users into performing unintended actions. This vulnerability could lead to loss of user trust and reputation damage.

## Attack scenario
1. Attacker creates a malicious webpage and embeds the target site in a transparent iframe positioned over deceiving content
2. User visits the attacker's page which displays fake content (e.g., 'Click here to win a prize')
3. User's click actually targets the hidden legitimate site's interactive element (button, link, form)
4. User unknowingly performs sensitive actions on the legitimate site (transfers funds, changes settings, authenticates)
5. Attack succeeds because browser allows framing due to missing frame-ancestors CSP directive or X-Frame-Options header
6. Attacker achieves goals such as account takeover, unauthorized transactions, or social engineering

## Root cause
The web application fails to implement protective HTTP response headers (CSP frame-ancestors directive or X-Frame-Options) to prevent embedding the page in iframes from unauthorized origins. This allows any external website to frame the content without restriction.

## Attacker mindset
An attacker recognizes that unprotected framing capabilities enable clickjacking attacks. They leverage the missing security headers to trick legitimate users into performing unwanted actions on the target site without their knowledge, maintaining plausible deniability while exploiting user interface manipulations.

## Defensive takeaways
- Implement CSP frame-ancestors directive (e.g., 'frame-ancestors self;') in HTTP response headers
- Set X-Frame-Options header to DENY or SAMEORIGIN as legacy protection mechanism
- Regularly audit web applications for missing security headers using automated tools
- Use security header scanning tools like Mozilla Observatory or OWASP ZAP during development and deployment
- Implement defense-in-depth with JavaScript frame-busting code as additional layer
- Document clickjacking defense requirements in security standards and include in CI/CD validation
- Test framing scenarios in security testing procedures

## Variant hunting
Search for other endpoints on the same domain and subdomains lacking CSP headers; test all user-facing pages, authentication flows, and sensitive operations for clickjacking vulnerability; check for partial CSP implementations that may not include frame-ancestors directive; test for CSP bypass techniques through policy manipulation.

## MITRE ATT&CK
- T1190
- T1185
- T1598

## Notes
Reporter expressed uncertainty about scope and requested potential closure as informative. The vulnerability is valid but commonplace in scope determination. Report includes references to OWASP standards and similar prior reports. No custom POC code details provided in the writeup text, though attachments referenced. Fix is straightforward: add appropriate security headers to HTTP responses.

## Full report
<details><summary>Expand</summary>

##i'm not sure if this vulnerability is in scope or not , kindly if you don't accept this report please close it as informative or allow me to self close it thanks in advance

##Summary:
URLs missing CSP headers they are vulnerable to clickjacking.

##Steps To Reproduce:
run the below code that i had attached
{F605393}

##Supporting Material/References:
https://hackerone.com/reports/337219

here is a refrence from owasp for more details : https://www.owasp.org/index.php/Clickjacking
you can find down
## Defending against Clickjacking
There are two main ways to prevent clickjacking:
Sending the proper Content Security Policy (CSP) frame-ancestors directive response headers that instruct the browser to not allow framing from other domains. (This replaces the older X-Frame-Options HTTP headers.)

##POC:
also this screenshot shows that csp header isn't implemented ( you can find the same when you visit
https://observatory.mozilla.org/analyze/etherscamdb.info
{F605394}

##Mitigation and fix:
implement csp header

also here is another link for more information about the fix :
https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Clickjacking_Defense_Cheat_Sheet.md

if you need any help please tell me i'd be happy to help out thanks in advance

## Impact

hackers embed the content your page within another page which may cause loss of reputation and trust as a result

</details>

---
*Analysed by Claude on 2026-05-24*
