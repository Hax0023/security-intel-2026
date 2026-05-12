# Reflected XSS via Error Parameter on admin.acronis.com

## Metadata
- **Source:** HackerOne
- **Report:** 970878 | https://hackerone.com/reports/970878
- **Submitted:** 2020-08-30
- **Reporter:** samincube
- **Program:** Acronis (HackerOne)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the /admin/su/ endpoint where the 'Error' query parameter is inadequately escaped, allowing injection of arbitrary HTML and JavaScript. An attacker can craft a malicious URL that executes JavaScript in the victim's browser when the page loads. This vulnerability is particularly dangerous in an admin context where authenticated users with elevated privileges could be targeted.

## Attack scenario
1. Attacker crafts a malicious URL with XSS payload in the Error parameter: https://admin.acronis.com/admin/su/?Error=%3cscript%3ealert(document.domain)%3c%2fscript%3e
2. Attacker sends the link to an authorized admin user via phishing email, social engineering, or by posting on a forum/platform the admin frequents
3. Admin user clicks the link while authenticated to admin.acronis.com
4. Malicious JavaScript executes in the admin's browser within the context of the admin domain
5. Attacker's script steals session cookies, authentication tokens, or performs actions on behalf of the admin
6. Attacker gains unauthorized access to the admin panel or escalates privileges using stolen credentials

## Root cause
The application fails to properly HTML-encode user-supplied input from the 'Error' query parameter before reflecting it in the HTTP response. The special characters < and > are not converted to their HTML entity equivalents (&lt; and &gt;), allowing script tags to be parsed and executed by the browser.

## Attacker mindset
An attacker would recognize this as a high-impact vulnerability because it targets the admin interface with authenticated users. The attacker would likely craft phishing campaigns or watering hole attacks to deliver the malicious URL to administrators, aiming to steal session cookies or authentication credentials for lateral movement and privilege escalation within the organization.

## Defensive takeaways
- Implement output encoding for all user-controlled data reflected in HTML context using framework built-in functions (e.g., htmlspecialchars() in PHP, html.escape() in Python, or built-in templating engines)
- Use a security-focused templating engine that auto-escapes variables by default
- Apply input validation to reject suspicious patterns, but rely on output encoding as the primary defense
- Implement Content Security Policy (CSP) headers with strict-dynamic and script-src directives to prevent inline script execution
- Conduct regular security testing including both automated scanning and manual code review focusing on all user input entry points
- Implement HTTPOnly and Secure flags on session cookies to mitigate cookie theft via XSS
- Educate developers on secure coding practices and the principle of encoding data based on context (HTML, JavaScript, URL, CSS)

## Variant hunting
Search for similar patterns: other query parameters on the /admin/su/ endpoint that may lack encoding (e.g., Error, Message, Status, Redirect, Return, etc.); review other admin endpoints (/admin/*, /management/*) for reflected parameters; test HTTP headers like Referer, User-Agent, X-Forwarded-For for XSS; look for URL parameters commonly used for error handling or messaging across the entire admin application

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (delivery mechanism)
- T1056 - Observation (exfiltration of cookies/credentials)
- T1539 - Steal Web Session Cookie
- T1560 - Archive Collected Data (if credentials are exfiltrated)

## Notes
The vulnerability is particularly severe because it affects the admin panel (admin.acronis.com) rather than the main application, meaning the target users likely have elevated privileges and access to sensitive functionality. The attacker can leverage this to compromise high-value accounts. The writeup duplicates the Impact section, suggesting this may have been a template issue. No specific bounty amount was disclosed in the report.

## Full report
<details><summary>Expand</summary>

## Summary

Hello,

There is possible to inject arbitrary HTML constructions on the page /admin/su/. The problem is in the insufficient escaping of special characters (like <>) for the **Error** parameter. If this parameter contains a specially crafted vector, the application will return the page that will reflect this vector directly into the HTML response without proper encoding.

This XSS vector will work in most modern browsers.

## Steps To Reproduce

1. Open the next URL in the browser: https://admin.acronis.com/admin/su/?Error=%3cscript%3ealert(document.domain)%3c%2fscript%3e

{F969715}

The XSS will be executed automatically when the page will be loaded.

## Impact

A cross-site scripting attack against the application's clients can be used to obtain user authentication information (like cookies), phishing or malware spreading. In this case, an authorized user can be the primary target of this attack, so cookie and credentials stealing are possible ways to exploit this vulnerability.

## Recommendations

It's recommended to provide the processing of web application user input by replacing potentially insecure characters that could be used to format HTML pages to their equivalents that are not HTML format characters. This should be done for any data obtained from external sources and displayed in a browser (including HTTP headers, like Referer).

## Impact

A cross-site scripting attack against the application's clients can be used to obtain user authentication information (like cookies), phishing or malware spreading. In this case, an authorized user can be the primary target of this attack, so cookie and credentials stealing are possible ways to exploit this vulnerability.

</details>

---
*Analysed by Claude on 2026-05-12*
