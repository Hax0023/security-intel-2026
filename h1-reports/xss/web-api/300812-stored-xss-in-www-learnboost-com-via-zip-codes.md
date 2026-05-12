# Stored XSS in LearnBoost Network Panel via ZIP Code Input

## Metadata
- **Source:** HackerOne
- **Report:** 300812 | https://hackerone.com/reports/300812
- **Submitted:** 2017-12-27
- **Reporter:** edoverflow
- **Program:** LearnBoost
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
LearnBoost's Network panel is vulnerable to stored XSS through ZIP code fields that are displayed alongside school names in search results. An attacker can inject malicious JavaScript that persists in the database and executes whenever the compromised data is displayed, particularly during search operations.

## Attack scenario
1. Attacker navigates to https://www.learnboost.com/settings/network/search
2. Attacker searches for a common term (e.g., 'fro' or 'aa') to locate a school entry
3. Attacker modifies the ZIP code field with XSS payload: "><img src=x onerror=alert(document.domain)>
4. Payload is stored in the database without sanitization
5. When any user searches for the same term, the stored payload executes in their browser
6. Attacker gains ability to steal session tokens, perform actions as victims, or redirect to phishing sites

## Root cause
The application fails to properly validate and encode user-supplied input in the ZIP code field before storing it in the database and rendering it in search results. The vulnerability exists in both input validation (allowing HTML/script content) and output encoding (failing to escape special characters when displaying data).

## Attacker mindset
An attacker would deliberately target high-traffic search terms to maximize payload execution across multiple users. They could exploit the educational nature of the platform to establish persistence and potentially compromise student/teacher data or accounts at scale.

## Defensive takeaways
- Implement strict input validation for ZIP code fields (numeric-only, length restrictions)
- Apply context-appropriate output encoding (HTML entity encoding) when rendering user-supplied data
- Use Content Security Policy (CSP) headers to restrict inline script execution
- Implement a Web Application Firewall (WAF) to detect common XSS patterns
- Conduct security code review of all user input handling paths
- Perform regular penetration testing focusing on stored XSS in secondary fields
- Sanitize data at both input and output layers using established libraries

## Variant hunting
Search for similar user-input fields in the Network panel (school names, addresses, phone numbers)
Test other search/filter functionality that displays user-controlled data
Check for stored XSS in user profiles or settings pages across LearnBoost
Investigate if ZIP code fields are mirrored in API responses or CSV exports
Look for reflected XSS in search parameters that might inform stored XSS vectors
Test for DOM-based XSS in client-side search filtering logic

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1059

## Notes
This is a classic stored XSS vulnerability with high impact due to its persistence and automatic execution on common search terms. The attacker's observation about mapping to high-frequency search terms (like 'aa') demonstrates understanding of attack optimization. The educational platform context means potential victims could include minors and sensitive institutional data may be at risk. The PoC is straightforward and reproducible, suggesting weak input handling throughout the application.

## Full report
<details><summary>Expand</summary>

# Summary
---

www.learnboost.com is vulnerable to stored XSS via ZIP codes stored alongside school names in the *Network* panel. 

# Browsers Verified In
---

* Mozilla Firefox 58.0b12 (64-bit)

# PoC
---

Visit https://www.learnboost.com/settings/network/search and search for `fro`. My entry will trigger the XSS payload.

```html
"><img src=x onerror=alert(document.domain)>
```

{F249746}

## Impact

I now have stored XSS that triggers whenever someone searches for `fro`. If I were to map the payload to a very common search term (e.g. `aa`) that would increase the likelihood that my payload would fire.

</details>

---
*Analysed by Claude on 2026-05-12*
