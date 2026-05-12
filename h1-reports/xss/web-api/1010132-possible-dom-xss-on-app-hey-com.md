# Possible DOM XSS on app.hey.com via Subject Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1010132 | https://hackerone.com/reports/1010132
- **Submitted:** 2020-10-16
- **Reporter:** enigmaticjohn
- **Program:** HackerOne - Hey (Basecamp)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Cross-Site Scripting (XSS) - DOM-based, HTML Injection, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in the email subject line search functionality on app.hey.com. While CSP prevents immediate script execution, malicious HTML tags can be injected into email subjects and rendered in search results, creating an attack vector if CSP protections are bypassed. The vulnerability stems from insufficient sanitization of the Subject parameter when displaying search results.

## Attack scenario
1. Attacker crafts a malicious email with HTML injection payload in the Subject field: TestPayload</a><a href="javascript:alert(1)">ClickHere</a>
2. Attacker sends the email to a victim user on the platform
3. When victim searches for emails containing 'TestPayload' in the search box, the unsafe subject is rendered in search results
4. The injected <a> tag with javascript: protocol is rendered in the DOM without proper escaping
5. Victim clicks the injected 'ClickHere' link, triggering the javascript: handler
6. If CSP can be bypassed (via whitelisted hosts or other weaknesses), arbitrary JavaScript executes in victim's browser context, enabling account takeover

## Root cause
Insufficient output encoding/sanitization of the email Subject parameter when rendering search results. The application fails to properly escape HTML special characters, allowing injection of malicious HTML elements. While CSP provides defense-in-depth, it should not be relied upon as the primary defense against XSS.

## Attacker mindset
A sophisticated attacker would recognize that CSP is in place but would investigate potential bypasses via whitelisted hosts (production.haystack-assets.com, stats.hey.com, braintree services, hcaptcha.com). They might chain this with other vulnerabilities or wait for CSP relaxation. The HTML injection alone could enable phishing or social engineering attacks.

## Defensive takeaways
- Implement proper output encoding for all user-controlled data rendered in HTML context, especially in search results
- Use context-aware encoding (HTML entity encoding) for Subject lines and other email metadata
- Apply defense-in-depth: never rely solely on CSP to prevent XSS
- Sanitize or validate email headers and Subject lines at input time to reject or strip dangerous characters
- Review CSP whitelisted hosts for potential bypass vectors and use nonce/hash-based policies instead of host whitelists where possible
- Implement automated security testing for XSS in search functionality and email rendering
- Use templating engines with auto-escaping enabled for rendering user data

## Variant hunting
Test other email metadata fields (From, To, CC, BCC) in search results for similar XSS/injection vulnerabilities
Search for event handlers in email body rendering: onmouseover, onerror, onclick, etc.
Test search functionality across other areas of the application for injection points
Investigate if CSP can be bypassed via whitelisted Braintree or hCaptcha hosts through upload/JSONP endpoints
Check if email subjects are also vulnerable in preview panes, threads, or notification contexts
Test for stored XSS persistence in archived/cached search results

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link

## Notes
The reporter correctly identified this as a CSP-mitigated but still concerning vulnerability. The practical impact is lower due to CSP protections, but the underlying input validation flaw is a security issue. The suggestion about whitelisted host bypass is worth deeper investigation. This is a good example of defense-in-depth importance - output encoding should be fixed regardless of CSP presence.

## Full report
<details><summary>Expand</summary>

#Summary:

Hello Team,
While testing it was observed that on https://app.hey.com/, on Search box there is a possibility of XSS. Although the payload is reflected in the DOM but the CSP blocks the execution of the script, the XSS can happen if the CSP is somehow bypassed. The Subject parameter is vulnerable.

Apart from XSS, the HTML injection attack is working pretty straight forward.

#Steps To Reproduce:
1. Go to https://app.hey.com
2. Login to your account.
3. Click on 'Write' Mail button.
4. Add the recipient as yourself.
5. In the Subject, add following payload
```
TestPayload&lt;/a&gt;&lt;a href="javascript:alert(1)"&gt;ClickHere&lt;/a&gt;
```
6. Send the mail.
7. Go to top left corner Search Box and type "**TestPayload**" 
8. You will see the mail you sent to yourself, and <a> tag will be there "ClickHere".
9. Click on it, you will see the CSP violation in the Console.
10. Below is the CSP of the page:

```
script-src 'self' https://production.haystack-assets.com stats.hey.com *.braintreegateway.com *.braintree-api.com hcaptcha.com *.hcaptcha.com; 
object-src 'none'; 
base-uri 'none'; 
form-action 'self'; 
frame-ancestors 'none'; 
report-uri https://sentry.io/api/1371426/security/?sentry_key=3a5ea420eecc45bd9e1d1c2424683f3a&sentry_environment=production&sentry_release=
```
As seen from the CSP, there might be a possibility of Host whitelists bypass.

## Impact

If attacker send such type of mail to a victim and if victim accidentally searches for the same mail then the Script will be executed leading to account takeover. This is possible only if CSP is bypassed.

</details>

---
*Analysed by Claude on 2026-05-12*
