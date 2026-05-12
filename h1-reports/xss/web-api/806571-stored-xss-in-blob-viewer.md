# Stored XSS in blob viewer via OpenAPI/Swagger file descriptions

## Metadata
- **Source:** HackerOne
- **Report:** 806571 | https://hackerone.com/reports/806571
- **Submitted:** 2020-02-27
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Unsafe HTML Rendering
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in GitLab's blob viewer when rendering OpenAPI/Swagger JSON files. The SwaggerUIBundle library allows HTML tags and attributes (class, style, data-*) in descriptions that bypass initial sanitization but remain dangerous in GitLab's context. Attackers can inject malicious payloads in OpenAPI file descriptions that execute arbitrary JavaScript when viewed by other users.

## Attack scenario
1. Attacker creates or modifies an OpenAPI/Swagger JSON file in a GitLab project with malicious payload in the description field
2. Payload includes HTML elements with data-* attributes (leveraging jquery-ujs) and style/class attributes for UI hijacking
3. Attacker commits the file or provides project access to victims
4. Victim views the blob/file in GitLab's web interface, triggering the OpenAPI viewer
5. SwaggerUIBundle renders the description with dangerous attributes intact
6. Malicious JavaScript executes in victim's browser with full user privileges, enabling CSRF attacks, data theft, or further exploitation

## Root cause
GitLab does not sanitize the output from SwaggerUIBundle's HTML rendering. While SwaggerUIBundle removes some malicious tags, it preserves class, style, and data-* attributes. In GitLab's context with jquery-ujs enabled, these attributes become attack vectors. Additionally, jQuery.globalEval can bypass Content Security Policy, allowing script execution.

## Attacker mindset
An attacker recognizes that file viewers are often lower-security targets and that library-generated HTML output is frequently trusted without re-validation. By chaining jquery-ujs's data-* attribute handling with UI overlays (class/style abuse), they can create clickjacking attacks and arbitrary request forgery without direct script tags.

## Defensive takeaways
- Never trust output from third-party rendering libraries; re-sanitize and validate before insertion into DOM
- Implement strict attribute whitelisting - remove data-*, event handlers, style, and class attributes from user-controlled content
- Use DOMPurify or similar vetted libraries for HTML sanitization with conservative default policies
- Disable or isolate jquery-ujs functionality for untrusted content contexts
- Implement Content Security Policy with script-src restrictions that prevent jQuery.globalEval bypasses
- Apply defense-in-depth: combine output encoding, input validation, and CSP
- Regularly audit third-party library integrations for implicit trust assumptions

## Variant hunting
Check other file viewers (Markdown, RST, AsciiDoc) for similar issues with HTML rendering libraries
Test other Swagger/OpenAPI viewers or documentation libraries in the application
Look for similar patterns where third-party libraries (highlight.js, markdown-it, etc.) output is rendered without re-sanitization
Search for other uses of jquery-ujs with user-controlled data-* attributes
Examine comment fields, wiki content, and other rich-text areas for the same vulnerability pattern
Test SVG/image viewers that might support embedded scripts or event handlers

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1563

## Notes
This report demonstrates sophisticated XSS exploitation beyond basic script injection - using class-based UI hijacking and jquery-ujs for CSRF-like attacks. The vulnerability chain shows how benign features (data attributes, CSS classes) become dangerous when sanitization is incomplete. The reference to jQuery.globalEval bypassing CSP is particularly notable for defense evasion considerations.

## Full report
<details><summary>Expand</summary>

### Summary

I found a Stored-XSS in blob viewer when viewing a json file.

In particular, when viewing an openapi file, [openapi_viewer](https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/assets/javascripts/blob/viewer/index.js#L43) is called to transfer the file's data to [SwaggerUIBundle](https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/assets/javascripts/blob/openapi/index.js#L10) to render.

SwaggerUIBundle does its job when rending graphical representation of the openapi's content. It also allows *html tags and attributes* in the description of the openapi. Although it removes malicious tags and attributes, but this is not enough in gitlab's context:

1. `class` and `style` attributes allow attackers to arbitrarily present their disposition. My demo below uses `class` attribute to create a transparent layer that fulfils the document to intercept any user's clics.

2. `data-*` attributes, under the help of [jquery-ujs](https://gitlab.com/gitlab-org/gitlab/-/blob/master/package.json#L90), allows attackers to create any requests to server when user clicking (not only `GET`, but also, `PUT`, `DELETE`, `HEAD`) with arbitrary parameters

3. The current CSP is easily by passed by [jQuery.globalEval](https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/assets/javascripts/main.js#L54). In my demo below, you should see an `alert` after clicking anywhere


### Steps to reproduce

1. In any project, create a file naming `xss-openapi.js`, then put the following content:
```
{
  "swagger" : "2.0",
  "info" : {
    "description" : "<a href=https://gitlab.com/yvvdwf/data/-/wikis/alert.md data-type=script style='cursor:default' data-remote=true class='atwho-view select2-drop-mask pika-select'></a><script>alert(0)</script>"
  }}
```

2. Click anywhere on the document view, you should see an alert.

### Impact

There are three impacts as in the Summary above. The most important impact is the stored-XSS allowing attackers to perform any action on behalf of users at the client side.

### Examples

(This repository is in private mode, please let me know if you cannot access it)
https://gitlab.com/yvvdwf/xss/-/blob/master/xss-openapi.json


### What is the current *bug* behavior?

Gitlab does not check the result generated by SwaggerUIBundle

### What is the expected *correct* behavior?

Should remove any inappropriate html attributes, such as, `data-*`, `style`, `class`.

### Output of checks

This bug happens on GitLab.com

## Impact

The stored-XSS allows attackers to perform any action on behalf of users at the client side.

</details>

---
*Analysed by Claude on 2026-05-12*
