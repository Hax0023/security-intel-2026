# Persistent XSS in Reverb.com Listing Page via SoundCloud Link Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 333008 | https://hackerone.com/reports/333008
- **Submitted:** 2018-04-03
- **Reporter:** bigshaq
- **Program:** Reverb.com
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Stored, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A persistent XSS vulnerability exists in the listing page where attacker-controlled SoundCloud links are stored without proper server-side validation or output encoding. An attacker can inject malicious JavaScript via the product[soundcloud_link_attributes][link] parameter by bypassing client-side validation through request interception, affecting all users who view the compromised listing.

## Attack scenario
1. Attacker creates or edits a legitimate Reverb.com listing with a valid SoundCloud URL
2. During submission, attacker intercepts the HTTP request using a proxy tool (Burp Suite)
3. Attacker modifies the product[soundcloud_link_attributes][link] parameter to inject XSS payload with event handler: https://soundcloud.com/user/track?fuzzing" onload=alert(document.domain) x="
4. Server accepts the malicious payload due to lack of server-side validation, storing it in the database
5. When any user (including other shop owners) visits the compromised listing page, the JavaScript payload executes in their browser context
6. Attacker can exfiltrate session cookies, perform unauthorized actions, or redirect users to malicious sites

## Root cause
Missing server-side input validation and output encoding on the soundcloud_link_attributes[link] parameter. Application relied solely on client-side validation which can be bypassed via request interception. The stored user input is rendered directly into HTML attributes without sanitization or proper escaping.

## Attacker mindset
The attacker identified a gap between client-side and server-side security controls. By observing that client-side validation rejected malicious input, they recognized an opportunity to bypass this protection layer through request tampering. They leveraged the application's trust in unvalidated user input to achieve persistent code injection affecting multiple victims.

## Defensive takeaways
- Implement robust server-side input validation for all URL parameters, especially those that reference external services
- Apply context-aware output encoding when rendering user-supplied URLs in HTML attributes (use HTML entity encoding or URL encoding)
- Never rely solely on client-side validation; always validate and sanitize on the server
- Use a URL validation library that properly validates protocol and structure before storage
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Store URLs in a normalized format and validate against a whitelist of allowed domains if possible
- Implement regular security testing including request interception scenarios

## Variant hunting
Check other user-supplied URL parameters (YouTube links, Spotify links, portfolio URLs, etc.) for similar encoding issues
Test other media embedding functionality for output encoding vulnerabilities
Examine profile pages, shop descriptions, and product descriptions for similar XSS patterns
Review other form fields accepting external URLs or user content across the platform
Test different HTML attributes beyond event handlers (src, href, data-, etc.)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing

## Notes
The vulnerability is particularly dangerous because it affects marketplace platforms where multiple sellers and buyers interact. The attacker references a related self-XSS vulnerability (report #331725), suggesting systematic security issues in the application's input handling. The sandbox environment indicates this was tested on a staging server before production disclosure. Video proof-of-concept provided demonstrates successful execution.

## Full report
<details><summary>Expand</summary>

# Description
I found a Persistent XSS in a listing page. The flaw is in the SoundCloud link that the listing owner can attach(The parameter is called *product[soundcloud_link_attributes][link]*). There's no encoding on the user input and it looks like there's only client-side validation.

# PoC
The payload:
```
https://soundcloud.com/rich-the-kid/sets/the-world-is-yours-15?fuzzing" onload=alert(document.domain) x="
```
If you try to put this payload straight into the "Edit Listing" page it'll give you the following error:
```
https://sandbox.reverb.com/listings/[YOUR_LISTING_ID]/edit
```
{F281627}

But it looks like there's only client side validation, when I tried to enter a valid link:
```
https://soundcloud.com/rich-the-kid/sets/the-world-is-yours-15
```
I got no error message(because it was a valid link)
But when I clicked "Save & Review Listing", intercepted the request and tampered the *product[soundcloud_link_attributes][link]* parameter's value to:
```
https://soundcloud.com/rich-the-kid/sets/the-world-is-yours-15?fuzzing" onload=alert(document.domain) x="
```
It updated successfully and because there's no encoding on this input parameter - it allowed me to inject javascript code that'll be stored on my listing page.
{F281640}

PoC Video: https://youtu.be/Y-8W422hLOw

## Impact

An attacker can:
* Perform a defacement on every possible store in the website (all he need is a single click from the victim)
* Deny future access from any other shop owner that access this listing(with the self-PXSS that i reported 2 days ago: https://hackerone.com/reports/331725 )
*  Perform operations in the application on behalf of the victim

The hacker selected the **Cross-site Scripting (XSS) - Stored** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://sandbox.reverb.com/item/

**Verified**
Yes



</details>

---
*Analysed by Claude on 2026-05-12*
