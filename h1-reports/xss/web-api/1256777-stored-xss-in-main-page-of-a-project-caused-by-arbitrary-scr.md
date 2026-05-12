# Stored XSS in Project Main Page via Group Default Initial Branch Name

## Metadata
- **Source:** HackerOne
- **Report:** 1256777 | https://hackerone.com/reports/1256777
- **Submitted:** 2021-07-10
- **Reporter:** joaxcar
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab's project main page where the 'default initial branch name' field in group settings accepts arbitrary JavaScript payloads without sanitization. When a project without an initial repository is created, the unsanitized branch name is displayed in terminal command examples, executing the malicious script for any developer or administrator accessing the project page.

## Attack scenario
1. Attacker creates a GitLab group and navigates to group repository settings
2. Attacker injects malicious JavaScript payload (e.g., <script>alert(1);</script>) into the 'Default initial branch name' field and saves
3. Attacker creates a blank project within the group, triggering XSS on the project main page
4. Attacker invites target users as Developers to the project via validated GitLab invitation emails/notifications
5. Victim clicks invitation link in email and lands on project main page, triggering stored XSS payload execution
6. Attacker's JavaScript executes in victim's browser context, potentially stealing personal access tokens or performing admin actions if victim is administrator

## Root cause
The 'default initial branch name' field accepts arbitrary input without validation or sanitization. The field value is included in two locations on the project main page (terminal command examples) without proper HTML encoding or escaping when rendered to users.

## Attacker mindset
An attacker with group creation privileges seeks to compromise developers and administrators through validated phishing vectors. By leveraging GitLab's own invitation system as a delivery mechanism, the attacker increases victim credibility and click-through rates. The stored nature of the XSS ensures persistence and broad impact across all project members.

## Defensive takeaways
- Implement strict input validation on all configuration fields, especially those displayed to users (whitelist allowed characters for branch names: alphanumeric, hyphens, underscores, slashes)
- Apply context-appropriate output encoding: HTML entity encoding for HTML context, JavaScript escaping for JavaScript context, URL encoding for URL context
- Enforce Content Security Policy (CSP) with strict-dynamic, no unsafe-inline, and no external script sources; set base-uri to 'self' to prevent base tag attacks
- Sanitize all user-controlled data before rendering in HTML templates using library functions (DOMPurify, OWASP sanitizers)
- Implement server-side validation independent of client-side checks
- Apply principle of least privilege: review why developers need access to group settings that affect project display
- Implement security headers: X-Content-Type-Options: nosniff, X-Frame-Options: DENY/SAMEORIGIN
- Add unit and integration tests specifically for XSS vectors in configuration fields
- Consider using template engines with auto-escaping enabled by default

## Variant hunting
Other group/project configuration fields that are displayed to users: project description, group description, custom instance name/domain settings
Any field accepted in settings pages that is rendered in user-facing pages without sanitization: webhook URLs, notification settings, custom CI/CD variables displayed in logs
Similar injection points in issue descriptions, comments, wiki pages where user input is reflected or stored
Avatar URLs, logo fields, or any file reference fields that might execute as scripts
Email template configuration fields that are later rendered in notifications
API endpoints that accept and return configuration values without proper encoding

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (validated phishing via GitLab invitations)
- T1199 - Trusted Relationship (exploiting developer/admin trust in GitLab)
- T1204 - User Execution - Malicious Link
- T1539 - Steal Web Session Cookie (potential token theft)
- T1555 - Credentials from Password Manager (if CSP disabled, can exfiltrate stored credentials)
- T1098 - Account Manipulation (token generation as victim)

## Notes
The vulnerability's impact varies significantly based on CSP configuration: GitLab.com's CSP mitigates direct script execution but allows base-uri manipulation for link redirection attacks; self-hosted instances without proper CSP allow full arbitrary script execution including personal access token generation. The attack chain is particularly effective because GitLab's own notification system validates the attack vector, dramatically increasing victim trust. The requirement that victims be at least Developers is not a significant limitation since attackers can invite users to their malicious project. The PoC demonstrates both the technical vulnerability and social engineering effectiveness.

