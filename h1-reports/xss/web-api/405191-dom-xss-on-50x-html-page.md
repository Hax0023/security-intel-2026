# DOM XSS on 50x.html page via location.search

## Metadata
- **Source:** HackerOne
- **Report:** 405191 | https://hackerone.com/reports/405191
- **Submitted:** 2018-09-04
- **Reporter:** cujanovic
- **Program:** DuckDuckGo
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Improper Input Validation, Unsafe DOM Manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists on DuckDuckGo's 50x.html error page where user-controlled input from the location.search parameter is directly written to the DOM via innerHTML without sanitization. An attacker can craft a malicious URL containing JavaScript payloads that execute in the context of the victim's browser session.

## Attack scenario
1. Attacker identifies that the 50x.html error page accepts query parameters via location.search
2. Attacker crafts a malicious URL containing HTML/JavaScript payload: https://duckduckgo.com/50x.html?e=&atb=test"%/><img src=x onerror=alert(document.domain);>
3. Attacker distributes the URL via phishing email, social engineering, or malicious website
4. Victim clicks the link while authenticated to DuckDuckGo
5. The payload is reflected into the DOM via innerHTML assignment in l110.js
6. JavaScript code executes in victim's browser with access to session cookies and sensitive data

## Root cause
The vulnerable code in l110.js at line 26 uses innerHTML to insert user-controlled data from location.search without proper HTML encoding or sanitization. The regex-based manipulation (b7.replace(aB, "<$1></$2>")) is insufficient to prevent XSS attacks as it only processes existing tags rather than sanitizing untrusted input.

## Attacker mindset
An attacker would view this as a critical vulnerability on a high-traffic domain enabling session hijacking, credential theft, malware distribution, or defacement. The error page is particularly attractive as users may be in a vulnerable state when accessing error pages.

## Defensive takeaways
- Never use innerHTML with untrusted input; use textContent for plain text or sanitize with a library like DOMPurify
- Implement Content Security Policy (CSP) headers with strict directives to prevent inline script execution
- Apply HTML entity encoding to all user-controlled data before DOM insertion
- Use security linters and static analysis tools to detect innerHTML/XSS patterns during code review
- Implement HTTPOnly and Secure flags on session cookies to limit XSS impact
- Add automated security testing for error pages which may receive less scrutiny
- Use DOM APIs like createElement and setAttribute instead of innerHTML when possible

## Variant hunting
Check other error pages (4xx.html, 500.html) for similar innerHTML patterns
Search for other instances of innerHTML usage with location-derived variables throughout the codebase
Test query parameters: e, atb, and any other accepted parameters for XSS
Examine l110.js for other potential sinks (eval, setTimeout, document.write)
Test POST-based error pages and alternate error handling endpoints
Check for Stored XSS if error messages are cached or logged

## MITRE ATT&CK
- T1190
- T1566.002
- T1566.001
- T1204.001

## Notes
The vulnerability affects an error page (50x.html) which may have lower security review priority but high impact due to user accessibility and trust in error handling pages. The use of minified JavaScript (l110.js) may have contributed to the oversight during security review.

## Full report
<details><summary>Expand</summary>

Hello,

The is a DOM XSS vulnerability on https://duckduckgo.com/50x.html, it seems like the sink is DIV.innerHTML and the source is location.search.
The PoC url is: https://duckduckgo.com/50x.html?e=&atb=test%22/%3E%3Cimg%20src=x%20onerror=alert(document.domain);%3E

The code that is causing this XSS is located in:
https://duckduckgo.com/lib/l110.js
Line 26, Column 60903

Below is the part of the vulnerable code:
`b5.createElement("div"));
cg = (m.exec(b7) || ["", ""])[1].toLowerCase();
b4 = R[cg] || R._default;
ce.innerHTML =  b4[1]  + b7.replace(aB, "<$1></$2>") + b4[2];
cb = b4[0];
while (cb--) {
	ce=ce.lastChild
}
if(!bI.support.leadingWhitespace&&b2.test(b7))`

Screenshot:
{F342240}

## Impact

The attacker can execute JS code.

</details>

---
*Analysed by Claude on 2026-05-12*
