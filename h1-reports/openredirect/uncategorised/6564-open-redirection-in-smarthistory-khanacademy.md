# Open Redirection in SmartHistory KhanAcademy

## Metadata
- **Source:** HackerOne
- **Report:** 6564 | https://hackerone.com/reports/6564
- **Submitted:** 2014-04-08
- **Reporter:** atom
- **Program:** Khan Academy
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirection, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirection vulnerability exists in the SmartHistory Flash player that allows attackers to redirect users to arbitrary external URLs through the 'link' parameter. By crafting a malicious link with the vulnerable parameter, an attacker can redirect users to phishing sites or other malicious destinations.

## Attack scenario
1. Attacker crafts a URL containing the vulnerable SmartHistory player with a malicious 'link' parameter pointing to attacker-controlled domain
2. Attacker distributes the link via email, social media, or embeds it in trusted-looking content
3. Victim clicks the link, loading the SmartHistory player hosted on the legitimate Khan Academy domain
4. Victim clicks the screen/button in the player as instructed
5. The player redirects the victim to the attacker's malicious URL (phishing page, malware distribution, etc.)
6. Victim believes they are interacting with legitimate content due to initial Khan Academy domain origin

## Root cause
The Flash player (player.swf) accepts unsanitized user input from the 'link' parameter and performs a redirect without validating that the target URL belongs to an allowed whitelist of domains. The application failed to implement proper URL validation or restrict redirects to same-origin/whitelisted domains.

## Attacker mindset
An attacker would leverage the trust associated with the Khan Academy brand to bypass user skepticism. Since the initial page load comes from the legitimate domain (smarthistory.khanacademy.org), users are more likely to trust the redirect destination. This is particularly effective in educational contexts where Khan Academy users may be less security-aware.

## Defensive takeaways
- Implement strict URL validation: only allow redirects to whitelisted internal URLs or trusted domains
- Use allowlist approach for redirect targets rather than blacklist
- Validate that redirect URLs are relative paths or belong to the same origin/domain
- Apply the same validation rigorously to all parameters that could control navigation (link, url, redirect, returnUrl, etc.)
- Implement security headers like Content-Security-Policy to restrict redirects
- Regular security audits of Flash content and legacy media players
- Consider deprecating Flash in favor of modern HTML5 implementations with built-in security controls
- Log and monitor redirect attempts to detect suspicious patterns

## Variant hunting
Search for similar patterns in other Flash-based players on Khan Academy or related properties. Check for: other parameter names used for redirects (url, target, href, goto, destination), Flash files embedded in educational platforms, legacy media players accepting external input, and any parameters passed to .swf files that might control navigation. Test variants like 'file', 'displayclick', and other parameters identified in the proof-of-concept.

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1598.002

## Notes
This vulnerability exploits Flash's capabilities to handle external URLs. The use of Flash made this particularly dangerous as users couldn't easily inspect the redirect target before the action occurred. The vulnerability demonstrates how legacy technologies can introduce security gaps even when running on trusted domains. The 'displayclick' parameter suggests the developer was aware of clickable elements but failed to secure the associated redirection.

## Full report
<details><summary>Expand</summary>

Proof: 
http://smarthistory.khanacademy.org/assets/images/media/player.swf?displayclick=link&link=http://google.com&file=1.jpg

STEPS:
Click the link after clicking click the SCREEN and you will be redirected to http://google.com

</details>

---
*Analysed by Claude on 2026-05-24*
