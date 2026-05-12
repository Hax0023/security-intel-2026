# Stored XSS in Staff Name Reflected in Internal Admin Panel

## Metadata
- **Source:** HackerOne
- **Report:** 946053 | https://hackerone.com/reports/946053
- **Submitted:** 2020-07-28
- **Reporter:** cyber__sec
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability was discovered where malicious JavaScript code injected into a staff member's name field persisted in the database and executed when displayed in Shopify's internal admin panel. The vulnerability allowed arbitrary code execution in the context of internal administrative tools, potentially compromising staff accounts and sensitive merchant data.

## Attack scenario
1. Attacker creates or modifies a staff member account with a crafted XSS payload in the name field (e.g., '<img src=x onerror="malicious_code()">')
2. Input validation fails to sanitize or reject the malicious payload
3. Payload is stored unencoded in the database
4. When an authorized admin views the staff management panel or related internal tools, the stored payload is retrieved
5. The admin panel fails to properly encode output when rendering the staff name
6. Malicious JavaScript executes in the context of the admin's session with full privileges

## Root cause
Lack of proper input validation on staff name field combined with insufficient output encoding when rendering staff information in internal admin panels. The application failed to implement context-aware output encoding (HTML entity encoding) for user-controlled data displayed in the DOM.

## Attacker mindset
Opportunistic security researcher testing a legacy test store to discover and document vulnerabilities. The attacker leveraged administrative access to inject payloads into less-restricted fields (staff names) that flow into privileged internal interfaces.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-provided fields, including staff names
- Apply context-appropriate output encoding (HTML entity encoding) for all dynamic content rendered in HTML context
- Use Content Security Policy (CSP) headers to limit script execution and reduce XSS impact
- Implement automated security testing (SAST/DAST) to detect stored XSS vulnerabilities before production
- Apply principle of least privilege - sanitize and validate data at database layer, not just presentation layer
- Regular security audits of internal admin panels which often receive less scrutiny than customer-facing features
- Use security libraries and frameworks that provide built-in XSS protection

## Variant hunting
Test all user-modifiable profile fields (email, phone, bio, title) for stored XSS
Check customer name fields, order notes, and product descriptions for similar vulnerabilities
Test internal tools and admin dashboards that display user-generated content
Look for stored XSS in comment fields, messaging systems, and collaboration tools
Test webhook payloads and API responses for stored XSS vectors
Examine third-party admin panel integrations that may inherit vulnerability

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1059.007

## Notes
Report lacks technical detail and bounty amount information. The reference to an email from a Shopify colleague suggests Shopify internally discovered the vulnerability before public submission. This highlights the importance of testing legacy/deprecated test environments which may have fewer security controls. The vulnerability affects internal tooling rather than customer-facing storefronts, limiting direct customer impact but enabling lateral movement within Shopify's internal systems.

## Full report
<details><summary>Expand</summary>

Hi all,

I had lots of tests for bug bounty in my test store "trstore-3.myshopify.com" (created about 4 years ago) and then one of your developers noticed that a stored cross-site scripting payload in my staff name fired in another your internal panel. 

I have attached the email sent to me by your collegue  and I'd like to get a award and I am very happy.

Thanks alot.

## Impact

Stored XSS

</details>

---
*Analysed by Claude on 2026-05-12*
