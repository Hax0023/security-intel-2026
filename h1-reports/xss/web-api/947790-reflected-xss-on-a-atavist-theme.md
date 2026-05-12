# Reflected XSS in Atavist Theme Search Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 947790 | https://hackerone.com/reports/947790
- **Submitted:** 2020-07-30
- **Reporter:** bugra
- **Program:** Atavist
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Atavist theme search functionality where user-supplied input in the 'search' parameter is not properly sanitized or encoded before being reflected in the response. The vulnerability affects multiple websites using this Atavist theme, including magazine.atavist.com and docs.atavist.com, allowing attackers to execute arbitrary JavaScript in users' browsers.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript code in the search parameter (e.g., ?search=<script>alert(document.domain)</script>)
2. Attacker distributes the malicious link via phishing email, social media, or other vectors to target users
3. Victim clicks the link and is directed to a legitimate Atavist-powered website
4. The search parameter is reflected in the page HTML without proper encoding or sanitization
5. The victim's browser interprets and executes the embedded JavaScript code
6. Attacker gains ability to steal cookies, session tokens, redirect users, perform actions on behalf of the user, or capture sensitive information

## Root cause
The search parameter value is directly reflected into the HTML response without proper output encoding, HTML entity encoding, or input validation. The application fails to implement contextual output encoding where user input is inserted into JavaScript/HTML context.

## Attacker mindset
The attacker discovered this vulnerability through basic parameter testing and recognized its widespread impact across multiple Atavist-powered websites. They demonstrated responsible disclosure by reporting to HackerOne, indicating awareness of bug bounty programs while emphasizing the large scope of affected sites.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied data, especially search parameters
- Apply contextual output encoding based on where data is being used (HTML encoding, JavaScript encoding, URL encoding, etc.)
- Use security libraries and frameworks that provide built-in XSS protection mechanisms
- Deploy Content Security Policy (CSP) headers to restrict script execution and mitigate XSS impact
- Implement HTTP-only and Secure flags on cookies to prevent JavaScript access to session tokens
- Conduct security code reviews and automated SAST scanning to identify reflection vulnerabilities
- Test all user input parameters systematically for XSS vulnerabilities during security testing
- Keep framework and dependencies updated with security patches
- Use templating engines that auto-escape output by default

## Variant hunting
Test other search/input parameters across Atavist sites for similar reflection vulnerabilities
Check filter, category, tag, or sort parameters for XSS
Investigate whether DOM-based XSS variants exist in JavaScript-driven search implementations
Test for stored XSS if search queries are persisted (e.g., user profiles, favorites, history)
Examine other Atavist themes and plugins for identical vulnerable patterns
Check for bypass techniques using encoding variations (double encoding, Unicode, etc.)
Test for Stored XSS through user-generated content features if available

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001

## Notes
This is a classic reflected XSS with notably high scope due to the shared Atavist theme affecting multiple independent websites. The reporter responsibly identified this as a template-level vulnerability rather than isolated to a single site. The simplicity of the exploitation (basic script injection) and ease of discovery suggests this may have existed undetected for some time. The vulnerability demonstrates the cascading impact of insecure third-party themes on multiple organizations' security posture.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi team,
I found Reflected XSS at a Atavist theme and there are a lot of affected websites.
I don't know the theme's name but it's in use at https://magazine.atavist.com/
Just write `<script>alert(document.domain)</script>` to  search field.

https://magazine.atavist.com/search?search=%3Cscript%3Ealert(document.domain)%3C/script%3E
https://docs.atavist.com/search?search=%3Cscript%3Ealert%28document.domain%29%3C%2Fscript%3E

Also there are more affected websites like http://www.377union.com/search?search=%3Cscript%3Ealert%28document.domain%29%3C%2Fscript%3E , http://www.lifeaftermaria.org/search?search=%3Cscript%3Ealert%28document.domain%29%3C%2Fscript%3E etc.

So, I think the scope of this vulnerability is very large.

## Impact

Reflected XSS

Thanks,
Bugra

</details>

---
*Analysed by Claude on 2026-05-12*
