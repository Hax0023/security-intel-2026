# Clickjacking Vulnerability on Login Page - hackers.upchieve.org

## Metadata
- **Source:** HackerOne
- **Report:** 1400405 | https://hackerone.com/reports/1400405
- **Submitted:** 2021-11-15
- **Reporter:** maisanisnotyours
- **Program:** Upchieve
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The login page at https://hackers.upchieve.org/login lacks clickjacking protections (X-Frame-Options header), allowing attackers to overlay malicious UI elements on the legitimate page rendered in an iframe. An attacker can deceive users into clicking on hidden login buttons, potentially leading to account compromise if combined with social engineering.

## Attack scenario
1. Attacker hosts a malicious webpage containing an iframe pointing to the vulnerable login page
2. Attacker overlays transparent or visually disguised buttons on top of the iframed login interface
3. Victim visits the malicious page, believing they are on a legitimate site or performing an innocent action
4. When victim clicks what appears to be a benign button, they unknowingly click the login submit button or credential entry fields
5. Attacker's JavaScript captures the victim's input or session tokens if form submission is intercepted
6. Attacker gains unauthorized access to the victim's account

## Root cause
The application does not implement the X-Frame-Options HTTP response header or Content-Security-Policy frame-ancestors directive to prevent the page from being embedded in frames on other domains. This allows any attacker to embed the login page in their own site.

## Attacker mindset
An attacker would leverage this to perform credential harvesting or unauthorized account access by disguising malicious overlays as trusted UI elements. The login page context makes this especially valuable for account takeover attacks. Combined with phishing social engineering, this becomes a practical exploitation vector.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all pages, especially authentication endpoints
- Set Content-Security-Policy header with frame-ancestors directive (e.g., frame-ancestors 'self')
- Apply frame-busting JavaScript as defense-in-depth measure
- Implement additional CSRF protections beyond clickjacking defense
- Use SameSite cookie attributes to limit session cookie exposure
- Implement per-request tokens or double-submit cookies to prevent unauthorized form submissions
- Add visual indicators warning users when accessing login pages across different contexts

## Variant hunting
Check other sensitive pages (password reset, payment, account settings) for same vulnerability
Test if X-Frame-Options can be bypassed with alternative framing techniques (object, embed, picture tags)
Verify if CSP header has frame-ancestors but contains unsafe values like 'self' with data: protocol
Test for partial clickjacking on admin panels or API authentication endpoints
Check if subdomains lack frame protection even if main domain has it

## MITRE ATT&CK
- T1189
- T1598
- T1539

## Notes
This is a straightforward clickjacking vulnerability with clear POC. The severity is high due to the login page context and potential for account takeover. The report includes a working HTML proof-of-concept demonstrating the iframe embedding and overlay button technique. No evidence of bounty amount in the HackerOne report reference provided.

## Full report
<details><summary>Expand</summary>

I found clickjacking at login page on https://hackers.upchieve.org that can be exploited if the UI overlay can be performed correctly by the attacker.

```<html>
<head>
<title>Clickjack test page</title>
</head>
<body>
<p>Website is vulnerable to clickjacking!</p>
<iframe src="https://hackers.upchieve.org/login" width="1000" height="550"></iframe>
<div style="height: 30px;width: 130px;left: 53%;bottom: 39%;background: #789;" class="xss"><button>Click me when you finish :)</button></div>
</body>
</body>
</html>```

## Impact

Its login page so if the UI overlay can be performed correctly by the attacker, this can lead to account takeover.

</details>

---
*Analysed by Claude on 2026-05-24*
