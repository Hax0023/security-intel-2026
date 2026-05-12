# CSS Injection via Custom Theme to Disable Slack App and Potential Data Exfiltration

## Metadata
- **Source:** HackerOne
- **Report:** 679969 | https://hackerone.com/reports/679969
- **Submitted:** 2019-08-22
- **Reporter:** fletchto99
- **Program:** Slack
- **Bounty:** Not specified in writeup
- **Severity:** Medium
- **Vuln:** CSS Injection, Denial of Service, Potential Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
A CSS injection vulnerability in Slack's custom theming feature allows attackers to inject malicious CSS that completely disables the application by hiding the entire DOM. The payload persists across application reinstalls on macOS, and there is theoretical potential for data exfiltration using CSS-only techniques, though no working proof-of-concept was provided.

## Attack scenario
1. Attacker crafts a malicious theme configuration with CSS payload in the column background field
2. Attacker shares the theme with target user via social engineering, theme marketplace, or direct distribution
3. Target user imports/applies the custom theme in Slack Preferences > Sidebar > Custom Theming
4. The injected CSS (`#FFFFFF;} html {display:none;}`) closes the CSS rule and applies `display:none` to the entire HTML element
5. The Slack application becomes completely unusable as the DOM is hidden
6. The payload persists even after application reinstall, potentially requiring manual theme configuration reset

## Root cause
Insufficient input validation and sanitization of custom theme values. The application directly interpolates user-supplied theme values into CSS without proper escaping or validation, allowing CSS injection through the column background color field.

## Attacker mindset
An attacker would recognize that theming functionality often accepts user input without sufficient guardrails. By injecting CSS syntax characters, they can break out of the intended CSS property context and execute arbitrary CSS rules. The persistence across reinstalls suggests theme configuration is stored in a location that survives application updates, making this particularly valuable for sustained attacks.

## Defensive takeaways
- Implement strict input validation for all theme customization fields - validate color values against a whitelist of valid hex/rgb color formats
- Use CSS preprocessors or templating engines that properly escape user input when generating stylesheets
- Sanitize and validate all user-supplied values before embedding them in CSS, treating theme input as untrusted
- Implement Content Security Policy (CSP) headers to restrict the scope of CSS-based attacks
- Apply proper bounds checking - ensure theme values cannot contain CSS syntax characters like braces, semicolons, and brackets
- Consider using CSS-in-JS libraries that provide better encapsulation and prevent global style injection
- Store theme configurations separately from executable CSS, only using validated properties to construct styles programmatically
- Add security testing for injection attacks in all customization features, especially theme/appearance settings

## Variant hunting
Test other customization fields in the theming interface (accent colors, text colors, background images) for similar injection vulnerabilities
Investigate whether other Slack clients (web, Windows, Linux) have the same vulnerability or if they sanitize differently
Check if theme sharing/import functionality validates themes before applying them
Attempt to inject CSS keyloggers or background-image exfiltration techniques via other color/style fields
Test if injected CSS can access or exfiltrate data through CSS selectors combined with attribute selectors
Examine if user-uploaded custom icons, emojis, or other media in themes could contain similar injection vectors
Check if theme data is synchronized across devices and whether injection persists across synced clients

## MITRE ATT&CK
- T1190
- T1499
- T1005

## Notes
The researcher appropriately marked this as low-to-medium severity due to the lack of a confirmed data exfiltration proof-of-concept, though the DoS impact is clearly demonstrated. The persistence across reinstalls is a notable aspect suggesting the malicious theme is stored in a user-writable configuration location. The theoretical CSS keylogging vector referenced (CSS-Keylogging) relies on exfiltrating data through background-image requests to attacker-controlled servers, which would depend on Slack's network policies and CSP implementation. This vulnerability demonstrates why security reviews of 'safe' feature areas like theming are critical.

## Full report
<details><summary>Expand</summary>

Tested on Slack for MacOS v4.0.2 - I've marked this as code injection since there was no "css injection"

1. In the app go to Preferences -> Sidebar
2. Enable custom theming 
3. Set the column BG to `#FFFFFF;} html {display:none;}`
4. The app will no-longer render (this survives re-installs)

If this theme were to be shared to someone unsuspecting they would be unable to use slack, even surviving a reinstall (on mac, untested on other platforms).

Furthermore it _might_ be possible to exfil message data using CSS only. As seen here it is _possible_ to keylog via CSS only https://github.com/maxchehab/CSS-Keylogging/ however I have not been able to come up with a proper PoC of this.

I've marked this as low for now as I don't have a PoC exiling data however I have shown that it is possible to inject to completely disable the app.

## Impact

The app is no longer able to render - there might be the possibility of data exfil but I didn't get a PoC working.

</details>

---
*Analysed by Claude on 2026-05-12*
