# Clickjacking on Certificate Warning Pages in Kaspersky Internet Security

## Metadata
- **Source:** HackerOne
- **Report:** 463695 | https://hackerone.com/reports/463695
- **Submitted:** 2018-12-17
- **Reporter:** palant
- **Program:** Kaspersky
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** clickjacking, UI redressing, certificate validation bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
Certificate warning pages and other security UI elements in Kaspersky Internet Security are vulnerable to clickjacking attacks, allowing attackers to trick users into overriding SSL certificate warnings and disabling security features like Safe Money. A single click on an attacker-controlled page positioned over legitimate warning dialogs can bypass certificate validation, enabling MITM attacks on SSL-protected connections.

## Attack scenario
1. Attacker positions themselves on a public WiFi network or performs DNS spoofing to redirect user traffic
2. User attempts to access an HTTPS site (e.g., www.google.com) but receives a certificate warning from Kaspersky due to the MITM attack
3. Attacker hosts a malicious HTML page that mimics a legitimate Kaspersky network warning message using clickjacking techniques
4. User is tricked into clicking what appears to be a benign link on the attacker's page, but the click actually triggers the hidden 'override certificate' button from the legitimate warning dialog
5. User receives a generic secondary confirmation prompt from Kaspersky and clicks 'Continue', unaware they are overriding a certificate for a legitimate high-profile website
6. Certificate override is permanently accepted, allowing the attacker to intercept all future HTTPS traffic to that domain via MITM attack

## Root cause
Certificate warning pages and other security dialogs lack adequate clickjacking protections. Specifically: (1) single-click activation of critical security decisions without multi-step confirmation, (2) insufficient use of UI obstruction techniques (e.g., X-Frame-Options headers), (3) generic confirmation messages that don't clearly identify the affected website, and (4) placement of interactive elements in predictable locations making them easy targets for overlay attacks.

## Attacker mindset
An attacker on a public network or with network access seeks to transparently intercept HTTPS traffic to steal sensitive data or perform account takeover. By leveraging social engineering combined with UI manipulation, they can bypass security warnings without requiring technical exploitation. The attacker recognizes that users trust warnings from installed security software and can be tricked into dismissing them through familiar-looking prompts. The ability to permanently override certificates eliminates the need for repeated attacks.

## Defensive takeaways
- Implement multi-step confirmation patterns for security-critical actions: require users to interact with multiple distinct UI elements before overriding security warnings
- Use X-Frame-Options HTTP headers (DENY or SAMEORIGIN) to prevent sensitive dialogs from being embedded in frames
- Display specific, non-generic confirmation messages that clearly identify the affected website/resource and the security risk being bypassed
- Follow browser vendor best practices: inspect how Firefox and Chrome implement certificate error pages with their two-click, two-location requirement
- Ensure advanced/technical options are hidden by default and only revealed through explicit user interaction
- Implement Content Security Policy (CSP) headers to further restrict framing and clickjacking vectors
- Consider adding visual indicators (e.g., focus borders, distinct styling) to distinguish genuine security dialogs from page content

## Variant hunting
Other warning pages in Kaspersky suite (Safe Money prompts, phishing alerts, blocked website notifications) - test for similar clickjacking vulnerabilities
Similar security products from other vendors (Avast, AVG, Norton, McAfee) that implement custom certificate warning pages
Browser extensions that override or augment certificate handling - test for UI redressing vulnerabilities
Password manager overlays and auto-fill prompts that appear on top of login pages
Banking and payment gateway 3D Secure authentication pages
Two-factor authentication prompts from security software
Update/patch installation confirmation dialogs

## MITRE ATT&CK
- T1190
- T1567
- T1557
- T1185
- T1200

## Notes
The vulnerability was demonstrated by simulating a MITM attack using local hosts file modification. The researchers responsibly noted that a related vulnerability (CVE reference 461780) compounded the risk by allowing certificate overrides for high-profile websites. The attack requires no special privileges and works across multiple browsers (Firefox, IE, Edge). The generic nature of Kaspersky's secondary confirmation popup meant users had no way to know they were overriding a certificate for Google specifically. This is a classic example of how security UI can become a liability when not properly protected against UI-layer attacks.

## Full report
<details><summary>Expand</summary>

**Summary**
Clickjacking can be used to trick users into overriding certificate warnings, disabling Safe Money functionality or phishing alerts.

**Description**
On certificate warning pages, a single click is sufficient to trigger overriding a wrong certificate. While an additional warning is displayed outside of the browser, the message is very generic and won't really tell users what they are agreeing to. This allows attackers who can MiTM user's connections (e.g. on a public WiFi) to attack SSL-protected connections. The issue reported under https://hackerone.com/reports/461780 makes matters worse here because certificates can be overridden even for high-profile websites like Google.

**Environment**
- Scope: Application
- Product name: Kaspersky Internet Security
- Product version: example: 19.0.0.1088
- OS name and version (incl SP): Windows 10.0.17134, tested browsers are Firefox 64, Internet Explorer 11, Microsoft Edge
- Attack type: Clickjacking
- Maximum user privileges needed to reproduce your issue: no privileges

**Steps to reproduce**
1. Edit the file %WINDIR%\sysnative\drivers\etc\hosts as administrator and add the following line: `93.184.216.34 www.google.com` (that's the IP address of example.com to simulate a MitM attack).
2. Go to https://www.google.com/ in your browser - note how Kaspersky will display a certificate error page.
3. Now download the attached certerror_clickjacking.html and open it in your browser (can be opened directly from the file system).
4. The page masquerades as a warning from Kaspersky about your network not being protected, which is probably true if the attackers managed to show you this page. Click the "I understand the risks and wish to continue" link. Note: this has been tested with the English version of Kaspersky, there is a slight chance that this link won't be positioned correctly with other languages.
5. An additional warning by Kaspersky opens saying: "You are about to go to an insecure web resource. Are you sure you want to continue?" That warning is in line with what you already saw, so you click "Continue."
6. Now go to https://www.google.com/ again. Note how the site loads now (shows "Not Found"), the certificate error is gone.

The link you clicked on in step 4 didn't belong to the certerror_clickjacking.html page but rather to the certificate error page for www.google.com. So when you clicked it you actually confirmed to override the wrong certificate of www.google.com.

Other warning pages displayed by Kaspersky are similarly affected by clickjacking. So the attackers could trick you into clicking the link which disables Safe Money protection for your bank for example. Or the link that permanently overrides the phishing warning for almost-my-bank.com. Both these actions would have worked without an additional confirmation, so no social engineering required - the user merely needs to click somewhere on the attacker's page.

**Recommendations**
Browsers' certificate error pages are resilient to clickjacking. Both Firefox and Chrome will require **two** clicks on **different** parts of the page to override a certificate: first "Advanced" button, then the actual override. This approach is also advisable for other reasons: technical details only confuse the general population, the important information being that they should leave the page which is not secure. Only people who are technical enough to look at the advanced section should see the override possibility.

Also, the additional confirmation message displayed by Kaspersky should be made less generic. At the very least, it should mention the website that the user is overriding the certificate for.

Finally, there is no valid reason for the Safe Money prompt to appear within a frame, so this could be prevented using X-Frame-Options HTTP header.

## Impact

On a public network, attackers might redirect user's unencrypted (plain HTTP) traffic to their server and display a message to them that they would plausibly want to override. If the user clicks the override link then, they will have unwittingly overridden the wrong certificate warning for some SSL-protected website and will have given attackers the possibility to hijack this connection.

</details>

---
*Analysed by Claude on 2026-05-24*
