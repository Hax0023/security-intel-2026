# Clickjacking Vulnerability on Periscope.tv Due to Unsupported X-FRAME-OPTIONS Directive in Chrome

## Metadata
- **Source:** HackerOne
- **Report:** 198622 | https://hackerone.com/reports/198622
- **Submitted:** 2017-01-15
- **Reporter:** mishre
- **Program:** Twitter/Periscope
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Improper Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
Periscope.tv used the ALLOW-FROM directive in X-FRAME-OPTIONS header, which is not supported by Chrome browser, leaving the site vulnerable to clickjacking attacks. An attacker could overlay malicious content on framed Periscope pages to trick users into performing unintended actions such as following accounts or performing other authenticated operations.

## Attack scenario
1. Attacker creates a malicious webpage that iframes Periscope.tv content
2. Attacker overlays transparent or deceptive UI elements on top of the framed Periscope content
3. Victim visits the attacker's webpage in Chrome browser
4. Victim unknowingly clicks on the overlaid elements, which actually interact with Periscope.tv
5. Victim's authenticated session with Periscope performs unintended actions (follow accounts, like content, etc.)
6. Attacker achieves malicious objectives through the victim's compromised account interactions

## Root cause
Developer used ALLOW-FROM directive which is only supported in Firefox and IE, not in Chrome. This directive was deprecated in favor of frame-ancestors CSP directive. Chrome's behavior defaults to allowing framing when unrecognized directives are used, exposing the application to clickjacking.

## Attacker mindset
An attacker would recognize browser compatibility gaps in security headers as an exploitation opportunity. By understanding that Chrome ignores unsupported X-FRAME-OPTIONS values, they can craft clickjacking attacks targeting Chrome users while the developers incorrectly believe protection is in place.

## Defensive takeaways
- Use 'frame-ancestors' directive in Content-Security-Policy header instead of deprecated X-FRAME-OPTIONS
- If X-FRAME-OPTIONS must be used, employ universally supported values: 'DENY' or 'SAMEORIGIN'
- Test security headers across all major browsers (Chrome, Firefox, Safari, Edge) to verify effectiveness
- Implement frame-ancestors with specific trusted origins: Content-Security-Policy: frame-ancestors 'self' https://twitter.com
- Combine multiple clickjacking defenses: CSP headers, frame-busting JavaScript, and SameSite cookies
- Regularly audit security headers using automated tools and manual testing

## Variant hunting
Hunt for other endpoints or subdomains on Periscope and Twitter properties using unsupported X-FRAME-OPTIONS directives. Check for sites using deprecated security headers like X-Content-Type-Options with unsupported values, or CSP directives without fallback mechanisms. Look for applications that rely solely on single-browser-supported security controls.

## MITRE ATT&CK
- T1185 - Man in the Browser
- T1187 - Forced Authentication
- T1598 - Phishing

## Notes
This vulnerability demonstrates the critical importance of cross-browser testing for security controls. The ALLOW-FROM directive has been deprecated since 2019 in favor of CSP frame-ancestors. The fix is straightforward but the impact is significant as it affects all Chrome users. This is a classic example of security misconfiguration rather than a logic flaw.

## Full report
<details><summary>Expand</summary>

Hi,

The X-FRAME-OPTIONS header returned from https://www.periscope.tv is:
```
X-Frame-Options: ALLOW-FROM https://twitter.com/
```
But Chrome doesn't support this value for the header: https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet.
Because of that, no value for X-FRAME-OPTIONS is set and all of the periscope.tv pages are vulnerable to Clickjacking. You can see for example my attached poc (Make sure you test it on chrome) that I am framing my own user on periscope. I can use regular Clickjacking tricks to make the user follow other users and do practically any action on the site.

</details>

---
*Analysed by Claude on 2026-05-24*
