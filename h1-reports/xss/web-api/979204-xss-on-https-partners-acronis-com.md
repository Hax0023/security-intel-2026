# DOM XSS on Acronis Partners Login Page via Unicode Escape Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 979204 | https://hackerone.com/reports/979204
- **Submitted:** 2020-09-11
- **Reporter:** yash_
- **Program:** Acronis
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** DOM-based XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists on the Acronis partners login page where the '-back' URL parameter is HTML encoded but then inserted into the DOM as a JavaScript string, allowing attackers to bypass encoding via Unicode escape sequences. An attacker can craft a malicious URL using Unicode escapes to inject arbitrary JavaScript code that executes in the victim's browser, potentially stealing login credentials.

## Attack scenario
1. Attacker identifies the '-back' parameter on the login page is reflected in JavaScript code as a string variable
2. Attacker discovers that HTML entities are applied but the resulting value is still used unsafely in JavaScript context
3. Attacker crafts a payload using JavaScript Unicode escapes (\u0022 for quotes, \u003e for >, \u003c for <) to bypass HTML encoding filters
4. Attacker sends phishing email with malicious URL to target users containing the Unicode-escaped XSS payload
5. Victim clicks the link while logged out, triggering the malicious JavaScript on the login page
6. Attacker harvests credentials via credential stealer or redirects user to fake login form

## Root cause
The application HTML-encodes the '-back' parameter but fails to properly escape it for the JavaScript context where it's used. The developers applied context-inappropriate encoding (HTML encoding for a JavaScript string context), and failed to account for Unicode escape sequences which bypass HTML entity encoding.

## Attacker mindset
Attackers targeting this vulnerability would focus on social engineering to deliver the malicious link to users, particularly those not yet authenticated. The login page context makes this especially valuable for credential harvesting. Unicode escaping is a known bypass technique that would be in an attacker's toolkit for evading basic XSS filters.

## Defensive takeaways
- Apply context-appropriate output encoding: use JavaScript escaping for values inserted into JavaScript code, not HTML encoding
- Implement Content Security Policy (CSP) to prevent inline script execution and restrict script sources
- Use templating engines that enforce proper escaping by default rather than manual encoding
- Validate that the '-back' parameter conforms to expected URL patterns (avoid allowing arbitrary strings)
- Perform security testing that specifically checks for Unicode escape bypass techniques
- Use a security code review process that verifies encoding is appropriate for the context where output appears
- Implement input validation to reject parameters containing suspicious patterns like Unicode escapes

## Variant hunting
Check other URL parameters for similar DOM-based XSS patterns with insufficient context-specific encoding
Test all pages that reflect user input in JavaScript string contexts for similar vulnerabilities
Search for other instances where HTML encoding is used instead of JavaScript escaping
Test for other Unicode bypass techniques (e.g., \x escapes, HTML numeric entities in JavaScript contexts)
Check if the same pattern exists in other Acronis properties or login pages
Review redirect parameters and back-to parameters across the application

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1056

## Notes
This is a classic example of context confusion in security controls. While HTML encoding is a valid technique, it must match the context where data is used. The login page context makes this particularly dangerous as it directly compromises authentication. The Unicode escape technique used here is a well-known bypass that sophisticated attackers employ. The vulnerability demonstrates the importance of framework-level protections like CSP rather than relying solely on manual encoding.

## Full report
<details><summary>Expand</summary>

Hello,

I found DOM XSS on login page of https://partners.acronis.com/
Open this URL https://partners.acronis.com/en-us/profile/login.html?-back=test123"> and search for `var back =`. Here input is HTML encoded but from that reflected value, element is created and appended to the form. 
{F983552}
We can use JavaScript's unicode escaping to bypass this..
  
  

## Steps To Reproduce
  1. For this payload `"><img src=x onerror=alert(1)><x y="` we have to replace `"` with `\u0022`, `>` with `\u003e` and `<` with `\u003c`.
So the payload will be `\u0022\u003e\u003cimg src=x onerror=alert(1)\u003e\u003cx y=\u0022`
  1. Open this URL   
   ```
https://partners.acronis.com/en-us/profile/login.html?-back=\u0022\u003e\u003cimg+src=x+onerror=alert(1)\u003e\u003cx+y=\u0022
    ```
  1. And you'll see alert dialog.  
{F983553}

## Impact

Attacker can execute JavaScript code on users who open the link. This XSS is in the login page so it can be used to get someone's credentials..

</details>

---
*Analysed by Claude on 2026-05-12*
