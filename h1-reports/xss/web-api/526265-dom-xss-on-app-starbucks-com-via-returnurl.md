# DOM XSS on app.starbucks.com via ReturnUrl Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 526265 | https://hackerone.com/reports/526265
- **Submitted:** 2019-04-04
- **Reporter:** gamer7112
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), DOM-based XSS, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in the ReturnUrl parameter on app.starbucks.com's sign-in page, allowing attackers to execute arbitrary JavaScript by injecting JavaScript protocol handlers with whitespace/control characters. An attacker can craft a malicious URL that executes when a victim signs in, potentially leading to session hijacking and account takeover.

## Attack scenario
1. Attacker crafts a malicious URL containing ReturnUrl parameter with JavaScript protocol: https://app.starbucks.com/account/signin?ReturnUrl=%09Jav%09ascript:alert(document.domain)
2. Attacker distributes the URL via social engineering, phishing email, or malicious website to target Starbucks users
3. Victim clicks the link and visits the sign-in page (which appears legitimate)
4. Victim enters their credentials and signs in successfully
5. Upon successful authentication, the browser redirects to the ReturnUrl without proper sanitization
6. JavaScript payload executes in the victim's browser context, allowing cookie/token theft and account takeover

## Root cause
The ReturnUrl parameter is not properly validated and sanitized before being used as a redirect destination. The application fails to detect JavaScript protocol handlers, particularly when obfuscated with control characters (0x09 tab character in this case). The validation likely only checked for 'javascript:' string literally without accounting for whitespace insertion.

## Attacker mindset
An attacker would recognize that redirect/return parameters are frequently vulnerable to open redirect and XSS attacks. By using control characters like tabs (%09) to bypass basic string matching filters on 'javascript:', the attacker can evade surface-level security checks. This is a common technique for bypassing weak input validation that relies on blacklisting rather than whitelisting.

## Defensive takeaways
- Implement strict whitelist validation for redirect URLs - only allow internal paths or explicitly whitelisted domains
- Use URL parsing APIs to properly decode and validate URLs before redirecting
- Reject any URLs containing protocol handlers (javascript:, data:, vbscript:, etc.)
- Strip or reject control characters (0x00-0x1F) from all user inputs as per OWASP recommendations
- Apply Content Security Policy (CSP) headers to prevent XSS execution even if injection occurs
- Use automatic redirect validation libraries instead of manual checks
- Encode output appropriately based on context where the parameter is used
- Implement a URL validation function that handles edge cases like unicode normalization and character encoding tricks

## Variant hunting
Test other redirect/return parameters on authentication flows (ReturnTo, Redirect, Callback, Continue, etc.)
Test with alternative JavaScript protocol obfuscations: newline (%0A), carriage return (%0D), null byte (%00), various unicode whitespace
Test data:// URIs with base64-encoded JavaScript payloads
Test on other Starbucks domains and properties (starbucks.com, account.starbucks.com, etc.)
Check for similar patterns in OAuth/SSO redirect handling
Test with mixed-case 'JaVaScRiPt:' variations if case-sensitive validation is used
Test nested encoding scenarios (%25%30%39 for encoded tab)
Test with scheme-relative URLs (//attacker.com) for open redirect variants

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
This vulnerability was discovered as a retest of a previous report (#438240), suggesting the initial fix was incomplete. The use of control characters to bypass validation is a well-known evasion technique. The researcher's recommendation to block hex characters 0x00-1F is sound but incomplete - a full fix requires proper URL validation using language-native parsing functions. High severity due to pre-authentication context combined with credential harvesting potential.

## Full report
<details><summary>Expand</summary>

**Summary:** XSS Can be achieved via the ReturnUrl when signing in on app.starbucks.com

**Platform(s) Affected:** app.starbucks.com

## Steps To Reproduce:
1. Visit https://app.starbucks.com/account/signin?ReturnUrl=%09Jav%09ascript:alert(document.domain)
2. Sign in

## Supporting Material/References:
{F461364}


## How can the system be exploited with this bug? 
XSS could be used to steal the account of any victim that signs in via the url.
  

## How did you come across this bug ?
Retesting report #438240


## Recommendations for fix
Improve the checks on ReturnUrl such as not allowing hex characters 00-1F

## Impact

As with any xss, it could be used to steal the cookies of the victim to gain access to their account.

</details>

---
*Analysed by Claude on 2026-05-12*
