# Stored XSS on Wiki Pages via Author Email in Git Config

## Metadata
- **Source:** HackerOne
- **Report:** 1087061 | https://hackerone.com/reports/1087061
- **Submitted:** 2021-01-25
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Trust Boundary Violation
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in GitLab wiki pages where user-controlled git commit author email addresses are rendered as HTML attributes without proper sanitization. An attacker can craft a malicious email in the git config that injects arbitrary DOM attributes and event handlers into anchor tags displayed on wiki pages.

## Attack scenario
1. Attacker clones the wiki repository of a project they have access to
2. Attacker modifies their local git config user.email to include XSS payload (e.g., "#' style=animation-name:blinking-dot onanimationstart=alert(document.domain) other")
3. Attacker commits and pushes a change to any wiki page with the malicious git config
4. When legitimate users view the wiki page, the malicious email is rendered as the author URL in an anchor tag
5. The browser executes the injected JavaScript payload (animation event handler triggers alert)
6. Attacker can escalate to session hijacking, credential theft, or privilege escalation via victim's browser

## Root cause
The `author_url` method in `wiki_page_version.rb` returns either a mailto link or user profile URL based on git commit author_email. In `show.html.haml`, this URL is marked as `.html_safe` without sanitization, causing it to be rendered as raw HTML. When the email contains special characters and quotes, it breaks out of the href attribute and injects arbitrary HTML/attributes.

## Attacker mindset
An attacker with commit access to a project's wiki repository can inject malicious payloads into git metadata that will execute in the browsers of all users viewing that wiki page. This is particularly dangerous because git commit metadata is typically trusted and not validated for security issues. The attacker leverages the Rails `.html_safe` method which explicitly disables XSS protection.

## Defensive takeaways
- Never mark user-controlled data or data derived from external sources (git commits, emails) as `.html_safe` without explicit sanitization
- Sanitize all output that will be used in HTML context, especially when constructing HTML attributes
- Validate and sanitize email addresses before using them in HTML rendering, even if they come from git metadata
- Use Rails helper methods like `link_to` with proper escaping instead of manually constructing HTML strings
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Apply the principle of least privilege to data sources - don't treat git commit metadata as inherently safe
- Add security-focused code reviews for changes involving `.html_safe` usage

## Variant hunting
Search for other uses of `.html_safe` on user-controlled or externally-sourced data in similar contexts
Check other wiki rendering pages for similar author_url or commit metadata rendering
Look for email addresses used in HTML attributes across the codebase without sanitization
Examine git hook metadata usage (author_name, committer_email, commit message) for similar issues
Check issue trackers and merge request pages that display commit author information
Search for other instances where `Gitlab::UrlBuilder.build()` output is marked safe without validation

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This vulnerability demonstrates how framework-level XSS protections can be circumvented when developers explicitly disable them with `.html_safe`. The attack requires commit access but affects all wiki viewers, making it a high-impact vulnerability for project collaboration platforms. The fix is straightforward: remove `.html_safe` or properly sanitize the output before marking it safe.

## Full report
<details><summary>Expand</summary>

Hello,

A Stored-XSS is existing on Wiki pages. It is caused by recent change in [show.html.haml#L10](https://gitlab.com/gitlab-org/gitlab/blob/3e543192b1179c79e0a44ae6f32648fa7155c10e/app/views/shared/wikis/show.html.haml#L10)

```ruby
       ... "<a href='#{@page.last_version.author_url}'>".html_safe ...
```

`author_url` is defined by committed email in [wiki_page_version.rb](https://gitlab.com/gitlab-org/gitlab/blob/3e543192b1179c79e0a44ae6f32648fa7155c10e/lib/gitlab/git/wiki_page_version.rb):

```ruby
     delegate :message, :sha, :id, :author_name, :author_email, :authored_date, to: :commit

      def author_url
        user = ::User.find_by_any_email(author_email)
        user.nil? ? "mailto:#{author_email}" : Gitlab::UrlBuilder.build(user)
      end
```

Since the `author_url`is considered as `safe`, attackers may inject any DOM attributes of `<a>` tag. 


### Steps to reproduce

1. Clone wiki repository of an existing project or a new one, for example: `git clone git@gl.local:root/test.wiki.git`
2. Go to inside `test.wiki` directory, then add the 3 following lines at then end of  `.git/config` file (if there exists `[user]` section in `.git/config`, then replace its section by the following lines):

```
[user]
	name = anyname
	email = "#' style=animation-name:blinking-dot onanimationstart=alert(document.domain) other"
```

3.  Modify/create any wiki page, for example: `echo "Hi" >> home.md`
4. Commit the modification and push it into gitlab server
5. Open the wiki page in Web browser,  http://gl.local/hi/test/-/wikis/home, you should see the alert

### Impact

XSS may allows attackers to perform any actions on behalf of victims at client side.


### What is the current *bug* behavior?

`author_url` is not sanitized

### What is the expected *correct* behavior?

`author_url`  should be sanitized

### Output of checks

#### Results of GitLab environment info

(For installations with omnibus-gitlab package run and paste the output of:
`sudo gitlab-rake gitlab:env:info`)

```
System:		Ubuntu 18.04
Proxy:		no
Current User:	git
Using RVM:	no
Ruby Version:	2.7.2p137
Gem Version:	3.1.4
Bundler Version:2.1.4
Rake Version:	13.0.3
Redis Version:	5.0.9
Git Version:	2.29.0
Sidekiq Version:5.2.9
Go Version:	unknown

GitLab information
Version:	13.8.0-ee
Revision:	1ae10d09692
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	12.4
URL:		http://gl.local
HTTP Clone URL:	http://gl.local/some-group/some-project.git
SSH Clone URL:	git@gl.local:some-group/some-project.git
Elasticsearch:	no
Geo:		no
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers: 

GitLab Shell
Version:	13.15.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

## Impact

XSS may allows attackers to perform any actions on behalf of victims at client side.

</details>

---
*Analysed by Claude on 2026-05-12*
