# Cross-Site Scripting (XSS) in Action Controller translate Method (Rails 7.0, 7.1)

## Metadata
- **Source:** HackerOne
- **Report:** 2303609 | https://hackerone.com/reports/2303609
- **Submitted:** 2024-01-04
- **Reporter:** ooooooo_q
- **Program:** Ruby on Rails
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Improper Output Encoding, HTML Injection
- **CVEs:** CVE-2020-15169
- **Category:** web-api

## Summary
The `translate` method in Action Controller (Rails 7.0+) is vulnerable to XSS through two attack vectors: (1) when translation keys containing `_html` suffix are missing, the error message containing user-controlled key values is marked as html_safe without escaping, and (2) when default values are passed to translate calls with `_html` suffix keys, defaults are not properly escaped before being marked as html_safe. This vulnerability does not exist in Action View's translate implementation due to different safety handling.

## Attack scenario
1. Attacker identifies an application using Rails 7.0+ with user-controlled input passed to the translate method in a controller
2. Attacker crafts a malicious translation key ending in `_html` containing JavaScript payload (e.g., `<script>alert(location)</script>_html`)
3. Attacker provides this key as a query parameter to trigger a missing translation error
4. Rails i18n returns an error message containing the malicious key, marked as html_safe by ActionView::Helpers::TranslationHelper
5. The unsanitized error message is rendered in the controller response, executing the JavaScript payload
6. Alternatively, attacker passes JavaScript payload as a default value in a translate call with `_html` suffix, which bypasses escaping

## Root cause
In Rails 7.0+, a commit (a5247bb) changed how translation errors are handled. The `translate` method in Action Controller marks error messages as html_safe without proper HTML escaping. Additionally, default values passed to translate are not escaped when the key contains the `_html` suffix, differing from the fixed behavior in Action View (CVE-2020-15169). The `_html` suffix indicates the content should be treated as safe HTML, but this assumption is violated when user input influences translation keys or defaults.

## Attacker mindset
An attacker would recognize that Rails translation keys with `_html` suffix bypass output encoding, making them attractive XSS vectors. By controlling translation key names through URL parameters or injecting into default values, the attacker can execute arbitrary JavaScript in victim browsers. The attacker would exploit the inconsistency between Action Controller and Action View implementations, targeting applications that validate input at the view layer but not the controller layer.

## Defensive takeaways
- Never pass untrusted user input directly as translation keys or in translation key construction
- If using user-controlled values in translate calls, validate against a whitelist of allowed keys
- Use Action View's translate helper instead of Action Controller's when possible, as it has proper safety handling
- Apply HTML escaping to default values passed to translate, especially when keys contain `_html` suffix
- Treat the `_html` suffix as a signal that content must be pre-validated and safe, not as a bypass for encoding
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Upgrade to patched Rails versions once available
- Audit all controller-level translate calls to ensure user input is not passed as keys

## Variant hunting
Search for other Rails framework features marked as `html_safe` without proper escaping; examine other action_controller methods that interact with i18n; check if similar issues exist in other framework versions or gems extending Rails translation functionality; test mail and job related translation helpers; investigate whether other Rails helper methods with HTML safety assumptions have similar vulnerabilities with user-controlled input

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1566 - Phishing

## Notes
The vulnerability was introduced in Rails 7.0 (not present in 6.1) due to commit a5247bb. This is a regression from CVE-2020-15169 which was fixed in Action View but overlooked in Action Controller. The `_html` suffix mechanism, meant to allow safe HTML content, becomes a security liability when combined with user-controlled input. The report includes clear PoC code demonstrating both attack vectors. This affects developers using Action Controller's translate method with any untrusted input.

## Full report
<details><summary>Expand</summary>

I have confirmed two ways that XSS can occur when using `translate` in Action Controller. ( https://github.com/rails/rails/blob/v7.1.2/actionpack/lib/abstract_controller/translation.rb#L15 )
This does not occur in Action View because the implementation of `tanslate` is different. ( https://github.com/rails/rails/blob/v7.1.2/actionview/lib/action_view/helpers/translation_helper.rb#L73 )


One is when the key value contains `_html` and also contains the tag value. 
XSS is possible because the error message returned by `I18n` contains the value of key and is marked as `html_safe`.
https://github.com/rails/rails/blob/v7.1.2/activesupport/lib/active_support/html_safe_translation.rb#L35

The other case is when the key value contains `_html` and the value passed as `default` is not escaped. This was fixed in Action View as [CVE-2020-15169](https://github.com/advisories/GHSA-cfjv-5498-mph5), but it is not modified on the Action Controller side.


## PoC

```
❯ ruby -v
ruby 3.2.2 (2023-03-30 revision e51014f9c0) [arm64-darwin22]

❯ rails new rails_server -G -M -O -C -A -J -T 
# Rails 7.1.2

❯ cd rails_server
```

`config/routes.rb`

```ruby
Rails.application.routes.draw do
   get "/articles/missing_key", to: "articles#missing_key"
   get "/articles/default", to: "articles#default"
end
```

`app/controllers/articles_controller.rb`

```ruby
class ArticlesController < ApplicationController

  def missing_key  
    @message = t(params[:text])
    render :show
  end

  def default  
    @message = t("message_html", default: "<script>alert(location)</script>")
    render :show
  end
end
```

`app/views/articles/show.html.erb`

```html
<h1><%= @message %></h1>

<%# Confirm translate is escape in Action View %>
<p><%= t("<script>alert(location)</script>_html") %></p>
<p><%= t("message_html", default: "<script>alert(location)</script>") %></p>
```

start server

```
❯ bundle exec rails s
```

You can confirm the XSS by accessing the URL below.

- http://127.0.0.1:3000/articles/missing_key?text=%3Cscript%3Ealert(location)%3C/script%3E_html
- http://127.0.0.1:3000/articles/default

## Impact

XSS occurs if pass an untrusted value to `translate` in the controller.

I confirmed that it occurs in versions 7.1 and 7.0, but the XSS did not occur in 6.1.
I'm guessing it's an effect of this commit. https://github.com/rails/rails/commit/a5247bb90895f843c45fb095a4072e8ef30eaa4e

</details>

---
*Analysed by Claude on 2026-05-12*
