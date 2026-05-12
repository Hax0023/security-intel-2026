# Persistent XSS via Email in Merge Request Notifications

## Metadata
- **Source:** HackerOne
- **Report:** 496973 | https://hackerone.com/reports/496973
- **Submitted:** 2019-02-16
- **Reporter:** mario-areias
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, HTML Injection
- **CVEs:** CVE-2019-5471
- **Category:** web-api

## Summary
GitLab failed to sanitize branch names in merge request email notifications, allowing attackers to inject arbitrary HTML/JavaScript code. When a reviewer receives an email notification about a merge request with a malicious branch name like `<script>alert(1)</script>`, the code executes in the email client's HTML rendering context. This enables attackers to target any GitLab user by adding them as repository members and assigning them to merge requests.

## Attack scenario
1. Attacker forks a public GitLab repository or controls their own repository
2. Attacker creates a branch with XSS payload in the name (e.g., `<script>alert(1)</script>` or `<img src=x onerror=malicious_code>`)
3. Attacker creates a merge request from the malicious branch to a target repository
4. Attacker assigns a reviewer (either a repository maintainer or a user added as member) to the merge request
5. Target receives email notification containing unsanitized branch name with embedded malicious script
6. Email client renders the HTML notification and executes the injected JavaScript payload

## Root cause
The GitLab notification templates (`notify/new_merge_request_email.html.haml` and `notify/repository_push_email.text.haml`) directly interpolated branch names into HTML email content without proper sanitization or HTML entity encoding. This allowed special characters and HTML/JavaScript tags to be interpreted as code rather than literal text.

## Attacker mindset
An attacker recognized that email notifications are often trusted by users and rendered as HTML, creating a privilege escalation vector. By leveraging GitLab's feature to add arbitrary users as repository members, the attacker could craft targeted phishing campaigns or deliver payloads to specific users while appearing to come from GitLab's official notifications.

## Defensive takeaways
- Always sanitize and HTML-encode user-controlled input when rendering HTML emails
- Implement output encoding at the template/view layer using framework-provided escaping functions
- Apply the principle of least privilege: restrict who can add members to repositories and create branches
- Validate branch names on creation to restrict dangerous characters (< > / etc.)
- Use Content Security Policy (CSP) headers in emails where supported
- Implement server-side email filtering that detects suspicious patterns in notification content
- Test email notification rendering across multiple email clients to verify escaping works correctly

## Variant hunting
Check other email templates for similar unsanitized branch/commit/user data injection points
Test commit messages, file paths, and other user-controllable metadata in email notifications
Verify if similar vulnerabilities exist in other GitLab notification types (issues, comments, wiki changes)
Test email headers (From, Reply-To) for header injection attacks
Check if API responses containing branch names properly escape output for JSON/XML contexts

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
The vulnerability demonstrates the importance of defense-in-depth: even though modern email clients have XSS protections, the attack remains viable. The attacker's ability to target specific users by adding them as repository members significantly increases the impact beyond simple self-XSS. The report correctly identifies this as medium severity due to reach and targeting capability despite email client defenses.

## Full report
<details><summary>Expand</summary>

**Summary:**
The vulnerability consists in the ability to create branch names that contain characters such as `<>/`. This branch name is sent via e-mail which is rendered as HTML.

**Description:**
One way to exploit this is by forking a repository. Then an attacker would create a branch called `<script>alert(1)</script>` and make a simple change. Now the attacker creates a merge request to the original repository and assign a reviewer to it. The reviewer will receive the e-mail with the branch name not sanitised. 

Another way to exploit is to by adding Gitlab users to a repository the attacker controls and assign them to review merge requests.

## Steps To Reproduce:

Note: These instructions work on GDK with the latest version. I wasn't sure if it is allowed to test something like on gitlab.com

  1.  Choose a public repository and fork it (let's say HTML5 boilerplate)
  2. Go through the repository main page http://yourserver:3000/root/html5-boilerplate
  3. Click on the button + button and select New File
  4. Create any file but choose a different target branch (something like <script>alert(1)</script>
  5. Gitlab will direct you to a page to create a new merge request from your recently create branch to master. Ignore that.
  6. Open a New Merge Request
  7. Select Source Branch as your fork and the recently created branch
  8. As for Target branch select the original repo and master
  9. Click submit
10. Select one the maintainers of the original repo 
11. Submit
12. Go to letter opener (/rails/letter_opener/)
13. See the alert popping up.

The steps above only require UI, but an attacker can create a branch name through git client as well. The create branch option UI protects against this attack.

There is also another version of the attack, where a repository owner can add any Gitlab users to become members of her repo. The attacker now create a Merge Request in his own repo and assign the new member to it. Same result. 

## Supporting Material/References:

* Vulnerable code at `gitlab-ce/app/views/notify/new_merge_request_email.html.haml` line 6. This is the exploit above.
* Vulnerable code at `gitlab-ce/app/views/notify/repository_push_email.text.haml` line 49. I haven't created an exploit for this one, but I would assume it should be similar.

## Impact

E-mail clients nowadays are well protected against XSS. However, a malicious user could use Gitlab's name to mislead users. The problem with this vulnerability is the reach. It is my understanding, an attacker can add whoever is a Gitlab user as a member of her own repo. So she could send malicious e-mails to them. I would usually say that is a low vulnerability, however, given the number of users that could be affected I would say is a medium

</details>

---
*Analysed by Claude on 2026-05-12*
