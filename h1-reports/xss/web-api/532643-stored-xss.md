# Stored XSS in Oberlo Supplier Messaging System

## Metadata
- **Source:** HackerOne
- **Report:** 532643 | https://hackerone.com/reports/532643
- **Submitted:** 2019-04-09
- **Reporter:** ashketchum
- **Program:** Oberlo
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Oberlo supplier messaging feature where user-supplied HTML/JavaScript payloads in message content are not properly sanitized or encoded before being stored and rendered. An attacker can inject malicious scripts through the message functionality that execute when any user views the message in their inbox.

## Attack scenario
1. Attacker navigates to the supplier products page on Oberlo
2. Attacker clicks the message icon on a supplier profile to initiate a message
3. Attacker fills in the message form with reason, subject, and a malicious XSS payload in the message body (e.g., "><img src=x onerror=prompt(document.cookie)>)
4. Attacker submits the message, which is stored in the database without proper sanitization
5. When the target supplier or any user views the message in their inbox, the injected script executes in their browser context
6. The attacker achieves cookie theft, session hijacking, credential capture, or other malicious actions depending on payload complexity

## Root cause
The application fails to implement proper input validation and output encoding on the messaging feature. User input in the message field is stored directly to the database and subsequently rendered as HTML/JavaScript without escaping special characters or stripping dangerous tags and event handlers.

## Attacker mindset
The attacker demonstrates reconnaissance capability by identifying the messaging functionality as an input vector, crafting a simple proof-of-concept payload to validate the vulnerability, and documenting clear reproduction steps. The use of a basic prompt() function suggests the attacker's primary goal was vulnerability discovery and reporting rather than active exploitation.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied content, especially in messaging and comment features
- Apply contextual output encoding (HTML entity encoding) when rendering user-generated content
- Use Content Security Policy (CSP) headers to restrict inline script execution and limit script sources
- Employ a whitelist-based HTML sanitization library (e.g., DOMPurify, Bleach) to strip dangerous tags and attributes
- Conduct security code reviews specifically targeting user input handling in communication features
- Implement automated scanning for XSS vulnerabilities in the development pipeline
- Apply the principle of least privilege to message content rendering

## Variant hunting
Check other messaging or comment features across the Oberlo platform for similar XSS patterns
Test product reviews, feedback forms, and user profile description fields for stored XSS
Examine notification systems to see if they render user-supplied content without encoding
Investigate API endpoints that handle message creation for direct injection possibilities
Test DOM-based XSS vectors in the messaging module's client-side message formatting code
Check for reflected XSS in the referralUrl parameter shown in the original report URL

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539

## Notes
The report lacks specific bounty amount and response timeline information. The POC is straightforward and well-documented with clear reproduction steps, making it easily verifiable. The vulnerability affects the confidentiality and integrity of user sessions and data. The payload demonstrated (document.cookie access) suggests potential session hijacking as a primary concern. The messaging feature's prevalence makes this a high-impact vulnerability affecting multiple users.

## Full report
<details><summary>Expand</summary>

Hello Security Team,
I have Found Stored XSS Vulnerability 

POC : 
Step1: Go to https://app.oberlo.com/suppliers
Step2: Click on any product you will be redirected to URL as i have given for example https://app.oberlo.com/suppliers/8/products/488813?referralUrl=https%3A%2F%2Fapp.oberlo.com%2Fsuppliers%2F8%2Fproducts
Step3: You will get message icon in front of supplier name 
Step4: Click on that message 
Step5: Add Reason-->Subject-->and in message add my payload 
Payload: "><img src=x onerror=prompt(document.cookie)>
Step6: Click on send message 
Step7: Go to Inbox and you will see XSS is triggered and your payload was executed successfully

I have attached POC Video, Please go through it 

Thank you!
Ashish Dhone

## Impact

An attacker who exploits a cross-site scripting vulnerability is typically able to:

1) Impersonate or masquerade as the victim user.
2) Carry out any action that the user is able to perform.
3) Read any data that the user is able to access.
4) Capture the user's login credentials.
5) Perform virtual defacement of the web site.
6) Inject trojan functionality into the web site.

</details>

---
*Analysed by Claude on 2026-05-12*
