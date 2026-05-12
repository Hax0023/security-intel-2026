# Stored XSS in Custom Emoji via Unescaped URL Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1198517 | https://hackerone.com/reports/1198517
- **Submitted:** 2021-05-15
- **Reporter:** ooooooo_q
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's custom emoji feature contains a stored XSS vulnerability in the emoji_image_tag method where the src parameter is rendered directly into HTML without escaping. An attacker can inject malicious JavaScript through the custom emoji URL field which executes when users view markdown containing the emoji reference.

## Attack scenario
1. Attacker enables the custom_emoji feature flag in a self-managed GitLab instance via Rails console
2. Attacker creates a group (e.g., xss_target) to host the malicious custom emoji
3. Attacker uses GraphQL API to create a custom emoji with a crafted URL containing JavaScript payload: http://aaa#'><img onerror=alert(location) src=>
4. Attacker creates a project with README.md containing reference to malicious emoji: :xssreplace:
5. When any user views the project README, the emoji is rendered and the JavaScript payload in the src attribute executes in the victim's browser context
6. Attacker gains ability to steal session tokens, perform actions as the victim user, or spread XSS to other users

## Root cause
The emoji_image_tag method concatenates user-controlled input (image_source/src) directly into an HTML img tag without HTML-escaping the value. While the name parameter has validation, the src URL is trusted implicitly. The .html_safe call on the result further prevents any automatic escaping by Rails.

## Attacker mindset
Attacker exploits a feature-flagged experimental feature that may have less security review. They leverage the GraphQL API to bypass potential UI-level validation and inject payload through a seemingly innocuous URL field. The stored nature allows widespread impact across all users viewing affected content.

## Defensive takeaways
- Always escape user-controlled data before rendering in HTML context, especially URLs in src attributes
- Use Rails helpers like sanitize(), h(), or url_encode() for output encoding rather than manual string concatenation
- Avoid .html_safe when concatenating user input; only apply to trusted strings
- Validate and sanitize URLs - consider URL parsing and scheme validation for emoji image sources
- Feature-flagged features still require security review; treat experimental features with same rigor as production code
- Implement Content Security Policy (CSP) headers to mitigate impact of injected scripts
- Use parameterized queries and templating engines that auto-escape by default

## Variant hunting
Check all instances where emoji rendering occurs - search for other emoji_tag or similar emoji-rendering methods
Look for other GraphQL mutations that accept URL/file path parameters and render them in HTML
Review all custom asset/image upload features that use src attributes without escaping
Check if custom emoji can be used in other contexts beyond markdown (titles, comments, descriptions)
Investigate if similar patterns exist in avatar uploads, group badges, or custom project icons
Search for other feature-flagged but unescaped content rendering in user-generated data

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1040 - Network Sniffing
- T1539 - Steal Web Session Cookie
- T1566 - Phishing

## Notes
The vulnerability only affects self-managed GitLab instances with the custom_emoji feature flag explicitly enabled. GitLab.com was not affected as the flag was not enabled by default. The fix required escaping the src parameter in emoji_image_tag method. This demonstrates the importance of security review for experimental features behind feature flags, as they may receive less scrutiny than stable code paths.

## Full report
<details><summary>Expand</summary>

### Summary

I found Stored XSS with a feature of custom emoji.

This feature hasn't been rolled out yet and need to set feature flags in self management installation. ( https://gitlab.com/gitlab-org/gitlab/-/issues/231317 )


The problem is the code here.
https://gitlab.com/gitlab-org/gitlab/-/blob/v13.11.4-ee/lib/gitlab/emoji.rb#L43

```ruby
    def emoji_image_tag(name, src)
      "<img class='emoji' title=':#{name}:' alt=':#{name}:' src='#{src}' height='20' width='20' align='absmiddle' />"
    end

    ...

    def custom_emoji_tag(name, image_source)
      data = {
        name: name
      }

      ActionController::Base.helpers.content_tag('gl-emoji', title: name, data: data) do
        emoji_image_tag(name, image_source).html_safe
      end
    end
```

Since the `src` value of `emoji_image_tag` is not escaped, it will be XSS.
(The value of `name` is not available for XSS as validation exists.)

### Steps to reproduce

The following steps should to be reproduced in a self-managed installation of gitlab.

 1. Set feature_flag

see https://docs.gitlab.com/ee/administration/feature_flags.html

```
# gitlab-rails console
--------------------------------------------------------------------------------
 Ruby:         ruby 2.7.2p137 (2020-10-01 revision 5445e04352) [x86_64-linux]
 GitLab:       13.11.3 (b321336e443) FOSS
 GitLab Shell: 13.17.0
 PostgreSQL:   12.6
--------------------------------------------------------------------------------
Loading production environment (Rails 6.0.3.6)
irb(main):001:0> Feature.enable(:custom_emoji)
=> true
```


 2. Create group

Create a group to set the custom emoji. For example, `xss_target`.


 3. Create custom emoji

The ability to create custom emoji only exists in graphql api.

Create by sending the following query from the graphiql page of `https://localhost/-/graphql-explorer`.

```
mutation {
  createCustomEmoji(input: 
    {
      groupPath: "xss_target", 
      name:"xssreplace",
      url:"http://aaa#'><img onerror=alert(location) src=.>"
    }) {
    customEmoji {
      id
      name
      url
    }
  }
}
```

{F1302828}

 4. Create project and file

Create a project to display custom emojis and create a `README.md` with the following content.

```
:xssreplace:
```


5. View rendering results in browser

The function of custom emoji replaces the `:xssreplace:` part to become Stored XSS.

### Impact

Stored XSS is possible with gitlab with feature flags set.

### Examples

There is no example because it works only with gitlab with feature flag set.

### What is the current *bug* behavior?

Insufficient escape of `src`.

### What is the expected *correct* behavior?

Escape the value of `src`.

### Relevant logs and/or screenshots

{F1302824}

### Output of checks

GitLab.com doesn't have a feature flag set so it doesn't affect.

#### Results of GitLab environment info

```
# gitlab-rake gitlab:env:info

System information
System:
Current User:	git
Using RVM:	no
Ruby Version:	2.7.2p137
Gem Version:	3.1.4
Bundler Version:2.1.4
Rake Version:	13.0.3
Redis Version:	6.0.12
Git Version:	2.31.1
Sidekiq Version:5.2.9
Go Version:	unknown

GitLab information
Version:	13.11.3
Revision:	b321336e443
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	12.6
URL:		https://gitlab.example.com
HTTP Clone URL:	https://gitlab.example.com/some-group/some-project.git
SSH Clone URL:	git@gitlab.example.com:some-group/some-project.git
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers:

GitLab Shell
Version:	13.17.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

## Impact

Stored XSS is possible with gitlab with feature flags set.

</details>

---
*Analysed by Claude on 2026-05-12*
