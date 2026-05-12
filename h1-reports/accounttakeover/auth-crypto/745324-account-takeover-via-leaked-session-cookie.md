# Account takeover via leaked session cookie

## Metadata
- **Source:** HackerOne
- **Report:** 745324 | https://hackerone.com/reports/745324
- **Submitted:** 2019-11-24
- **Reporter:** haxta4ok00
- **Program:** HackerOne
- **Bounty:** Unknown
- **Severity:** critical
- **Vuln:** Session Management, Credential Exposure, Broken Authentication, Information Disclosure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A researcher disclosed that HackerOne staff session cookies were leaked in a previous report, allowing unauthorized account takeover and access to sensitive security reports and program data. The attacker was able to impersonate staff members and read confidential information across multiple programs.

## Attack scenario
1. Attacker identifies session cookie exposed in a previous vulnerability report
2. Attacker extracts the valid session cookie from the disclosed report
3. Attacker injects the session cookie into their own browser/requests
4. Attacker bypasses authentication by leveraging the valid session token
5. Attacker gains access to HackerOne staff dashboard and private reports
6. Attacker reads sensitive security information across multiple programs

## Root cause
Session cookies were inadvertently included in a previous public report disclosure, likely containing plaintext or insufficiently redacted sensitive credentials. The platform failed to properly sanitize or redact session tokens before publishing reports.

## Attacker mindset
Opportunistic researcher discovering leaked credentials in public disclosures; exploiting poor secret management and lack of automated redaction in report publishing workflow.

## Defensive takeaways
- Implement automated redaction of sensitive tokens (session cookies, API keys, JWTs) in all user-generated content before publication
- Rotate all session tokens immediately upon detection of exposure
- Implement short session expiration times and consider binding sessions to IP addresses or device fingerprints
- Add comprehensive logging and alerting for account access anomalies
- Establish clear guidelines for researchers on what should not be included in reports
- Implement secret scanning tools to detect credentials in reports before publishing
- Use secure session storage with httpOnly and Secure flags
- Conduct regular audits of previously published reports for leaked credentials

## Variant hunting
Search for API keys or tokens in historical HackerOne report archives
Check if other platforms have similar report publication workflows without redaction
Identify if session cookies from other reports are still valid
Test for other sensitive data leaks in public disclosures (tokens, keys, passwords)
Review version control systems and collaborative platforms for credential exposure

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1110 - Brute Force
- T1556 - Modify Authentication Process
- T1550 - Use Alternate Authentication Material
- T1550.001 - Use Alternate Authentication Material: Application Access Token
- T1528 - Steal Application Access Token
- T1539 - Steal Web Session Cookie

## Notes
The report content appears intentionally obfuscated or poorly formatted, suggesting either a language barrier or deliberate anonymization. The actual severity and impact details are redacted. This highlights the risk of sensitive information disclosure in public bug bounty platforms and the critical need for automated secret detection before publication.

## Full report
<details><summary>Expand</summary>

**Summary:**
You are disclose for me you session
**Description:**
you are gevi me your session on last report
I am can use your session(sorry)
███
████████
█████████

## Impact

HackerOneStaff Access, i can read all reports @security and more program

</details>

---
*Analysed by Claude on 2026-05-11*