## Full report
<details><summary>Expand</summary>

### Summary

A stored XXS exists in the main page of a `project`. By changing the "default branch name" of a group a malicious user can inject arbitrary JavaScript into the main page of a project. Any user that is either at least developer of the project, or an administrator of the GitLab instance, and access the project URL will trigger the payload.

The field "default branch name" under https://gitlab.com/groups/group_name/-/settings/repository accepts arbitrary text (long JavaScript strings as an example). When a project without a initial repository is created in the group the developers are presented with an information page with example terminal commands to execute to set up a repository. This information includes two unzanatized inclusions of the "default branch name", resulting in execution of the JavaScript payload.
{F1371756}

As a default self-hosted GitLab instance does not enforce any CSP rules any javascript can be called. Including inclusion of external script files (<script src="external_script"></script>). On GitLab.com I have not been able to bypass the CSP except from changing the `base-uri` which causes all links on the page(including navigation bars) to point to the attackers site (with payload `<Base Href="attacker_site">`).

On a self-hosted instance without proper CSP I was able to generate `personal access tokens` from the victim that could be extracted by the attacker to get complete access to the victims content and actions. If the victim is an Administrator this leads to complete access to the system. (I will post a script PoC when I have cleaned it up)

As I mentioned, the victim needs to be at least a `Developer` on the project (if not a site admin) when accessing the project main page. This is not a problem (rather an asset) for the attacker. All the attacker needs to do is invite targeted victim users as `Developers` to the project. This will trigger GitLab to send out information to the victim (emails or notifications) that will work as validated phishing links (see image below). The victim just need to click the link in the email and land on the project main page.
{F1371755}

### Steps to reproduce

1. Create two users, `attacker01` and `victim01`
2. Log in as `attacker01`
3. Create a group `attack_group` by visiting https://gitlab.domain.com/groups/new#create-group-pane
4. Go to https://gitlab.domain.com/groups/attack_group/-/settings/repository and expand the "Default initial branch name" tab
5. Enter `<script>alert(1);</script>` as "Default initial branch name" and click "save changes"

{F1371757}

6. Go to https://gitlab.domain.com/groups/attack_group and click the button "New project" and choose to create a "Create blank project"
7. Name the project `attacking_project` and click "Create project"
8. Now the project will load and the alert should pop up.

{F1371758}

optional:
9. On the project main page click the "Invite members" button and invite `victim01` as a Developer
10. Log in with `victim01`
11. Visit https://gitlab.domain.com/attack_group/attacking-project and the script will run for the victim as well

### Impact

Stored XXS capable of arbitrary script execution. Impact depends on the instance CSP settings.

### Examples

If an administrator of GitLab.com visit https://gitlab.com/attack_xxs_group/test3 (a private group and project) one can see that ALL links on the site (all navigation and actions) are redirected to google.com. This is caused by the payload `<Base Href="//www.google.com">`

### What is the current *bug* behavior?

Arbitrary JavaScript is executed on a project main page

### What is the expected *correct* behavior?

The branch name should be sanitized and checked for bad input, and the included branch name should be sanitized when displayed.

### Output of checks

This bug happens on GitLab.com

But CSP removes most of the impact

#### Results of GitLab environment info

I did not manage to run the environment script. I tried this on a Azure hosted GitLab server created from the Azure store.

## Impact

Stored XXS capable of arbitrary script execution. Impact depends on the instance CSP settings. If CSP is not properly set the attacker can execute arbitrary commands as the victim and/or generate `personal access tokens` for full account access. If an Administrator gets compromised, this could lead to complete instance access.

On GitLab.com an attacker can change the `base-uri` to make all links redirect to the attacker's site

</details>

---
*Analysed by Claude on 2026-05-12*
