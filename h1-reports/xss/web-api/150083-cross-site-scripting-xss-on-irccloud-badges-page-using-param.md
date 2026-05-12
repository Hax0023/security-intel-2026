# Cross Site Scripting (XSS) on IRCCloud Badges Page via Parameter Pollution

## Metadata
- **Source:** HackerOne
- **Report:** 150083 | https://hackerone.com/reports/150083
- **Submitted:** 2016-07-08
- **Reporter:** rohitdua
- **Program:** IRCCloud
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Parameter Pollution, Filter Evasion
- **CVEs:** None
- **Category:** web-api

## Summary
IRCCloud's badges page is vulnerable to reflected XSS through parameter pollution combined with JavaScript comment-based filter evasion. By passing the 'hostname' parameter multiple times with specially crafted payloads, an attacker can bypass XSS filters and execute arbitrary JavaScript in a victim's browser.

## Attack scenario
1. Attacker crafts a malicious URL with duplicate 'hostname' parameters containing XSS payload with JavaScript comment sequences
2. Attacker distributes the malicious link via email, chat, or social engineering to IRCCloud users
3. Victim clicks the link and visits www.irccloud.com/badges with the malicious parameters
4. Server processes duplicate parameters inconsistently, with one parameter being reflected in HTML output
5. The JavaScript comments (/* */) in the payload combine with subsequent parameters to break out of HTML context and inject script tags
6. Browser executes the injected JavaScript in the victim's security context, allowing session hijacking or credential theft

## Root cause
The application reflects the 'hostname' parameter directly into HTML output without proper context-aware encoding. Parameter pollution processing combined with weak or insufficient XSS filtering allows malicious input to reach the page rendering. The filter attempted to block XSS but failed against the specific combination of HTML breakout syntax and JavaScript comment-based evasion.

## Attacker mindset
Systematic testing for filter bypasses by leveraging inconsistencies in parameter handling. Recognition that multiple parameter values create ambiguity in parsing, and JavaScript comments can selectively neutralize portions of WAF/filter rules while preserving the malicious payload execution.

## Defensive takeaways
- Implement strict input validation and reject duplicate parameters or define clear handling rules (accept first, last, or reject entirely)
- Use context-aware output encoding (HTML entity encoding for HTML context, URL encoding for URLs, JavaScript escaping for script context)
- Apply a Content Security Policy (CSP) with 'script-src' restrictions to mitigate inline script execution
- Implement allowlist-based validation for hostname parameter (alphanumeric, dots, hyphens only)
- Use parameterized/templated rendering frameworks that enforce automatic escaping
- Test XSS filters against polyglot payloads and filter evasion techniques including comment-based bypasses
- Implement security headers like X-XSS-Protection and X-Content-Type-Options

## Variant hunting
Look for parameter pollution in other query parameters (user, domain, email, token). Test mutation payloads using different comment styles (// HTML comments, <!-- -->, multiline /* */ variants). Check POST parameters for similar issues. Examine other pages accepting user input (search, settings, profile). Test parameter repetition with other special characters or encoding variations (URL encoding, double encoding).

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing

## Notes
The vulnerability combines two distinct weaknesses: parameter pollution (server-side logic flaw) and incomplete XSS filtering (security control bypass). The JavaScript comment technique is a creative filter evasion method that exploits the assumption filters would catch basic XSX payloads. The vulnerability is reflected XSS requiring user interaction via malicious link. No stored/persistent XSS indicated.

## Full report
<details><summary>Expand</summary>

I. Vulnerability
---------------------
IRCCloud is affected by Cross Site Scripting vulnerability in its badges page. (www.irccloud.com/badges)

II. Description
---------------------
IRCCloud is open to parameter pollution attacks ie. a parameter passed more than once with different values results in varying different results.
This bug is used to leverage an XSS in the badges page.

####POC link:
```
www.irccloud.com/badges?hostname=hostname" type="text/javascript"> /*&hostname=*/alert('XSS\n-Rohit Dua'); //
```
If  you visit the link a javascript pops up showing the message 'XSS - Rohit Dua'. (screenshot_irccloud.png)

Even after parameter pollution, the attack is ineffective due to strong XSS filters(possibly firewall)
The _filter evasion_ is possible due a certain combination of javascript comments in the url that combine and comment out the unneeded part.

#####[Attached]
POC source code screenshot
POC alert box screenshot

Please verify and fix the same.

</details>

---
*Analysed by Claude on 2026-05-12*
