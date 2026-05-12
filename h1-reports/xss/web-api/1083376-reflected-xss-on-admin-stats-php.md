# Reflected XSS on /admin/stats.php in Revive Adserver 5.1.0

## Metadata
- **Source:** HackerOne
- **Report:** 1083376 | https://hackerone.com/reports/1083376
- **Submitted:** 2021-01-21
- **Reporter:** solov9ev
- **Program:** Revive Adserver
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** CVE-2021-22875
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the /admin/stats.php endpoint of Revive Adserver 5.1.0 where the 'setPerPage' parameter is not properly sanitized before being rendered in an HTML attribute. An attacker can inject malicious JavaScript that executes when a user interacts with the crafted payload using accesskey combinations.

## Attack scenario
1. Attacker identifies that the 'setPerPage' parameter in /admin/stats.php is reflected without proper encoding
2. Attacker crafts a malicious URL containing JavaScript payload in the setPerPage parameter, closing the HTML tag with a quote and injecting onclick and accesskey attributes
3. Attacker sends the malicious link to an authenticated admin user via email, social engineering, or other phishing methods
4. Admin user clicks the link and visits the page, which loads with the injected payload in an input element's accesskey attribute
5. Admin user presses the browser-specific accesskey combination (Alt+Shift+X in Firefox) to activate the hidden input field
6. The onclick event fires, executing the attacker's JavaScript code which can steal session cookies, perform unauthorized actions, or redirect to malicious sites

## Root cause
The 'setPerPage' query parameter is directly reflected into an HTML attribute value without proper HTML entity encoding or input validation. The application fails to sanitize user-controlled input before embedding it in HTML context, specifically within HTML attributes where quote characters can break out of the attribute context.

## Attacker mindset
An attacker seeks to compromise admin accounts by leveraging the trust relationship between the admin and the application. The use of accesskey demonstrates understanding of HTML features and browser-specific behavior to craft a less obvious exploitation vector. The attacker recognizes that admin panels often contain sensitive functionality and account takeover could lead to server-wide compromise.

## Defensive takeaways
- Implement strict output encoding for all user-controlled data reflected in HTML context, using context-appropriate encoding (HTML entity encoding for tag content, attribute encoding for attributes)
- Apply input validation to reject or sanitize unexpected characters in the 'setPerPage' parameter (should only contain numeric values)
- Use a templating engine with auto-escaping capabilities to prevent accidental XSS vulnerabilities
- Implement Content Security Policy (CSP) headers to prevent inline script execution even if XSS occurs
- Use security headers like X-XSS-Protection and X-Content-Type-Options to provide defense-in-depth
- Conduct regular code reviews focusing on user input handling in all parameters, query strings, and form inputs
- Implement automated security testing (SAST/DAST) in the CI/CD pipeline to catch XSS vulnerabilities early

## Variant hunting
Test all pagination and display-related parameters (setPerPage, listorder, orderdirection) for similar XSS vulnerabilities
Check other admin pages for identical vulnerable patterns in parameter handling
Test for stored XSS variants if user-controlled data is persisted in reports or settings
Investigate DOM-based XSS possibilities in JavaScript event handlers using these parameters
Check if other HTML attributes can be similarly broken out of (title, placeholder, data-* attributes)
Test for bypasses using HTML entity encoding, Unicode encoding, or other obfuscation techniques

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The vulnerability requires user interaction (pressing an accesskey combination) which makes it slightly less critical than typical reflected XSS. However, this can be reliably triggered through user education or combined with other attacks. The administrative context of the vulnerable endpoint significantly increases the impact potential. The report demonstrates good technical understanding by identifying the specific accesskey requirement and providing clear reproduction steps.

## Full report
<details><summary>Expand</summary>

I found a reflected XSS attack on `/admin/stats.php`.

Revive-Adserver version is `revive-adserver-5.1.0`.

- Go to `http://revive-adserver.loc/admin/stats.php?statsBreakdown=day&listorder=key&orderdirection=up&day=&setPerPage=15%27%20onclick=alert(document.domain)%20accesskey=X%20&entity=global&breakdown=history&period_preset=last_month&period_start=01+December+2020&period_end=31+December+2020`

- For the payload to be executed, the user needs to press the access key combination for the hidden input field (for Firefox, `Alt`+`Shift`+`X`, see [this](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/accesskey) for other browsers).

{F1166756}

## Impact

With this vulnerability, an attacker can for example steal users cookies or redirect users on malicious website.

</details>

---
*Analysed by Claude on 2026-05-12*
