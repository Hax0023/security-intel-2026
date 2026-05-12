# Stored XSS in Public Profile Reviews via Data URI in Product Descriptions

## Metadata
- **Source:** HackerOne
- **Report:** 1398285 | https://hackerone.com/reports/1398285
- **Submitted:** 2021-11-11
- **Reporter:** vj1naruto
- **Program:** HackerOne Platform (likely internal or partner program)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the public profile review feature where users can add product recommendations with descriptions. Attackers can inject data URI-encoded XSS payloads in HTML anchor tags within product descriptions, which execute when other users view the profile and click the link. The vulnerability persists because user input is not properly sanitized or encoded before storage and rendering.

## Attack scenario
1. Attacker registers an account on the vulnerable platform
2. Attacker navigates to their profile and clicks 'Add Recommendation'
3. Attacker fills in product details with a malicious description containing base64-encoded data URI XSS payload in an anchor tag
4. Attacker saves the form, storing the malicious payload in the database
5. Victim user views the attacker's public profile
6. Victim clicks the HTML anchor link, triggering JavaScript execution in their browser context

## Root cause
The application fails to implement proper input validation and output encoding on user-supplied content in product descriptions. Specifically: (1) no sanitization of HTML/JavaScript in description fields, (2) no encoding of stored data before rendering, (3) no Content Security Policy to prevent data URI execution, (4) inadequate validation of href attributes in anchor tags

## Attacker mindset
An attacker exploiting this vulnerability aims to conduct account compromise, credential theft, session hijacking, or malware distribution by leveraging the trust relationship between users on the platform. The use of base64 encoding suggests an attempt to evade basic input filters. Targeting the public profile increases exposure and likelihood of multiple victims clicking the link.

## Defensive takeaways
- Implement strict input validation on all user-supplied content, especially HTML rich text fields
- Use context-aware output encoding (HTML entity encoding) when rendering user content
- Deploy a robust HTML sanitization library (e.g., DOMPurify, bleach) to strip dangerous tags and attributes
- Implement Content Security Policy (CSP) with restrictions on data: URI scheme and script-src directives
- Use allowlist approach for permitted HTML tags and attributes in descriptions
- Add server-side validation to reject or escape href attributes containing data: protocol
- Consider using iframe sandboxing for displaying user-generated content
- Implement security headers including X-XSS-Protection and X-Content-Type-Options
- Conduct regular security testing including XSS payload fuzzing during QA
- Log and monitor suspicious content submissions for detection of attack patterns

## Variant hunting
Test other user input fields (comments, reviews, titles, tags) for similar XSS vulnerabilities
Attempt alternative XSS encodings: UTF-7, UTF-16, HTML entities, Unicode escapes
Try javascript: protocol instead of data: URI
Test SVG/XML-based XSS vectors in description fields
Attempt event handler injection in other HTML contexts (img onerror, iframe onload, etc.)
Check profile customization features (bio, headers, avatars) for stored XSS
Test product recommendation feature in other languages/locales for encoding bypass
Attempt polyglot XSS payloads combining multiple encoding schemes

## MITRE ATT&CK
- T1190
- T1559.001
- T1566.002
- T1598.003

## Notes
This is a classic stored XSS vulnerability exploiting insufficient output encoding. The use of data URI with base64 encoding is a known obfuscation technique to bypass simple string-matching filters. The public profile context amplifies impact as multiple users may be exposed. The vulnerability requires user interaction (clicking link) but stored nature means the payload persists indefinitely. Organization should prioritize remediation given exposure on public profiles and potential for widespread exploitation.

## Full report
<details><summary>Expand</summary>

Summary:
Stored XSS found in public profile review in which we can add product details in shop addition options. In description of shop product we can add data URI XSS in HTML format which is led to XSS once user click on HTML.
In data URI XSS payload is encrypted in base64

Steps To Reproduce:
  1. Login with registered username and go to profile.
  2. After that click on add recommendation and add product details and in it's description add below payload:
<a href="data:text/html;charset=utf-7;base64,PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4=">Click Here</a>
{ Data URI XSS: data:text/html;charset=utf-7;base64,PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4=
(PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4=) : <script>alert('XSS')</script> }
  3. Now save the form by filling rest columns.
  4. If any one views public profile and click on HTML tag, it will trigger XSS.

Proof Of Concept:
Video POC attached

## Impact

Attacker can execute XSS in the victim user using judge platform

</details>

---
*Analysed by Claude on 2026-05-12*
