# Stored XSS on app.crowdsignal.com and survey.fm via Embed Media Parameter Injection

## Metadata
- **Source:** HackerOne
- **Report:** 920005 | https://hackerone.com/reports/920005
- **Submitted:** 2020-07-09
- **Reporter:** ali
- **Program:** Crowdsignal
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Embed Media feature of Crowdsignal's quiz builder, allowing attackers to inject malicious JavaScript through the media parameter. The vulnerability persists across multiple domains including app.crowdsignal.com and survey.fm public sharing links, enabling cookie theft and session hijacking.

## Attack scenario
1. Attacker creates a quiz on app.crowdsignal.com and navigates to the quiz question editor
2. Attacker adds a Multiple Choice question and uses the 'Add media' button to initiate media embedding
3. Attacker selects 'Embed Media' and initially enters a benign wpvideo embed code to pass validation
4. Attacker intercepts the save request in Burp Suite and modifies the media parameter with XSS payload breaking out of the expected format
5. Attacker's malicious payload containing SVG/onload event handler is stored in the database without proper sanitization
6. When quiz viewers or the quiz creator visit the page or public survey.fm link, the stored JavaScript executes in their browsers, stealing session cookies or performing actions on their behalf

## Root cause
The application fails to properly validate and sanitize user input in the media embedding functionality. The backend accepts and stores the media parameter value without sanitizing HTML/JavaScript content, and the frontend renders it without proper output encoding, allowing embedded script execution.

## Attacker mindset
An attacker recognizes that media embedding features often have relaxed validation to support rich content. By intercepting requests and modifying parameters that appear to be properly validated on the client-side, they can bypass weak server-side controls. The fact that the payload persists across shared public links indicates the attack affects not just the quiz creator but all viewers.

## Defensive takeaways
- Implement strict server-side input validation for all media embedding parameters, rejecting any input that doesn't conform to expected formats
- Apply proper output encoding (HTML entity encoding) when rendering user-supplied content, or use Content Security Policy to prevent inline script execution
- Use a whitelist approach for allowed embed types and validate against known safe patterns rather than blacklisting malicious patterns
- Implement parameterized queries and content security policies to prevent stored XSS execution
- Sanitize all user inputs using established libraries (e.g., DOMPurify) before storage and again before rendering
- Apply defense-in-depth: validate on client-side for UX, validate again on server-side, and encode on output
- Use subresource integrity and CSP headers to limit attack surface of embedded content

## Variant hunting
Search for similar embedding features in other Crowdsignal products (Crowdsignal.com surveys, polls). Look for other media-related parameters (image, video, iframe) that may have identical validation bypasses. Check for parameter pollution attacks using similar patterns on other user-generated content features like descriptions, option names, or custom HTML fields.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1056 - Adversary-in-the-Middle (if modifying responses)
- T1539 - Steal Web Session Cookie

## Notes
The vulnerability is particularly severe because it affects public sharing links (survey.fm), exposing the XSS to all quiz respondents and viewers. The attack requires burp suite interception, suggesting the application has insufficient server-side validation that solely relies on client-side checks. The payload `[wpvideo w0MiG12Exx1"><svg/onload=prompt(document.domain)>]` demonstrates a format string attack breaking out of the expected shortcode syntax.

## Full report
<details><summary>Expand</summary>

Hello there,
I found a stored xss vulnerability.

Steps:
1. Go to `https://app.crowdsignal.com/dashboard`
2. Create a quiz.
3. Go to `https://app.crowdsignal.com/quizzes/{your-quiz-id}/question`
4. Add `Multiple Choice`
5. Put a name to answer 1.
6. Click Add media button.

{F901543}
7. Select Embed Media
8. Paste this:  `[wpvideo w0MiG12E]`
9. Insert it.
10. Open `Burp Suite` and click `Save` button.
11. Return to burp suite and paste this payload to `media[23168664]` parameter: `[wpvideo%20w0MiG12Exx1\"><svg/onload=prompt(document.domain)>]`
12. Forward the request and refresh the page. You will see xss alert.

Also go to `https://app.crowdsignal.com/sharing/quiz/{your-quiz-id}/` and copy survey.fm link. Go to it and you will see xss alert.

## Impact

Stealing cookies

Regards,
@mygf

</details>

---
*Analysed by Claude on 2026-05-12*
