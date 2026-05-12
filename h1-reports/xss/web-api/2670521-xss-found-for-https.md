# Reflected Cross-Site Scripting (XSS) in /web/guest/search POST Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 2670521 | https://hackerone.com/reports/2670521
- **Submitted:** 2024-08-20
- **Reporter:** thpless
- **Program:** Unknown - Redacted
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the POST /web/guest/search endpoint where the 'query' parameter is not properly sanitized or encoded before being reflected in the server response. An attacker can inject arbitrary JavaScript code through a crafted payload, which executes in the victim's browser when the response is rendered.

## Attack scenario
1. Attacker identifies the /web/guest/search endpoint accepts POST requests with a 'query' parameter
2. Attacker crafts a malicious JavaScript payload designed to break out of the current context: "'};alert('XSS');var x={y:'"
3. Attacker creates an HTML form that auto-submits to the vulnerable endpoint with the malicious payload
4. Attacker tricks or socially engineers a user into visiting the attacker-controlled HTML page
5. User's browser automatically submits the POST request to the vulnerable endpoint with the XSS payload
6. Server reflects the unsanitized payload in the response, causing JavaScript execution in the victim's browser context

## Root cause
The application fails to implement proper input validation and output encoding on the 'query' parameter in the /web/guest/search endpoint. User-supplied data is directly reflected in the HTTP response without sanitization, allowing arbitrary code injection.

## Attacker mindset
An attacker would recognize that search functionality often reflects user input for displaying results. By testing various payload encoding techniques and context breakout sequences, they identified that the application processes and reflects the query parameter without proper escaping, enabling script injection.

## Defensive takeaways
- Implement strict input validation using whitelist-based approaches for the query parameter
- Apply context-aware output encoding (HTML entity encoding for HTML context, JavaScript encoding for JS context, URL encoding for URLs)
- Deploy Content Security Policy (CSP) headers to restrict script execution sources and mitigate XSS impact
- Use established templating engines with automatic escaping enabled by default
- Implement HTTPOnly and Secure flags on cookies to prevent session hijacking
- Conduct regular security testing including manual XSS payload testing and automated SAST/DAST scanning
- Apply defense-in-depth: combine input validation, output encoding, and CSP for layered protection

## Variant hunting
Search for similar POST endpoints that accept user input (filtering, sorting, pagination parameters). Test other search-related endpoints for reflected XSS. Check for similar vulnerabilities in GET-based search functionality. Investigate if other form parameters in the same endpoint are also vulnerable. Test for stored XSS if search queries are persisted and displayed to other users.

## MITRE ATT&CK
- T1190
- T1566
- T1059

## Notes
The vulnerability uses a context-breaking payload that closes a string and JavaScript object literal to inject arbitrary code. The use of an auto-submitting form in the PoC bypasses browser XSS filters that may block reflected payloads in URLs. This is a classic reflected XSS suitable for phishing campaigns combined with social engineering. The redacted report details suggest this is from a private program with enterprise software.

## Full report
<details><summary>Expand</summary>

* Location: POST request to the endpoint `/web/guest/search`
* Parameter Affected: `query=`
* Proof of Concept:

```
<html>
<body>
<script>
	window.onload = function(){document.forms['XSS'].submit();}
</script>
	<form id='XSS' action='https://█████████/web/guest/search' method='post'>
		<input type='text' name='query' value="'};alert('XSS');var x={y:'">
	</form>
</body>
</html>
```

## Impact

An attacker can craft a malicious payload and trick a user into sending a POST request to the vulnerable endpoint. The unvalidated and unsanitized data is then reflected in the server’s response, allowing the attacker to execute arbitrary JavaScript code in the victim’s browser. This could lead to session hijacking, redirection to malicious sites, or unauthorized actions being performed in the context of the authenticated user.

## System Host(s)
██████████

## Affected Product(s) and Version(s)
██████████ WebPortal

## CVE Numbers


## Steps to Reproduce
You can download the added exploit.html and open it in a browser

████

## Suggested Mitigation/Remediation Actions
To fix this issue, ensure that all user-supplied data is properly sanitized and encoded before being reflected in the server's response. Implementing Content Security Policy (CSP) headers can also mitigate the risk of XSS attacks by restricting the sources from which scripts can be loaded.



</details>

---
*Analysed by Claude on 2026-05-12*
