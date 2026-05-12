# Reflected XSS and HTML Injection in pressable.com Search Box

## Metadata
- **Source:** HackerOne
- **Report:** 1537149 | https://hackerone.com/reports/1537149
- **Submitted:** 2022-04-11
- **Reporter:** sawrav-chowdhury
- **Program:** Pressable
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The search functionality on pressable.com/knowledgebase/ fails to properly sanitize user input, allowing attackers to inject arbitrary JavaScript and HTML code through the search parameter. Malicious payloads in the 's' query parameter are directly reflected in the response without encoding, enabling credential theft and phishing attacks.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the search parameter (e.g., ?s=<img src=x onerror=alert(document.cookie)>)
2. Attacker distributes the URL via email, social media, or other channels to target users
3. Victim clicks the link and visits pressable.com with the injected payload
4. The search parameter is reflected in the page without HTML encoding, causing JavaScript execution in victim's browser
5. Attacker's script executes in victim's context, stealing cookies, session tokens, or capturing credentials
6. Attacker can redirect victim to phishing site or perform further malicious actions

## Root cause
The search parameter 's' is reflected directly into the HTML response without proper output encoding or Content Security Policy enforcement. The application fails to sanitize or escape user input before displaying it in the search results page.

## Attacker mindset
An attacker would target this vulnerability to harvest session cookies/authentication tokens, redirect users to malicious sites for credential harvesting, distribute malware, or conduct phishing campaigns against pressable.com users who may include developers and website owners.

## Defensive takeaways
- Implement output encoding/HTML entity encoding on all user-controlled data before reflecting in HTML context
- Use a templating engine with auto-escaping enabled by default
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Perform input validation on search parameters to reject or sanitize HTML/script tags
- Use security libraries like OWASP ESAPI or similar for context-aware encoding
- Regular security testing including SAST/DAST tools to detect XSS vulnerabilities
- Implement HTTPOnly and Secure flags on session cookies to mitigate impact

## Variant hunting
Search for similar vulnerabilities in: other search boxes on pressable.com domain, query parameters in knowledge base filtering functionality, any user input reflected in search results or suggestions, autocomplete features that may reflect user input, and admin search interfaces

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a straightforward reflected XSS vulnerability with clear PoC. The vulnerability is easily exploitable and requires no authentication. The impact is significant as it affects user trust and can lead to credential compromise. The HTML Injection variant, while less immediately dangerous than XSS, demonstrates lack of input validation.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi, I have found that search box  on pressable.com is vulnerable for XSS attack and HTML Injection .

## Steps To Reproduce:

1. Visit https://pressable.com/knowledgebase/
2. Put the payload on the search box. 

XSS Payload: "><img src=x onerror=javascript:alert(document.cookie)>

HTML Injection Payload: <h1><font Color=red>Visit  Our  New  WebSite </h1><h3><mark><a href="https://example.com">e x a m p l e . c o m </a></mark></h3>

3.XSS will be triggered /HTML Injection will be reflected.

Link with XSS Payload: [https://pressable.com/?s=%22%3E%3Cimg+src%3Dx+onerror%3Djavascript%3Aalert%28document.cookie%29%3E&post_type=knowledgebase](https://pressable.com/?s=%22%3E%3Cimg+src%3Dx+onerror%3Djavascript%3Aalert%28document.cookie%29%3E&post_type=knowledgebase)

Link with HTML Injection Payload: [https://pressable.com/?s=%3Ch1%3E%3Cfont+Color%3Dred%3EVisit++Our++New++WebSite+%3C%2Fh1%3E%3Ch3%3E%3Cmark%3E%3Ca+href%3D%22https%3A%2F%2Fexample.com%22%3Ee+x+a+m+p+l+e+.+c+o+m+%3C%2Fa%3E%3C%2Fmark%3E%3C%2Fh3%3E&post_type=knowledgebase](https://pressable.com/?s=%3Ch1%3E%3Cfont+Color%3Dred%3EVisit++Our++New++WebSite+%3C%2Fh1%3E%3Ch3%3E%3Cmark%3E%3Ca+href%3D%22https%3A%2F%2Fexample.com%22%3Ee+x+a+m+p+l+e+.+c+o+m+%3C%2Fa%3E%3C%2Fmark%3E%3C%2Fh3%3E&post_type=knowledgebase)

## Supporting Material/References:
POC Video Attached

## Impact

Due to these vulnerabilities, attacker can easily divert victims to their malicious site and able to get credentials of victims.

</details>

---
*Analysed by Claude on 2026-05-12*
