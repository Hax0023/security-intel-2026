# Clickjacking Vulnerability via Ineffective Iframe Breakout Detection

## Metadata
- **Source:** HackerOne
- **Report:** 200419 | https://hackerone.com/reports/200419
- **Submitted:** 2017-01-22
- **Reporter:** b1b62e8d81ce1e3993ad913
- **Program:** Pushwoosh
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Insufficient Iframe Protection
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application attempted to prevent clickjacking by detecting iframe embedding but used a flawed detection method that could be bypassed with the sandbox attribute. The vulnerable iframe breakout code fails to actually prevent the application from rendering within an iframe, allowing attackers to overlay malicious UI elements.

## Attack scenario
1. Attacker creates a malicious webpage containing an iframe with sandbox attributes pointing to a Pushwoosh application page
2. The sandbox attribute restricts certain capabilities but allows scripts and forms, bypassing the frame-breaking logic
3. Attacker overlays transparent or deceptive elements on top of the framed content to trick users into unintended actions
4. User believes they are interacting with legitimate Pushwoosh functionality but is actually clicking attacker-controlled elements
5. Attacker captures sensitive user interactions such as account registration, data submission, or authorization grants
6. Session hijacking, credential theft, or unauthorized actions are performed on behalf of the victim user

## Root cause
The iframe detection logic using `window.self !== window.top` is ineffective when the embedding page uses the sandbox attribute, as this constraint does not raise an exception in modern browsers. The code relies on exception handling as a fallback, but the sandbox attribute prevents the exception from occurring, allowing the breakout attempt to fail silently.

## Attacker mindset
An attacker recognizes that simple frame-breaking techniques are commonly implemented but often contain logical flaws. By leveraging sandbox attributes and understanding browser security model nuances, they can defeat naive iframe detection and set up a clickjacking attack to perform unauthorized actions or steal user input.

## Defensive takeaways
- Implement X-Frame-Options HTTP header (DENY or SAMEORIGIN) as the primary defense against clickjacking
- Use Content-Security-Policy frame-ancestors directive as a modern alternative to X-Frame-Options
- Avoid relying solely on JavaScript-based frame breakout code, as it can be bypassed
- Test iframe detection logic against various embedding scenarios including sandbox attributes
- Implement multiple layers of defense rather than a single protection mechanism
- Monitor and log instances where frame-breaking attempts fail or are detected
- Use UI gestures and confirmation dialogs for sensitive operations to prevent successful clickjacking

## Variant hunting
Search for other applications using similar window.self !== window.top detection patterns without server-side X-Frame-Options headers. Test with various sandbox attribute combinations (sandbox='allow-scripts allow-forms', sandbox='allow-same-origin', etc.) to identify which bypass the detection.

## MITRE ATT&CK
- T1190
- T1149

## Notes
This vulnerability demonstrates why HTTP security headers are essential and JavaScript-only defenses are insufficient. The sandbox attribute's interaction with frame-breaking code is a known bypassing technique. Modern browsers support X-Frame-Options since IE8+ and CSP frame-ancestors since modern versions, making these the reliable defenses.

## Full report
<details><summary>Expand</summary>

Steps to reproduce:

create index.html file with following content:
<iframe sandbox="allow-scripts allow-forms" src="https://go.pushwoosh.com/register" width="1000" height="600"></iframe>

Open index.html in browser

Actual result: Pushwoosh viewed in iframe.
Expected result: do not allow clickjacking
Root cause:

```
var isInIFrame = (function () {
			try {
				return window.self !== window.top;
			} catch (e) {
				return true;
			}
		})();
```

</details>

---
*Analysed by Claude on 2026-05-24*
