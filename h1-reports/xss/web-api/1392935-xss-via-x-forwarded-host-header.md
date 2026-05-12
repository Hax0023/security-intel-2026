# Reflected XSS via X-Forwarded-Host Header in Omise

## Metadata
- **Source:** HackerOne
- **Report:** 1392935 | https://hackerone.com/reports/1392935
- **Submitted:** 2021-11-06
- **Reporter:** oblivionlight
- **Program:** Omise
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Header Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The Omise website (omise.co) is vulnerable to reflected XSS through the X-Forwarded-Host HTTP header, which is read and reflected back into the response without proper sanitization. An attacker can craft a malicious URL with a specially crafted X-Forwarded-Host header containing JavaScript payload to execute arbitrary code in a victim's browser and steal sensitive information like cookies and session tokens.

## Attack scenario
1. Attacker identifies that the Omise website reflects the X-Forwarded-Host header value in HTTP responses without sanitization
2. Attacker crafts a malicious X-Forwarded-Host header containing JavaScript payload: X-Forwarded-Host: bing.com"><img src/onerror=prompt(document.cookie)>
3. Attacker tricks or socially engineers a victim into sending a request with this malicious header (via proxy, MitM, or if application accepts it directly)
4. The vulnerable server processes the request and reflects the unsanitized X-Forwarded-Host value back in the response HTML
5. Victim's browser parses the response and executes the injected JavaScript code
6. Malicious script accesses sensitive data (cookies, tokens, session data) or performs actions on behalf of the victim

## Root cause
The application directly reads the X-Forwarded-Host header from incoming HTTP requests and reflects it into the HTTP response without proper HTML entity encoding, input validation, or output sanitization. This is often seen when developers trust proxy headers without validation, assuming they come from trusted infrastructure.

## Attacker mindset
Identify commonly trusted but often unsanitized HTTP headers (X-Forwarded-Host, X-Forwarded-For, etc.). Assume developers may trust proxy headers and skip validation. Test reflection points where headers are output to responses. Leverage trust boundaries where infrastructure headers are reflected without sanitization.

## Defensive takeaways
- Never trust HTTP headers blindly; validate and sanitize all input including proxy headers regardless of source
- Apply output encoding appropriate to context (HTML entity encoding for HTML context, JavaScript escaping for JavaScript context)
- Implement Content Security Policy (CSP) headers to restrict script execution and mitigate XSS impact
- Use security-focused templating engines that auto-escape output by default
- Maintain an allowlist of valid X-Forwarded-Host values rather than reflecting arbitrary values
- Implement input validation to reject headers containing metacharacters and HTML/JavaScript syntax
- Use HTTPOnly and Secure flags on sensitive cookies to prevent JavaScript access
- Perform security testing on proxy-related headers and trust boundary violations

## Variant hunting
Test other proxy headers for reflection: X-Forwarded-For, X-Forwarded-Proto, X-Original-Host, X-Proxy-Authorization, CF-Connecting-IP, True-Client-IP. Check for reflected values in error messages, redirects, and response headers (Location, Set-Cookie). Test for DOM-based XSS if JavaScript processes these headers client-side. Look for stored variants if headers are logged or persisted.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
X-Forwarded-Host header vulnerability is common in cloud/reverse proxy deployments. Many developers assume proxy headers are sanitized by infrastructure. The payload injection point is at the HTTP header level, bypassing some browser protections. Cookie theft via XSS is particularly dangerous as it can lead to session hijacking. POC video provided but not included in this analysis.

## Full report
<details><summary>Expand</summary>

Summary:
The https://www.omise.co/ website is vulnerable to a cross-site scripting flaw if the server receives a crafted X-Forwarded-Host header.

Description:
The server reads data directly from the HTTP request and reflects it back in the HTTP response. Reflected XSS exploits occur when an attacker causes a victim to supply dangerous content to a vulnerable web application, which is then reflected back to the victim and executed by the web browser. The most common mechanism for delivering malicious content is to include it as a parameter in a URL that is posted publicly or e-mailed directly to the victim. URLs constructed in this manner constitute the core of many phishing schemes, whereby an attacker convinces a victim to visit a URL that refers to a vulnerable site. After the site reflects the attacker's content back to the victim, the content is executed by the victim's browser.


Steps To Reproduce:
Original Link - https://www.omise.co/

 1. Visit https://www.omise.co/ capture the request in Intercept 
 2. Send the request to Repeater add X-Forwarded-Host: bing.com"><img src/onerror=prompt(document.cookie)>  below Host: www.omise.co
 3. The JavaScript alert box displays some cookie information. 

Mitigation:
Ignore invalid browser headers. Filter metacharacters from user input.

POC:
Attached Video.

## Impact

This flaw allows attackers to pass rogue JavaScript to unsuspecting users. The user’s browser has no way to know the script should not be trusted, so it will execute the script and because the browser thinks the script came from a trusted source, aka your website, a malicious script can access any cookies, session tokens, or other sensitive information retained by the browser and used with your site. These scripts can even rewrite the content of the HTML page.

</details>

---
*Analysed by Claude on 2026-05-12*
