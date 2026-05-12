# Reflected Cross-Site Scripting (XSS) in Imprint Search Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1211148 | https://hackerone.com/reports/1211148
- **Submitted:** 2021-05-28
- **Reporter:** mersenne
- **Program:** Drugs.com
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (Reflected), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the imprint search parameter of drugs.com/imprints.php that allows attackers to execute arbitrary JavaScript by injecting malicious payloads through the URL. The vulnerability requires at least one search result to be present, which attackers can guarantee by using sufficiently long search strings. The injected JavaScript executes in the victim's browser context when hovering over certain UI elements.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the 'imprint' parameter, encoded to bypass basic filters
2. Attacker ensures search results are returned by padding the payload with legitimate characters or long strings
3. Attacker sends the malicious URL to victim via email, chat, or posts it on a forum frequented by target users
4. Victim clicks the link and the page loads with injected HTML/JavaScript attributes on search result elements
5. When victim hovers over UI elements like 'sort by' or 'amount of results' dropdowns, the onpointerover event fires
6. Attacker's JavaScript executes with victim's session context, allowing cookie theft, credential harvesting, or malicious redirects

## Root cause
The application fails to properly sanitize and encode user input from the 'imprint' URL parameter before reflecting it in HTML attributes within the page response. The search result display mechanism echoes the imprint parameter value into HTML element attributes without adequate escaping, allowing attackers to break out of the attribute context and inject arbitrary attributes with event handlers.

## Attacker mindset
An attacker would recognize that generating dummy search results (via padding) guarantees the vulnerable code path executes. They would leverage event handlers like onpointerover that don't require user interaction beyond hovering to trigger payload execution. The use of URL encoding and attribute fragmentation demonstrates an attempt to bypass simplistic XSS filters.

## Defensive takeaways
- Implement strict input validation on all search parameters with whitelist of allowed characters
- Apply context-aware output encoding: HTML-encode for HTML content, JavaScript-encode for JS context, URL-encode for URLs
- Use a modern templating engine with automatic escaping enabled by default
- Implement Content Security Policy (CSP) headers to restrict inline script execution and attribute-based event handlers
- Apply the principle of least privilege to search functionality - only display what's necessary
- Conduct security testing of search/filter functionality with both simple and padded payloads
- Use HTTPOnly and Secure flags on session cookies to mitigate session theft attacks
- Implement server-side rate limiting and validation to prevent abuse of search padding technique

## Variant hunting
Look for similar reflected XSS in other filter/search parameters (color, shape parameters mentioned); test other page features that echo user input; check if results sorting/pagination parameters are vulnerable; investigate whether authenticated search features have better protection; examine any API endpoints that power the search functionality

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1204

## Notes
The POC demonstrates a sophisticated payload using custom attributes (v1-v7) to split the script tags and JavaScript code, then reconstructing it via template literals in the onpointerover handler. This suggests the application has basic XSS filters that can be bypassed with creative encoding. The fact that it works differently across browsers (Firefox vs Chrome) indicates browser-specific XSS filter differences. The requirement for search results to exist is a conditional exploitation requirement but not a true barrier given the padding technique described.

## Full report
<details><summary>Expand</summary>

Hello,
I found a XSS vulnerability in https://www.drugs.com/imprints.php?imprint=&color=&shape=0
The vulnerability is in the parameter *imprint*.
The vulnerability only exists if there is at least one result in the search. However, if you put a text long enough, you will always have search results. 

For example, the search: 'sometext' (https://www.drugs.com/imprints.php?imprint=sometext&color=8&shape=24) doesn't have results. However, the search 'sometextsometextsometextsometextsometextsometextsometextsometextsometextsometextsometextsometextsometext' (https://www.drugs.com/imprints.php?imprint=sometextsometextsometextsometextsometextsometextsometextsometextsometextsometextsometextsometextsometext&color=8&shape=24) have 971 results.
In this way, an attacker can put a long text and always have search results and perform the xss attack (although the protection against xss makes things a bit difficult).

**Steps To Reproduce**:
Visit de following POC link  (works in firefox but not in chrome) and move your mouse over the search filters ('sort by' or 'amount of results'):
https://www.drugs.com/imprints.php?imprint=_%22%3E%3C%78%20%69%64%3D%22%78%22%20%76%35%3D%22%29%22%20%76%31%3D%22%3C%22%20%76%32%3D%22%53%43%52%49%50%54%3E%22%20%76%33%3D%22%61%6C%65%22%20%76%34%3D%22%72%74%28%31%22%20%76%36%3D%22%3C%2F%22%20%76%37%3D%22%53%43%52%49%50%54%3E%22%20%6F%6E%70%6F%69%6E%74%65%72%6F%76%65%72%3D%22%64%6F%63%75%6D%65%6E%74%2E%77%72%69%74%65%60%24%7B%77%69%6E%64%6F%77%2E%78%2E%61%74%74%72%69%62%75%74%65%73%2E%76%31%2E%76%61%6C%75%65%2B%77%69%6E%64%6F%77%2E%78%2E%61%74%74%72%69%62%75%74%65%73%2E%76%32%2E%76%61%6C%75%65%2B%77%69%6E%64%6F%77%2E%78%2E%61%74%74%72%69%62%75%74%65%73%2E%76%33%2E%76%61%6C%75%65%2B%77%69%6E%64%6F%77%2E%78%2E%61%74%74%72%69%62%75%74%65%73%2E%76%34%2E%76%61%6C%75%65%2B%77%69%6E%64%6F%77%2E%78%2E%61%74%74%72%69%62%75%74%65%73%2E%76%35%2E%76%61%6C%75%65%2B%77%69%6E%64%6F%77%2E%78%2E%61%74%74%72%69%62%75%74%65%73%2E%76%36%2E%76%61%6C%75%65%2B%77%69%6E%64%6F%77%2E%78%2E%61%74%74%72%69%62%75%74%65%73%2E%76%37%2E%76%61%6C%75%65%7D%60%22%3E&color=8&shape=24

## Impact

An XSS attack allows an attacker to execute arbitrary JavaScript in the context of the attacked website and the attacked user. This can be abused to steal session cookies,  redirect users on malicious website, perform requests in the name of the victim, and more.

</details>

---
*Analysed by Claude on 2026-05-12*
