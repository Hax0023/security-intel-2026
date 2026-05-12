# Reflected XSS in nin.mtn.ng Success Page - NIN Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2039384 | https://hackerone.com/reports/2039384
- **Submitted:** 2023-06-26
- **Reporter:** hazemhussien99
- **Program:** MTN Nigeria
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Missing Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the 'nin' parameter of the nin.mtn.ng/nin/success endpoint, allowing unauthenticated attackers to inject arbitrary JavaScript code. The vulnerability persists despite a previous report (1737682) claiming to have resolved the issue. Attackers can craft malicious URLs to execute arbitrary JavaScript in victims' browsers.

## Attack scenario
1. Attacker identifies the nin parameter in nin.mtn.ng/nin/success is vulnerable to XSS injection
2. Attacker crafts a malicious URL: https://nin.mtn.ng/nin/success?message=lol&nin=<script>alert(1)</script>
3. Attacker sends the URL to victims via phishing email, social engineering, or social media
4. Victim clicks the link while authenticated to MTN services
5. Malicious JavaScript executes in victim's browser with their session context
6. Attacker steals session cookies, credentials, performs actions on victim's account, or redirects to credential harvesting page

## Root cause
The application fails to properly encode user input from the 'nin' URL parameter before rendering it in the HTML response. Input validation and/or output encoding mechanisms are either absent or insufficient to prevent script injection.

## Attacker mindset
An attacker would target this endpoint because: (1) it's on a high-value financial/government ID verification domain, (2) users are likely logged in when accessing it, (3) the parameter name 'nin' suggests it handles sensitive National Identification Numbers making victims attractive targets, (4) the previous incomplete fix demonstrates inadequate security review processes that can be exploited again.

## Defensive takeaways
- Implement strict output encoding on all user-controlled parameters using context-aware encoding (HTML entity encoding for HTML context)
- Apply input validation with whitelisting of expected NIN format (numeric, specific length)
- Implement Content Security Policy (CSP) headers to restrict script execution
- Use templating engines with auto-escaping enabled by default
- Conduct thorough security testing including fuzzing with XSS payloads before marking issues as resolved
- Implement automated security scanning in CI/CD pipeline to catch regressions
- Establish regression testing for previously fixed vulnerabilities
- Sanitize all reflection points where user input appears in HTML responses

## Variant hunting
Test 'message' parameter for XSS - likely similarly vulnerable
Check other endpoints on nin.mtn.ng domain for same pattern
Test HTTP parameter pollution with multiple 'nin' parameters
Attempt DOM-based XSS through JavaScript evaluation of URL parameters
Test for stored XSS if NIN values are persisted in user profiles
Check for double-encoding bypasses (e.g., %253Cscript%253E)
Test mutation XSS techniques with case variations and unicode encoding
Examine if error messages reflect parameters without encoding

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1539
- T1185

## Notes
This is a re-report of vulnerability #1737682 which was allegedly fixed but remains exploitable. This indicates: (1) inadequate remediation verification, (2) possible incomplete patch deployment, (3) weak security controls for ensuring fixes persist through code updates. The reporter explicitly documented this as a re-occurrence, suggesting process failures in the MTN security workflow. The use of government ID verification (NIN) data makes this particularly sensitive for Indian/Nigerian users.

## Full report
<details><summary>Expand</summary>

###Summary:
Hello team,
Found a reflected XSS on one your domains i believe https://nin.mtn.ng/nin/success?message=msg&nin= as the nin parameter is vulnerable.
Please check the following PoC:
Run the following command from a terminal:
curl -ski "https://nin.mtn.ng/nin/success?message=lol&nin=<script>alert(1)</script>"  | grep "alert"
{F2446627}

I reported this before in report #1737682 but it was closed as resolved while still vulnerable.

## Impact

Attacker could execute js in the victim's browser.

</details>

---
*Analysed by Claude on 2026-05-12*
