# iOS App Can Establish FaceTime Calls Without User Permission via URL Scheme in iFrame

## Metadata
- **Source:** HackerOne
- **Report:** 28500 | https://hackerone.com/reports/28500
- **Submitted:** 2014-09-18
- **Reporter:** gepeto42
- **Program:** Apple
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** URL Scheme Hijacking, Implicit Intent Invocation, Cross-Site Request Forgery-like behavior, Unauthorized Capability Invocation
- **CVEs:** None
- **Category:** web-api

## Summary
iOS WebView automatically executes URL schemes embedded in iframes without user consent, allowing attackers to initiate FaceTime calls by embedding malicious iframes in web content. This vulnerability leaks caller identity (email/phone number) and establishes calls to arbitrary recipients without user interaction.

## Attack scenario
1. Attacker crafts HTML page containing iframe with facetime-audio:// URL scheme pointing to target phone number or email
2. Attacker hosts malicious page or injects content into legitimate website (via XSS, MITM, or compromised ad network)
3. Victim visits compromised website via Twitter app or Safari on iOS
4. WebView automatically processes and launches the facetime-audio:// URL scheme from iframe without prompting user
5. FaceTime Audio call is initiated to attacker's number, revealing victim's caller ID (email/phone associated with FaceTime account)
6. Victim is unaware of the unauthorized call initiation until call connects or appears in FaceTime history

## Root cause
iOS WebView fails to implement user interaction requirement for URL scheme invocation when schemes are embedded in iframes. The system trusts iframe-loaded content to execute privileged URL schemes without explicit user gesture or confirmation dialog.

## Attacker mindset
An attacker could exploit this for reconnaissance (discovering active FaceTime accounts/numbers), harassment (initiating unwanted calls), social engineering (appearing as legitimate caller), or privacy violations (leaking presence/availability information). Low effort required—just hosting a single HTML file.

## Defensive takeaways
- Require explicit user gesture (tap/click) before executing any URL scheme from webview content
- Implement whitelist of allowed URL schemes in webview context; restrict sensitive schemes (facetime, tel, mailto) to user-initiated actions only
- Disable automatic iframe navigation to URL schemes; require same-origin policy or user approval
- Add permission/confirmation dialog for FaceTime initiation similar to phone call prompts
- Audit all custom URL scheme handlers for implicit invocation vulnerabilities
- Implement Content Security Policy (CSP) with frame-src restrictions
- Log and alert users when FaceTime calls are initiated to track unauthorized usage

## Variant hunting
Test other URL schemes (tel://, sms://, mailto://) embedded in iframes for similar auto-execution behavior
Check if object tags, embed tags, or meta refresh can trigger URL schemes without user interaction
Test whether javascript: protocol execution is also subject to iframe auto-execution
Examine if deeplinks to other apps (maps://, youtube://) suffer the same issue
Verify if the vulnerability exists in webviews of third-party apps that embed untrusted content
Test if Content-Security-Policy headers can mitigate the issue as defense-in-depth

## MITRE ATT&CK
- T1190
- T1204.001
- T1566.002

## Notes
Report ID #28500 from HackerOne. Vulnerability demonstrates iOS WebView's insufficient validation of URL scheme execution context. The reporter correctly notes this is CSRF-like but distinct—it's a direct implicit invocation of system capabilities. Affects iOS 8+ at time of disclosure. The ability to leak caller identity (email/phone) elevates severity beyond just unwanted calls; it's also a privacy/information disclosure issue. Similar vulnerabilities likely exist in Android apps using WebView with unvalidated URL scheme handlers.

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
