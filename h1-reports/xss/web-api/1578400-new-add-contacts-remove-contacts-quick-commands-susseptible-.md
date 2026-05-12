# XSS in GitLab Customer Relations /add_contacts and /remove_contacts Quick Commands via Contact Name Fields

## Metadata
- **Source:** HackerOne
- **Report:** 1578400 | https://hackerone.com/reports/1578400
- **Submitted:** 2022-05-22
- **Reporter:** cryptopone
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Input Validation Failure
- **CVEs:** CVE-2022-1948
- **Category:** web-api

## Summary
GitLab 15.0.0 introduced a new Customer Relations feature with quick commands /add_contacts and /remove_contacts. The contact firstname and lastname fields are not properly HTML-escaped when displayed in the quick command autocomplete popup, allowing stored XSS execution. An attacker can inject malicious JavaScript through contact creation that executes when any user attempts to use these quick commands.

## Attack scenario
1. Attacker creates a group and enables the Customer Relations feature in group settings
2. Attacker creates a contact with firstName or lastName set to <script>alert(document.domain)</script>
3. Contact is stored in the database with unescaped payload
4. Victim creates an issue in a project under the same group
5. Victim types /add_contacts quick command in the issue description
6. The autocomplete popup renders contact list without HTML escaping, executing the stored JavaScript payload in victim's context

## Root cause
The Customer Relations quick command implementation fails to HTML-escape user-controlled contact data (firstname/lastname) when rendering the autocomplete suggestion list. The vulnerability exists at the rendering layer where contact information is displayed without proper sanitization.

## Attacker mindset
An attacker with ability to create contacts in a Customer Relations-enabled group can persistently inject XSS payloads that affect all users attempting to use the quick commands. This is a low-effort attack requiring only group access and basic XSS knowledge.

## Defensive takeaways
- Always HTML-escape user-supplied data before rendering in HTML context, especially in dynamic UI components like autocomplete popups
- Implement Content Security Policy (CSP) to prevent inline script execution as defense-in-depth
- Apply input validation to reject or sanitize special characters in contact name fields
- Use templating engines with automatic escaping by default
- Add security tests to verify quick command autocomplete rendering with special characters
- Conduct security review of new features, especially those handling user input in UI suggestions

## Variant hunting
Check other quick commands for similar rendering vulnerabilities (/add_due_date, /assign, /label, etc.)
Test other user-facing fields in Customer Relations (email, organization, etc.) for XSS
Examine other GitLab autocomplete features for identical escaping issues
Search for similar patterns in issue/merge request quick commands that display user data
Test if the vulnerability affects other markdown preview contexts where contacts are referenced

## MITRE ATT&CK
- T1190
- T1566
- T1204

## Notes
This is a stored XSS vulnerability affecting all users in a group where an attacker has contact creation privileges. The impact is user session hijacking, credential theft, and malicious actions on behalf of victims. The vulnerability was reproducible on both self-hosted GitLab 15.0.0 and gitlab.com. The fix requires proper output encoding in the quick command autocomplete rendering component.

## Full report
<details><summary>Expand</summary>

### Summary

In Gitlab 15.0.0 a new Customer Relations feature was added that allows us to use quick actions to find the contact we wish to select.

However, I noticed that if I set the contact's first name or last name to <script>alert(document.domain)</script> we can get the XSS to trigger when we are attempting to use the quick commands to add/remove a contact.

### Steps to reproduce

1. Create a new group.
1. Once the group is created, navigate to the Settings -> General options for the group.
1. Expand the section "Permissions and group features" and under "Customer Relations" make sure "Enable customer relations" is selected.
1. Return back to the group page. On the left side of the screen a new menu option will appear titled "Customer relations". Select it.
1. Create a new contact with "First name" set to "`<script>alert(document.domain)</script>`" and "Last name" set to "`<script>alert(document.domain)</script>`". Provide an email address and save your changes.
1. The user you created in the previous step should now appear as a contact on the Customer Relations page.
1. Go to the create new project URL (https://gitlab.com/projects/new#blank_project) and under Project URL, select the Group you created earlier. Give the project a name Ex. "CustomerProject".
1. Once the project has been created on the left side of the project page select "Issues" and then click "New Issue".
1. In the description pane type "/add_contacts" so the popup appears, then press "enter" to trigger the XSS.

### Impact

Users attempting to utilize the quick commands /add_contacts or /remove_contacts could inadvertently trigger XSS while attempting to add/remove a customer to an issue.

### Examples

This bug was discovered originally on my self-hosted 15.0.0 but is reproducible on gitlab.com.

Create a contact with the payload in firstname and lastname fields
{F1740002}

Create a new issue and type "/add_contacts" in the markdown text area to trigger the popup to appear
{F1740003}

Press enter, which will trigger the XSS when attempting to load the list of contacts
{F1740004}

### What is the current *bug* behavior?
The HTML special characters are not escaped, allowing an iframe to be injected into the page with XSS.

### What is the expected *correct* behavior?

The HTML special characters would be escaped and shown in the diagram.

### Output of checks

This bug is reproducible on Gitlab.com

#### Results of GitLab environment info

```System information
System:         Ubuntu 20.04
Proxy:          no
Current User:   git
Using RVM:      no
Ruby Version:   2.7.5p203
Gem Version:    3.1.4
Bundler Version:2.2.33
Rake Version:   13.0.6
Redis Version:  6.2.6
Sidekiq Version:6.4.0
Go Version:     unknown

GitLab information
Version:        15.0.0-ee
Revision:       3b397c17532
Directory:      /opt/gitlab/embedded/service/gitlab-rails
DB Adapter:     PostgreSQL
DB Version:     12.10
URL:            http://gitlab-pentest4.example.com
HTTP Clone URL: http://gitlab-pentest4.example.com/some-group/some-project.git
SSH Clone URL:  git@gitlab-pentest4.example.com:some-group/some-project.git
Elasticsearch:  no
Geo:            no
Using LDAP:     no
Using Omniauth: yes
Omniauth Providers:

GitLab Shell
Version:        14.3.0
Repository storage paths:
- default:      /var/opt/gitlab/git-data/repositories
GitLab Shell path:              /opt/gitlab/embedded/service/gitlab-shell```

## Impact

JavaScript execution as the authenticated user when the user attempts to add or remove a contact for the new customer relations feature.

</details>

---
*Analysed by Claude on 2026-05-12*
