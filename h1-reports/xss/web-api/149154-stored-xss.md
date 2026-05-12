# Stored XSS in Algolia Explorer - Attributes to Index Field

## Metadata
- **Source:** HackerOne
- **Report:** 149154 | https://hackerone.com/reports/149154
- **Submitted:** 2016-07-04
- **Reporter:** sysecure
- **Program:** Algolia
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Algolia Explorer application where unsanitized user input in the 'Attributes to index' field is persisted and executed in the browser on subsequent page visits. An attacker can inject malicious JavaScript that will execute for all users accessing the affected explorer configuration.

## Attack scenario
1. Attacker navigates to Algolia Explorer and accesses the ranking configuration tab
2. Attacker injects malicious payload in 'Attributes to index' field: "><img src=x onerror=prompt('XSS');>
3. Attacker clicks save, causing the malicious payload to be stored server-side
4. Injected JavaScript executes in attacker's browser, proving code execution
5. Attacker shares the explorer link with other users or waits for legitimate users to access it
6. When any user visits the same explorer URL, the stored XSS payload executes in their browser, enabling session hijacking, credential theft, or malware distribution

## Root cause
The application fails to properly sanitize and encode user input before storing it in the database and again when rendering it in the DOM. The 'Attributes to index' parameter accepts raw HTML/JavaScript without validation, and the stored payload is rendered directly without HTML entity encoding or Content Security Policy protections.

## Attacker mindset
An attacker seeks to compromise multiple users through a single payload injection. By storing XSS in a shared configuration that multiple users access, the attacker maximizes impact with minimal effort. This is particularly valuable in a developer tool context where users may have elevated privileges or access to sensitive data.

## Defensive takeaways
- Implement strict input validation on all user-supplied data, rejecting or escaping special HTML characters
- Apply context-aware output encoding when rendering user data (HTML entity encoding for HTML context)
- Utilize a robust HTML sanitization library to strip potentially dangerous elements and attributes
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Apply the principle of least privilege to API endpoints handling configuration storage
- Conduct security testing of all user input fields, especially in admin/configuration interfaces
- Use templating engines that auto-escape by default rather than manual encoding

## Variant hunting
Test other input fields in Algolia Explorer for similar XSS vulnerabilities (search queries, filters, custom ranking)
Check if the vulnerability extends to other Algolia dashboard components or configuration pages
Attempt DOM-based XSS through URL fragments and JavaScript event handlers
Test for reflected XSS in query parameters before the save/storage step
Investigate if other special characters or encoding bypasses (Unicode, HTML entities) can evade filters
Check for blind XSS using out-of-band detection methods in backend logging or admin panels

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1539

## Notes
This is a classic stored XSS vulnerability in a web application's user-facing feature. The persistent nature makes it particularly dangerous as the payload automatically executes for all subsequent visitors. The simplified proof-of-concept using img onerror demonstrates the vulnerability clearly but could be weaponized with more sophisticated payloads. The report lacks detail on impact assessment and responsible disclosure timeline.

## Full report
<details><summary>Expand</summary>

Hi ,i have found an xss issue here : https://www.algolia.com/explorer#?index=test&tab=ranking
Steps to reproduce :
1-Go to : https://www.algolia.com/explorer#?index=test&tab=ranking
2-At the Attributes to index add this script  :`"><img src=x onerror=prompt('XSS');> ` and press enter .
3-Click save 
You will see that the xss has been fired .
You can go to https://www.algolia.com/explorer#?index=test&tab=ranking again you will see that xss is fired again .

Thanks ,
Saleh

</details>

---
*Analysed by Claude on 2026-05-12*
