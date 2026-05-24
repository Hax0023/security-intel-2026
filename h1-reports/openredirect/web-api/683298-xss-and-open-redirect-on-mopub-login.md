# XSS and Open Redirect on MoPub Login Page

## Metadata
- **Source:** HackerOne
- **Report:** 683298 | https://hackerone.com/reports/683298
- **Submitted:** 2019-08-27
- **Reporter:** jackb898
- **Program:** MoPub
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Open Redirect, Cross-Site Scripting (XSS), Unvalidated Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
The MoPub login page contains an unvalidated 'next' parameter that allows attackers to redirect users to arbitrary domains or execute JavaScript code via javascript: URIs. An attacker could leverage this for phishing attacks, session hijacking, or credential theft by crafting a malicious login URL.

## Attack scenario
1. Attacker identifies the vulnerable 'next' parameter on the MoPub login page
2. Attacker crafts a malicious URL with javascript:alert() or external redirect (e.g., https://app.mopub.com/login?next=https://phishing-site.com)
3. Attacker sends the crafted URL to a MoPub user via email, social media, or other channels
4. Victim clicks the link, which appears legitimate as it uses the official MoPub domain
5. Upon login, victim is redirected to attacker's phishing site or malicious JavaScript executes in the context of MoPub
6. Attacker harvests credentials, steals session cookies, or performs account takeover

## Root cause
The application fails to validate or sanitize the 'next' redirect parameter before using it in post-login redirection. The parameter accepts any URL scheme including javascript: without whitelist validation or URL parsing safeguards.

## Attacker mindset
An attacker recognizes that post-login redirects are trusted by users and can be exploited for credential harvesting. By combining open redirect with XSS (javascript: URIs), they can create convincing phishing campaigns or steal authentication tokens without requiring complex social engineering.

## Defensive takeaways
- Implement strict whitelist validation for redirect parameters - only allow internal URLs or explicitly approved domains
- Use URL parsing to validate scheme (http/https only) and prevent javascript:, data:, and other dangerous protocols
- Store redirect URLs server-side mapped to tokens rather than accepting user input
- Implement same-site cookie flags and CSP headers to limit XSS impact
- URL-encode any user-controlled redirect URLs in responses
- Log and alert on suspicious redirect attempts for security monitoring
- Use security linters to detect open redirect vulnerabilities during code review

## Variant hunting
Similar 'next', 'redirect', 'return', 'goto', 'url', 'target' parameters on other authentication endpoints; check OAuth/SSO flows; investigate mobile app deep linking; test URL schemes (ftp://, file://, custom protocols); look for redirect validation bypasses using //double-slash, \backslash, or protocol-relative URLs (//attacker.com)

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1056.004
- T1539

## Notes
This is a classic unvalidated redirect combined with XSS vector. The fact that javascript: URIs are accepted is particularly severe as it bypasses the traditional assumption that open redirects only affect external sites. URL encoding can be used to obfuscate the malicious intent, making detection harder for users. The report demonstrates good security instinct by recognizing the dual vulnerability and its compounding impact on attack scenarios.

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
*Analysed by Claude on 2026-05-24*
