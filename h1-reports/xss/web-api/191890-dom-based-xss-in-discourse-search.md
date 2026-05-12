# DOM Based XSS in Discourse Search

## Metadata
- **Source:** HackerOne
- **Report:** 191890 | https://hackerone.com/reports/191890
- **Submitted:** 2016-12-17
- **Reporter:** khizer47
- **Program:** Discourse
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** DOM-based XSS, Stored XSS, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in Discourse's search functionality where user-supplied input containing script tags is not properly sanitized before being rendered in advanced search results. An attacker can inject malicious JavaScript by crafting a search query with embedded script tags, which executes when the advanced search page loads or when a victim clicks on a shared link.

## Attack scenario
1. Attacker navigates to a Discourse instance (e.g., try.discourse.org) and clicks the search button
2. Attacker enters a malicious payload containing a script tag (e.g., @<script>prompt(1337)</script>gmail.com) in the search field
3. Attacker clicks on 'Advanced Search' which processes the unsanitized input
4. The JavaScript payload executes in the attacker's browser context, proving code execution
5. Attacker copies the resulting URL containing the payload and shares it with victims
6. When victims click the link or load the page, the embedded script executes in their browser, potentially stealing session tokens or performing actions on their behalf

## Root cause
The search functionality fails to properly sanitize or encode user input before incorporating it into the DOM. The advanced search feature dynamically renders search parameters without applying appropriate output encoding or Content Security Policy protections, allowing injected script tags to execute as legitimate code.

## Attacker mindset
An attacker with basic knowledge of XSS vulnerabilities can easily craft and distribute malicious search links. The low barrier to entry (simple payload injection) and high impact (session hijacking, account takeover) make this an attractive vector for phishing campaigns or mass exploitation.

## Defensive takeaways
- Implement robust input validation and sanitization for all search parameters
- Apply proper output encoding (HTML entity encoding) when rendering user input in the DOM
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Use a templating engine with auto-escaping enabled (e.g., Ember.js SafeString handling)
- Conduct regular security audits of search and filter functionality
- Apply framework-level protections for DOM manipulation to prevent XSS
- Implement DOMPurify or similar libraries for sanitizing user-generated content

## Variant hunting
Look for similar XSS vulnerabilities in: other search features across Discourse, filter/advanced query parameters, user mention functionality, tag searches, category searches, and any other user input that flows to the DOM without sanitization. Test for both stored and reflected XSS variants in search history and shared search links.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a straightforward DOM-based XSS with potential for stored impact if search queries are persisted. The vulnerability is easily exploitable and has clear attack vectors through social engineering. The use of @ prefix in the payload suggests context-specific filtering may have been partially implemented but bypassed. The Discourse platform should have been using framework-level XSS protections given it's built on Ember.js.

## Full report
<details><summary>Expand</summary>

###Steps to Reproduce:

1. Load http://try.discourse.org
2.Now From Top Right Corner Click on Search Button 
3. Enter payload their 

###Payload:

@<script>prompt(1337)</script>gmail.com

4: Now in new windows that opens click on advance search and The XSS will Occur :) 
5: Now copy the link and send to victim there the XSS will Occur To 

Thanks
Khizer Javed 


</details>

---
*Analysed by Claude on 2026-05-12*
