# Clickjacking: X-Frame-Options Header Missing

## Metadata
- **Source:** HackerOne
- **Report:** 129650 | https://hackerone.com/reports/129650
- **Submitted:** 2016-04-10
- **Reporter:** white_hat_0003
- **Program:** Unknown (not specified in report)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application fails to implement the X-Frame-Options HTTP response header on critical pages including sign-in, sign-up, and the main domain, allowing the site to be framed by malicious third-party websites. An attacker can overlay these pages with transparent iframes to trick users into performing unintended actions such as changing account settings or authorizing transactions.

## Attack scenario
1. Attacker creates a malicious webpage with an invisible iframe embedding the target site's sign-in page
2. Victim visits the attacker's webpage which displays enticing content (e.g., 'Click here to win a prize')
3. User clicks on the malicious content, which actually activates a button on the hidden sign-in page
4. Victim unknowingly authenticates or performs sensitive actions on the framed application
5. Attacker gains unauthorized access to victim's account or performs actions on their behalf
6. Session hijacking or unauthorized account modifications occur without victim awareness

## Root cause
The development team failed to configure the X-Frame-Options HTTP response header (or CSP frame-ancestors directive) on authentication and main domain endpoints, allowing unrestricted embedding in foreign contexts.

## Attacker mindset
An attacker targets high-value pages (authentication, account management) where user clicks have security implications. By exploiting missing framing protections, they can silently hijack user sessions or coerce actions without requiring the victim to notice the attack.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN on all pages, especially authentication endpoints
- Alternatively, use Content-Security-Policy header with frame-ancestors directive for more granular control
- Apply security headers consistently across all domains and subdomains via middleware or reverse proxy
- Conduct security header audit to identify missing protections on all user-facing pages
- Include security headers in SDLC requirements and automated security scanning
- Test framing restrictions as part of regular security testing procedures

## Variant hunting
Check for missing X-Frame-Options on password reset pages
Audit payment/transaction confirmation pages for clickjacking protection
Test administrative dashboards and account settings pages for frame-ancestors restrictions
Verify security header implementation on API endpoints that handle sensitive operations
Search for other missing headers (CSP, X-Content-Type-Options, HSTS) in same report scope

## MITRE ATT&CK
- T1190
- T1566

## Notes
Report references a duplicate submission (report #7492), suggesting clickjacking was a known or recurring issue in the program. The lack of specific bounty amount and program details limits context. PoC attachment likely demonstrated successful framing. This is a common finding in security assessments and indicates security header implementation gaps in the development pipeline.

## Full report
<details><summary>Expand</summary>

same as this report https://hackerone.com/reports/7492
vulnerable :- sign in ,sign up ,and main domain 
poc attached

</details>

---
*Analysed by Claude on 2026-05-24*
