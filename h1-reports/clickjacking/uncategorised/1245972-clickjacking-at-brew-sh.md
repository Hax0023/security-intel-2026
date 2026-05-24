# Clickjacking Vulnerability at brew.sh

## Metadata
- **Source:** HackerOne
- **Report:** 1245972 | https://hackerone.com/reports/1245972
- **Submitted:** 2021-06-28
- **Reporter:** sai545
- **Program:** Homebrew (brew.sh)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redress Attack, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The brew.sh website lacks an X-Frame-Options HTTP response header, making it vulnerable to clickjacking attacks where malicious actors can embed the site in an iframe and trick users into performing unintended actions. An attacker can overlay transparent or disguised frames to hijack user clicks or keystrokes, potentially leading to credential theft or unauthorized actions.

## Attack scenario
1. Attacker creates a malicious webpage that embeds brew.sh in an invisible or transparent iframe
2. Attacker overlays fake UI elements (buttons, forms) on top of the framed content using CSS positioning and opacity
3. Victim visits attacker's webpage believing they are interacting with legitimate content
4. Victim's clicks intended for the fake overlay are actually registered on the embedded brew.sh frame
5. Attacker harvests credentials, triggers unintended actions, or captures keystrokes through invisible text input fields
6. Victim remains unaware their interactions have been redirected to the embedded frame

## Root cause
The web server hosting brew.sh does not implement the X-Frame-Options HTTP response header (or Content-Security-Policy frame-ancestors directive) to restrict embedding in iframes, allowing any external website to frame the content without restrictions.

## Attacker mindset
An attacker seeks to perform social engineering attacks by leveraging user trust in the Homebrew brand. They aim to trick users into clicking on elements within a framed context (e.g., install malicious packages, reveal credentials, or trigger downloads) by disguising malicious overlays as legitimate Homebrew interface elements.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all HTTP responses
- Alternatively, use Content-Security-Policy header with frame-ancestors directive (CSP: frame-ancestors 'self')
- Regularly test for missing clickjacking protections in security scanning and penetration testing
- Consider implementing frame-busting JavaScript code as defense-in-depth for older browser compatibility
- Apply security headers consistently across all pages and endpoints
- Educate users about verifying URL bar and being cautious with overlaid content

## Variant hunting
Test other Homebrew subdomains and related properties for X-Frame-Options header presence
Check if CSP frame-ancestors directive is implemented as an alternative defense
Verify if the vulnerability extends to authenticated pages or sensitive functionality within brew.sh
Test for keystroke hijacking variants by overlaying transparent input fields
Assess if other open-source project websites share similar misconfigurations
Look for draggable iframe vulnerabilities and CORS misconfigurations that could compound the issue

## MITRE ATT&CK
- T1189: Drive-by Compromise
- T1598: Phishing - Spearphishing Link
- T1055: Process Injection (in context of framing attacks)
- T1566: Phishing

## Notes
This is a straightforward clickjacking vulnerability report with clear documentation. The severity is medium rather than high because brew.sh is primarily an informational/download site without sensitive user interactions like banking or sensitive account management. However, it could be elevated if the site hosts package installation scripts or user authentication. The POC is basic but effective. The report lacks specific impact demonstration but correctly identifies the vulnerability class and remediation path.

## Full report
<details><summary>Expand</summary>

hello ,
While performing security testing of your website i have found the vulnerability called Clickjacking.
URL is in scope and vulnerable to Clickjacking.
What is Clickjacking ?
Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or taking control of their computer while clicking on seemingly innocuous web pages.
The server didn't return an X-Frame-Options header which means that this website could be at risk of a clickjacking attack. The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a <frame> or <iframe>. Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
vulnerable url:
https://brew.sh/
no x-frames in the above website 
For POC we can use either the html script or burpsuite
script:
<html lang="en-US">
<head>
<meta charset="UTF-8">
<title>I Frame</title>
</head>
<body>
<h3>clickjacking vulnerability</h3>
<iframe src="https://brew.sh" width="700px"></iframe>
</body>
</html>

## Impact

Using a similar technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
