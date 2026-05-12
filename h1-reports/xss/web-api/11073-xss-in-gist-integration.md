# XSS in Gist Integration

## Metadata
- **Source:** HackerOne
- **Report:** 11073 | https://hackerone.com/reports/11073
- **Submitted:** 2014-05-06
- **Reporter:** zemnmez
- **Program:** Slack
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Sanitization, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
Slack's gist integration failed to properly sanitize gist filenames containing SVG payloads, allowing attackers to execute arbitrary JavaScript through specially crafted gist names. When a gist with a malicious filename was shared via Slack and accessed through the 'raw' or 'new window' preview pages, the payload would execute in the victim's browser.

## Attack scenario
1. Attacker creates a GitHub gist with a filename containing SVG payload: "><svg onload=alert(1)>
2. Attacker enables gist integration in Slack workspace and shares the link to the malicious gist in a channel
3. Slack embeds or previews the gist integration, extracting the filename without proper sanitization
4. Victim clicks on the 'raw' or 'new window' link to view the gist content
5. Browser renders the preview page which includes the unsanitized filename in the DOM
6. SVG onload event executes, running arbitrary JavaScript in the victim's security context

## Root cause
Slack's gist integration did not properly HTML-encode or sanitize gist filenames when rendering them in preview pages. The filename was directly inserted into the HTML response without escaping special characters, allowing SVG injection and event handler execution.

## Attacker mindset
An attacker would recognize that file metadata (like filenames) is often overlooked during sanitization efforts since developers assume it's benign user-generated content. By leveraging the gist integration feature's trust in GitHub data and Slack's preview rendering, they could bypass typical input validation that might exist on form fields.

## Defensive takeaways
- Always HTML-encode all user-controlled data before inserting into HTML context, regardless of source (internal/external APIs)
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Sanitize metadata fields (filenames, titles, descriptions) with the same rigor as body content
- Use templating engines that auto-escape by default rather than string concatenation
- Validate third-party integrations and API responses don't introduce injection vectors
- Apply output encoding based on context: HTML, JavaScript, URL, CSS encoding as appropriate

## Variant hunting
Search for other integrations that display third-party metadata (filenames, commit messages, issue titles) without sanitization
Test preview/embed features of document sharing integrations (Google Drive, Dropbox, OneDrive)
Check notification systems that include user-generated content from external sources
Review any feature showing file/folder names in rendered HTML contexts
Test markdown rendering in integration previews for injection vectors

## MITRE ATT&CK
- T1190
- T1080

## Notes
This vulnerability demonstrates the importance of consistent output encoding across all user-facing content, not just primary input fields. The trust relationship between platforms (Slack trusting GitHub gist data) created an implicit assumption of safety that the attacker exploited. The use of SVG with onload handlers is a common XSS technique that bypasses filters looking only for script tags.

## Full report
<details><summary>Expand</summary>

1. Create a gist called:
"><svg onload=alert(1)>
2. have gist integration enabled and put a link in a slack chat
3. Visit the 'raw' or 'new window' pages for this gist, for example: https://outpost.slack.com/files/zemnmez/F029MDY33/___svg_onload_alert_1__



</details>

---
*Analysed by Claude on 2026-05-12*
