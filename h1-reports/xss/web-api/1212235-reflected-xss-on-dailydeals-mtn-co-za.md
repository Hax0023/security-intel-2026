# Reflected XSS on dailydeals.mtn.co.za via cpID Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1212235 | https://hackerone.com/reports/1212235
- **Submitted:** 2021-05-28
- **Reporter:** musab_alharany
- **Program:** MTN
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the dailydeals.mtn.co.za application on the index.cfm page via the cpID POST parameter. An attacker can inject arbitrary JavaScript code that executes in the victim's browser, enabling session hijacking and account compromise.

## Attack scenario
1. Attacker identifies that the cpID parameter in POST requests to index.cfm?GO=DEALS is not properly sanitized
2. Attacker crafts a malicious payload: category_id=7&cpID=1"> <img src=a onerror=alert("XSS")><!--
3. Attacker tricks a victim into visiting a specially crafted link or submitting a form with the malicious payload
4. When the victim's request is processed, the payload is reflected in the HTML response without encoding
5. The browser parses the reflected payload and executes the JavaScript code in the victim's context
6. Attacker can harvest session cookies, perform actions as the victim, or redirect to phishing/malware sites

## Root cause
The application fails to properly HTML-encode user-supplied input from the cpID parameter before reflecting it in the HTTP response. ColdFusion's improper use of cfml tags or missing output encoding functions like htmlEditFormat() or encodeForHTML() allows the HTML/JavaScript to be interpreted as code rather than safe text.

## Attacker mindset
An opportunistic attacker performing reconnaissance on MTN's e-commerce platform discovered this parameter-based vulnerability through standard parameter fuzzing. The ability to execute arbitrary JavaScript with minimal user interaction makes this an attractive vector for credential theft and malware distribution campaigns.

## Defensive takeaways
- Implement strict input validation: whitelist only expected values for cpID parameter (numeric IDs)
- Apply contextual output encoding: use htmlEditFormat() in ColdFusion or equivalent encoding functions for all user-supplied data reflected in HTML context
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Use HTTPOnly and Secure flags on session cookies to mitigate cookie theft
- Employ web application firewalls (WAF) with XSS detection signatures
- Conduct security code review of all form-handling and parameter reflection code
- Implement automated SAST scanning in the development pipeline to catch reflection vulnerabilities

## Variant hunting
Test other parameters in index.cfm for similar reflection issues (category_id, GO parameter, etc.)
Check GET request variants of the same endpoint for reflected XSS
Probe other ColdFusion pages on dailydeals.mtn.co.za domain for improper output encoding
Test for DOM-based XSS vulnerabilities in client-side JavaScript handling of these parameters
Investigate stored XSS if cpID values are persisted in database and displayed elsewhere
Check for blind XSS via time-delayed callbacks or out-of-band data exfiltration

## MITRE ATT&CK
- T1190
- T1566.002
- T1566.003
- T1598.003
- T1187

## Notes
The vulnerability report demonstrates a POST-based reflected XSS, which is less common than GET-based variants but equally dangerous. The use of image onerror event handler is a straightforward bypass technique. The reporter's reproduction steps involve intercepting traffic and using Burp Suite, indicating the need for POST method interaction. ColdFusion applications are particularly vulnerable to XSS if developers do not explicitly encode output, as the language doesn't encode by default.

## Full report
<details><summary>Expand</summary>

Hello MTN Team.
i found Reflected XSS on``` https://dailydeals.mtn.co.za/index.cfm?GO=DEALS```  vi ```cpID``` parameter with POST method 

## Steps To Reproduce:
1. Intercept the https://dailydeals.mtn.co.za/index.cfm?GO=DEALS 
2. Change Method to POST
3. Add empty line after last header
4. Write this code 
>category_id=7&cpID=1%22%3e%20%3cimg%20src%3da%20onerror%3dalert("XSS")%3e<!--

{F1319085}
5. Sent the Request.
6. Right Click on response area, then Click on ```Show response in browser```
7. copy the link, and put it on browser use BurpSuite as proxy 
8. press the Enter key, then you will see the ```XSS``` on your browser
{F1319086}

## Impact

attacker can convinces a victim to visit a URL then he can:
1. steal users cookies
2. redirect the user to malicious website

</details>

---
*Analysed by Claude on 2026-05-12*
