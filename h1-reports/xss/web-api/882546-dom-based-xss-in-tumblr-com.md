# DOM-Based XSS in tumblr.com Share Tool via Malicious Title Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 882546 | https://hackerone.com/reports/882546
- **Submitted:** 2020-05-26
- **Reporter:** keer0k
- **Program:** Tumblr
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** DOM-Based XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in Tumblr's share widget tool that allows attackers to inject malicious JavaScript code through the title parameter. The vulnerability is triggered when a victim reblogs a crafted post and interacts with a specially-crafted link containing a javascript: protocol handler.

## Attack scenario
1. Attacker creates a malicious URL using the share tool endpoint with a javascript: protocol in the title parameter's href attribute
2. Attacker shares this URL to a Tumblr user, enticing them to interact with the post
3. Victim visits the malicious share URL and creates/reblogs the post to their timeline
4. Victim clicks on the injected link (e.g., 'click me') in the reblogged post
5. Victim selects 'open in new tab' option
6. JavaScript payload executes in the victim's browser with their Tumblr session context, allowing account compromise

## Root cause
The share tool widget fails to properly sanitize or encode the title parameter before rendering it in the DOM. The title parameter containing HTML with javascript: protocol handlers is inserted into the page without adequate validation, allowing the browser to interpret and execute the malicious JavaScript.

## Attacker mindset
An attacker would recognize that user-supplied content in share tools is often trusted implicitly. They would test various injection points in URL parameters and discover that the title parameter accepts HTML markup with event handlers or protocol schemes. The multi-step nature of the attack (create post → victim reblogs → victim clicks) suggests they understand Tumblr's content distribution mechanism and user behavior patterns.

## Defensive takeaways
- Implement strict input validation on all URL parameters, particularly those containing user-controlled content that will be rendered as HTML
- Use proper output encoding appropriate to the context (HTML entity encoding for HTML context, URL encoding for URLs)
- Implement Content Security Policy (CSP) headers to prevent inline script execution and restrict javascript: protocol usage
- Sanitize HTML content using a well-tested library (e.g., DOMPurify) that strips dangerous elements while preserving legitimate formatting
- Use DOM-safe methods (textContent instead of innerHTML) when possible
- Validate and whitelist only safe URL protocols (http, https, mailto); reject javascript:, data:, and vbscript: protocols
- Implement security review for all user-facing widget/sharing tools which are common attack vectors

## Variant hunting
Test other share tool parameters (url, selection, shareSource) for similar XSS injection
Investigate if other Tumblr widgets or embedded content features have similar parameter-based XSS
Check if the vulnerability affects different reblog contexts or post types
Test protocol handlers beyond javascript: (data:, vbscript:, etc.)
Examine if attribute-based injection (onerror, onload) works in addition to href-based injection
Test single-step exploitation (direct URL visit without reblog requirement)
Investigate if the 'denied:' prefix mentioned in the report is a bypass mechanism applied to certain payloads

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link
- T1059.007 - Command and Scripting Interpreter: JavaScript

## Notes
The report mentions removing 'denied:' from the link, suggesting Tumblr may have partial client-side filtering that was bypassed. The multi-step attack vector (requiring victim to reblog and click) reduces immediate impact but the session-based context makes account takeover plausible. The use of javascript: protocol combined with comment injection (://http://evil.com/) shows sophisticated payload crafting. The vulnerability class is DOM-based rather than stored XSS, though the malicious content persists through reblogging.

## Full report
<details><summary>Expand</summary>

# Description
Hi, i just found a XSS that i think it's a valid issue and i think it is in scope this time.

To get the XSS the attacker needs to create a post in tumblr.com using `https://www.tumblr.com/widgets/share/tool?url=https%3A%2F%2Fkeerok.github.io%2F&title=%3Ca%20href=%22javascript:alert(document.domain);//http://evil.com/%22%3Eclick%20me%3C/a%3E&selection=click%20in%20the%20link%20after%20reblog&shareSource=chrome_extension` URL and change the link of click me text to `javascript:alert(document.domain);//https://evil.com/` without the "denied:". 

After post the payload , the victim needs to reblog the post in www.tumblr.com and click in "click me" and  in "open" to open in a new tab the URL, after this, XSS will be triggered.

I also attached a video of the PoC:
{F842750}


# Steps to reproduce
1. go to `https://www.tumblr.com/widgets/share/tool?url=https%3A%2F%2Fkeerok.github.io%2F&title=%3Ca%20href=%22javascript:alert(document.domain);//http://evil.com/%22%3Eclick%20me%3C/a%3E&selection=click%20in%20the%20link%20after%20reblog&shareSource=chrome_extension`
2. remove "denied:" from click me link
3. save the post
4. victim reblog the post
5. click in "click me"
6. click in open (Abrir)
7. XSS will be triggered

## Impact

it is possible to perform malicious actions on the victim's account

</details>

---
*Analysed by Claude on 2026-05-12*
