# Stored XSS in group issue list via user profile full name

## Metadata
- **Source:** HackerOne
- **Report:** 859333 | https://hackerone.com/reports/859333
- **Submitted:** 2020-04-25
- **Reporter:** mike12
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the group issue list view when the 'vue_issuables_list' feature is enabled. An attacker can inject malicious JavaScript through their user profile's full name field, which gets executed when other users view the group issue list. The vulnerability allows attackers to perform arbitrary actions, steal credentials, or compromise other users' accounts.

## Attack scenario
1. Attacker sets their GitLab profile full name to a malicious payload: 'foo style=animation-name:gl-spinner-rotate onanimationend=alert(1)'
2. Attacker creates or joins a group and creates an issue within a project in that group
3. When other users navigate to the group's issue list view, the user's full name is rendered without proper sanitization
4. The injected JavaScript payload in the onanimationend event handler executes in the victim's browser with their session context
5. Attacker can steal session tokens, perform actions impersonating the victim, or redirect users to phishing sites
6. The XSS payload persists in the database, affecting all users who view the group issue list

## Root cause
The Vue-based issuables list component ('vue_issuables_list') fails to properly sanitize or encode user-supplied data from profile fields (full name) before rendering it in the DOM. The output is rendered as raw HTML rather than text content, allowing attribute injection and event handler execution.

## Attacker mindset
An attacker with a valid GitLab account discovers that user profile data is not properly sanitized in the new Vue-based UI component. They craft a payload using CSS animation events as a vector since script tags might be filtered. By setting this in their own profile, they ensure the payload executes whenever their name appears in group issue lists, affecting all group members who view those lists.

## Defensive takeaways
- Always sanitize and encode user-supplied data before rendering in templates, especially in newly developed Vue components
- Use Vue's built-in text interpolation ({{}} in templates) instead of v-html for user content
- Implement Content Security Policy (CSP) headers to prevent inline script execution and limit XSS impact
- Validate profile input fields server-side to reject or escape HTML/CSS special characters
- Apply security reviews to new features before enabling them by default
- Use templating libraries with auto-escaping enabled by default
- Implement automated security testing for XSS vulnerabilities in UI components
- Consider denylist approach for dangerous HTML attributes and event handlers

## Variant hunting
Check other user-supplied fields rendered in list views (username, email, bio, organization name)
Test other Vue-based components for similar sanitization gaps
Examine group names, project names, and issue titles for the same vulnerability
Look for other feature flags controlling new UI components that might have similar issues
Test custom fields or metadata that users can set
Check comment/description rendering in issue details and merge requests
Review any user-to-user data rendering in dashboards or activity feeds

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204.001 - User Execution: Malicious Link
- T1566.002 - Phishing: Spearphishing Link
- T1539 - Steal Web Session Cookie
- T1056.004 - Interaction - Capture: Credential API Hooking

## Notes
This vulnerability demonstrates a common pattern in modern web frameworks: developer reliance on framework-provided sanitization without explicit verification. The use of animation events rather than traditional script tags shows attacker creativity in bypassing potential filters. The fact this was in a feature flag that wasn't yet default suggests the security review process may not adequately cover in-development features. The Docker reproduction steps provided are valuable for verification and testing. The vulnerability affects all users viewing the group issue list, making it high-impact despite requiring initial account creation.

## Full report
<details><summary>Expand</summary>

Hello Gitlab!

To reproduce the bug, we need to enable the "vue_issuables_list" feature in Gitlab. This feature is not enabled by default, but I think it would be better to fix this issue before this feature is permanently available.

#### Steps to reproduce:

1. Run Gitlab `docker run --detach --hostname gitlab.example.com --publish 443:443 --publish 80:80 --publish 22:22 --name gitlab gitlab/gitlab-ce:latest`
2. Enable the "vue_issuables_list" feature
	1. Connect to the GitLab container: `docker exec -it gitlab /bin/bash`
	2. Start a session on GitLab Rails console (in the container): `gitlab-rails console`
	3. Once the Rails console session has started, run: `Feature.enable(:vue_issuables_list)`
3. Go to the profile settings and set the full name: `foo style=animation-name:gl-spinner-rotate onanimationend=alert(1)`
{F803617}
4. Create a group and create a project in this group
5. Create an issue in the project
6. Go to the group issue list
{F803618}
{F803619}

#### My GitLab version

```
root@gitlab:/# gitlab-rake gitlab:env:info

System information
System:		
Current User:	git
Using RVM:	no
Ruby Version:	2.6.5p114
Gem Version:	2.7.10
Bundler Version:1.17.3
Rake Version:	12.3.3
Redis Version:	5.0.7
Git Version:	2.26.2
Sidekiq Version:5.2.7
Go Version:	unknown

GitLab information
Version:	12.10.1
Revision:	e658772bd63
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	11.7
URL:		http://gitlab.example.com
HTTP Clone URL:	http://gitlab.example.com/some-group/some-project.git
SSH Clone URL:	git@gitlab.example.com:some-group/some-project.git
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers: 

GitLab Shell
Version:	12.2.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

## Impact

An attacker can:

1. Perform any action within the application that a user can perform
2. Steal sensitive user data
3. Steal user's credentials

</details>

---
*Analysed by Claude on 2026-05-12*
