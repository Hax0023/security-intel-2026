# Reflected Cross-Site Scripting (XSS) in Acronis Czech Roadshow 2020 Form

## Metadata
- **Source:** HackerOne
- **Report:** 1081747 | https://hackerone.com/reports/1081747
- **Submitted:** 2021-01-19
- **Reporter:** darkdream
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (Reflected), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Acronis Czech roadshow 2020 form where user-supplied JavaScript code is executed directly in the victim's browser without proper sanitization or encoding. An attacker can inject malicious scripts through form fields to steal session tokens, credentials, or perform actions on behalf of the victim.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload: https://www.acronis.cz/dotaznik/roadshow-2020/?field=><script>alert(1);</script>
2. Attacker sends the URL via phishing email or social engineering to target users
3. Victim clicks the link and accesses the form page with injected JavaScript in the query parameters
4. Form renders without proper encoding, executing the attacker's JavaScript in victim's browser context
5. Attacker's script steals session cookies, CSRF tokens, or redirects to credential harvesting page
6. Victim is unaware while attacker gains unauthorized access to their account or sensitive data

## Root cause
The application fails to properly validate and encode user input before rendering it in HTML responses. Form field values are reflected directly into the DOM without HTML entity encoding or Content Security Policy protections.

## Attacker mindset
An attacker would identify this form as a low-hanging fruit for credential theft, session hijacking, or malware distribution campaigns. The vulnerability is trivial to exploit and can be chained with social engineering for maximum impact.

## Defensive takeaways
- Implement strict input validation with whitelist approach for all form fields
- Apply HTML entity encoding to all user-controlled data before rendering in HTML context
- Deploy Content Security Policy (CSP) headers to restrict inline script execution
- Use security-focused templating engines that auto-escape by default
- Implement output encoding libraries appropriate to the rendering context (HTML, JavaScript, URL, CSS)
- Enable httpOnly and Secure flags on session cookies to prevent XSS-based theft
- Conduct regular security testing including SAST/DAST and manual code reviews
- Implement Web Application Firewall (WAF) rules to detect common XSS patterns

## Variant hunting
Search for similar patterns in other Acronis Czech regional sites (/dotaznik/ paths), test all form inputs across the application, check for DOM-based XSS in JavaScript event handlers, investigate stored XSS if form data is persisted, test for mutation-based XSS with alternative encoding bypasses

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1056

## Notes
The vulnerability write-up is incomplete with placeholder sections. The impact statement acknowledges script execution risk but lacks specific damage scenarios. No evidence of security patches or response timeline provided in the report excerpt.

## Full report
<details><summary>Expand</summary>

You can post javascript code in form fields  
## Summary
[add summary of the vulnerability]

## Steps To Reproduce
[add details for how we can reproduce the issue]
steps :
1-go to vulnerability link : https://www.acronis.cz/dotaznik/roadshow-2020/
2- enter this javascript   code    "><script>alert(1);</script>     in  form field 
  1. [add step]
  1. [add step]
  1. [add step]

## Recommendations
[add details for how to fix or at least mitigate the issue]

## Impact

If an attacker can control a script that is executed in the victim's browser

</details>

---
*Analysed by Claude on 2026-05-12*
