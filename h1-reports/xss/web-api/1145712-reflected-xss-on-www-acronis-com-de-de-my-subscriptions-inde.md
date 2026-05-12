# Reflected XSS on www.acronis.com/de-de/my/subscriptions/index.html

## Metadata
- **Source:** HackerOne
- **Report:** 1145712 | https://hackerone.com/reports/1145712
- **Submitted:** 2021-04-02
- **Reporter:** cabelo
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS)
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the subscriptions page where the 'b' parameter is not properly sanitized before being rendered in the HTML response. An attacker can inject arbitrary HTML/JavaScript through a malicious URL, leading to arbitrary code execution in the victim's browser context.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the 'b' parameter with event handler (OnToggle) on a Details element
2. Attacker sends the crafted URL to a victim via phishing email, social engineering, or malicious website
3. Victim clicks the link while authenticated to Acronis account
4. Malicious payload is reflected in the response and parsed by the browser
5. Browser executes the injected JavaScript code (confirm dialog in this case, but could be credential theft)
6. Attacker gains ability to steal session cookies, perform actions on behalf of user, or redirect to phishing page

## Root cause
User input from the 'b' URL parameter is not properly validated, sanitized, or HTML-encoded before being embedded into the HTML response. The application fails to implement output encoding or Content Security Policy (CSP) headers to prevent script execution.

## Attacker mindset
The attacker identified an unauthenticated reflection point and used polyglot XSS encoding techniques to bypass basic filters (using tag closures like </Title/</Textarea/</Script/> and alternative event handlers like OnToggle on Details element). The attacker aimed to demonstrate arbitrary code execution capability with minimal payload complexity.

## Defensive takeaways
- Implement strict input validation on all URL parameters, rejecting or sanitizing special HTML characters
- Apply proper output encoding (HTML entity encoding) when reflecting user input into HTML context
- Implement a robust Content Security Policy (CSP) that disallows inline scripts and restricts script sources
- Use a security-focused templating engine with auto-escaping enabled
- Conduct regular security testing including XSS fuzzing across all user input vectors
- Implement HTTP Security Headers (X-XSS-Protection, X-Content-Type-Options)
- Use a Web Application Firewall (WAF) with XSS detection rules
- Perform code review focusing on all output rendering logic

## Variant hunting
Hunt for similar reflection points in: query parameters on other authenticated pages (/my/* endpoints), form parameters, API endpoints returning user-controlled data, error messages, search functionality, and redirect parameters. Test with alternative XSS vectors using different HTML5 elements and event handlers.

## MITRE ATT&CK
- T1190
- T1566.002
- T1566.001

## Notes
The payload uses sophisticated XSS bypass techniques including tag-based closing sequence (</Title/</Textarea/</Script/>) and event handler delegation (OnToggle on Details element with Details/Open attribute). This suggests the application may have basic XSS filters attempting to block common patterns. The 'u' parameter (likely user identifier) suggests this is within an authenticated context. The vulnerability requires user interaction (clicking malicious link) making it practical for targeted attacks.

## Full report
<details><summary>Expand</summary>

Hello Team,

I would like to report a Reflected XSS vulnerability on https://www.acronis.com/de-de/my/subscriptions/index.html

Vulnerable parameter: b
Payload: '"1<!--></Title/</Textarea/</Script/><Details/Open/OnToggle=(confirm)(1)>

POC:
```
 https://www.acronis.com/de-de/my/subscriptions/index.html?b='"1<!--></Title/</Textarea/</Script/><Details/Open/OnToggle=(confirm)(1)>&u=ine3
```
{F1252106}

## Impact

A XSS attack allows an attacker to execute arbitrary JavaScript in the context of the attacked website and the attacked user.

</details>

---
*Analysed by Claude on 2026-05-12*
