# Reflected XSS on terra-6.indriverapp.com

## Metadata
- **Source:** HackerOne
- **Report:** 1969696 | https://hackerone.com/reports/1969696
- **Submitted:** 2023-05-02
- **Reporter:** maxdha
- **Program:** InDriver
- **Bounty:** Unknown (redacted in report)
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered on terra-6.indriverapp.com that allows attackers to execute arbitrary JavaScript in users' browsers. The vulnerability appears to be triggered through a crafted URL parameter that is insufficiently sanitized before being reflected in the response.

## Attack scenario
1. Attacker identifies a vulnerable parameter on terra-6.indriverapp.com that reflects user input without proper sanitization
2. Attacker crafts a malicious URL containing JavaScript payload (e.g., alert box) in the vulnerable parameter
3. Attacker sends the crafted URL to victims via phishing email, social engineering, or malicious website
4. Victim clicks the link or visits the attacker-controlled page that redirects to the malicious URL
5. Browser executes the malicious JavaScript in the context of terra-6.indriverapp.com domain
6. Attacker can steal session cookies, perform actions on behalf of the victim, or redirect to credential harvesting pages

## Root cause
User input from URL parameters is reflected directly into the HTML response without proper encoding or validation, allowing JavaScript execution through browser interpretation

## Attacker mindset
Opportunistic reconnaissance - discovering low-hanging fruit through manual testing of URL parameters; potential for credential theft or account takeover via session hijacking

## Defensive takeaways
- Implement robust input validation and whitelisting for all user-controlled parameters
- Apply context-appropriate output encoding (HTML entity encoding for HTML context, JavaScript escaping for JS context)
- Use a Content Security Policy (CSP) header to mitigate XSS impact
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Conduct security code review focusing on all data reflection points
- Use templating engines with auto-escaping enabled by default
- Perform regular penetration testing and security assessments on subdomain infrastructure

## Variant hunting
Search for similar reflection points: other subdomains (terra-*.indriverapp.com), different parameter names, alternative HTTP methods (POST), DOM-based XSS in JavaScript code, stored XSS if user input is persisted

## MITRE ATT&CK
- T1190
- T1566

## Notes
Report contains significant redactions making full analysis difficult. The specificity of 'terra-6' subdomain suggests potential infrastructure or testing environment. Severity should be elevated if impact includes sensitive user data or critical functionality. Similar XSS vulnerabilities across InDriver infrastructure should be investigated.

## Full report
<details><summary>Expand</summary>

I've found an XSS on terra-6.indriverapp.com


## Steps To Reproduce:

1. Go to  ██████

An alert window will popup.


## Supporting Material/References:
███████

## Impact

Executing javascript code on users browsers.

</details>

---
*Analysed by Claude on 2026-05-12*
