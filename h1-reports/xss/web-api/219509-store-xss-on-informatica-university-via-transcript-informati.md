# Stored XSS in Training Description Field via Informatica University Transcript

## Metadata
- **Source:** HackerOne
- **Report:** 219509 | https://hackerone.com/reports/219509
- **Submitted:** 2017-04-08
- **Reporter:** alfredsaonoy
- **Program:** Informatica
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Training Description field of the Informatica University transcript module. An authenticated attacker can inject malicious JavaScript that executes when any user views the training details, potentially leading to session hijacking or credential theft.

## Attack scenario
1. Attacker authenticates to Informatica University account
2. Attacker navigates to Universal Profile > Transcript tab
3. Attacker selects 'Add external training' from dropdown menu
4. Attacker injects XSS payload into Training Description field: '"><img src=x onerror=alert(document.cookie);>
5. Attacker completes form submission with malicious payload stored in database
6. When any user views the attacker's training details via 'View training details' option, malicious JavaScript executes in their browser context with access to cookies and session tokens

## Root cause
The application fails to properly sanitize and validate user input in the Training Description field before storing it in the database. Additionally, the application does not properly encode output when rendering training details, allowing HTML and JavaScript to be interpreted as code rather than plain text.

## Attacker mindset
An authenticated insider or compromised account holder could exploit this to conduct phishing attacks, steal session cookies/credentials from other users viewing their fake training entries, or perform account takeover attacks. Low barrier to exploitation due to authentication already being bypassed.

## Defensive takeaways
- Implement input validation and sanitization on all user-provided fields, particularly free-text fields like descriptions
- Use context-appropriate output encoding (HTML entity encoding) when rendering user-controlled content
- Employ a Content Security Policy (CSP) to prevent inline script execution
- Implement server-side input validation using allowlists rather than blocklists
- Use established libraries like OWASP ESAPI or DOMPurify for HTML sanitization
- Apply principle of least privilege - restrict who can add external training entries
- Implement security testing in CI/CD pipeline to catch XSS vulnerabilities early

## Variant hunting
Check other form fields accepting user input (training name, provider, dates) for similar XSS issues
Test profile bio/description fields for stored XSS
Examine comment or feedback functionality on training modules
Review any rich text editors used in the platform for bypass techniques
Test reflected XSS in transcript viewing/filtering parameters
Check for DOM-based XSS in JavaScript handling of training data

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Spearphishing Link (via XSS redirect)
- T1056: Input Capture (stealing cookies/credentials)
- T1105: Ingress Tool Transfer (malware delivery via XSS)

## Notes
Report demonstrates clear vulnerability chain with reproduction steps. Vulnerability is stored/persistent, affecting multiple users. Authentication requirement reduces scope but increases impact potential in enterprise environment. Multi-browser confirmation (Chrome, Firefox) indicates stable exploitation. Report lacks evidence of Informatica's patch/remediation status.

## Full report
<details><summary>Expand</summary>

Hi,

Vulnerable field: Training Description

Steps to reproduce:
1. Login to your account and go Informatica University.
2. You can either click on "My Training" or "Universal Profile" at the upper right hand corner of the page.
3. You will then be redirected to the Universal profile bio page, click on the "Transcript tab"
4. Select options on the upper right side then select "Add external training: on the drop down option.
5. Fill out the needed information but for the Training Description use the following payload:
'"><img src=x onerror=alert(document.cookie);>
6. Complete the rest of the form and click on Submit.
7. You will then be redirected to your training transcript.
8. On the right side of the transcript which has a label withdraw, select from the drop down "View training details"
9. The page will be redirected and you will then get the xss pop-up.

Would be best to sanitize all input on this form to avoid xss. 

Works on latest versions of chrome, and firefox.


Please let me know if you need further information. Thanks!

Cheers,

@ninjakatz__


</details>

---
*Analysed by Claude on 2026-05-12*
