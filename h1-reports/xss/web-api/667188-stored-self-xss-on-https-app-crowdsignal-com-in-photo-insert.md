# Stored Self XSS in Photo Insert App (Crowdsignal) + Stored XSS on Survey.fm

## Metadata
- **Source:** HackerOne
- **Report:** 667188 | https://hackerone.com/reports/667188
- **Submitted:** 2019-08-04
- **Reporter:** ali
- **Program:** Crowdsignal (Automattic)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Self XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored self XSS vulnerability was discovered in the Crowdsignal photo insert functionality where unsanitized SVG payloads could be injected via the media_code parameter during quiz creation. The vulnerability persists across multiple views and propagates to Survey.fm subdomains, allowing arbitrary JavaScript execution when users view the affected quiz.

## Attack scenario
1. Attacker creates a new quiz on app.crowdsignal.com
2. Attacker uploads a photo via the image insert button in a Multiple Choice question
3. Attacker intercepts the save request and modifies the media_code parameter with SVG XSS payload: "><svg/onload=alert(document.domain)>
4. Attacker forwards the modified request, storing the payload in the application database
5. Attacker shares the quiz link with victims
6. When victims open the quiz link, the stored XSS payload executes in their browser context, potentially stealing session cookies or performing actions on their behalf

## Root cause
The application fails to properly sanitize or validate the media_code parameter before storing and rendering it. SVG tags with event handlers are not stripped or escaped during input validation, and output encoding is insufficient when the parameter is rendered in HTML context.

## Attacker mindset
An attacker recognized that image file parameters could be manipulated at the HTTP level to inject malicious code. By understanding the parameter structure (media_code) and testing with SVG payloads, the attacker discovered the stored nature of the vulnerability and its cross-domain propagation to survey.fm subdomains, enabling widespread exploitation.

## Defensive takeaways
- Implement strict input validation and whitelist allowed values for file identifiers and media references
- Use content security policy (CSP) headers to prevent inline script execution
- Sanitize all user-controlled input before storage using a robust library (e.g., DOMPurify, bleach)
- Encode output based on context (HTML entity encoding for HTML context, JavaScript encoding for script context)
- Avoid trusting parameters in HTTP requests; validate against known file metadata stored server-side
- Implement a Web Application Firewall (WAF) to detect and block XSS patterns in requests
- Conduct security testing of file upload and media handling workflows
- Use security headers like X-Content-Type-Options: nosniff and X-Frame-Options

## Variant hunting
Search for similar vulnerabilities in: (1) other media/file insertion features across Crowdsignal and Automattic products, (2) any parameter that references file IDs or media identifiers that could be manipulated, (3) other quiz/survey platforms with image insertion capabilities, (4) parameters used in dashboard creation flows that handle attachments or media, (5) any legacy image handling code that may bypass modern sanitization filters

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
This vulnerability demonstrates the danger of trusting client-side parameter manipulation on file/media references. The fact that it persists across subdomains (survey.fm) indicates shared backend infrastructure or database. The 'self XSS' designation in the title is potentially misleading—this appears to be a stored XSS that affects other users viewing the quiz, not just the creator. The report demonstrates proper vulnerability disclosure methodology with step-by-step reproduction and proof-of-concept images.

## Full report
<details><summary>Expand</summary>

Steps:
1. Go to https://app.crowdsignal.com/dashboard and click Create a New > Quiz
2. Add Multiple Choice to your page and click image button, upload a photo and click upload.
3. Start the burp suite and click Save button. Look at the request (poc1.png) and you will see media_code= parameter. It will be your photo's id and change it as payload and forward the request. Payload: "><svg/onload=alert(document.domain)> 
4. Now you will see xss (poc2.png). Copy the quiz link and open it the new tab. You will see second xss (poc3.png). And this one is stored xss.

## Impact

XSS

</details>

---
*Analysed by Claude on 2026-05-12*
