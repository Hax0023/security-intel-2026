# Flash Based Reflected XSS on www.grouplogic.com/jwplayer/player.swf

## Metadata
- **Source:** HackerOne
- **Report:** 859806 | https://hackerone.com/reports/859806
- **Submitted:** 2020-04-26
- **Reporter:** ali
- **Program:** Group Logic
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Flash Parameter Injection, Inadequate Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the JWPlayer Flash component hosted on grouplogic.com, where the 'playerready' parameter is passed directly to JavaScript without proper sanitization. An attacker can craft a malicious URL containing JavaScript code in the playerready parameter to execute arbitrary code in the victim's browser within the context of the grouplogic.com domain.

## Attack scenario
1. Attacker crafts malicious URL with JavaScript payload in playerready parameter: http://www.grouplogic.com/jwplayer/player.swf?playerready=alert(document.domain)
2. Attacker distributes URL via phishing email, social media, or injects into trusted websites
3. Victim clicks the malicious link and opens the URL in their browser
4. Flash player loads and processes the playerready parameter without sanitization
5. JavaScript payload executes in victim's browser with grouplogic.com origin
6. Attacker can steal session cookies, perform account takeover, or redirect to malicious sites

## Root cause
The Flash player component (player.swf) accepts user-supplied input via the 'playerready' URL parameter and passes it directly to JavaScript evaluation without proper input validation or encoding. This violates secure coding practices for handling untrusted data.

## Attacker mindset
An opportunistic attacker targets legacy Flash components which are often overlooked in security updates. The attacker recognizes that Flash parameters are frequently passed to JavaScript and tests common parameter names for injection vulnerabilities. They leverage the trust users place in legitimate domains to deliver malicious payloads.

## Defensive takeaways
- Immediately deprecate and remove Flash components; migrate to modern HTML5 video players
- Implement strict Content Security Policy (CSP) headers to prevent inline script execution
- Validate and sanitize all URL parameters before passing to JavaScript functions
- Use parameter whitelisting rather than blacklisting for Flash player configuration
- Implement URL encoding/escaping for all user-controlled data passed to DOM or JavaScript
- Conduct security audit of all legacy Flash components across the application
- Apply Web Application Firewall (WAF) rules to detect and block XSS payloads
- Use security scanning tools to identify similar vulnerabilities in other endpoints

## Variant hunting
Test other JWPlayer instances for similar parameter injection vulnerabilities
Check for other Flash components accepting URL parameters without validation
Fuzz the 'playerready' parameter with various XSS payloads (javascript:, onerror=, event handlers)
Test other parameter names like 'onComplete', 'onError', 'callback', 'onReady' for similar issues
Search for other grouplogic.com subdomains hosting Flash files
Check if similar vulnerable Flash players are used by partner companies or CDNs
Test for Stored XSS if the playerready parameter is saved in any backend system

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1185 - Man in the Browser
- T1539 - Steal Web Session Cookie

## Notes
This vulnerability demonstrates the security risks of legacy Flash technology still in production. Flash was officially discontinued by Adobe and major browsers no longer support it, making this a critical issue for remaining deployments. The simplicity of the PoC (basic alert box) indicates this was likely an easy discovery but represents a serious security gap. The reporter's minimal submission suggests either a responsible disclosure approach or low confidence in the initial report.

## Full report
<details><summary>Expand</summary>

Hello there,
I hope you are well!

Steps:
1. Open firefox.
2. Go to http://www.grouplogic.com/jwplayer/player.swf?playerready=alert(document.domain) 
You will see xss alert.

## Impact

Reflected XSS

Regards,
@mygf

</details>

---
*Analysed by Claude on 2026-05-12*
