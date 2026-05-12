# Persistent XSS via filename in projects

## Metadata
- **Source:** HackerOne
- **Report:** 662204 | https://hackerone.com/reports/662204
- **Submitted:** 2019-07-28
- **Reporter:** foobar7
- **Program:** Talk / Spreed
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Cross-Site Scripting (XSS), Persistent/Stored XSS, Improper Output Encoding
- **CVEs:** CVE-2019-15619
- **Category:** web-api

## Summary
Talk/Spreed 6.0.3 fails to properly encode filenames when displaying them in the projects tab during mouseover interactions, allowing authenticated users to inject persistent XSS payloads via specially crafted filenames. An attacker can exploit this to execute arbitrary JavaScript in the context of victim users' browsers, potentially leading to account takeover and unauthorized access to files and conversations.

## Attack scenario
1. Attacker creates a file with a malicious filename containing XSS payload: test'"><img src=x onerror=alert(document.location)>.txt
2. Attacker shares the malicious file with the victim user
3. Attacker creates a new conversation and invites the victim as a participant
4. Attacker adds the malicious file as a project link within the conversation
5. Victim opens the conversation and navigates to the projects tab
6. Victim hovers their mouse over the file symbol, triggering the unencoded filename display and executing the injected JavaScript payload

## Root cause
The application echoes the filename without proper HTML encoding when rendering the tooltip/hover information in the projects tab. User-controlled input (filename) is directly inserted into the DOM without sanitization, allowing HTML/JavaScript injection.

## Attacker mindset
An attacker with low-level authenticated access identifies that filenames are displayed without encoding in the UI. They recognize that projects are shared within conversations and that hover interactions trigger tooltip displays, making this a reliable vector for persistent XSS. The attacker leverages file sharing and conversation features to inject malicious payloads that execute when victims interact with projects.

## Defensive takeaways
- Implement strict output encoding for all user-controlled data before rendering in HTML context, particularly for filenames and file-related metadata
- Use templating engines with auto-escaping enabled (e.g., Angular, React with proper escape functions)
- Apply Content Security Policy (CSP) headers to mitigate XSS impact by restricting inline script execution
- Sanitize and validate filenames at upload time, rejecting or escaping special characters that could be used for injection
- Implement comprehensive input validation for filenames, restricting allowed characters to alphanumeric, underscores, hyphens, and dots
- Use security-focused libraries like OWASP ESAPI or DOMPurify for sanitization if dynamic HTML construction is necessary
- Conduct regular security testing of tooltip/hover interactions and all dynamic content rendering
- Implement browser security headers (X-XSS-Protection, X-Content-Type-Options) as defense-in-depth measures

## Variant hunting
Check all file metadata fields (description, tags, comments) for similar encoding issues
Audit other tooltip/hover elements throughout the application for unencoded user input
Test other file operations (rename, move, copy) where filenames might be displayed
Examine avatar uploads and profile fields for similar XSS vulnerabilities
Check conversation titles and participant names for persistent XSS via similar mechanisms
Review any location where filenames are displayed in HTML attributes without encoding
Test for DOM-based XSS in JavaScript event handlers related to file interactions

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability required low privilege access and user interaction (hovering), reducing immediate impact but making it highly reliable for targeted attacks. The persistent nature means the payload remains in the conversation for all participants. Admin accounts being particularly valuable targets elevates the severity. The vulnerability demonstrates a common mistake of trusting user-generated content (filenames) as safe to display without encoding.

## Full report
<details><summary>Expand</summary>

CVSS
----

Medium 5.4 [CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N](https://www.first.org/cvss/calculator/3.0#CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N)

Description
-----------

Affected: Talk / Spreed 6.0.3

The name of a file is echoed without encoding when moving the mouse onto it in the projects tab of a conversation, leading to persistent XSS.

A successful attack requires an account with low-level permissions as well as a usual amount of user interaction (interacting with the project of a talk in a usual manner).

Successful exploitation allows the attacker to take over the account of the attacked user. If the attacked user is an administrator, this would allow a user full access to the application & files.

POC
--- 

To place the payload as the attacker:

- create a file named `test'"><img src=x onerror=alert(document.location)>.txt`. Share the file with the victim. 
- Create a new conversation: Talk -> new conversation -> enter a name.
- Invite the victim: Participants -> Add participant -> select the user
- Add a project: Projects -> Add a project -> Link to a file -> select the file from step 1. 

To trigger the payload as the victim: 

- open the conversation -> projects -> hover over the file symbol to trigger the payload.

## Impact

Successful exploitation allows an attacker to read any data the attacked user has access to, or to perform arbitrary requests the user can perform.

</details>

---
*Analysed by Claude on 2026-05-12*
