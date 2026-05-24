# Unauthorized Access to Premium Templates via Business Logic Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1166993 | https://hackerone.com/reports/1166993
- **Submitted:** 2021-04-16
- **Reporter:** 20kilograma
- **Program:** Stripo
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Business Logic Flaw, Authorization Bypass, Insufficient Access Control
- **CVEs:** None
- **Category:** memory-binary

## Summary
A free user can access and use premium email templates by selecting a template from the public templates page, clicking 'use in editor', and then signing in, bypassing the intended paywall mechanism. This allows unauthorized access to paid features and causes direct revenue loss for the business.

## Attack scenario
1. Attacker navigates to the public templates page (https://stripo.email/templates/) without being logged in or as a free user
2. Attacker identifies and selects a premium template marked as paid-only
3. Attacker clicks the 'use in editor' button on the premium template
4. The application loads the template editor without validating subscription status
5. Attacker signs in or creates a free account during or after the editing session
6. The premium template is now saved and accessible in the attacker's free account, effectively granting unauthorized access to paid content

## Root cause
The application performs authorization checks for template access only after user signup, rather than validating license/subscription status before allowing template loading in the editor. The 'use in editor' functionality is not protected by proper access control checks.

## Attacker mindset
An opportunistic user seeking to gain premium features without payment, recognizing that the application allows template interaction before enforcing subscription validation.

## Defensive takeaways
- Implement authorization checks on the client-side template selection and before rendering any premium template
- Validate subscription status prior to allowing 'use in editor' action for any premium content
- Implement license verification at multiple layers: template API endpoints, editor initialization, and save operations
- Require authentication before exposing premium template functionality
- Audit template access logs to identify exploitation patterns
- Implement rate limiting on template access attempts per IP/session

## Variant hunting
Check if other premium features (images, plugins, integrations) have similar pre-authentication bypass vectors
Test if premium templates can be accessed via direct API calls without authentication
Verify if exporting/downloading premium template content is also unprotected
Check whether subscription downgrade scenarios properly revoke access to previously loaded premium content
Test if template sharing mechanisms bypass subscription validation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts (unauthorized use of free account to access premium features)

## Notes
This is a straightforward business logic vulnerability with clear revenue impact. The fix should involve moving authorization checks earlier in the workflow. The report lacks detail (no attachments provided in summary) but the vulnerability is easily reproducible and has significant business implications for a SaaS email template platform.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello, I found security vulnerability in your web application, another business logic.

## Steps To Reproduce
  1. Go to https://stripo.email/templates/?utm_source=viewstripo&utm_medium=referral
  2. Choose any premium template and click ```use in editor```
  3. Then sign in to save and it is in your templates

## Supporting Material/References:
Down there is video showing everything

  * [attachment / reference]

## Impact

Lose of business

</details>

---
*Analysed by Claude on 2026-05-24*
