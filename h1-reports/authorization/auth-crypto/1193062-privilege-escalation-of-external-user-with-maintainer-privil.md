# Privilege Escalation of External User to Internal Access via Project Token

## Metadata
- **Source:** HackerOne
- **Report:** 1193062 | https://hackerone.com/reports/1193062
- **Submitted:** 2021-05-12
- **Reporter:** joaxcar
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Privilege Escalation, Insufficient Access Control, Information Disclosure, Authorization Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An external user granted maintainer role on any project can create a project token linked to a bot user with internal privileges, bypassing external user restrictions. This allows the external user to access all internal projects, source code, create issues, and enumerate internal resources that should be restricted. The vulnerability stems from project tokens inheriting internal user status rather than maintaining the creator's external user restrictions.

## Attack scenario
1. Attacker creates external user account or social engineers existing user to grant maintainer access on any project
2. Attacker logs in as external user and navigates to project settings to create a project access token
3. System automatically links the token to a bot user with internal status rather than external status
4. Attacker uses the token to call GitLab API endpoints, querying /api/v4/projects to enumerate all internal projects
5. Attacker retrieves sensitive source code and project data via repository API endpoints accessible to internal guest users
6. Attacker creates issues on internal projects and groups to further interact with restricted resources

## Root cause
GitLab's project token implementation creates a bot user with internal privileges by default, regardless of the creator's user status. The access control logic does not restrict the bot user's visibility scope to match the external user creator's limitations, allowing internal project access that should be prohibited.

## Attacker mindset
An attacker would recognize that external users are intended to have limited access but notice that maintainer privileges are grantable without admin oversight. Creating a project token becomes an obvious privilege escalation vector since the resulting bot user inherits higher privileges than the external user, effectively acting as an account takeover mechanism within GitLab's permission model.

## Defensive takeaways
- Implement status inheritance for bot users created via tokens - bot user status should match or be more restrictive than the creating user's status
- Add warnings and restrictions preventing external users from being granted maintainer roles on projects, or require admin approval for such assignments
- Scope project tokens to the creator's effective permissions rather than granting broader internal access
- Implement audit logging for token creation and use, especially when external users are involved
- Add validation that project token permissions do not exceed the creator's permission set
- Require explicit admin configuration or approval for external users to access maintainer-level token creation features
- Document security implications of granting maintainer roles to external users

## Variant hunting
Test if group tokens exhibit the same privilege escalation when created by external users with group maintainer access
Check if other token types (deploy tokens, personal access tokens for groups) bypass external user restrictions
Investigate whether external users with other high-privilege roles (Developer, Maintainer on multiple projects) can escalate differently
Test if the bot user created by tokens can be further leveraged to create additional tokens with different scope
Check API endpoints for internal-only resources that should be restricted to external users but are accessible via token
Verify if webhooks or integrations created by external users with tokens inherit internal privileges
Test if impersonation or sudo features are accessible through the bot token user

## MITRE ATT&CK
- T1078.002 - Valid Accounts: Domain Accounts (compromised external user account)
- T1078.001 - Valid Accounts: Default Accounts (bot user with unintended privileges)
- T1110.003 - Brute Force: Password Spraying (social engineering for maintainer access)
- T1526 - Enumerate Cloud Resources (discovering internal projects via API)
- T1087 - Account Discovery (enumerating internal users and projects)
- T1518 - Software Discovery (identifying accessible internal resources)
- T1530 - Data from Cloud Storage Object (accessing internal project repositories)

## Notes
The vulnerability is particularly severe because it requires minimal attacker effort - external users only need to convince one internal user to grant maintainer access, which has no built-in restrictions or approval workflows. The discrepancy between documented behavior (project tokens scoped to project) and actual behavior (bot inherits internal status) makes this a documentation-implementation gap. Affects GitLab 13.10.4 and likely multiple versions. The attack is difficult for administrators to detect as it uses legitimate project token features.

## Full report
<details><summary>Expand</summary>

### Summary

An "external user" (a user account with the status external) which is granted "Maintainer" role on any project on the GitLab instance where "project tokens" are allowed can elevate its privilege to "Internal". An external user with maintainer permissions could create a project token, which will be connected to a bot user with internal privileges on the GitLab instance. Thus, now being able to access all internal projects and snippets as a Guest user. This includes

* Accessing all information about internal projects as if having Guest permissions (including source code)
* Creating issues on internal projects
* Creating projects and groups (these will contain no members and thus be of little use)

