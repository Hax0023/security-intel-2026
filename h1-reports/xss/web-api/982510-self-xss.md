# Self XSS in Shopify App Import Store via CSV Filename

## Metadata
- **Source:** HackerOne
- **Report:** 982510 | https://hackerone.com/reports/982510
- **Submitted:** 2020-09-15
- **Reporter:** ahmedalahmed
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Cross-Site Scripting (XSS), Self-XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A self-XSS vulnerability was identified in the Shopify admin panel's app import functionality where malicious JavaScript could be executed through a crafted CSV filename containing XSS payloads. The vulnerability requires the authenticated user to manually upload a file with a malicious filename, making it a self-XSS that would primarily impact the uploader themselves.

## Attack scenario
1. Attacker authenticates to their own Shopify store (myshopify.com/admin)
2. Attacker navigates to Settings > Apps > Import Store section
3. Attacker selects platform and prepares a CSV file with payload in the filename: '<img src=xx onerror=alert(document.domain)>'
4. Attacker uploads the malicious CSV file through the import interface
5. The application fails to properly sanitize/encode the filename when displaying file information or upload status
6. JavaScript payload executes in the attacker's browser session with admin privileges

## Root cause
The application does not properly encode or sanitize user-supplied filenames when displaying them in the admin interface. The CSV filename is directly rendered in HTML without proper escaping, allowing embedded JavaScript to execute.

## Attacker mindset
Low-skill attacker demonstrating basic XSS payload knowledge. The attacker either doesn't recognize this is self-XSS with limited impact, or is attempting to chain it with account takeover techniques. Could also be a proof-of-concept to demonstrate input validation gaps.

## Defensive takeaways
- Implement strict output encoding for all user-supplied data including filenames
- Apply HTML entity encoding when displaying filenames in the UI
- Use Content Security Policy (CSP) headers to restrict script execution
- Validate and sanitize filenames on upload, rejecting special HTML characters
- Implement input validation that restricts filenames to alphanumeric characters and safe symbols
- Use a whitelist approach for allowed characters in filenames
- Apply defense-in-depth: validate on backend, sanitize on frontend, and encode on output

## Variant hunting
Check other file upload functionality in Shopify admin for similar filename XSS
Test other admin settings pages that display user-supplied filenames
Look for CSV/spreadsheet import features in other Shopify products
Search for DOM-based XSS in file management interfaces
Test filename handling in bulk operations and data import tools
Check if payloads can be stored and executed on page refresh (stored XSS upgrade)
Test if filename XSS can be reflected to other users via shared import templates

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is classified as self-XSS with very limited practical impact since it only affects the user uploading the file. The vulnerability would have higher severity if it could be stored and reflected to other users, or if it could lead to admin account compromise. The report lacks detail on actual impact demonstration and whether this could be chained with other vulnerabilities. Shopify likely triaged this as low priority or informational due to self-XSS nature.

## Full report
<details><summary>Expand</summary>

I have found self xss in `myshopify.com/admin/apps/import-store/`
POC

1 - Go to yourstore.myshopify.com
2 - Go to settings > App -> Import [ maybe ask you for your platform select any one ]
3 -  Upload  file csv with file name payload xss "><img src=xx onerror=alert(document.domain)>

## Impact

XSS Attack

</details>

---
*Analysed by Claude on 2026-05-12*
