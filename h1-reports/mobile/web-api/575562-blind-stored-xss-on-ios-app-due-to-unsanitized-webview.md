# Blind Stored XSS on iOS App due to Unsanitized Webview

## Metadata
- **Source:** HackerOne
- **Report:** 575562 | https://hackerone.com/reports/575562
- **Submitted:** 2019-05-09
- **Reporter:** n00bsec
- **Program:** Unknown (HackerOne report #575562)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Improper Input Validation, Unsafe Webview Configuration
- **CVEs:** CVE-2019-15614
- **Category:** web-api

## Summary
The iOS application fails to sanitize user-supplied HTML content before rendering it in a WebView with JavaScript enabled, allowing attackers to execute arbitrary JavaScript code when victims open malicious HTML payloads. This blind XSS vulnerability enables attackers to exfiltrate sensitive information including IP address, geolocation, and OS details from victim devices.

## Attack scenario
1. Attacker crafts malicious HTML containing embedded JavaScript payload that exfiltrates device information (IP, location, OS)
2. Attacker uploads the malicious HTML file to the application or shares it via email/messaging
3. Victim opens the malicious HTML file through the vulnerable iOS application
4. Application renders the HTML in a WebView with JavaScript enabled without sanitization
5. JavaScript payload executes automatically in victim's browser context
6. Attacker receives exfiltrated victim data at their command and control server

## Root cause
The application uses WKWebView or UIWebView to display user-supplied HTML content without proper sanitization or validation, and JavaScript is enabled in the WebView preferences, allowing arbitrary script execution with the privileges of the application context.

## Attacker mindset
Attackers recognize that users frequently open untrusted files shared through legitimate channels and exploit this behavior by disguising malicious content as benign HTML. The blind nature of the XSS (no visible attack) makes it difficult to detect, and the information exfiltration provides reconnaissance data for further targeted attacks.

## Defensive takeaways
- Disable JavaScript execution in WebViews unless absolutely required (set WKPreferences.javaScriptEnabled to false)
- Implement strict Content Security Policy (CSP) headers to limit script execution sources
- Sanitize and validate all user-supplied HTML input using established libraries (e.g., DOMPurify)
- Use sandboxing and restrict WebView capabilities to minimum required permissions
- Implement proper origin validation and CORS policies
- Apply allowlist-based content filtering for uploaded files
- Use HTTPOnly and Secure flags for sensitive cookies
- Implement subresource integrity checks for external resources
- Conduct regular security testing including XSS payload fuzzing

## Variant hunting
Test for stored XSS in other user-generated content fields (comments, profiles, documents)
Check if other WebViews in the application have JavaScript enabled
Verify if file upload mechanisms properly restrict file types or execute uploaded content
Test for DOM-based XSS through JavaScript bridge methods between native and web context
Check if sensitive data can be accessed through JavaScript context (localStorage, cookies, sessionStorage)
Look for reflected XSS in WebView URL parameters or deep links
Test custom URL schemes for command injection vulnerabilities

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1592
- T1557

## Notes
This report demonstrates a common mobile security misconfiguration. The 'blind' aspect indicates the attacker cannot directly observe the XSS execution but receives data exfiltration through out-of-band channels. The proof-of-concept attached (referenced as F487447, F487448) likely contains a working payload template requiring only IP address modification. The vulnerability is particularly dangerous because it operates silently without user-visible indicators of compromise.

## Full report
<details><summary>Expand</summary>

Hi Team!

I found a Blind XSS can executed on iOS App due to unsanitized webview. Using this issue, attacker can extract information from victim.

##Steps To Reproduce:
1. Upload malicious HTML, share to victim
2. Waiting victim to open it

{F487447}

{F487448}

HTML payload attached, don't forget to change IP Address to yours.

**Recomendation:** Disabling Javascript on Webview
**Reference:**
https://developer.apple.com/documentation/webkit/wkpreferences#//apple_ref/occ/instp/WKPreferences/javaScriptEnabled

## Impact

In this PoC, attacker can extract information from victim such as IP Address, Location, OS.

</details>

---
*Analysed by Claude on 2026-05-24*
