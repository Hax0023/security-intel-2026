# Stored XSS in Merge Request Pages via Malicious Branch Names

## Metadata
- **Source:** HackerOne
- **Report:** 723307 | https://hackerone.com/reports/723307
- **Submitted:** 2019-10-26
- **Reporter:** mike12
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab's merge request widget component where branch names are rendered without proper HTML encoding. An attacker can create a branch with a malicious name containing JavaScript code that executes when users without push permissions view the merge request page. This allows arbitrary code execution in the context of the victim's browser session.

## Attack scenario
1. Attacker creates a GitLab project or gains access to an existing one
2. Attacker creates a branch with a name containing XSS payload: `<img/src='x'/onerror=alert(document.domain)>`
3. Attacker pushes commits to this malicious branch and creates a merge request targeting a protected branch
4. Attacker makes the project public or shares the merge request link with target users
5. Victim without push permissions to source branch visits the merge request page
6. The malicious branch name is rendered without encoding in the rebase widget, triggering JavaScript execution in victim's browser

## Root cause
The Vue component `mr_widget_rebase.vue` displays branch names in the merge request widget without HTML escaping. When the application constructs the rebase message with the source branch name, it fails to sanitize or encode HTML special characters, allowing arbitrary HTML/JavaScript injection.

## Attacker mindset
An attacker with repository access creates a deliberately malicious branch name to exploit a rendering vulnerability. The attacker leverages the trust users place in viewing merge request pages and targets users with limited permissions who may be more likely to click/interact with content from seemingly legitimate merge requests.

## Defensive takeaways
- Always HTML-encode user-controlled input (branch names, commit messages, user names) when rendering in DOM contexts
- Use Vue's template escaping by default and only use v-html when absolutely necessary with sanitized content
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Apply input validation on branch names to reject or sanitize special characters
- Use security linters and static analysis tools to detect potential XSS in Vue templates
- Implement automated security testing for user-generated content rendering
- Perform security code reviews specifically focused on data binding in dynamic components

## Variant hunting
Search for other Vue components rendering branch/tag/ref names without encoding
Check commit message rendering in merge request diffs and comments
Audit user name, group name, and project name rendering across the platform
Review merge request title and description rendering in widgets
Examine pipeline name and job name rendering
Check issue/epic title rendering in related items
Audit webhook payload displays and integration outputs
Review any dynamic DOM manipulation using branch/ref data

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1005

## Notes
This vulnerability required specific conditions: (1) merge method must be 'Merge commit with semi-linear history' or 'Fast-forward merge', (2) MR must require rebase, (3) viewer must lack push permissions to source branch. The permission restriction is key - it prevents the MR creator from testing their own exploit. The vulnerability affects the rebase widget specifically, suggesting other widgets may have similar issues. The report includes excellent reproduction steps with Docker setup, making it easily verifiable.

## Full report
<details><summary>Expand</summary>

Hello Gitlab!

[Vulnerable code](https://gitlab.com/gitlab-org/gitlab/blob/9d81e97d9d111f874799605ce50ae480ae15b0c5/app/assets/javascripts/vue_merge_request_widget/components/states/mr_widget_rebase.vue#L47)

To reproduce the bug, we need to open a merge request with the following conditions:
1. Project must have 'Merge commit with semi-linear history' or 'Fast-forward merge' merge method
2. The merge request must require rebase before fast-forward/merge
3. A visitor of the merge request page must not have permissions to push to source branch
4. Target branch name must have a special name `<img/src='x'/onerror=alert(document.domain)>` :) 

**Steps to reproduce:**

1. Run Gitlab `docker run --detach --hostname gitlab.example.com --publish 443:443 --publish 80:80 --publish 22:22 --name gitlab gitlab/gitlab-ce:latest`
2. Create a new project
3. Go to the project settings and set the 'Merge method' to 'Fast-forward merge' or 'Merge commit with semi-linear history' {F618529}
4. Clone the repository and run the following in the repository:

    ```bash
    touch 1.txt
    git add 1.txt
    git commit -m "initial commit"
    git push origin master
    
    git checkout -b "<img/src='x'/onerror=alert(document.domain)>"
    touch 2.txt
    git add 2.txt
    git commit -m "add 2.txt"
    git push origin "<img/src='x'/onerror=alert(document.domain)>"
    
    git checkout master
    touch 3.txt
    git add 3.txt
    git commit -m "add 3.txt"
    git push origin master
    ```

5. Create a merge request `master` => `<img/src='x'/onerror=alert(document.domain)>`
6. Then we have to visit the merge request page under a user who does not have permissions to push to the source branch (in our case, `master` branch). For example: 
  * Make the project public and visit the merge request page under any user who does not have permissions in the project (or without authorization)
  * Invite a user to the project, but without permissions to push to the source branch.

{F618526}
{F618527}
{F618528}

```bash
root@gitlab:/# gitlab-rake gitlab:env:info

System information
System:		
Current User:	git
Using RVM:	no
Ruby Version:	2.6.3p62
Gem Version:	2.7.9
Bundler Version:1.17.3
Rake Version:	12.3.3
Redis Version:	3.2.12
Git Version:	2.22.0
Sidekiq Version:5.2.7
Go Version:	unknown

GitLab information
Version:	12.4.0
Revision:	1425a56c75b
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	10.9
URL:		http://gitlab.example.com
HTTP Clone URL:	http://gitlab.example.com/some-group/some-project.git
SSH Clone URL:	git@gitlab.example.com:some-group/some-project.git
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers: 

GitLab Shell
Version:	10.2.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
root@gitlab:/# 
```

## Impact

An attacker can:

1. Perform any action within the application that a user can perform
2. Steal sensitive user data
3. Steal user's credentials

</details>

---
*Analysed by Claude on 2026-05-12*
