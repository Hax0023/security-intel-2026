# Stored XSS on Issue details page via Markdown image syntax

## Metadata
- **Source:** HackerOne
- **Report:** 384255 | https://hackerone.com/reports/384255
- **Submitted:** 2018-07-19
- **Reporter:** 8ayac
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Sanitization, Markdown Parsing Vulnerability
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists on GitLab's Issue details page where malicious JavaScript can be injected through the issue description field using malformed Markdown image syntax. The payload persists and executes when the issue details page is viewed by any user, affecting both issue creation and editing functionality.

## Attack scenario
1. Attacker authenticates to GitLab and creates a new project or identifies an existing one with write permissions
2. Attacker clicks 'New issue' or edits an existing issue and enters malicious payload in the Description field: ![xss" onload=alert(1);//](a)
3. The Markdown parser fails to properly sanitize the malformed image syntax, allowing the onload event handler to be injected into the DOM
4. Attacker submits/saves the issue, and the malicious payload is stored in the database
5. Any user (including administrators) who views the issue details page triggers the JavaScript execution in their browser context
6. Attacker can steal session tokens, perform actions on behalf of victims, or escalate privileges depending on user context

## Root cause
GitLab's Markdown parser and HTML sanitization logic failed to properly validate and escape attributes in image syntax. The parser accepted malformed image syntax like ![xss" onload=...](url) and did not adequately sanitize event handler attributes before rendering to the client.

## Attacker mindset
An authenticated attacker recognized that image syntax in Markdown descriptions wasn't properly escaped, allowing attribute injection. They tested the attack across browsers to understand scope and confirmed persistence by editing existing issues, demonstrating this wasn't a reflection-only vulnerability.

## Defensive takeaways
- Implement strict HTML sanitization libraries (e.g., DOMPurify, Bleach) with whitelist-based attribute filtering for all user-generated content
- Use context-aware output encoding: escape HTML entities in Markdown-generated content before rendering
- Validate and normalize Markdown syntax before parsing; reject malformed constructs rather than attempting to interpret them
- Implement Content Security Policy (CSP) headers with strict script-src directives to mitigate XSS impact
- Apply defense-in-depth: sanitize at input validation, processing, and output rendering stages
- Regularly audit Markdown parsing libraries for known XSS vulnerabilities and keep dependencies updated
- Conduct security testing specifically targeting attribute injection in various markup contexts

## Variant hunting
Test for similar XSS in other Markdown-rendered fields (comments, merge request descriptions, wiki pages, commit messages). Investigate other Markdown syntax elements for attribute injection: `[link](url" onclick=alert(1))`, `[text](javascript:alert(1))`, table syntax, code block syntax. Test SVG/XML injection through image URLs. Examine user-generated content in other projects (Jira, GitHub, Gitea) using Markdown rendering.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1566 - Phishing
- T1539 - Steal Web Session Cookie
- T1534 - Internal Spearphishing

## Notes
This is a classic Stored XSS with high impact due to persistence and automatic execution. Browser variability (Firefox/Chrome affected, IE11/Edge not) suggests the vulnerability may depend on specific HTML parsing behavior. The use of image syntax as an injection vector is a common bypass technique against basic sanitizers that focus on script tags but miss event handler attributes. The writeup demonstrates good security research methodology by testing multiple reproduction methods (creation vs. editing) and multiple browsers.

## Full report
<details><summary>Expand</summary>

**Summary:**
The detail page of Issue (the page that provides the content of an Issue) is vulnerable to Stored XSS.

**Description:**
The two exploits are via the function of submittin an issue or the function of editing an issue.
This vulnerability is reproduced in `Firefox` and`Chrome`. `IE11` and`Edge` are not. I did not test the reproduction on other browsers.

## Steps To Reproduce:
1. Sign in to GitLab.
2. Click the "[+]" icon.
3. Click "New Project".
4. Fill out "Project name" form with "PoC".
5. Check the check box of "Public".
6. Click "Issues"
7. Click "New issue" button.
8. Fill out the each form as follows:
    * Title: PoC
    * Description: `![xss" onload=alert(1);//](a)`
9. Click "Submit issue".

Furthermore, when editing an already existing issue, you can also reproduce by entering A in the "Description" form and saving it.

## Impact

The security impact is the same as any typical Stored XSS.

Thank you!

</details>

---
*Analysed by Claude on 2026-05-12*
