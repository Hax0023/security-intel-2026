# Reflected Cross-Site Scripting (XSS) via ReturnUrl Parameter on Starbucks Sign-In

## Metadata
- **Source:** HackerOne
- **Report:** 438240 | https://hackerone.com/reports/438240
- **Submitted:** 2018-11-09
- **Reporter:** cujanovic
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the ReturnUrl parameter of Starbucks' sign-in page, allowing attackers to execute arbitrary JavaScript in a victim's browser after authentication. The vulnerability affects multiple Starbucks domains globally. An attacker can craft a malicious URL using encoded JavaScript protocol handlers and newline characters to bypass basic filters.

## Attack scenario
1. Attacker crafts a malicious sign-in URL with JavaScript code embedded in the ReturnUrl parameter using encoding tricks (e.g., %19Jav%09asc%09ript%3a with newlines)
2. Attacker sends the crafted URL to a victim via phishing email, social media, or other social engineering techniques
3. Victim clicks the link and is taken to the legitimate Starbucks sign-in page
4. Victim enters their credentials and authenticates successfully
5. Upon successful authentication, the browser redirects to the ReturnUrl parameter containing the injected JavaScript
6. The JavaScript executes in the victim's browser with their authenticated session, enabling account compromise, credential theft, or fraudulent transactions

## Root cause
The application fails to properly validate and sanitize the ReturnUrl parameter before using it in a redirect. The application does not adequately check for dangerous protocol handlers (javascript:, data:, etc.) and does not escape or encode the output. The attacker bypassed simple filters using URL encoding, tab characters (%09), and newline characters (%0A).

## Attacker mindset
The attacker discovered this vulnerability while testing for open redirect vulnerabilities, demonstrating opportunistic security research. The goal is to execute arbitrary code in authenticated user sessions to potentially steal sensitive information, manipulate account settings, or perform unauthorized transactions on Starbucks accounts.

## Defensive takeaways
- Implement strict whitelist validation for redirect URLs - only allow redirects to trusted domains within the same origin or a pre-approved list
- Use URL parsing libraries to validate the protocol and domain before redirecting, rejecting any non-http/https protocols
- Properly encode all user-controlled input before rendering in HTML context using context-specific encoding (HTML entity encoding for URL context)
- Implement Content Security Policy (CSP) headers to prevent inline JavaScript execution
- Use client-side redirect validation in addition to server-side checks
- Consider using a redirect confirmation page that shows users where they're being redirected
- Regularly test for open redirect and XSS vulnerabilities in authentication flows
- Apply defense-in-depth: validate, encode, and use security headers simultaneously

## Variant hunting
Test other redirect parameters: ReturnUrl, redirectUrl, redirect, returnUrl, next, url, target, destination
Try different encoding schemes: double URL encoding, Unicode encoding, HTML entity encoding, mixed encoding
Test protocol handlers: javascript:, data:, vbscript:, file:, and variations with whitespace/newlines
Test on password reset, email verification, and other post-authentication redirects
Look for similar patterns in other domains listed (starbucks.ca, .br, .co.uk, .de, .fr)
Test for stored XSS if any user-controllable data flows to the ReturnUrl parameter
Check for CORS misconfigurations that might enable cross-origin redirect exploitation

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1056

## Notes
This is a post-authentication XSS, making it particularly dangerous as it executes in the context of an authenticated user. The attacker used multiple encoding and obfuscation techniques (tab characters, newlines, URL encoding) to bypass what appears to be a basic filter. The vulnerability affects multiple international Starbucks domains, indicating a systemic issue with the authentication framework. The researcher appropriately noted this was discovered during open redirect testing, suggesting the two vulnerabilities may be related or stem from the same root cause of insufficient redirect parameter validation.

## Full report
<details><summary>Expand</summary>

**Summary:** Reflected Cross site Scripting (XSS) on https://www.starbucks.com/account/signin?ReturnUrl

**Description:** The attacker can execute javascript on  the victims account just after the authentication process.

**Platform(s) Affected:**
www.starbucks.com
www.starbucks.ca
www.starbucks.com.br
www.starbucks.co.uk
www.starbucks.de
www.starbucks.fr

## Steps To Reproduce:

1. Open the url: https://www.starbucks.com/account/signin?ReturnUrl=%19Jav%09asc%09ript%3ahttps%20%3a%2f%2fwww%2estarbucks%2ecom%2f%250Aalert%2528document.domain%2529
2. Login
3. The JS will execute on users(victims) account.

## Supporting Material/References:
Screenshot:
{F373210}

## How can the system be exploited with this bug?
The attacker can execute JS code.
  

## How did you come across this bug ?
I was testing for open redirect vulnerability.


## Recommendations for fix
Content based escaping on the users input, in this case the redirect parameter.

## Impact

The attacker can execute JS code.

</details>

---
*Analysed by Claude on 2026-05-12*
