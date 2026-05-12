# Stored XSS in Invited Team Member via Email Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 267177 | https://hackerone.com/reports/267177
- **Submitted:** 2017-09-09
- **Reporter:** coldd
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Shopify Partners where privileged users (owners or staff with member management permissions) can inject malicious JavaScript through the email parameter when inviting team members. The payload is executed when any team member visits the invitation details page, affecting all users who access the compromised invitation.

## Attack scenario
1. Attacker with owner or staff member privileges logs into partners.shopify.com
2. Navigates to Team section and initiates invite owner workflow
3. Injects malicious payload (e.g., <svg/onload=alert(document.cookie)>) in the email field
4. Submits the invitation despite error message ('problem connecting to Shopify')
5. Malicious payload is stored in the database without proper sanitization
6. Any team member who visits the invitation details page (invitations/[id]) triggers the XSS, allowing cookie theft, session hijacking, or credential harvesting

## Root cause
The email parameter in the team invitation endpoint lacks proper output encoding when rendering the invitation details page. Input validation may reject obviously malicious emails, but stored payloads are not properly escaped in the HTML context when displayed to users viewing the invitation.

## Attacker mindset
Insider threat actor with legitimate access to partner management functions seeks to compromise other team members' sessions or steal sensitive data. The persistence of stored XSS allows for delayed attacks affecting multiple victims without requiring repeat injection.

## Defensive takeaways
- Implement strict input validation on email fields with whitelist approach for valid email formats
- Apply context-aware output encoding (HTML entity encoding) when rendering user-supplied data in HTML contexts
- Use Content Security Policy (CSP) headers to restrict inline script execution and external script loading
- Sanitize all user inputs using established libraries (e.g., OWASP ESAPI, DOMPurify) before storage
- Implement server-side validation separate from client-side controls
- Add security headers like X-XSS-Protection and X-Content-Type-Options
- Conduct security code review of all user input handling in invitation workflows
- Implement automated XSS detection in testing pipeline with payload testing

## Variant hunting
Check other invitation/membership management endpoints for similar XSS patterns
Test other user-supplied fields in team management (name, role, etc.) for stored XSS
Examine bulk invitation import features for CSV/file upload XSS vectors
Test role assignment, permission modification endpoints for stored XSS
Verify API endpoints for team management accept same malicious payloads
Check email notification content generation for reflected XSS via email parameter tampering

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1187

## Notes
The vulnerability demonstrates a privilege escalation aspect - while lower-privileged staff can create the injection, any team member (including other staff) can trigger it by viewing the page. The reported error message suggests the backend may have validation that triggers but doesn't prevent storage of the malicious payload. The fact that the XSS executes despite an error message indicates the validation/error handling is inconsistent between creation and retrieval endpoints.

## Full report
<details><summary>Expand</summary>

Hey there, while testing your program I found a stored XSS vulnerability which can placed by owners or **other staff members who have ability to manage members** and it will triggered by visiting invited team member page (e.g. https://partners.shopify.com/642416/invitations/15406).

### Reproduction Steps

1. login to partners.shopify.com.
2. navigate to *Team* (e.g. https://partners.shopify.com/642416/memberships).
3. click on *Invite owner*.
4. use `<svg/onload=alert(document.cookie)>abcdef@test.com` as email address.
5. click on *Send invite*.
6. you'll see a warning: *There was a problem connecting to Shopify*.
7. navigate to *Team* section again (e.g. https://partners.shopify.com/642416/memberships).
8. open invited user page (e.g. https://partners.shopify.com/642416/invitations/15411).

note: it does not matter who send the invitation, attack can be triggered by other team members (including owners) by opening invitation page.

also attached two file to show you that this vulnerability can placed by both owners and staff members with *manage members* access.

</details>

---
*Analysed by Claude on 2026-05-12*