An external user is by the documentation described as a way to let external contractors get access to limited parts of a GitLab instance [link](https://docs.gitlab.com/ee/user/permissions.html#external-users). Stating that
```
This feature may be useful when for example a contractor is working on a given project and should only have access to that project.
```
There are no warnings about giving an external user maintainer permissions. It is also possible for ANY internal user to elevate the external user to maintainer on any internal project created by that user. Thus, there is no need to ask an Admin for permission to do this. Thus, an external user (if not already granted maintainer on a project) only needs to convince one other user on the system to create a project and invite the external user as maintainer. 


### Steps to reproduce

1. Create a user with "external user" activated
2. Use any internal user to invite the "external user" as maintainer to a project
3. Login as the "external user" and create a project token on the project, save the token
4. Use the token to probe internal projects
```
 curl --header "Authorization: Bearer <TOKEN>" "https://gitlab.domain.com/api/v4/projects"
```
create groups
```
 curl -X POST --header "Authorization: Bearer <TOKEN>" "https://gitlab.domain.com/api/v4/groups?name=newg&path=newgroup"
```
create issues on internal projects
```
curl -X POST --header "Authorization: Bearer <TOKEN>" "https://gitlab.domain.com/api/v4/projects/21/issues?title=iWasHere" 
```
access source code
```
curl --header "Authorization: Bearer <TOKEN>" "https://gitlab.domain.com/api/v4/projects/19/repository/blobs/83d9398518bdf1519b7b8fbbb3fa3e305a8554ef/raw"
```

### Impact

An external user can access all internal projects. Thus leading to severe information disclosure and ability to interact by issues. 

### What is the current *bug* behavior?

An external user with maintainer privileges to a project can create a project token which is connected to a Bot with internal access.

### What is the expected *correct* behavior?

The bot should not have internal access to the GitLab instance. It is stated that
```
Project access tokens are scoped to a project and can be used to authenticate with the GitLab API.
```
[link](https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html)
Which makes it seam like the token does not have any permissions outside the project.
The bot should probably have "external privilege" as standard. At least an external user should not be able to use the bot to access internal projects.

#### Results of GitLab environment info

```
System information
System:		
Current User:	gitlab
Using RVM:	no
Ruby Version:	3.0.1p64
Gem Version:	/usr/lib/ruby/2.7.0/bundler/spec_set.rb:86:in `block in materialize': Could not find rake-13.0.3 in any of the sources (Bundler::GemNotFound)
	from /usr/lib/ruby/2.7.0/bundler/spec_set.rb:80:in `map!'
	from /usr/lib/ruby/2.7.0/bundler/spec_set.rb:80:in `materialize'
	from /usr/lib/ruby/2.7.0/bundler/definition.rb:170:in `specs'
	from /usr/lib/ruby/2.7.0/bundler/definition.rb:237:in `specs_for'
	from /usr/lib/ruby/2.7.0/bundler/definition.rb:226:in `requested_specs'
	from /usr/lib/ruby/2.7.0/bundler/runtime.rb:101:in `block in definition_method'
	from /usr/lib/ruby/2.7.0/bundler/runtime.rb:20:in `setup'
	from /usr/lib/ruby/2.7.0/bundler.rb:149:in `setup'
	from /usr/lib/ruby/2.7.0/bundler/setup.rb:20:in `block in <top (required)>'
	from /usr/lib/ruby/2.7.0/bundler/ui/shell.rb:136:in `with_level'
	from /usr/lib/ruby/2.7.0/bundler/ui/shell.rb:88:in `silence'
	from /usr/lib/ruby/2.7.0/bundler/setup.rb:20:in `<top (required)>'
	from <internal:/usr/lib/ruby/3.0.0/rubygems/core_ext/kernel_require.rb>:85:in `require'
	from <internal:/usr/lib/ruby/3.0.0/rubygems/core_ext/kernel_require.rb>:85:in `require'
Bundler Version:unknown
Rake Version:	13.0.3
Redis Version:	6.2.3
Git Version:	2.31.1
Sidekiq Version:5.2.9
Go Version:	go1.16.4 linux/amd64

GitLab information
Version:	13.10.4
Revision:	e11cc45d59e
Directory:	/usr/share/webapps/gitlab
DB Adapter:	PostgreSQL
DB Version:	13.2
URL:		http://gitlab.joaxcar.com
HTTP Clone URL:	http://gitlab.joaxcar.com/some-group/some-project.git
SSH Clone URL:	gitlab@gitlab.joaxcar.com:some-group/some-project.git
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers: 

GitLab Shell
Version:	13.17.0
Repository storage paths:
- default: 	/var/lib/gitlab/repositories
GitLab Shell path:		/usr/share/webapps/gitlab-shell
Git:		/usr/bin/git
```

## Impact

An external user can access all internal projects. Thus leading to severe information disclosure and ability to interact by issues. 

The user can now
* Accessing all information about internal projects as if having Guest permissions (including source code)
* Creating issues on internal projects
* Creating projects and groups (these will contain no members and thus be of little use)

</details>

---
*Analysed by Claude on 2026-05-24*
