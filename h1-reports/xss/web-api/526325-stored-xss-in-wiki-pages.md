# Stored XSS in Wiki pages via Hierarchical Link Markdown

## Metadata
- **Source:** HackerOne
- **Report:** 526325 | https://hackerone.com/reports/526325
- **Submitted:** 2019-04-04
- **Reporter:** ryhmnlfj
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Unsafe Markdown Processing
- **CVEs:** CVE-2019-5467
- **Category:** web-api

## Summary
GitLab Wiki pages are vulnerable to Stored XSS through improper handling of wiki-specific hierarchical link Markdown syntax. An attacker can create a wiki page with a malicious title containing protocol schemes (javascript:, data:, vbscript:) that, when combined with relative link syntax, generates executable javascript: URLs. The vulnerability affects all users who view the compromised wiki page.

## Attack scenario
1. Attacker gains access to create or edit wiki pages in a GitLab project
2. Attacker creates a new wiki page with slug 'javascript:' and title 'javascript:'
3. Attacker fills content with markdown link syntax [XSS](.alert(1);) exploiting the dot hierarchy notation
4. GitLab's markdown processor incorrectly concatenates the title scheme with the relative path, creating javascript:alert(1);
5. When any user visits the wiki page and clicks the XSS link, arbitrary JavaScript executes in their browser context
6. If wiki is public, attack reaches large user base including unauthenticated visitors

## Root cause
GitLab's Markdown processor for Wiki pages fails to validate and sanitize protocol schemes in page titles before using them in href attribute construction. The hierarchical link notation (.) is processed without proper URL validation, allowing relative paths to be concatenated with dangerous scheme prefixes. No whitelist of safe protocols (http/https) is enforced on generated href attributes.

## Attacker mindset
Attacker seeks to compromise multiple GitLab users efficiently by exploiting permissive wiki editing capabilities. By leveraging wiki visibility settings, a single malicious page can reach numerous victims. The attacker exploits the application's trust in internal markdown processing and demonstrates knowledge of URL scheme exploitation patterns.

## Defensive takeaways
- Implement strict URL validation on all generated href attributes using whitelist approach (only allow http/https)
- Sanitize and validate page titles and slugs to reject or escape dangerous protocol schemes before processing markdown
- Use a security-focused markdown library with built-in XSS protections rather than custom implementation
- Apply Content Security Policy (CSP) headers to prevent inline script execution even if filtering fails
- Implement markdown rendering in sandboxed context separate from user content
- Validate relative path resolution in markdown links to prevent scheme injection
- Add security unit tests specifically targeting protocol scheme injection in markdown processing
- Consider disallowing certain dangerous page title patterns or escaping special characters

## Variant hunting
Test other markdown link syntaxes for similar vulnerabilities; investigate image markdown ![alt](url) for same issue; check comment/issue markdown for identical flaws; test other wiki-specific markdown features (brackets, braces) for path traversal or scheme injection; examine how other markdown processors (comments, issues, merge requests) handle relative links; test with encoded schemes (javascript%3a) and case variants (JavaScript:, jAvAsCrIpT:); attempt to inject other dangerous schemes (data:, vbscript:, file:); check if similar patterns work in other text fields accepting markdown

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
Report dated GitLab 11.9.4-ee. Vulnerability demonstrates importance of defense-in-depth - even with markdown processing, output encoding and CSP would have prevented execution. The use of wiki-specific syntax makes this less obvious than standard XSS, suggesting custom markdown handling without proper security review. Attacker could chain this with social engineering or embed in documentation repositories. The public project + wiki visibility setting multiplies impact significantly.

## Full report
<details><summary>Expand</summary>

### Summary

I found Stored XSS using Wiki-specific Hierarchical link Markdown in Wiki pages.

### Steps to reproduce

1. Sign in to GitLab.
2. Open a Project page that you have permission to edit Wiki pages.
3. Open Wiki page.
4. Click "New page" button.
5. Fill out "Page slug" form with `javascript:`.
6. Click "Create page" button.
7. Fill out the each form as follows:    
Title: `javascript:`    
Format: Markdown    
Content: `[XSS](.alert(1);)`    
(Please see "CreatePage.png")    
{F462086}    
8. Click "Create page" button.
9. Click "XSS" link in created page.

### What is the current *bug* behavior?

The alert dialog appears after clicking "XSS" link in created page.
Please see "Result_Firefox.png".
{F462087}

#### Description In Detail:

GitLab application converts the Markdown string `.alert(1);` to the href attribute `javascript:alert(1);`.
Furthermore, Wiki-specific Markdown string `.` is converted to `javascript:` in this case.

### What is the expected *correct* behavior?

The dangerous href attribute `javascript:alert(1);` should be filtered.
A safe HTTP/HTTPS link should be rendered instead.

### Additional Informations:

1. In the above case, another Wiki-specific Markdown string `..` is also converted to `javascript:`.

2. Using Title string such as `javascript:STRING_EXPECTED_REMOVING` also reproduces this vulnerability.
For example, if a wiki page is created with a disguised Title string `JavaScript::SubClassName.function_name`, GitLab application converts Wiki-specific Markdown string `.` to `JavaScript:` in such page.
It seems that GitLab application recognizes scheme-like string `JavaScript:` and removes the rest of Title string `:SubClassName.function_name`.

3. An attacker can use various schemes by replacing Title string `javascript:` to other scheme. (e.g. `data:`, `vbscript:`, and so on.)

### Output of checks

This bug happens on the official Docker installation of GitLab Enterprise Edition 11.9.4-ee.

#### Results of GitLab environment info

Output of `sudo gitlab-rake gitlab:env:info`:

```
System information
System:		
Proxy:		no
Current User:	git
Using RVM:	no
Ruby Version:	2.5.3p105
Gem Version:	2.7.6
Bundler Version:1.16.6
Rake Version:	12.3.2
Redis Version:	3.2.12
Git Version:	2.18.1
Sidekiq Version:5.2.5
Go Version:	unknown

GitLab information
Version:	11.9.4-ee
Revision:	55be7f0
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	postgresql
DB Version:	9.6.11
URL:		http://gitlab.example.com
HTTP Clone URL:	http://gitlab.example.com/some-group/some-project.git
SSH Clone URL:	git@gitlab.example.com:some-group/some-project.git
Elasticsearch:	no
Geo:		no
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers: 

GitLab Shell
Version:	8.7.1
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

## Impact

If wiki pages created by using this vulnerability are visible to everyone (Wiki Visibility setting is set to "Everyone With Access") in "Public" project, there is a possibility that a considerable number of GitLab users and visitors click a malicious link.

</details>

---
*Analysed by Claude on 2026-05-11*
