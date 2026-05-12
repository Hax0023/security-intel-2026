# Cross-Site Scripting via XSRF Token Exposure in Nextcloud Enterprise Purchase Form

## Metadata
- **Source:** HackerOne
- **Report:** 858255 | https://hackerone.com/reports/858255
- **Submitted:** 2020-04-24
- **Reporter:** a9hora
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Stored Cross-Site Scripting (XSS), Information Disclosure, CSRF Token Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in the Nextcloud enterprise purchase form that allows attackers to inject malicious JavaScript payloads into form fields. When the form is processed, the XSS payload executes and the CSRF token is exposed in the email confirmation, enabling attackers to use this token for subsequent CSRF attacks.

## Attack scenario
1. Attacker navigates to the Nextcloud enterprise purchase form at https://nextcloud.com/enterprise/buy/
2. Attacker fills in legitimate name and email address fields, but injects XSS payload in other input fields (e.g., company name, phone, etc.)
3. Form submission triggers server-side processing without proper input sanitization
4. The XSS payload executes in context and exfiltrates the XSRF-TOKEN from the page DOM or cookies
5. Confirmation email is sent containing the XSRF-TOKEN in email source or rendered content
6. Attacker accesses the victim's email or intercepts the confirmation email to extract the token for CSRF attacks

## Root cause
Insufficient input validation and output encoding on the enterprise purchase form. User-supplied input is not properly sanitized before being processed or reflected back in confirmation emails. CSRF tokens are exposed in email content or responses without proper protection.

## Attacker mindset
An attacker targets the purchase form as a trust vector, knowing legitimate users will complete it. By injecting XSS, they can harvest CSRF tokens to perform unauthorized actions on behalf of victims, such as modifying account settings, making purchases, or accessing sensitive data.

## Defensive takeaways
- Implement strict input validation and whitelisting for all form fields
- Apply context-appropriate output encoding (HTML, URL, JavaScript encoding) based on where data is used
- Sanitize HTML content in emails using libraries like DOMPurify or OWASP sanitizers
- Never expose CSRF tokens in email confirmations or client-side accessible locations unnecessarily
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Use parameterized templates to prevent injection of malicious payloads into emails
- Implement server-side validation on all user inputs before processing
- Consider using httpOnly, Secure flags on CSRF token cookies to limit exposure
- Perform regular security testing including SAST/DAST on publicly facing forms

## Variant hunting
Test other user input forms on Nextcloud properties for similar XSS vulnerabilities
Check if CSRF tokens are exposed in other email templates (password reset, account confirmation, etc.)
Investigate if the same vulnerability exists in other enterprise/commercial product purchase flows
Test for DOM-based XSS variants using different payload encoding techniques
Check if error messages or validation responses reflect user input without sanitization
Test file upload functionality on purchase forms for XSS vectors
Investigate webhook implementations that might process and reflect form data
Test for mutation XSS (mXSS) in the email rendering process

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1095
- T1189

## Notes
The vulnerability chain demonstrates the danger of combining XSS with CSRF token exposure. While CSRF tokens are designed to protect against cross-site attacks, their exposure in email or client-side contexts negates this protection. The attacker demonstrates a two-stage attack: first using XSS to access the token, then leveraging it for CSRF. The reporter appropriately identified both the XSS flaw and the downstream CSRF risk.

## Full report
<details><summary>Expand</summary>

Please follow below mentioned steps for reproducing the vulnerability.
1. Open URL: https://nextcloud.com/enterprise/buy/
2. Fill up valid name and email address and put payload in other fields.
    
    Payload/s:
			<img src="x" onload=alert(document.cookie);>
			<svg/onload=alert(document.cookie);>	
3. Submit it
4. Open email address you mentioned in the email field.
5. Open up the email source.
6. You will be prompted with xsrf-token.

## Impact

As an attacker is getting the xsrf-token, he can utilize it in later attack such as, CSRF.

</details>

---
*Analysed by Claude on 2026-05-12*
