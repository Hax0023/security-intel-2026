# Open Redirect Vulnerability in WebSummit Form Handlers

## Metadata
- **Source:** HackerOne
- **Report:** 172746 | https://hackerone.com/reports/172746
- **Submitted:** 2016-09-28
- **Reporter:** j0_1_0_1_0_0_0_0
- **Program:** WebSummit
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirects and Forwards
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple WebSummit-related domains contain open redirect vulnerabilities in their form gate endpoints. An attacker can craft malicious referrer parameters to redirect users to arbitrary external URLs after form submission. The vulnerability exists across at least three separate subdomains (forms.moneyconf.com, forms.collisionconf.com, forms.websummit.net).

## Attack scenario
1. Attacker identifies the /gates endpoint accepts a 'referrer' parameter in POST requests
2. Attacker crafts a malicious URL with referrer parameter pointing to attacker-controlled domain (e.g., http://openbugbounty.org)
3. Attacker tricks users into submitting the form (via phishing email, social engineering, or malicious link)
4. User submits form data with the malicious referrer parameter
5. Server processes the form and redirects user to the URL specified in the referrer parameter
6. User is redirected to attacker's site, believing it's part of legitimate WebSummit flow

## Root cause
The application accepts user-supplied referrer parameter without proper validation or whitelisting. The referrer value is directly used in HTTP redirects without checking if it points to an authorized domain.

## Attacker mindset
Attacker could leverage this for credential harvesting, malware distribution, or phishing campaigns by redirecting users expecting legitimate WebSummit/MoneyConf/Collision sites. The multi-domain nature suggests scalable attack potential.

## Defensive takeaways
- Implement strict whitelist validation for all redirect destinations
- Use relative URLs or only allow redirects to same-origin destinations
- Sanitize and validate the referrer parameter against a predefined list of acceptable domains
- Implement Content Security Policy (CSP) to restrict redirects
- Log and monitor redirect attempts to detect abuse patterns
- Conduct security audit of all form handlers across all subdomains for similar issues

## Variant hunting
Check other form endpoints on affected domains for similar redirect issues
Audit all URL parameters that could influence navigation (return, callback, redirect, next, etc.)
Test POST and GET methods separately for bypass techniques
Examine other WebSummit event subdomains for the same vulnerability pattern
Look for double-encoding bypasses (e.g., %252F instead of %2F)

## MITRE ATT&CK
- T1598.003
- T1566.002

## Notes
This is a classic open redirect vulnerability with minimal complexity to exploit. The fact that it exists across multiple related domains suggests either shared infrastructure or common vulnerable code. The report is sparse on remediation details and bounty information. No indication of authentication bypass or chaining with other vulnerabilities, limiting severity to medium rather than high.

## Full report
<details><summary>Expand</summary>

Same Open Redirect issue at 3 websites:

-https://forms.moneyconf.com/gates
Post data: phone_number=922+222+222&full_number=%2B351922222222aaaaaaaaaaaa&referrer=http://openbugbounty.org&slug=+moneyconf_17_exhibitor_17

-https://forms.collisionconf.com/gates
Post data: phone_number=914+444+444&full_number=%2B35191444444aaaaaaaa4&referrer=http://openbugbounty.org&slug=collision_startups_alpha


-https://forms.websummit.net/gates
Post data: phone_number=916+666+765&full_number=%2B351916666765aaaaaaa&referrer=http://openbugbounty.org&slug=ws16_alpha_14sept

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
