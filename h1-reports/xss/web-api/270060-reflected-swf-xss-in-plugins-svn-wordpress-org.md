# Reflected XSS in Flash Files (video-js.swf and moxieplayer.swf) on plugins.svn.wordpress.org

## Metadata
- **Source:** HackerOne
- **Report:** 270060 | https://hackerone.com/reports/270060
- **Submitted:** 2017-09-21
- **Reporter:** m7mdharoun
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, Insecure Flash Parameters, Content Spoofing
- **CVEs:** None
- **Category:** web-api

## Summary
Flash files hosted on the WordPress plugin repository are vulnerable to reflected XSS through unsafe parameter handling. The video-js.swf file accepts a 'readyFunction' parameter that executes arbitrary JavaScript, and moxieplayer.swf accepts untrusted 'url' parameters enabling content spoofing attacks.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the readyFunction or url parameters of vulnerable SWF files
2. Attacker sends phishing link to victim containing the malicious URL pointing to plugins.svn.wordpress.org
3. Victim clicks link and the SWF file loads the attacker-controlled parameter value
4. Flash player interprets and executes the JavaScript payload in the context of the plugins.svn.wordpress.org domain
5. Attacker gains ability to steal session cookies, credentials, or perform actions on behalf of the victim
6. Content spoofing variant allows attacker to redirect video playback to malicious content, deceiving users about media source

## Root cause
SWF files accept user-supplied parameters (readyFunction, url) without proper validation or sanitization before passing them to JavaScript evaluation functions or content loading mechanisms. Legacy Flash security model fails to restrict parameter interpretation.

## Attacker mindset
Target older web applications still relying on Flash content. Exploit trust in WordPress plugin repository domain to bypass user security perception. Use URL shorteners to obfuscate malicious links in phishing campaigns. Chain with social engineering for higher success rates.

## Defensive takeaways
- Remove or deprecate all Flash content from production systems
- If Flash must be used, implement strict whitelist validation for all parameters before use
- Never pass user input directly to JavaScript eval() or similar functions
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Use modern video players built with HTML5 instead of Flash-based solutions
- Apply input validation and output encoding for any dynamic parameter handling
- Regular security audits of legacy components still in use

## Variant hunting
Search WordPress plugin repository for other .swf files with similar parameter patterns
Audit other media players (JWPlayer, Flowplayer) for similar unsafe parameter handling
Test for double URL encoding bypasses in parameter validation
Check for XSS in callback function parameters across all legacy plugins
Investigate if vulnerabilities exist in archived/older plugin versions
Look for similar issues in other CDNs hosting legacy plugin versions

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1204

## Notes
This vulnerability represents the broader issue of legacy Flash components persisting in production systems. The reflected nature means every victim requires direct interaction with a malicious link. The plugins.svn.wordpress.org domain provides false legitimacy to the attack. This report demonstrates why Flash has been deprecated across all major browsers by 2021.

## Full report
<details><summary>Expand</summary>

Hello ,
 I have found XSS in flash File ( video-js.swf ) in  plugins.svn.wordpress.org 
 and Content Spoofing Vulnerability in moxieplayer.swf

          ** POC **
https://plugins.svn.wordpress.org/1player/tags/1.3/players/video-js/video-js.swf?readyFunction=alert(%27Hello%27)


{F222664}


https://plugins.svn.wordpress.org/agile-video-player/trunk/js/plugins/media/moxieplayer.swf?url=hekimuso1973.xsl.pt/723.flv

</details>

---
*Analysed by Claude on 2026-05-12*
