# Reflected XSS in Starbucks Japan Store Locator

## Metadata
- **Source:** HackerOne
- **Report:** 496375 | https://hackerone.com/reports/496375
- **Submitted:** 2019-02-15
- **Reporter:** wa1m3im
- **Program:** Starbucks
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS)
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the store locator search functionality at starbucks.co.jp where user-supplied input via the 'free_word' parameter is reflected directly into the page without proper sanitization or encoding. An attacker can craft malicious URLs containing JavaScript payloads that execute in the context of a victim's browser when visited.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'free_word' parameter
2. Attacker distributes the URL via phishing email, social media, or other social engineering techniques
3. Victim clicks the malicious link believing it leads to a legitimate Starbucks store search
4. The URL is processed by the store search application without proper input sanitization
5. The JavaScript payload is reflected in the HTML response and executed in the victim's browser context
6. Attacker can steal session cookies, redirect to phishing pages, or perform actions on behalf of the victim

## Root cause
The application fails to properly sanitize or HTML-encode user input from the 'free_word' query parameter before reflecting it back into the HTTP response. The input is inserted directly into the HTML/JavaScript context without validation or encoding mechanisms.

## Attacker mindset
An attacker would recognize that search parameters are commonly vulnerable to reflection attacks when developers assume user input is safe. By testing common XSS payloads in the search field, the attacker discovered the lack of output encoding, enabling arbitrary JavaScript execution. This could be leveraged for credential theft, malware distribution, or brand impersonation attacks.

## Defensive takeaways
- Implement strict input validation on all user-supplied parameters
- Apply context-appropriate output encoding (HTML entity encoding for HTML context, JavaScript encoding for JS context)
- Use a robust HTML templating engine that enforces automatic escaping by default
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Deploy Web Application Firewall (WAF) rules to detect and block common XSS payloads
- Conduct regular security code reviews focusing on input/output handling
- Use security testing tools to identify reflected XSS vulnerabilities in the SDLC

## Variant hunting
Test other search/filter parameters on the Starbucks site for similar reflection patterns
Check other Starbucks regional domains (starbucks.com, starbucks.co.uk, etc.) for the same vulnerability
Investigate similar e-commerce search functionalities that may have identical coding patterns
Test for DOM-based XSS in client-side JavaScript that processes the free_word parameter
Look for stored XSS if search terms are saved in user profiles or shared between users

## MITRE ATT&CK
- T1190
- T1566

## Notes
The vulnerability report is relatively minimal in detail but clearly demonstrates a working proof-of-concept. The payload uses basic HTML/script tag injection to break out of the existing HTML context. This is a straightforward reflected XSS that would likely be high-priority for remediation due to Starbucks' large user base and the simplicity of exploitation.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Please indicate NA, if not applicable. Remember, the more detail you provide, the easier it is for us to verify and then potentially issue a bounty, so be sure to take your time filling out the report!

**Summary:** 
I found a Refrect XSS in store locator pages.


**Description:**
This vulnerability would allow a user to insert javascript payloads which can be reflected in a browser.

## Steps To Reproduce:

1. Go to https://www.starbucks.co.jp/store/search/?free_word=%22%3E%3Cscript%3Ealert()%3C/script%3E%3E



## Reproduction environment
Firefox 65.0

## Impact

It is possible to run arbitrary javascript.


Thank you.

</details>

---
*Analysed by Claude on 2026-05-12*
