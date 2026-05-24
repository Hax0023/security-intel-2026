# iOS App URL Scheme Hijacking via Iframe - Unauthorized FaceTime Calls

## Metadata
- **Source:** HackerOne
- **Report:** 28500 | https://hackerone.com/reports/28500
- **Submitted:** 2014-09-18
- **Reporter:** gepeto42
- **Program:** Apple
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** URL Scheme Hijacking, Unsafe Iframe Loading, Missing User Confirmation, Privilege Escalation, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
iOS WebView automatically executes local URL schemes (e.g., facetime-audio://) when embedded in iframes without user interaction or confirmation. An attacker can craft malicious HTML pages that trigger FaceTime calls, SMS messages, or other sensitive app actions when loaded in a browser, bypassing user permission controls and potentially leaking caller ID information.

## Attack scenario
1. Attacker creates a webpage containing an iframe with a URL scheme pointing to facetime-audio://victim@email.com
2. Attacker distributes the malicious page via Twitter, email, or other social engineering vectors
3. Victim visits the page in Safari or another iOS browser (including via in-app WebView)
4. iOS WebView automatically initiates the FaceTime call without prompting the user
5. Victim's device establishes a call to attacker's number, revealing caller ID and contact information
6. Attacker confirms victim's phone number or email is valid and active on FaceTime

## Root cause
iOS WebView does not restrict or prompt for confirmation when URL schemes targeting local applications are invoked from web content. The iframe's src attribute is processed the same as direct navigation, allowing automatic execution of privileged actions without user consent.

## Attacker mindset
An attacker seeks to abuse trust in web content delivery to trigger high-privilege actions (phone calls, messages) without user knowledge. The motivation could be reconnaissance (validating active phone numbers), harassment, OSINT collection, or demonstrating a proof-of-concept vulnerability. Using an iframe makes the attack invisible to users and difficult to detect.

## Defensive takeaways
- Implement user confirmation dialogs for all sensitive URL schemes (tel:, facetime:, facetime-audio:, sms:, mailto:)
- Disable automatic URL scheme execution from iframes and sandboxed content
- Whitelist only necessary URL schemes and require explicit user gestures (tap) to trigger them
- Implement Content Security Policy (CSP) restrictions to control which protocols can be invoked
- Add warnings or visual indicators when URL schemes are about to be executed
- Regularly audit WebView security configuration and update to latest iOS versions
- Educate users about suspicious web pages that trigger unexpected calls or messages

## Variant hunting
Test other sensitive URL schemes: tel://, sms://, mailto://, maps://, itms://, itms-apps://
Verify if the vulnerability affects different iframe attributes (src, data, nested iframes)
Check if other embedding methods (embed, object, form action) bypass protections
Test across different iOS browsers (Safari, Chrome, Firefox) and in-app WebViews (Twitter, Facebook, Instagram)
Examine if localStorage, sessionStorage, or meta refresh can trigger URL schemes
Check if JavaScript-based navigation (window.location.href, window.open) requires additional permissions
Test with encoded/obfuscated URL schemes to bypass simple filters

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1598 - Phishing for Information
- T1200 - Hardware Additions
- T1204 - User Execution
- T1570 - Lateral Tool Transfer

## Notes
This vulnerability demonstrates a critical gap between web sandbox security and native OS integration on iOS. URL schemes were designed for legitimate inter-app communication but lack proper authorization checks when invoked from web content. The reporter correctly notes this behaves similarly to CSRF but is technically a different class of vulnerability (URL scheme injection/hijacking). The information disclosure aspect is significant as it reveals whether specific phone numbers/emails are registered on FaceTime. This was likely patched in later iOS versions with mandatory user confirmation for sensitive schemes.

## Full report
<details><summary>Expand</summary>

When URL Schemes for local applications are inserted in an inline frame, the web view launches them automatically.

###Example###: 


    <html>
    <header><title>Facetime Audio URL Scheme Test</title></header>
    <body>
    <iframe src="facetime-audio://guillaume@binaryfactory.ca"></iframe>
    </body>
    </html>

This page ( which you can also find at http://binaryfactory.ca/urlschemes/facetime.html ) - when loaded from Twitter on iOS (including 8), automatically establishes a Facetime Audio call to me, leaking the user's email address or phone number (caller ID information for their Facetime account).

I marked this as a CSRF but that isn't technically correct, but it is similar in behavior.

Thank you.

</details>

---
*Analysed by Claude on 2026-05-24*
