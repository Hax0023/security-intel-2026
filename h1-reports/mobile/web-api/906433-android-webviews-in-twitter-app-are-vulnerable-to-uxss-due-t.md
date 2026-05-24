# Android WebViews in Twitter app vulnerable to UXSS due to CVE-2020-6506 misconfiguration

## Metadata
- **Source:** HackerOne
- **Report:** 906433 | https://hackerone.com/reports/906433
- **Submitted:** 2020-06-23
- **Reporter:** alesandroortiz
- **Program:** Twitter Security
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Universal Cross-Site Scripting (UXSS), Same-Origin Policy Bypass, Insecure WebView Configuration
- **CVEs:** CVE-2020-6506
- **Category:** web-api

## Summary
Twitter for Android's WebView implementation for Video Website Cards is vulnerable to CVE-2020-6506, a UXSS vulnerability allowing cross-origin iframes to execute arbitrary JavaScript in the top-level document. The vulnerability stems from default WebView configuration with setSupportMultipleWindows() disabled, enabling iframes to use window.open() with javascript: URLs to bypass same-origin policies. Exploitation requires minimal user interaction and affects all unpatched Android WebView versions prior to 83.0.4103.106.

## Attack scenario
1. Attacker creates a malicious Video Website Card on Twitter pointing to a legitimate-looking advertiser URL
2. The card is shared via tweets or paid advertising campaigns, reaching Twitter users on Android
3. When a user opens the Video Website Card in Twitter's WebView, the page loads with an embedded iframe from a different origin containing malicious code
4. User interacts with the page (tap, click, or types) which the invisible iframe captures
5. The malicious iframe calls window.open() with a javascript: URL payload, exploiting the UXSS vulnerability
6. Arbitrary JavaScript executes in the context of the top-level document, allowing data exfiltration, page modification, or credential harvesting

## Root cause
Twitter's WebView configuration keeps WebSettings.setSupportMultipleWindows() at its default value (false), which disables multiwindow support. This specific configuration combined with CVE-2020-6506 in the underlying Chromium WebView engine allows cross-origin iframes to bypass same-origin policies by using window.open() with javascript: URLs, as the vulnerability is only present when multiwindow support is disabled.

## Attacker mindset
An attacker seeks to compromise users of the Twitter Android app by creating seemingly legitimate Video Website Cards that deliver malicious content. The attacker understands that users trust Twitter's interface and advertiser URLs, and exploits this trust by embedding weaponized iframes that require only passive user interaction (unintentional keypresses or clicks). The goal is to exfiltrate sensitive data, modify page content to phish credentials, or perform account takeover.

## Defensive takeaways
- Keep Android WebView and all system components updated to patch security vulnerabilities promptly
- Avoid relying on default security configurations; explicitly review and harden all WebView settings
- Enable multiwindow support (setSupportMultipleWindows=true) and implement proper window handling callbacks to mitigate UXSS vulnerabilities from embedded iframes
- For non-browser use cases, restrict WebView rendering to trusted content only and implement Content Security Policy (CSP) headers
- Implement monitoring and alerting for WebView exploitation attempts, particularly for embedded iframe activity
- Consider sandboxing WebView instances and limiting their access to sensitive user data and APIs
- Use iframe sandbox attributes to restrict capabilities of embedded content and prevent window.open() abuse

## Variant hunting
Search for other Android apps using WebView with Video Website Cards, embedded content players, or any external URL rendering functionality. Look for applications that embed third-party iframes without multiwindow support enabled. Examine frameworks and libraries that wrap WebView functionality (Cordova, React Native, etc.) for the same misconfiguration. Check other social media platforms' Android implementations for similar WebView configuration issues.

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1539 Steal Web Session Cookie
- T1598 Phishing - Spearphishing Link
- T1566 Phishing
- T1056 Input Capture
- T1041 Exfiltration Over C2 Channel

## Notes
Report was embargoed pending disclosure of crbug-1083819. The vulnerability is particularly critical because it requires minimal user interaction and the malicious iframe can capture keystrokes intended for the top-level document without direct iframe interaction. Twitter was provided multiple mitigation options; the report suggests options 1a or 1b as most suitable for their use case. The vulnerability affects all unpatched Android WebView versions prior to 83.0.4103.106 (released June 15, 2020). This is a vendor-level vulnerability affecting any app using WebView with the vulnerable configuration, not unique to Twitter.

## Full report
<details><summary>Expand</summary>

## Summary:

CVSS score: 8.1 / High / CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N

**Embargo notice: Do Not Disclose publicly until https://crbug.com/1083819 is disclosed.**

Twitter for Android is affected by a UXSS vulnerability due to its configuration of Android WebView and CVE-2020-6506.

Vendor mitigation is recommended to protect unpatched WebView users, due to its impact and ease of exploitation. Mitigation options which minimize breaking changes are provided for various use cases.

Android WebView is the system component which allows Android apps to display web pages. Apps typically use Android WebView directly or via frameworks/libraries.

CVE-2020-6506 is a universal cross-site scripting (UXSS) vulnerability in Android WebView which allows cross-origin iframes to execute arbitrary JavaScript in the top-level document. This vulnerability affects vendors which use Android WebView with a default configuration setting, and run on systems with Android WebView version prior to 83.0.4103.106.

All relevant details to understand and mitigate the vulnerability should be in this report. As an affected vendor, you may request access to the restricted crbug for full details and discussion, subject to acceptance by the Chromium Security Team. To request access, send me an email.

## CVE-2020-6506 Details:
Embargo notice: Do Not Disclose publicly until https://crbug.com/1083819 is disclosed.

