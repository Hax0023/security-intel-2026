# Stored XSS on PyPI Simple API Endpoint via Unsanitized required_python Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 856836 | https://hackerone.com/reports/856836
- **Submitted:** 2020-04-23
- **Reporter:** vakzz
- **Program:** GitLab Bug Bounty (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The PyPI package simple API endpoint at `/api/:version/projects/:id/packages/pypi/simple/*package_name` fails to properly sanitize the `required_python` field when generating HTML package links. An attacker can inject arbitrary HTML/JavaScript by setting a malicious `required_python` value during package upload, which will be rendered unescaped in the response HTML. The vulnerability is stored and affects any user accessing the simple API endpoint for the compromised package.

## Attack scenario
1. Attacker creates or gains access to a GitLab project
2. Attacker uploads a PyPI package via the API endpoint, setting the `required_python` parameter to a malicious payload like `"><script>alert(1)</script>`
3. Malicious payload is stored in the database without proper sanitization
4. When a victim visits the simple API endpoint for that package, the payload is rendered unescaped in the HTML response
5. Victim's browser executes the injected JavaScript in the context of GitLab's domain
6. Attacker can steal session tokens, perform actions on behalf of the victim, or distribute malware

## Root cause
The `package_link` method in `package_presenter.rb` directly interpolates user-supplied `required_python` value into an HTML attribute without escaping or sanitizing. While a 50-character length constraint exists, it does not prevent HTML/JavaScript injection. The value is inserted directly into the `data-requires-python` attribute without HTML entity encoding.

## Attacker mindset
An attacker recognizes that package metadata fields are directly rendered in HTML responses without proper escaping. By crafting a payload that breaks out of the HTML attribute context using quote and angle bracket characters, they can inject arbitrary JavaScript that executes with the same origin privileges as GitLab. The storage aspect makes this particularly dangerous as it affects all users accessing the package.

## Defensive takeaways
- Always HTML-encode/escape user-supplied data before inserting into HTML context, especially in attributes
- Use template engines with automatic escaping enabled (e.g., ERB with `<%=` instead of `<%`)
- Implement comprehensive input validation for all user-supplied fields, not just length checks
- Apply the principle of least privilege: encode output based on context (HTML, attribute, JavaScript, URL)
- Content Security Policy (CSP) can mitigate impact but should not be the sole defense against XSS
- Perform security code review for all code paths that render user input as HTML
- Use libraries specifically designed for HTML sanitization (e.g., Loofah in Rails) when HTML content is intentional
- Implement automated security testing (SAST) to detect unescaped variable interpolation in templates

## Variant hunting
Check other package presenter classes (npm, maven, etc.) for similar unescaped interpolations
Search for other uses of `data-*` attributes that might receive unsanitized user input
Review all API endpoints that generate HTML responses from user-supplied package metadata
Examine other fields in package uploads (name, version, description, etc.) for similar vulnerabilities
Look for other presenter methods that might be vulnerable to attribute-based XSS injection
Test different character payloads (single quotes, backticks) to bypass attribute escaping

## MITRE ATT&CK
- T1190
- T1598.003

## Notes
The report mentions that on gitlab.com this is 'currently blocked by the csp', indicating the primary vulnerability exists but impact is partially mitigated. However, CSP can be bypassed or weakened over time, and the vulnerability would be critical on GitLab instances without strict CSP policies. The 50-character length constraint on `required_python` is insufficient for security purposes and suggests a misunderstanding of the threat model. This is a textbook example of why output encoding is critical even with input length restrictions.

## Full report
<details><summary>Expand</summary>

### Summary
The recently released PyPi package feature has a new endpoint at `/api/:version/projects/:id/packages/pypi/simple/*package_name` which exposes an HTML page listing the package versions. The `package_link`'s are generated using the following code:

[package_presenter.rb#L50](https://gitlab.com/gitlab-org/gitlab/-/blob/master/ee/app/presenters/packages/pypi/package_presenter.rb#L50)

```ruby
      def package_link(url, required_python, filename)
        "<a href=\"#{url}\" data-requires-python=\"#{required_python}\">#{filename}</a><br>"
      end
```

The only sanitation on `required_python` is that it is less than 50 characters (db constraint), otherwise arbitrary html can be injected.
### Steps to reproduce

1. Create project
1. Create a pypi package with `requires_python='"><script>alert(1)</script>'`

    ```bash
curl -v "https://__token__:$TOKEN@gitlab.com/api/v4/projects/18315917/packages/pypi" -F content=@/tmp/lala.txt -F requires_python=2.7 -F version=1 -F name='package_test_1' -F requires_python='"><script>alert(1)</script>'
    ````
1. Visit the simple api endpoint and see the injected code: https://gitlab.com/api/v4/projects/18315917/packages/pypi/simple/package_test_1

    ```html
        <!DOCTYPE html>
        <html>
          <head>
            <title>Links for package_test_1</title>
          </head>
          <body>
            <h1>Links for package_test_1</h1>
            <a href="https://gitlab.com/api/v4/projects/18315917/packages/pypi/files/lala.txt#sha256=" data-requires-python=""><script>alert(1)</script>">lala.txt</a><br>
          </body>
        </html>
    ```

Currently will be blocked by the csp on gitlab.com

### Impact
* An attacker could execute arbitrary javascript by sending a user or getting them to click on a url to the simple api endpoint 

### Examples
* https://gitlab.com/api/v4/projects/18315917/packages/pypi/simple/package_test_1

### What is the current *bug* behavior?
The user supplied fields used by the `package_presenter` are not all sanitized

### What is the expected *correct* behavior?
All of the user supplied fields in `package_presenter` should be sanitized before being turned into html

### Output of checks
This bug happens on GitLab.com

## Impact

* An attacker could execute arbitrary javascript by sending a user or getting them to click on a url to the simple api endpoint

</details>

---
*Analysed by Claude on 2026-05-12*
