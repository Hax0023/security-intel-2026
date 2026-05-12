# Cross-Site Scripting (XSS) through Search Form Filter on mtnplay.co.zm

## Metadata
- **Source:** HackerOne
- **Report:** 761573 | https://hackerone.com/reports/761573
- **Submitted:** 2019-12-19
- **Reporter:** cristiancornea
- **Program:** MTN Play
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (Reflected XSS), Input Validation Failure, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the search form filter functionality on mtnplay.co.zm that allows injection of arbitrary JavaScript code through Track, Album, or Artist input fields. An attacker can craft malicious URLs with JavaScript payloads that execute in the victim's browser when the search filter is applied, enabling session hijacking, credential theft, or malware distribution.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in a search filter field parameter
2. Attacker sends URL via phishing email, social media, or direct message to MTN Play users
3. Victim clicks the link and is redirected to mtnplay.co.zm with the XSS payload embedded in the search form
4. Victim applies the search filter by clicking submit/filter button
5. JavaScript payload executes in victim's browser context with full access to session cookies and local data
6. Attacker steals authentication tokens, performs actions on victim's behalf, or redirects to phishing site

## Root cause
The application fails to properly validate and encode user input from search filter fields (Track, Album, Artist) before reflecting it back in the HTML response. The filter functionality processes untrusted input without sanitization or context-aware output encoding.

## Attacker mindset
An attacker would target the search form's filter functionality because it accepts multiple input fields with apparent lack of validation. The reflective nature makes it ideal for crafting phishing URLs. MTN Play likely has a substantial user base with valuable session data, making credential theft or account compromise highly profitable.

## Defensive takeaways
- Implement input validation with strict whitelisting of allowed characters for search fields
- Apply context-aware output encoding (HTML entity encoding) to all user inputs reflected in responses
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Use a templating engine with automatic escaping enabled by default
- Conduct security testing of all user input points, particularly filters and search functionality
- Implement HTTPOnly and Secure flags on session cookies to limit XSS impact
- Perform regular security code reviews focusing on data flow from input to output

## Variant hunting
Search for similar reflected XSS in: other filter parameters on mtnplay.co.zm, advanced search features, sorting parameters, pagination parameters, category filters, and any user-controlled input reflected in search results pages. Check for DOM-based XSS variants in client-side search handling.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
Report lacks specific bounty amount and demonstrates vulnerability through video evidence. The vulnerability is in a public-facing search feature making it easily exploitable at scale. MTN Play serves a substantial African user base, making this a high-impact vulnerability for credential theft.

## Full report
<details><summary>Expand</summary>

## Summary:
There is a XSS vulnerability that can be triggered through a search form on mtnplay.co.zm

## Steps To Reproduce:
  1. Navigate to http://www.mtnplay.co.zm/smart/jqm.aspx
  2. Click on the search button (or go to this link: http://www.mtnplay.co.zm/smart/jqm.aspx?event=search&mnu=search&ctrlid=92)
  3. Click on the filter button 
  4. The XSS can be triggered in any field of that form by inputting a javascript payload (Track/Album/Artist)

## Demonstration: 
https://www.youtube.com/watch?v=doLHsUqnvgE

## Impact

Malicious javascript code can be injected into the application

</details>

---
*Analysed by Claude on 2026-05-12*
