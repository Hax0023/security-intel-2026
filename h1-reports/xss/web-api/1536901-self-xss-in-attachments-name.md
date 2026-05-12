# Self XSS in Support Request Attachments Name

## Metadata
- **Source:** HackerOne
- **Report:** 1536901 | https://hackerone.com/reports/1536901
- **Submitted:** 2022-04-10
- **Reporter:** hacker1_agent
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Cross-Site Scripting (XSS), Self-XSS, Stored XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A self-XSS vulnerability exists in the support request feature where malicious JavaScript can be injected through attachment filenames. When a user uploads a file with a crafted filename containing XSS payload, the payload executes in their own session when viewing the attachment.

## Attack scenario
1. Attacker logs into account.acronis.com with valid credentials
2. Attacker navigates to Support requests and creates a new case
3. Attacker expands the Case ID section and attempts to leave a comment
4. Attacker uploads a file with malicious filename: "><img src="x" onerror="alert(document.domain)">.png
5. Attacker or another user views the support case/attachment
6. JavaScript payload executes in victim's browser context, potentially stealing session tokens or cookies

## Root cause
Insufficient input validation and output encoding of attachment filenames. The application fails to sanitize or properly escape filename content when displaying attachments in the support request interface.

## Attacker mindset
Low-privilege attacker or social engineer seeking to establish persistence or escalate attacks through seemingly trusted support channel. Could be leveraged in multi-stage attack after account compromise.

## Defensive takeaways
- Implement strict filename validation - whitelist allowed characters and reject special characters
- Apply proper output encoding (HTML entity encoding) when displaying filenames in HTML context
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Store filenames separately from display names to enable safe rendering
- Implement filename sanitization both server-side and client-side
- Add security testing for file upload features as part of regular security assessments
- Consider using UUIDs or hashed names internally while displaying sanitized user-friendly names

## Variant hunting
Similar self-XSS in other file upload features (invoices, documents, attachments in tickets)
DOM-based XSS through filename manipulation in download functionality
Stored XSS in file metadata fields (description, tags associated with attachments)
Reflected XSS through filename parameter in URL query strings
SVG/polyglot file uploads with embedded XSS
XSS in other user input fields within support request system (case title, description)

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is classified as self-XSS with limited impact since it primarily affects the attacker's own session. However, if the vulnerability allows stored execution visible to support staff or other users, impact increases significantly. The report lacks POC evidence and specific impact demonstration. Verify if this is truly self-XSS or if support staff viewing the case can also be affected.

## Full report
<details><summary>Expand</summary>

Hello Gents,
> + While testing `account.acronis.com` I found that I could inject XSS payload in attachments name at  **"Support requests"** .

### Steps to Reproduce:
1. Please Login at `account.acronis.com`.
2. From support request, support a new case.
3. Expand Case ID,  Leave a comment for support professional, upload a file: `"><img src="x" onerror="alert(document.domain)">.png`.


### Proof of Concept:
{F1687467}

## Impact

XSS

</details>

---
*Analysed by Claude on 2026-05-12*
