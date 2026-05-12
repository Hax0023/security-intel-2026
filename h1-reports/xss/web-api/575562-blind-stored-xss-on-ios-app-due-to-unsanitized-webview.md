# Blind Stored XSS on iOS App due to Unsanitized WebView

## Metadata
- **Source:** HackerOne
- **Report:** 575562 | https://hackerone.com/reports/575562
- **Submitted:** 2019-05-09
- **Reporter:** n00bsec
- **Program:** Unknown (HackerOne Report #575562)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Blind XSS, Improper Input Validation, Unsafe WebView Configuration
- **CVEs:** CVE-2019-15614
- **Category:** web-api

## Summary
A Blind Stored XSS vulnerability exists in an iOS application's WebView that fails to sanitize user-supplied HTML content. An attacker can upload malicious HTML containing JavaScript that executes when victims open the content, allowing extraction of sensitive information including IP address, geolocation, and OS details.

## Attack scenario
1. Attacker crafts malicious HTML payload containing JavaScript code with exfiltration capability (IP, location, OS detection)
2. Attacker uploads the malicious HTML to the application's content upload feature
3. Attacker shares the uploaded content link with target victim(s) via social engineering or other distribution methods
4. Victim opens the malicious HTML content within the iOS application's WebView
5. JavaScript executes in the victim's browser context without CSP/XSS protections
6. Attacker's command and control server receives exfiltrated victim data (IP, geolocation, OS information)

## Root cause
The iOS application renders user-supplied HTML content directly in a WebView without proper input sanitization or output encoding. JavaScript is enabled in the WebView preferences, and no Content Security Policy (CSP) headers are implemented to restrict script execution. The application trusts user-provided HTML content without validation.

## Attacker mindset
Reconnaissance and data collection focused. Attacker seeks to gather passive intelligence about victims (IP, location, OS) through a low-effort, scalable attack vector. The blind nature suggests interest in mass exploitation and victim profiling rather than targeted attacks.

## Defensive takeaways
- Disable JavaScript execution in WebViews unless absolutely necessary: set WKPreferences.javaScriptEnabled to false
- Implement strict Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize all user-supplied HTML input using established libraries (e.g., DOMPurify, OWASP Java HTML Sanitizer)
- Use WebView sandboxing features to isolate rendered content from application context
- Implement allowlisting for permitted HTML tags and attributes
- Use safe HTML rendering libraries instead of raw WebView HTML injection
- Validate and escape all dynamic content before insertion into WebView
- Implement Origin restrictions and CORS policies on WebView requests
- Log and monitor for suspicious JavaScript patterns in uploaded content

## Variant hunting
Check for similar WebView XSS in Android applications using WebView.loadData() or loadDataWithBaseURL()
Search for other iOS features using WKWebView without JavaScript restrictions (JavaScriptEnabled=true)
Investigate file upload functionality that serves content in WebView without sanitization
Look for blind XSS in notification/alert rendering systems using WebView
Check for SVG/XML file uploads rendered in WebView context allowing script execution
Search for data: URI scheme handling that bypasses origin restrictions
Identify localStorage/sessionStorage access in WebView contexts that could expose auth tokens

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1566.001
- T1566.002
- T1091
- T1185

## Notes
This is a classic blind XSS vulnerability where the attacker cannot see the payload execute but receives out-of-band confirmation through server logs. The report lacks critical details: no specific program identification, no bounty amount disclosed, and limited technical depth on the actual exfiltration mechanism. The PoC references attached screenshots ({F487447}, {F487448}) and HTML payload are not visible in this text. The recommendation to disable JavaScript is the most effective mitigation but may break legitimate functionality; a defense-in-depth approach combining sanitization, CSP, and selective JS restriction is preferred.

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
*Analysed by Claude on 2026-05-12*
