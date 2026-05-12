# Stored XSS in Product Comments via Transfers Tab

## Metadata
- **Source:** HackerOne
- **Report:** 738072 | https://hackerone.com/reports/738072
- **Submitted:** 2019-11-15
- **Reporter:** chj2934
- **Program:** Unknown (HackerOne Report #738072)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the product comments section of the transfers tab, allowing attackers to inject malicious JavaScript code that persists in the database. By crafting a product name with XSS payload and manipulating the code editor, an attacker can execute arbitrary JavaScript in the context of other users' browsers, potentially stealing session cookies and performing actions on their behalf.

## Attack scenario
1. Attacker creates a product with a name containing XSS payload: '"'><img src=x onerror=alert(domain.domain)>'
2. Attacker adds a transfer using the malicious product
3. Attacker navigates to product settings and enters the same XSS payload in the title field using code editor
4. XSS payload executes in attacker's browser (proof of concept)
5. Attacker copies the rendered malicious code snippet and deletes the original payload
6. Attacker pastes the copied code into the transfers product comments section, which now stores and reflects the XSS to all users viewing that transfer

## Root cause
The application fails to properly sanitize and encode user input in product names and comments before storing in the database. Additionally, the transfers tab does not perform output encoding when displaying product comments, allowing stored XSS payloads to execute in users' browsers.

## Attacker mindset
An attacker exploits the code editor's rendering behavior to obfuscate the XSS payload, making it harder to detect via simple pattern matching. By separating payload injection from payload execution across different fields and tabs, the attacker attempts to evade security filters.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-supplied data, especially product names and comments
- Apply context-aware output encoding (HTML entity encoding) when displaying user-generated content
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize HTML input using libraries like DOMPurify or similar XSS prevention libraries
- Implement server-side validation independent of client-side controls
- Regularly audit code editors and rich-text fields for XSS vulnerabilities
- Apply least-privilege principles to comment rendering (render as text by default, not HTML)

## Variant hunting
Test other product metadata fields (description, tags, SKU) for similar stored XSS
Check if the vulnerability affects different user roles (admin, customer, vendor)
Test event handlers beyond 'onerror' (onload, onclick, onmouseover, etc.)
Verify if the vulnerability persists across different browsers and JavaScript engines
Check other tabs/sections where products are referenced for the same vulnerability
Test multipart payloads using SVG, iframe, or script tag variations
Examine if file upload fields in product creation allow XSS injection

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1539

## Notes
The writeup suggests a somewhat convoluted reproduction path, but the core issue is straightforward: unsanitized user input in product fields is stored and reflected in comments without encoding. The use of the code editor appears to be a red herring or attack sophistication technique rather than a fundamental requirement for exploitation. The primary impact is cookie theft via XSS, but could extend to session hijacking, credential harvesting, and account takeover. The report lacks specific impact quantification and bounty information.

## Full report
<details><summary>Expand</summary>

summery: 

You are able to copy and paste stored XSS code into the comment section of a product in the transfers tab and receive the error.

Reproduce:

1. Create a product with the name '"'><img src=x onerror=alert(domain.domain)>'
2. add a transfer with that product
3. now go back to the product use the code button and type the same code for the title . '"'><img src=x onerror=alert(domain.domain)>'
4. you will get a XSS pop-up however ignore it. as soon as you get here you need to get out of the code setting and into the normal text and copy the the little piece of code with the image.
5. delete the code that we put in the html for the XSS.
6. go back to transfers and paste the code that we copied there
7. error

## Impact

steal cookie

</details>

---
*Analysed by Claude on 2026-05-12*
