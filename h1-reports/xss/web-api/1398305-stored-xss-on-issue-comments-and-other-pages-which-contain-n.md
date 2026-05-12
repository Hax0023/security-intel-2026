# Stored XSS on issue comments and other pages which contain notes

## Metadata
- **Source:** HackerOne
- **Report:** 1398305 | https://hackerone.com/reports/1398305
- **Submitted:** 2021-11-11
- **Reporter:** jarij
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Sanitization, Server-Side Template Injection
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's SyntaxHighlightFilter and gl-emoji custom element contain two independent XSS sanitization bypasses that allow attackers to inject malicious JavaScript into issue comments and other note-bearing pages. An attacker with comment privileges can craft payloads using HTML entity encoding to bypass server-side and frontend sanitization filters, affecting self-managed GitLab instances.

## Attack scenario
1. Attacker identifies a GitLab self-managed instance and gains access to create comments on issues or snippets
2. Attacker crafts a payload combining SyntaxHighlightFilter bypass using data-sourcepos attributes and gl-emoji element with malicious name attribute
3. Attacker posts the payload as a comment using HTML entity encoding to evade initial filters (&#34; for quotes, &#34; for special characters)
4. When other users view the issue/comment, the SyntaxHighlightFilter processes the malicious data-sourcepos attribute without sanitization, creating raw HTML
5. The gl-emoji custom element processes the name attribute containing the onload event handler, bypassing v-safe-html directive
6. JavaScript executes in the victim's browser context, allowing session hijacking, credential theft, or further malicious actions

## Root cause
Two distinct vulnerabilities in sanitization mechanisms: (1) SyntaxHighlightFilter directly interpolates unsanitized sourcepos attribute into HTML template without escaping, (2) gl-emoji emojiImageTag function unsafely constructs img tag from name parameter without proper escaping, and frontend v-safe-html directive fails to sanitize the resulting HTML due to attribute-based injection

## Attacker mindset
Attackers leverage the trust placed in code highlighting and emoji rendering features to bypass multi-layered XSS protections. By combining two separate weaknesses and using HTML entity encoding, they work around both server-side Ruby filtering and client-side Vue.js sanitization directives to achieve persistent XSS.

## Defensive takeaways
- Always escape user input before interpolating into HTML templates, especially in server-side rendering contexts
- Implement Content Security Policy (CSP) headers with strict directives to limit JavaScript execution even if XSS occurs
- Sanitize HTML at the point of output, not just at input, using established libraries (DOMPurify, bleach, etc.)
- Use template engines that auto-escape by default rather than manual string concatenation
- Apply defense-in-depth: validate input, sanitize on server-side AND client-side independently
- Test custom HTML elements and Vue directives (v-safe-html) with polyglot and attribute-based XSS payloads
- Implement strict Content-Security-Policy headers to block inline scripts and event handlers
- Regular security audits of filters and sanitization logic, particularly where raw HTML generation occurs

## Variant hunting
Search for other instances of string interpolation in filter chains, particularly in: (1) markdown processors and syntax highlighters, (2) custom HTML element implementations, (3) any code constructing HTML attributes from user data, (4) other Banzai filters that may have similar data-sourcepos or similar metadata attributes, (5) frontend directives marked as 'safe' that may not properly handle encoded payloads

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1566 - Phishing

## Notes
Reporter notes GitLab SaaS is not vulnerable due to CSP headers, highlighting the critical importance of CSP as a defense-in-depth measure. The vulnerability affects self-managed instances. Payload uses HTML entity encoding (&#34; for quotes) to bypass initial filters, demonstrating encoding-aware bypass techniques. The combination of two separate filter bypasses creates a more severe vulnerability than either alone.

## Full report
<details><summary>Expand</summary>

### Summary

This report contains two XSS sanitization bypasses:

* The [SyntaxHighlightFilter](https://gitlab.com/gitlab-org/gitlab/-/blob/c2e5d7b89b84cc5b44575592bb706ef75c3d1bbb/lib/banzai/filter/syntax_highlight_filter.rb) creates html from unsanitized data. This can be used to bypass the XSS filter on the server-side. 

```ruby
 def highlight_node(node)
...
sourcepos = node.parent.attr('data-sourcepos')
...
sourcepos_attr = sourcepos ? "data-sourcepos=\"#{sourcepos}\"" : ""

 highlighted = %(<pre #{sourcepos_attr} class="#{css_classes}"
                             lang="#{language}"
                             #{lang_params}
                             v-pre="true"><code>#{code}</code></pre>)
```

* The [gl-emoji](https://gitlab.com/gitlab-org/gitlab/-/blob/5b0bedde99d676116221b56ad75fa89ccf8a9f28/app/assets/javascripts/behaviors/gl_emoji.js) custom element can be used to bypass the gitlab-ui `v-safe-html` directive sanitization on the frontend side by injecting the payload into the name attribute:

```js
export function emojiImageTag(name, src) {
  return `<img class="emoji" title=":${name}:" alt=":${name}:" src="${src}" width="20" height="20" align="absmiddle" />`;
}
```

* Gitlab SaaS is not vulnerable because this report does not include CSP bypass. I'm currently working on this.

### Steps to reproduce

{F1510920}

1. Launch self-managed Gitlab instance
2. Create issue
3. Copy and paste the following payload into the comment field:

```
<pre data-sourcepos="&#34; href=&#34;x&#34;></pre>
<gl-emoji data-name='&#34;x=&#34y&#34 onload=&#34;alert(document.location.href)&#34;' data-unicode-version='x'>
abc
</gl-emoji>
<pre x=&#34;">
<code></code></pre>
```

#### Results of GitLab environment info

```
# gitlab-rake gitlab:env:info         

System information
System:
Proxy:          no
Current User:   git
Using RVM:      no
Ruby Version:   2.7.4p191
Gem Version:    3.1.4
Bundler Version:2.1.4
Rake Version:   13.0.6
Redis Version:  6.0.16
Git Version:    2.33.0.
Sidekiq Version:6.2.2
Go Version:     unknown

GitLab information
Version:        14.4.2-ee
Revision:       84aa6daaffd
Directory:      /opt/gitlab/embedded/service/gitlab-rails
DB Adapter:     PostgreSQL
DB Version:     12.7
URL:            http://localhost:8888
HTTP Clone URL: http://localhost:8888/some-group/some-project.git
SSH Clone URL:  git@localhost:some-group/some-project.git
Elasticsearch:  no
Geo:            no
Using LDAP:     no
Using Omniauth: yes
Omniauth Providers:

GitLab Shell
Version:        13.21.1
Repository storage paths:
- default:      /var/opt/gitlab/git-data/repositories
GitLab Shell path:              /opt/gitlab/embedded/service/gitlab-shell
Git:            /opt/gitlab/embedded/bin/git
```

## Impact

Attacker who can comment on issue will be able to XSS users that visit that issue. This also affects other pages where comments can be posted, such as snippets.

</details>

---
*Analysed by Claude on 2026-05-12*
