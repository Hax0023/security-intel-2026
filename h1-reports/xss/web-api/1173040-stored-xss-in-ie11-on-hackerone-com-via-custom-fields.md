# Stored XSS in IE11 on HackerOne via Custom Fields

## Metadata
- **Source:** HackerOne
- **Report:** 1173040 | https://hackerone.com/reports/1173040
- **Submitted:** 2021-04-23
- **Reporter:** user_name2023
- **Program:** HackerOne
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Input Validation Failure, Output Encoding Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability was discovered in HackerOne's custom fields functionality affecting Internet Explorer 11 users. Malicious JavaScript code injected through custom fields is executed in victims' browsers, allowing attackers to perform arbitrary actions on behalf of authenticated users.

## Attack scenario
1. Attacker identifies custom fields input on HackerOne platform that lacks proper sanitization
2. Attacker crafts malicious JavaScript payload optimized for IE11 rendering engine
3. Attacker submits payload through custom fields, which is stored in backend database without sanitization
4. When victim user views the page containing the custom field, malicious script executes in their browser context
5. Script can steal session tokens, redirect to malicious site, perform actions as the victim, or exfiltrate sensitive data
6. Attack persists as payload remains stored until manually removed

## Root cause
Custom fields input was not properly validated on submission and not properly output-encoded when rendered in HTML/JavaScript context, particularly in IE11 which has less stringent XSS protections than modern browsers

## Attacker mindset
Opportunistic vulnerability discoverer targeting a high-profile security platform; likely motivated by proof-of-concept demonstration and potential bounty reward; selected IE11 as target due to known weaker security model

## Defensive takeaways
- Implement strict input validation on all custom field submissions using allowlist approach
- Apply context-aware output encoding (HTML entity encoding minimum, JavaScript encoding where applicable)
- Utilize Content Security Policy (CSP) headers to prevent inline script execution
- Employ DOMPurify or similar HTML sanitization library for any user-generated content
- Implement server-side validation alongside client-side controls
- Test across multiple browsers including legacy IE versions if user base is supported
- Store rich content safely using markdown or structured formats rather than HTML
- Regular security code reviews focusing on input/output handling in user-controllable fields

## Variant hunting
Search for similar patterns in: comment fields, description fields, profile customization areas, report title/description fields, any textarea or rich-text editor inputs; check for XSS in other custom metadata fields; test with polyglot payloads affecting IE11 specifically; examine API endpoints accepting custom field data

## MITRE ATT&CK
- T1190
- T1583.001
- T1566.002
- T1204.001

## Notes
Report lacks detailed POC images (F#### references indicate missing attachments in JSON conversion); IE11 targeting suggests report may date to 2018-2021 era when IE11 was still in significant use; HackerOne's own custom fields feature makes this particularly ironic and impactful

## Full report
<details><summary>Expand</summary>

Hi There,

i found  stored xss via Custom Fields

 {F1275694}

----------------------------------

{F1275691}



POC:

{F1275692}

## Impact

The attacker can use this issue to execute malicious script code in the victim user browser also redirect the victim user to malicious sites.

</details>

---
*Analysed by Claude on 2026-05-12*
