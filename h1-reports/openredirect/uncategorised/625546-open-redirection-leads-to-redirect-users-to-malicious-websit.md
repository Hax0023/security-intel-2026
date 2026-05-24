# Open Redirection via Unvalidated 'l' Parameter in Email Verification Flow

## Metadata
- **Source:** HackerOne
- **Report:** 625546 | https://hackerone.com/reports/625546
- **Submitted:** 2019-06-22
- **Reporter:** bb00x
- **Program:** Unikrn/Uniko Gold
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, Improper Input Validation, Path Traversal in Redirect Logic
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the email verification endpoint (/s/doi) where the 'l' parameter accepts arbitrary URLs with path traversal sequences, allowing attackers to redirect authenticated users to malicious websites. The vulnerability can be chained with XSS to steal user credentials or facilitate phishing attacks.

## Attack scenario
1. Attacker creates a legitimate account on unikoingold.com to obtain a valid email verification link with hash parameter
2. Attacker crafts malicious URL by modifying the 'l' parameter with payloads like '//attacker.com/' or '//whitelisted.tld@attacker.com/../'
3. Attacker sends phishing email with crafted redirect URL to target users or posts it in forums/social media
4. Victim clicks the seemingly legitimate verification link from Unikrn domain
5. Browser follows the redirect to attacker's malicious website hosting credential-stealing forms or XSS payloads
6. Attacker harvests credentials, session tokens, or executes arbitrary JavaScript in victim's browser context

## Root cause
The redirect destination parameter 'l' is not properly validated or sanitized. The application likely uses a whitelist approach but fails to correctly parse URLs with special characters (double slashes, @-signs, dot-dot-slash sequences), allowing bypass of domain validation logic. URL parsing inconsistencies between client and server enable the vulnerability.

## Attacker mindset
An attacker would recognize that email verification flows are high-trust vectors where users are likely to click links without scrutiny. By leveraging URL parsing quirks (protocol-relative URLs, userinfo field bypasses, path traversal), they can bypass simple whitelist checks. The combination with XSS amplifies impact by enabling credential theft on the attacker's domain while appearing to come from the trusted company.

## Defensive takeaways
- Implement strict whitelist validation: use URL parsing libraries (java.net.URL, urllib.parse) to extract and validate only the hostname component against an allowlist
- Prefer server-side redirects with token-based destination mapping instead of accepting user-controlled URLs
- Disable protocol-relative URLs by enforcing explicit protocol validation (https:// only)
- Remove or properly encode special URL characters (@, //, ..) before validation
- Apply Content Security Policy (CSP) with redirect-src restrictions to limit where page can redirect users
- Use security headers like X-Frame-Options and X-Content-Type-Options to prevent framing attacks
- Implement rate limiting on verification endpoints to slow brute force attempts on hash parameter
- Audit all redirect/location parameters across the application for similar vulnerabilities
- Add logging and alerts for unusual redirect destinations

## Variant hunting
Test other URL parameters in the /s/doi endpoint (h, utm_medium, utm_campaign) for similar bypass patterns
Check for open redirects in password reset, email change, and two-factor authentication flows
Examine other endpoints accepting 'redirect', 'return', 'next', 'goto', 'url', 'link' parameters with path traversal payloads
Test protocol-relative URLs (//attacker.com), data URIs (data:text/html...), javascript: URIs
Investigate if the hash parameter 'h' can be brute-forced or if it's tied to specific user accounts
Check if similar vulnerabilities exist on sibling domains (*.unikrn.com, *.unikoingold.com)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link
- T1598.004 - Phishing for Information: Spearphishing Attachment (credential harvesting post-redirect)
- T1187 - Forced Authentication (via redirect to credential-stealing page)

## Notes
The reporter effectively demonstrated the vulnerability by chaining it with XSS and using Burp Suite to identify the exploitable parameter. The PoC requires authentication to trigger, reducing severity but not eliminating risk for active users. The whitelist bypass technique using double-slash and @-sign suggests the application was using string prefix matching rather than proper URL parsing. The vulnerability affects the critical email verification flow, meaning new and account recovery scenarios are compromised.

## Full report
<details><summary>Expand</summary>

---
Summary
---

I found an open redirect bug on unikoingold.com .First, I create an account on unikoingold.com , I fill all the forms with the required information (First name,Birth,etc...), until I came on the final step to verify my account , there was a mechanism to send a verification link to my email , therefore ,I open my email an click to this LINK to confirm my account and using burp suite proxy to see what traffic is passed into this request so I came over this url `https://unikrn.com//s/doi?h=maafad1d6d_cb9789f50190531e43c7409eeead93ff1a7e21ff&l=//www.whitelisteddomain.tld@localdomain.pw/../&utm_medium=doi&utm_campaign=doi_welcome` then I try to play with `l` parametre until I have redirection to my input (Malicious website with XSS code executed).

---
Steps
---

1. Create An account on unikoingold.com .
2. Set up your Burp suite proxy with your browser .
3. Intercept the request Like This :

```http
GET /s/doi?h=maafad1d6d_cb9789f50190531e43c7409eeead93ff1a7e21ff&l=//www.whitelisteddomain.tld@localdomain.pw/%2e%2e%2f&utm_medium=doi&utm_campaign=doi_welcome HTTP/1.1
Host: unikrn.com
Connection: close
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: __cfduid=dc2e81d88677939ce456f73a18c2a09b51561192429; CW=fplg5rn6s118blhgpb20hi0phlhuv4jr
```
4 . Note the Value of ``l`` parametre 
5 . Or just Click on this [URL POC](https://unikrn.com//s/doi?h=maafad1d6d_cb9789f50190531e43c7409eeead93ff1a7e21ff&l=//www.whitelisteddomain.tld@localdomain.pw/../&utm_medium=doi&utm_campaign=doi_welcome) ***You must be logged in***
6 . Redirected successfully and Javascript code Executed .

-------

##POC
* `https://unikrn.com//s/doi?h=maafad1d6d_cb9789f50190531e43c7409eeead93ff1a7e21ff&l=//www.whitelisteddomain.tld@localdomain.pw/../&utm_medium=doi&utm_campaign=doi_welcome`
 
* `https://unikrn.com//s/doi?h=maafad1d6d_cb9789f50190531e43c7409eeead93ff1a7e21ff&l=///localdomain.pw/%2e%2e%2f&utm_medium=doi&utm_campaign=doi_welcome`


{F514634}

-----------

## Impact

* An Attacker can redirect user to a malicious website and execute some dangerous script to steal credentiels .

* Simplifies pishing Attacks .

</details>

---
*Analysed by Claude on 2026-05-24*
