# Stored XSS in Intense Debate Comment System via Image Tags

## Metadata
- **Source:** HackerOne
- **Report:** 1039750 | https://hackerone.com/reports/1039750
- **Submitted:** 2020-11-20
- **Reporter:** hundredpercent
- **Program:** Intense Debate
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
Intense Debate's comment system fails to properly sanitize user-supplied HTML when the 'allow images in comments' feature is enabled, allowing authenticated users to inject malicious JavaScript via img tag event handlers. This stored XSS payload executes in the context of admin/moderator accounts viewing comments, enabling session hijacking and content manipulation attacks.

## Attack scenario
1. Attacker enables 'allow images in comments' feature in Intense Debate moderation dashboard
2. Attacker crafts comment containing img tag with malicious onload event handler (e.g., stealing cookies or executing JavaScript)
3. Attacker submits comment through blog comment form
4. Comment is stored in database without proper sanitization or encoding
5. Admin/moderator views comments in moderation panel, triggering the stored XSS payload
6. Malicious JavaScript executes in admin's browser context, exfiltrating session tokens or performing unauthorized actions

## Root cause
Intense Debate implements a whitelist approach allowing img tags in comments but fails to strip or encode event handler attributes (onload, onerror, etc.). The application trusts user input when the image feature is enabled and does not apply Content Security Policy or proper output encoding when rendering stored comments.

## Attacker mindset
Low-skill opportunist exploiting a logical gap in the sanitization logic. The attacker recognizes that explicitly allowing images creates an assumption of safety, but overlooks the need to block dangerous event handlers. This represents a 'feature misuse' attack where legitimate functionality is weaponized.

## Defensive takeaways
- Implement strict HTML sanitization libraries (DOMPurify, bleach, etc.) that strip ALL event handler attributes even in whitelisted tags
- Use attribute-based sanitization: whitelist only safe attributes (src, alt) for img tags, explicitly blacklist on* event handlers
- Apply Content Security Policy (CSP) with strict rules to block inline script execution and limit script sources
- Encode all user-generated content during output using context-appropriate encoding (HTML entity encoding for HTML context)
- Implement Security Headers (X-XSS-Protection, X-Content-Type-Options) as defense-in-depth
- Conduct security review of all user-configurable features that relax input restrictions
- Test sanitization against both common and obscure XSS payloads (event handlers, SVG, data URIs, HTML5 constructs)

## Variant hunting
Test other event handlers: onerror, onmouseover, onmouseenter, onfocus, onchange
Try SVG tags with embedded script: <svg onload='alert(1)'>
Test data URI protocol in img src with base64-encoded JavaScript
Check if video/audio tags with event handlers bypass restrictions
Test HTML5 data attributes combined with CSS expressions or other vectors
Verify if other user-facing input fields (author name, website URL) also lack sanitization
Check for bypass via encoding (URL encoding, unicode, HTML entities) in payload itself

## MITRE ATT&CK
- T1190
- T1199
- T1566
- T1204

## Notes
The report demonstrates good practical exploitation with reproduction steps and impact assessment. However, it lacks technical depth (no payload variation testing, no discussion of sanitization mechanisms attempted). The writeup would benefit from: (1) clarifying if XSS is reflected or stored upon admin view, (2) confirming execution context and access level, (3) testing sanitization robustness against encoding bypasses. The 'helpful video' reference suggests clear PoC was provided. Security implication is significant as comment systems are high-value targets for account compromise.

## Full report
<details><summary>Expand</summary>

Hi Team,

## _Summary:_
The  Intense Debate comment system is vulnerable to stored xss by users , this would allow for atacking admins/users on the blog ,

## Platform(s) Affected:
*  Intense Debate comment system



________________________________________________________________________________________
________________________________________________________________________________________

## _Steps To Reproduce:_


  1. Go to **intensedebate.com/moderate/{{-ID-}}**
  2. Go to comments > allow images in comments
  3. Now go to your blog and add this payload as comment :

```html
<img src="https://intensedebate.com/images/a-addblog.png" onload="alert()">
```
  4. You'll notice the alert will pop as result for the "onload" attribute ,
  

________________________________________________________________________________________
________________________________________________________________________________________


A helpful video :
{F1087899}

## Impact

* Stealing cookie and secter tokens 
* Editing html/css/js content for phishing attacks



Thanks for taking your valuable time to read and validate this report

</details>

---
*Analysed by Claude on 2026-05-12*
