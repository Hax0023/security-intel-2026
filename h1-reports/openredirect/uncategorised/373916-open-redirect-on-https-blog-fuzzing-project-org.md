# Open Redirect on https://blog.fuzzing-project.org/exit.php

## Metadata
- **Source:** HackerOne
- **Report:** 373916 | https://hackerone.com/reports/373916
- **Submitted:** 2018-06-29
- **Reporter:** juliocesar
- **Program:** The Fuzzing Project
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Unvalidated Redirect, Open Redirect, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
The exit.php endpoint on blog.fuzzing-project.org contains an unvalidated redirect vulnerability in the 'url' parameter, allowing attackers to redirect users to arbitrary external websites. The application fails to validate or sanitize user-supplied redirect destinations, enabling phishing attacks and credential harvesting.

## Attack scenario
1. Attacker discovers the exit.php endpoint accepts a base64-encoded URL parameter
2. Attacker crafts a malicious link: blog.fuzzing-project.org/exit.php?url=[base64(attacker-phishing-site)]
3. Attacker distributes the link via email or social engineering, disguised as legitimate content from the Fuzzing Project
4. Victim clicks the link, trusting the blog.fuzzing-project.org domain prefix
5. Application silently redirects victim to attacker-controlled phishing site without validation
6. Attacker harvests credentials or sensitive information from the fake login page

## Root cause
The exit.php script directly uses the 'url' parameter value for HTTP redirection without implementing validation checks, whitelist enforcement, or domain verification. No server-side redirect mapping or destination sanitization was implemented.

## Attacker mindset
Leverage trusted domain reputation to bypass user skepticism. Use base64 encoding for obfuscation to evade basic URL filters. Create convincing phishing pages that mimic legitimate services to harvest credentials or deploy malware.

## Defensive takeaways
- Implement server-side URL mapping: store redirect destinations as numeric IDs and map them to safe URLs, never accepting user-supplied URLs directly
- Enforce strict whitelist validation: maintain a list of approved redirect domains and reject all others
- Validate URL scheme and domain: reject URLs with protocol specifiers or ensure they match expected internal domains only
- Add user confirmation: display a warning page showing the destination URL before redirecting external users
- Use HTTP security headers: implement X-Frame-Options and CSP to prevent redirect exploitation in attack chains
- Log and monitor: track all redirect attempts to detect abuse patterns
- Consider rel=noopener: if generating links to external sites, use rel=noopener and rel=noreferrer attributes

## Variant hunting
Search for other endpoints with redirect functionality: callback.php, return.php, redirect.php, forward.php, login_redirect.php
Test variations of parameter names: redirect, target, destination, url, goto, next, return_url, back
Test alternative URL encodings: double URL encoding, HTML entity encoding, mixed case bypass
Check for partial URL validation bypasses: using //example.com, javascript:, data:, vbscript: protocols
Test relative path traversal: ../../../, ./, for intra-domain redirect bypasses
Look for endpoint aliases or legacy endpoints serving similar functionality
Test POST method variants if only GET was checked

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1187 - Forced Authentication
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information

## Notes
The PoC uses base64 encoding (aHR0cHM6Ly93d3cuaW5mb3NlYy5jb20uYnI= decodes to https://www.infosec.com.br), suggesting the application may have lightweight obfuscation. This is a common OWASP Top 10 issue (A05:2021 Security Misconfiguration). The vulnerability is straightforward but highly effective for credential theft and malware distribution due to the trusted domain origin.

## Full report
<details><summary>Expand</summary>

**Summary:**

There is an Open Redirect on  https://blog.fuzzing-project.org/exit.php?url= due to the application not checking the value passed by the user to the "url" parameter.

**Description:**

Unchecked redirects occur when an application redirects to a destination controlled by attackers. This often occurs in functionality returning users to a previous page, e.g. after authenticating.

An attacker can control the value of the "url" parameter and make it redirect to a malicious endpoint.

https://blog.fuzzing-project.org/exit.php?url=

## Steps To Reproduce:

Here is a proof of concept to demonstrate how an open redirect occurs. Please note that this particular example is not a vulnerability and just here for demonstration purposes.

PoC: https://blog.fuzzing-project.org/exit.php?url=aHR0cHM6Ly93d3cuaW5mb3NlYy5jb20uYnI=

The URL looks like it should go to https://blog.fuzzing-project.org, but you are redirected to https://www.infosec.com.br

## Supporting Material/References:

Mitigation:

When possible, do not allow user input to directly control redirect destinations; rather, generate them on the server side (e.g. via ID -> URL mapping). When this is not an option, a strict whitelist is highly recommended. Finally, a last-ditch mitigation can be performed by removing protocol specifiers from user input prior to redirection. This last method will not fix intra-site redirect exploits, but can prevent redirects to an attacker-controlled website.

Reference:

https://www.owasp.org/index.php/Unvalidated_Redirects_and_Forwards_Cheat_Sheet

## Impact

Attackers may be able to use this to execute believable phishing attacks, bypass authentication, or (in rare circumstances) violate CSRF mitigations.

</details>

---
*Analysed by Claude on 2026-05-24*
