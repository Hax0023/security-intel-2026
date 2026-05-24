# Open Redirect Vulnerability on Smule

## Metadata
- **Source:** HackerOne
- **Report:** 440484 | https://hackerone.com/reports/440484
- **Submitted:** 2018-11-14
- **Reporter:** assassin_marcos
- **Program:** Smule
- **Bounty:** unknown
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists where attackers can manipulate the redirection_url parameter to redirect authenticated users to arbitrary external websites. This can be exploited to direct users to phishing pages or malicious sites to harvest credentials.

## Attack scenario
1. Attacker identifies the redirection_url parameter on Smule login/authorization page
2. Attacker crafts a malicious URL using protocol-relative path (////) to bypass validation checks
3. Attacker sends phishing email with crafted URL to Smule users
4. Victim clicks link and authenticates on legitimate Smule domain
5. Application redirects victim to attacker-controlled phishing site instead of expected destination
6. Victim unknowingly enters credentials on fake login page, compromising account security

## Root cause
Insufficient validation of the redirection_url parameter allowing protocol-relative URLs and path traversal notation (////) to bypass whitelist/validation logic, enabling redirect to any external domain

## Attacker mindset
An attacker leverages the trust users place in Smule's domain to disguise phishing attacks. By redirecting after authentication, the attacker captures credentials while the victim believes they're on a legitimate service.

## Defensive takeaways
- Implement strict whitelist validation for redirect URLs, rejecting protocol-relative paths and external domains
- Use URL parsing libraries to normalize and validate URLs before redirecting
- Implement server-side validation that only allows relative URLs or explicitly whitelisted domains
- Add security warnings or confirmation dialogs when redirecting to external domains
- Use URL parameter encoding standards and reject encoded bypass attempts
- Log and monitor redirect parameters for suspicious patterns
- Educate users about verifying URLs in browser address bar before entering credentials

## Variant hunting
Test redirect_url, return_url, next, target, destination, callback, redirect parameters on login flows
Try double encoding: %252f%252f
Test javascript: and data: protocol handlers
Try backslash variants: \\\\domain.com
Test mixed case: ////DOMAIN.COM
Attempt null byte injection: ////domain.com%00.smule.com
Test on logout, password reset, and OAuth callback endpoints

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1598.002 - Phishing: Spearphishing Link with Credential Harvesting
- T1566.002 - Phishing: Phishing - Spearphishing Link

## Notes
Report is incomplete with redacted details and minimal supporting evidence (no screenshots, POC). The validation bypass using protocol-relative paths (////) is a known technique. Severity is medium as it requires user interaction and relies on social engineering effectiveness. HackerOne template was not properly completed.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

**Summary:** Open Redirect at ███

**Your Smule Username:** [If applicable]

**Description:** an attacker can redirect victim to malicious site/ phishing site

## Steps To Reproduce:

(Add details for how we can reproduce the issue)

  1.Visit 1: ████████?redirection_url=////█████████

Just Login And Watch  :)

Boom User Redirected :)



## Impact:  Redirect user to malicious site or phishing site to steal credentials

## Supporting Material/References:

  * List any additional material (e.g. screenshots, logs, etc.)

## Impact

Can get user login credential after redirecting user to malicious site/ his phishing site

</details>

---
*Analysed by Claude on 2026-05-24*
