# Stored XSS in Project Notifications via Malicious Project Name Change

## Metadata
- **Source:** HackerOne
- **Report:** 1070859 | https://hackerone.com/reports/1070859
- **Submitted:** 2021-01-04
- **Reporter:** optional
- **Program:** Logitech (oslo.io)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
An editor with project modification permissions can rename a project to contain malicious HTML/JavaScript that executes when project owners view notifications. The vulnerability persists in the notification dropdown, affecting any user who receives notifications about the renamed project.

## Attack scenario
1. Attacker with editor permissions on a shared project navigates to project settings
2. Attacker modifies project name field to include malicious payload (e.g., <img src=x onerror='malicious_js()'>)
3. System stores the unsanitized project name in the database
4. Project owner logs in and clicks the notification bell to view project updates
5. Notification UI renders the project name without proper HTML encoding
6. Malicious JavaScript executes in the context of the owner's session, allowing privilege escalation or account takeover

## Root cause
The application fails to properly sanitize and validate user input in the project name field during rename operations. Additionally, the notification rendering component does not HTML-encode the project name before inserting it into the DOM, allowing stored XSS payloads to execute.

## Attacker mindset
An insider threat or compromised editor account seeking to escalate privileges. The attacker exploits the trust relationship between project members and the lack of input validation on admin-visible notifications. By leveraging editor permissions (lower barrier), they can compromise higher-privileged accounts (project owners) without direct owner access.

## Defensive takeaways
- Implement strict input validation on all user-modifiable fields including project names (whitelist allowed characters, set length limits)
- Apply HTML entity encoding/escaping on all user-controlled data before rendering in DOM (use framework-provided escaping mechanisms)
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Implement output encoding at the template/view layer for notification rendering
- Apply the principle of least privilege - review editor permission scope and consider limiting project rename capability
- Conduct security code review of notification rendering components across the application
- Implement automated security testing (SAST/DAST) to detect XSS vulnerabilities in input fields and rendered content

## Variant hunting
Check other user-modifiable fields that appear in notifications (project description, labels, tags, comments)
Audit all notification types for similar XSS patterns (invitations, project updates, permission changes)
Test other permission levels (viewer, commenter, etc.) for similar vulnerabilities
Examine email notifications containing project names for HTML injection
Review admin/settings pages that display project metadata for stored XSS
Test project import/bulk operations that may accept project names
Check API endpoints for project name updates - verify they apply same sanitization

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1567.002
- T1539

## Notes
This is a privilege escalation vector combining stored XSS with permission-based abuse. The vulnerability is particularly dangerous because notifications are trust mechanisms - users expect safe content in system notifications. The attack chain requires editor-level access, making it a realistic insider threat scenario or post-compromise lateral movement technique. The use of project rename (typically an expected action) as the attack vector demonstrates social engineering potential. Recommend immediate patching and audit of all user-controlled fields in notification rendering.

## Full report
<details><summary>Expand</summary>

Hey Logitech team.

## Summary:
It is possible for an editor on a project to rename a project to a malicious HTML element, which when opened in the notification dropdown will render and fire javascript.

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Invite user to join the project and allow editor permissions.
  1. As the editor account, click on any of the projects and click rename. Insert malicious HTML there.
  1. Log in as the owner of the project directory and click on the notification bell on the top right. This will cause the XSS to fire.

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

_Fig 1: Inviting the editor to project_
{F1143360}

_Fig 2: Notification Settings for Owner:_
{F1143367}

_Fig 3: Editor Changing Project name to malicious object_
{F1143363}
{F1143364}

_Fig 4: Logging in as the owner again_
{F1143361}

_Fig 5: Opening Notification Bell_
{F1143362}

## Impact

The impact of this vulnerability is that users who are invited onto projects as an editor are able to inject malicious javascript such as keyloggers to escalate their privileges or perform actions as other users.

</details>

---
*Analysed by Claude on 2026-05-12*
