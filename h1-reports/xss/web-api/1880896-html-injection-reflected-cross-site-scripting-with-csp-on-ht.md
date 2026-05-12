# HTML Injection / Reflected XSS in accounts.firefox.com flowId Parameter with CSP Bypass Consideration

## Metadata
- **Source:** HackerOne
- **Report:** 1880896 | https://hackerone.com/reports/1880896
- **Submitted:** 2023-02-21
- **Reporter:** celesian
- **Program:** Mozilla Firefox
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), HTML Injection, Open Redirect, UI Redressing / Clickjacking
- **CVEs:** None
- **Category:** web-api

## Summary
The flowId parameter on accounts.firefox.com/settings is reflected into the HTML response without proper escaping, allowing attackers to inject arbitrary HTML content. While the CSP prevents script execution, attackers can still perform UI redressing attacks, open redirects, and potentially exfiltrate data through the connect-src directive to localhost:4318 (OpenTelemetry Collector).

## Attack scenario
1. Attacker crafts a malicious URL with HTML injection payload in the flowId parameter (e.g., meta refresh tag or fake download button)
2. Attacker distributes the URL via phishing email or social engineering to Firefox account users
3. Victim clicks the link and is redirected to the legitimate accounts.firefox.com domain, bypassing browser trust indicators
4. Malicious HTML is rendered on the page without JavaScript execution due to CSP protection
5. For open redirect attack: victim is automatically redirected to attacker's domain via meta refresh; for UI redressing: victim sees fake warning messages and downloads malware
6. Optional: attacker leverages connect-src localhost:4318 to make requests to OpenTelemetry Collector and potentially exfiltrate telemetry data

## Root cause
Insufficient output encoding of the flowId parameter before rendering it into the HTML response. The application fails to HTML-encode user-controlled input, allowing raw HTML tags to be injected and interpreted by the browser.

## Attacker mindset
An attacker recognizes that while CSP prevents direct JavaScript execution, HTML injection still enables dangerous attacks that rely on user interaction (redirect attacks, social engineering, UI spoofing). The discovery of the localhost:4318 endpoint in connect-src suggests potential data exfiltration opportunities against Firefox/Mozilla employees or users.

## Defensive takeaways
- Implement robust output encoding: HTML-encode all user-controlled input before rendering in HTML context using context-appropriate encoding functions
- Apply input validation: whitelist expected flowId format and reject unexpected characters
- Strengthen CSP: remove unnecessary connect-src to localhost:4318 or restrict it only to trusted internal services, implement stricter directives
- Use security headers: implement X-Frame-Options to prevent clickjacking, X-Content-Type-Options: nosniff to prevent MIME type sniffing
- Server-side validation: validate all parameters against expected values before rendering
- Security testing: include HTML injection and XSS testing in regular security assessments, even when CSP is in place
- Monitor CSP violations: log and alert on CSP violations to detect attack attempts

## Variant hunting
Test other parameters (deviceId, broker, context, service, uniqueUserId) for similar HTML injection vulnerabilities
Check if flowBeginTime parameter is similarly vulnerable
Test for CSS injection through style attribute injection if HTML tags are partially filtered
Examine error pages and redirects for similar unescaped parameter reflection
Test POST parameters if available for the same endpoint
Check subdomains (api.accounts.firefox.com, profile.accounts.firefox.com) for parameter reflection
Test for DOM-based XSS where these parameters might be processed client-side
Investigate if CSP violations can be leveraged to deliver payloads to localhost:4318

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1557
- T1187
- T1200

## Notes
The researcher responsibly disclosed that while JavaScript execution is blocked by CSP, the HTML injection vulnerability remains exploitable for script-less attacks. The mention of OpenTelemetry Collector (localhost:4318) in the connect-src directive represents an interesting attack surface that could compromise Mozilla employees. The vulnerability demonstrates that CSP is a defense-in-depth measure and does not eliminate the need for proper input encoding. The two PoCs demonstrate different attack vectors: open redirect via meta refresh and UI redressing via fake warning messages.

## Full report
<details><summary>Expand</summary>

## Summary:
Good morning,

There is a vulnerability on accounts.firefox.com, where the flowId parameter is reflected into the server response without being escaped for HTML. This causes a Cross-Site Scripting attack, which may allow attackers to take over accounts. 
To do that, one would need to bypass the Content-Security-Policy on Firefox's website, which looks like this:
```http
Content-Security-Policy: connect-src 'self' https://api.accounts.firefox.com https://graphql.accounts.firefox.com https://oauth.accounts.firefox.com https://profile.accounts.firefox.com wss://channelserver.services.mozilla.com https://channelserver.services.mozilla.com https://*.sentry.io http://localhost:4318;default-src 'self';form-action 'self' https://accounts.google.com https://appleid.apple.com;font-src 'self' https://accounts-static.cdn.mozilla.net;frame-src 'none';img-src 'self' blob: data: https://secure.gravatar.com https://firefoxusercontent.com https://profile.accounts.firefox.com https://accounts-static.cdn.mozilla.net;media-src blob:;object-src 'none';report-uri /_/csp-violation;script-src 'self' https://accounts-static.cdn.mozilla.net;style-src 'self' https://accounts-static.cdn.mozilla.net;base-uri 'self';frame-ancestors 'self';script-src-attr 'none';upgrade-insecure-requests
```
Bypassing the Content-Security-Policy was not done yet, and I am not sure if its even doable. Therefore I am reporting the vulnerability as is because even without Javascript execution there are some attacks that are still possible script-less. One theoretical attack that could be possible is using the connect-src directive to make requests to the http://localhost:4318 URL and then possibly leak traces or other sensitive data from OpenTelemetry Collector (making Mozilla employees possibly a target for this attack).

## PoCs
1. Open Redirect
https://accounts.firefox.com/settings?deviceId=cc10a15a5ac94bdf8a9a0bc5b2912520&flowBeginTime=1676972087857&flowId=%22%3E%3Cmeta%20http-equiv=%22refresh%22%20content=%221;%20http://example.com%22%3E&broker=web&context=web&isSampledUser=false&service=none&uniqueUserId=dbf23f86-d3d1-4576-92bc-ebaa4fd14795

2. UI Redressing
https://accounts.firefox.com/settings?deviceId=cc10a15a5ac94bdf8a9a0bc5b2912520&flowBeginTime=1676972087857&flowId=e587d1d6ceb%22%3E%3Ch1%3EYour+machine+needs+to+be+analyzed.+Please+download+and+run+this+file+to+continue%3a+%3Ca+href%3d%22http%3a//evil.tld/a.exe%22%3EClick%20here%20to%20Download%3C/a%3E%3C/h1%3E%3C!--&broker=web&context=web&isSampledUser=false&service=none&uniqueUserId=dbf23f86-d3d1-4576-92bc-ebaa4fd14795

## Impact

An attacker can inject HTML on the page and potentially run attacks involving user interaction, with achieving arbitrary javascript code execution not being possible due to the Content Security Policy installed on the server.

</details>

---
*Analysed by Claude on 2026-05-12*
