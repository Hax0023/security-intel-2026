# Stored XSS in Merge Request Source Branch via Unsanitized Title Attribute

## Metadata
- **Source:** HackerOne
- **Report:** 977697 | https://hackerone.com/reports/977697
- **Submitted:** 2020-09-09
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Sanitization, Template Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab merge request pages where the source branch name is rendered unsanitized in an HTML title attribute. An attacker can create a malicious branch name containing JavaScript that executes when any user views the merge request, allowing arbitrary API actions on behalf of victims despite GitLab's CSP.

## Attack scenario
1. Attacker creates a new branch with a malicious name: '><iframe/srcdoc='<script/src=/path/alert.js></script>'></iframe>
2. Attacker creates a merge request from this malicious branch to master
3. The branch name is stored in GitLab's database without proper sanitization
4. When any user views the merge request, the unsanitized branch name is rendered in the sidebar's title attribute
5. The injected JavaScript breaks out of the attribute and executes in the victim's browser context
6. Attacker uses victim's authenticated session to perform API actions like modifying code, stealing tokens, or compromising the repository

## Root cause
In _sidebar.html.haml, the source_branch variable is directly interpolated into an HTML title attribute using string concatenation marked as html_safe without prior sanitization. The code treats the branch name as trusted content despite it being user-controlled input.

## Attacker mindset
Exploit the automatic rendering of merge request pages to execute malicious code without user interaction. The attacker recognizes that branch names are persisted data rendered across multiple user sessions, making this high-impact. By bypassing CSP through iframe and srcdoc attributes, they ensure reliable code execution.

## Defensive takeaways
- Never mark user-controlled data as html_safe without explicit sanitization
- Always escape special characters in HTML attributes, especially quotes and angle brackets
- Use templating engine escaping by default rather than html_safe for dynamic content
- Apply input validation to branch names to reject suspicious patterns early
- Implement comprehensive output encoding for all template variables
- Review all instances of .html_safe usage and eliminate those combining with user input
- Test CSP effectiveness against iframe/srcdoc injection vectors
- Consider stricter branch name validation rules

## Variant hunting
Check for similar unsanitized branch/tag name rendering in other UI locations (commits, releases, tags pages)
Search for other .html_safe % interpolations with user-controlled variables throughout templates
Test issue/MR title fields for similar XSS vectors
Examine any user-supplied data rendered in tooltips or title attributes
Look for insufficient sanitization in pipeline/job artifact paths exposed in URLs
Test other string-based entity names (usernames, group names) for attribute injection

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1566.002 - Phishing: Spearphishing Link
- T1598 - Phishing for Information

## Notes
The vulnerability bypasses GitLab's CSP through clever use of iframe srcdoc attributes. The automatic rendering without user interaction significantly increases real-world impact. The public PoC reference shows this was actively exploitable on GitLab.com. The root cause demonstrates a common pattern: mixing user input with html_safe without proper escaping in template systems.

## Full report
<details><summary>Expand</summary>

Hi team,

A stored XSS is existing in the merge requests pages.

### Steps to reproduce

1. In any existing project or create a new project with checking option "Initialize repository with a README"
2. Create a new branch with name `'><iframe/srcdoc='<script/src=/yvvdwf/data/-/jobs/552156057/artifacts/raw/alert.js></script>'></iframe>`, e.g., `git push origin master:"'><iframe/srcdoc='<script/src=/yvvdwf/data/-/jobs/552156057/artifacts/raw/alert.js></script>'></iframe>"`
3. Create a new merge request from the new branch to master
4. When open the merge request being created, you should see an alert

### Impact

This stored-XSS allows attacker to execute arbitrary actions on behalf of victim notably via gitlab API. It occurs automatically without any need of victim's interaction despite gitlab CSP.

### Examples

(the alert occurs although existing of CSP of gitlab)

https://gitlab.com/yvvdwf/store-xss-merge-request/-/merge_requests/1

### What is the current *bug* behavior?

In [_sidebar.html.haml](https://gitlab.com/gitlab-org/gitlab/-/blob/3d10455ebe4d90f3a6c4fd73a0d52aa4506e40f8/app/views/shared/issuable/_sidebar.html.haml#L170), the `source_branch` is not sanitized when using as `title` attribute

```ruby
%span
    = _('Source branch: %{source_branch_open}%{source_branch}%{source_branch_close}').html_safe % { source_branch_open: "<cite title='#{source_branch}'>".html_safe, source_branch_close: "</cite>".html_safe, source_branch: source_branch }
```

### What is the expected *correct* behavior?

`sourche_banch` should be sanitized

### Output of checks

This bug happens on GitLab.com

## Impact

This stored-XSS allows attacker to execute arbitrary actions on behalf of victim notably via gitlab API. It occurs automatically without any need of victim's interaction despite gitlab CSP.

</details>

---
*Analysed by Claude on 2026-05-12*
