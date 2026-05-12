# XSS and Open Redirect on MoPub Login Page

## Metadata
- **Source:** HackerOne
- **Report:** 683298 | https://hackerone.com/reports/683298
- **Submitted:** 2019-08-27
- **Reporter:** jackb898
- **Program:** MoPub
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Open Redirect, Cross-Site Scripting (XSS), Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The MoPub login page at https://app.mopub.com/login contains an unvalidated 'next' URL parameter that allows open redirects to arbitrary domains and execution of JavaScript URIs. An attacker can craft malicious login URLs to redirect authenticated users to phishing sites or execute arbitrary JavaScript in the user's browser.

## Attack scenario
1. Attacker identifies the vulnerable 'next' parameter in MoPub login URL
2. Attacker crafts a malicious URL with next=javascript:alert('XSS') or next=https://attacker-phishing.com
3. Attacker distributes the malicious login URL via email, social media, or other channels to MoPub users
4. Victim clicks the link and logs into their legitimate MoPub account
5. Upon successful authentication, victim is redirected to attacker's phishing site or JavaScript payload executes in browser context
6. Attacker harvests credentials, session tokens, or performs account takeover using stolen session cookies

## Root cause
The 'next' parameter is not properly validated or sanitized before being used in post-login redirects. The application fails to implement a whitelist of allowed redirect domains or validate that the parameter contains only safe HTTP/HTTPS URLs.

## Attacker mindset
An attacker would recognize this as a high-impact vulnerability combining open redirect and XSS capabilities. They could leverage it for credential harvesting, session hijacking, malware distribution, or account compromise at scale by targeting MoPub users with convincing phishing attacks.

## Defensive takeaways
- Implement strict whitelist validation for redirect URLs - only allow redirects to explicitly approved domains
- Reject or sanitize javascript: and data: URI schemes completely
- Use URL parsing libraries to validate the protocol (http/https only) and domain components
- Consider removing the redirect parameter entirely if not essential, or use an internal redirect mapping table
- Implement Content Security Policy (CSP) headers to prevent inline JavaScript execution
- Log and monitor unusual redirect attempts for security analysis
- Perform security code review of all authentication and redirect logic

## Variant hunting
Look for similar unvalidated redirect parameters in: password reset flows, OAuth callback handlers, logout redirect URLs, account recovery flows, and any other post-authentication redirects. Check for similar issues in other MoPub properties and related authentication systems.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1056

## Notes
This is a classic example of chaining two vulnerabilities (open redirect + XSS) for amplified impact. The use of javascript: URIs is particularly dangerous as it bypasses typical redirect validation that only checks for http/https. The attacker could use URL encoding to obfuscate the malicious payload further, making it harder for users to detect the attack before clicking.

## Full report
<details><summary>Expand</summary>

**Summary:** I found open redirect at the MoPub login page, https://app.mopub.com/login?next=https://google.com. It also allows javascript URIs, leading to XSS.


**Description:** You can modify the "next" URL parameter to redirect to any website upon logging in on MoPub. 

## Steps To Reproduce:

1. Take this URL: https://app.mopub.com/login?next=https://google.com
2. Change "https://google.com" to whatever URL you want to redirect to.
3. Visit the URL and login
4. You will be redirected to that site

## Impact: Outlined in Impact section below

## Supporting Material/References:

Here's a proof of concept using the URL javascript:alert("proof of concept"):
{F568245}

## Impact

An attacker could use this for phishing, cookie jacking, etc. since it allows javascript URIs and therefore XSS vectors. Additionally, they could use URL encoding to hide the URL that the victim is being redirected to.

</details>

---
*Analysed by Claude on 2026-05-12*