An Android WebView instance with WebSettings.setSupportMultipleWindows() kept at default or set to false allows an iframe on a different origin bypass same-origin policies and execute arbitrary JavaScript in the top document.

To perform the attack, an iframe can call window.open() with a javascript: URL. Other methods of opening a new window, such as a link with target=”_blank” and href=”javascript:...”, can also be used to perform the attack.

Performing the attack requires a single user interaction (a tap/click or a keypress). The malicious iframe does not need to be visible, and can obtain the keypress interaction while a user attempts to type in the top-level document (no direct iframe interaction required).

The patched version of Android WebView (83.0.4103.106) was released on Monday, June 15th, 2020: https://chromereleases.googleblog.com/2020/06/stable-channel-update-for-desktop_15.html

Vendors can and should mitigate CVE-2020-6506 to protect their users using unpatched Android WebView versions.

## Vendor Details:
Twitter for Android uses WebViews to render the URL in Video Website Cards. This type of Card uses the vulnerable WebView configuration, therefore there's two ways a user can reach the vulnerable WebView:
1. Advertiser creates legitimate Video Website Card pointing to the advertiser URL, then shares it via regular Tweets or paid advertising campaigns.
2. Attacker creates Video Website Card with the user-trusted target URL, then shares it via regular Tweets or paid advertising campaigns.

If the advertiser/target URL has a malicious or compromised iframe, the iframe can perform the UXSS attack with minimal user interaction (tap/click or keypress). If there's sensitive data in the WebView, it is vulnerable to exfiltration. Page contents and data can also be altered to benefit the attacker, such as requesting sensitive info from the user while purporting to be the advertiser/target URL.

Based on Twitter's use case, the suggested solution is option 1a or 1b. The final determination is left to the vendor. Reference implementations for each option is available by request.

If none of these options appear suitable, please provide feedback to address concerns. Other vendors could have the same concerns, so your input is appreciated to best mitigate for all affected vendors.

### Potential Solutions:
Vendors generally have two choices to mitigate for unpatched WebView users:
1. Enable multiwindow support. If needed, implementation options exist to mimic single-window behavior and minimize breaking changes. Does not require multi-tab UI. Suitable for browsers and frameworks.
2. Keep multiwindow support disabled, and strictly limit WebView rendering to trusted content only. Suitable for non-browser apps, and for frameworks when used in non-browser apps.

Detailed choices:
* Option 1a: Enable multiwindow support, and create a new tab in UI or block window creation.
    * Suitable and preferred choice for browsers.
    * Implementation: Set WebSettings.setSupportMultipleWindows() to true, and handle onCreateWindow() callback to create new tab in UI or block window creation.
    * Potential downsides: If all window creation is blocked, user experience may be negative.

* Option 1b: Enable multiwindow support, and mimic single-window behavior via WebView instance replacement.
    * Suitable for browsers and frameworks. Preferred choice for frameworks.
    * Potential implementation: Set WebSettings.setSupportMultipleWindows() to true, and handle onCreateWindow() callback to create a new WebView on top of existing WebView. Rebind any event listeners, state info, and other logic to the new WebView. Finally, destroy the old WebView as soon as possible.
    * Potential downsides: May cause breaking changes if existing code expects a single WebView instance for duration of use.
To minimize breaking changes, vendor could add an abstraction layer to internally track WebView instances. The abstraction could perform necessary setup/cleanup for each instance to maintain current WebView behavior (such as JS injection on first page load or each page load, event listeners, state, etc.). The abstraction layer could then seamlessly provide existing interfaces to other layers.

* Option 1c: Enable multiwindow support, and mimic single-window behavior via WebView instance reuse.
    * Suitable for browsers and frameworks.
    * Only if Option 1b is not feasible, and existing code expects a single WebView instance for duration of use. Minimizes breaking changes at the cost of complexity and fragility.
    * Potential implementation: Set WebSettings.setSupportMultipleWindows() to true, and handle onCreateWindow() callback. In the callback, create a temporary WebView with shouldOverrideUrlLoading() which returns true (prevents loading) and stores the attempted URL in a variable. Filter the attempted URL to ensure it is a safe HTTP(S) URL, then call loadUrl() on the initial WebView with the attempted URL. Finally, destroy the temporary WebView when convenient.
    * Potential downsides: May still cause breaking changes. May break if Android WebView behavior changes in future. Adds complexity which may be difficult to maintain.

* Option 2: Keep multiwindow support disabled, and enforce strict origin allowlist.
    * Suitable for non-browser apps, and for frameworks when used in non-browser apps.
    * Because the vulnerability is not mitigated with this option, WebViews must only render first-party trusted content in top-level window and iframes. If using cross-origin iframes, they must be properly sandboxed. Cross-origin iframes must avoid sandbox="allow-popups allow-top-navigation allow-scripts" because this allows exploitation.
    * Potential downsides: Any bypass of origin filtering allows exploitation of unpatched WebView users. For frameworks with configurable origin allowlists, developers can misconfigure allowlists and make their apps vulnerable.

Adjacent phishing mitigation: If the current page URL is not guaranteed to be shown to the user, origin allowlists are recommended to mitigate phishing risks. This is an adjacent vulnerability, but it's a good opportunity to mitigate it because URL filtering is likely to be implemented as part of the UXSS mitigation.

Additional implementation details for options 1a and 1b: When using multiple WebView instances simultaneously, ensure to destroy the background WebView, unload the background page, or handle background page events safely. Otherwise, background pages can perform actions which should only be allowed by a foregrou

</details>

---
*Analysed by Claude on 2026-05-24*
