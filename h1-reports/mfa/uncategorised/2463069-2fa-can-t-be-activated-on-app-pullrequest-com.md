# 2FA Cannot Be Activated Due to Deprecated Google Chart API

## Metadata
- **Source:** HackerOne
- **Report:** 2463069 | https://hackerone.com/reports/2463069
- **Submitted:** 2024-04-14
- **Reporter:** iam_srpk
- **Program:** Pull Request (app.pullrequest.com)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Functionality, Dependency on Deprecated Service, Security Feature Unavailability
- **CVEs:** None
- **Category:** uncategorised

## Summary
The 2FA setup functionality on app.pullrequest.com is completely broken because it relies on Google's deprecated Chart API for QR code generation. This prevents all users from enabling two-factor authentication, eliminating a critical security control. The issue affects both existing and new users attempting to secure their accounts.

## Attack scenario
1. Attacker identifies that the target application uses deprecated Google Chart API for QR code generation
2. Attacker logs into their own account and attempts to enable 2FA
3. QR code fails to load due to API deprecation, preventing 2FA setup completion
4. Attacker realizes entire user population cannot enable 2FA protection
5. Attacker could exploit this to compromise accounts knowing 2FA is unavailable as a defensive measure
6. Attacker gains unauthorized access to sensitive user accounts without 2FA resistance

## Root cause
The application directly depends on Google's Chart API (charts.googleapis.com) for generating QR codes during 2FA enrollment. When Google deprecated this service, the integration broke without fallback or alternative implementation, leaving users unable to complete 2FA setup.

## Attacker mindset
An attacker would recognize this as a systemic security weakness affecting the entire user base. Rather than targeting individual accounts, they could exploit the absence of 2FA across all users to conduct mass account compromises, credential stuffing, or targeted attacks on high-value accounts.

## Defensive takeaways
- Implement internal or self-hosted QR code generation instead of relying on third-party APIs
- Establish monitoring for deprecated service dependencies and API sunsets
- Create fallback mechanisms for critical security features dependent on external services
- Regularly audit third-party service integrations and plan migrations proactively
- Implement graceful degradation: if QR generation fails, provide alternative 2FA setup methods (manual key entry)
- Add automated testing for 2FA enrollment workflow to detect breakage early
- Version and maintain internal copies of critical security libraries

## Variant hunting
Check for other deprecated third-party API dependencies in authentication workflows
Scan for hardcoded external service endpoints that may have been sunset
Review backup authentication methods to ensure they're also functional
Test password reset flows and other account recovery mechanisms for similar issues
Examine email verification and other security-related features for external API dependencies
Look for other Google services (reCAPTCHA, Fonts, Maps) that may be misconfigured or deprecated

## MITRE ATT&CK
- T1190
- T1499
- T1556

## Notes
This is a critical availability issue for security controls rather than a traditional vulnerability. The impact is severe because it affects authentication security posture at scale. The fix likely requires minimal code changes (switching to an alternative QR library like qrcode.js), making this a high-impact, low-effort remediation. The reporter's assessment is accurate—while technical in nature, the business impact of disabled 2FA is substantial.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hello Team,
Since you are using deprecated google chart API service (which doesn't work now) for generating 2fa qr code image, users cannot setup 2fa for securing account.

### Steps To Reproduce

1. Log into https://app.pullrequest.com
2. Go to "User Settings" -> "Security" -> "Two-Factor Authentication"
3. You cannot when you try enabling it

## Impact

I understand it is kinda technical bug. But I decided to report as it literally affects all existing and new users by not allowing them to secure their account.

</details>

---
*Analysed by Claude on 2026-05-24*
