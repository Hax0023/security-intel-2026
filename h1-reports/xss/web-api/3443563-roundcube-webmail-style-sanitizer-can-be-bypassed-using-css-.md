# Roundcube Webmail Style Sanitizer Bypass via CSS Character Escapes

## Metadata
- **Source:** HackerOne
- **Report:** 3443563 | https://hackerone.com/reports/3443563
- **Submitted:** 2025-11-27
- **Reporter:** somerandomdev
- **Program:** Roundcube
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** CSS Injection, HTML Sanitization Bypass, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Roundcube's style sanitizer can be bypassed using CSS character escapes (e.g., \0026) to inject arbitrary inline CSS properties like url(). This allows attackers to exfiltrate victim information such as IP addresses and user agents through resource requests triggered by opening malicious emails.

## Attack scenario
1. Attacker crafts an HTML email containing a style attribute with CSS character escapes
2. The escape sequence (\0026) is decoded to an ampersand (&) character, breaking out of the sanitizer's string context
3. The resulting CSS includes a url() property pointing to an attacker-controlled server
4. Victim receives and opens the email in Roundcube HTML mode
5. Browser renders the HTML and requests the external resource specified in url()
6. Attacker's server receives the HTTP request containing victim's IP address and User-Agent header

## Root cause
The style sanitizer does not account for CSS character escape sequences (hexadecimal Unicode escapes) when parsing and validating inline styles. It only sanitizes the literal string provided without decoding CSS escapes first, allowing attackers to encode dangerous characters and bypass validation logic.

## Attacker mindset
An attacker seeks to extract reconnaissance information (IP address, browser user agent) from email recipients without their knowledge. This is achieved through passive monitoring of HTTP requests triggered by email rendering, requiring no user interaction beyond opening the email.

## Defensive takeaways
- Decode all CSS escape sequences before sanitization to prevent bypasses
- Use a whitelist-based approach for allowed CSS properties and values
- Strip or sandbox url() functions and other resource-loading CSS properties entirely
- Implement multiple layers of validation: parse CSS into AST, validate tokens, then sanitize
- Consider using a robust HTML/CSS sanitization library rather than custom regex-based filters
- Disable external resource loading in email rendering contexts
- Apply Content Security Policy (CSP) headers to prevent external requests

## Variant hunting
Search for similar bypasses in other email clients and web applications using style sanitization. Test other CSS escape mechanisms (octal escapes, unicode escapes without leading zero), attribute value escapes, and JavaScript escapes. Examine other Roundcube sanitization functions for similar character encoding blind spots.

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1190
- T1030

## Notes
The vulnerability demonstrates a classic sanitization bypass pattern: insufficient handling of character encoding mechanisms. CSS escapes are a legitimate CSS feature, making this a challenging security problem requiring decode-before-sanitize workflows. The attack is passive and leaves minimal traces, making it suitable for reconnaissance prior to targeted attacks.

## Full report
<details><summary>Expand</summary>

## Summary:
The style sanitizer in Roundcube Webmail can be bypassed by creating HTML entities using CSS character escapes. This allows using arbitrary inline CSS, like e.g. `url()`, and retrieve the IP address and user agent of the person reading the email.

## Steps To Reproduce:

1. Send an HTML email to your account with the following contents:
```html
<div style='content: "\0026quot;; background: url(//http.cat/418); content:""; width: 100%; height: 100%;'>hi, this shouldn't work :(</div>
```
2. Open the email in Roundcube in the HTML mode

The background image will be applied to the element, causing a HTTP request to https://http.cat/418

## Supporting Material/References:
{F5056779}
{F5056780}

## Explanation

`\0026` is a CSS entity and will be decoded to `&`. Together with the `quot;` afterwards, this will close the string token and cause the rest of the string token to be interpreted as CSS.
{F5056781}

## Impact

An attacker can send a malicious email to a victim and retrieve the victim's IP address and user agent.

</details>

---
*Analysed by Claude on 2026-05-12*
