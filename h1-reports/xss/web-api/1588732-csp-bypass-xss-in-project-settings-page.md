# CSP-bypass XSS in project settings page via unsanitized deployment key title

## Metadata
- **Source:** HackerOne
- **Report:** 1588732 | https://hackerone.com/reports/1588732
- **Submitted:** 2022-06-01
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Improper Input Validation, DOM-based XSS
- **CVEs:** None
- **Category:** web-api

## Summary
The deployment key management feature in GitLab project settings fails to sanitize user-controlled deployment key titles before rendering them in a dropdown menu. An attacker can inject arbitrary HTML/JavaScript payloads that bypass CSP restrictions due to jQuery's HTML rendering method, allowing execution of malicious scripts in the context of authenticated users with project maintainer access.

## Attack scenario
1. Attacker creates or obtains maintainer access to a GitLab project
2. Attacker navigates to Settings/Repository and adds a deployment key with a malicious title containing script tags (e.g., '<script>alert(document.domain)</script>')
3. Attacker saves the deployment key successfully to the project
4. When any maintainer or project member visits Settings/Repository and clicks on 'Allowed to push' dropdown in Protected Branches section, the malicious script executes
5. JavaScript executes in the victim's browser context with access to session cookies and API tokens
6. Attacker can perform unauthorized API requests, steal credentials, modify project settings, or compromise other resources

## Root cause
The deployKeyRowHtml() function constructs HTML by directly interpolating key.title into a template literal without escaping. While key.fullname is escaped and key.username appears limited, key.title is inserted raw into a <strong> tag. The subsequent jQuery rendering via $('<ul>').append(html) executes script tags even when CSP script-src has 'strict-dynamic', as jQuery's append() method treats the string as HTML and evaluates embedded scripts.

## Attacker mindset
An insider or attacker with project maintainer privileges seeks to compromise other project members or stakeholders. They leverage the fact that deployment key titles are user-controlled and insufficiently validated. The attacker exploits jQuery's HTML parsing behavior to bypass strict CSP policies that would normally block inline scripts. The attack is stealthy because it triggers only when maintainers access specific dropdown menus, making detection difficult.

## Defensive takeaways
- Always escape user-controlled data before inserting into DOM, even when using template literals - use innerText or textContent instead of innerHTML
- Use DOMPurify or similar libraries when HTML content is genuinely needed, with strict allowlists excluding script-related tags
- Replace jQuery's html()/append() with safer alternatives like textContent for untrusted data
- Implement strict Content Security Policy with 'unsafe-inline' and 'unsafe-eval' removal
- Apply additional input validation on server-side for title fields - whitelist safe characters and enforce length limits
- Use framework-provided templating with auto-escaping (e.g., Vue, React) instead of manual string concatenation
- Audit all locations where user-controlled deployment key attributes are rendered
- Consider using data attributes instead of direct HTML injection for dynamic content

## Variant hunting
Check all other deployment key attributes (description, notes fields) for similar XSS vulnerabilities
Search for other uses of user-controlled SSH key metadata in dropdowns or list renderings
Review other settings pages that render user-supplied titles or names in dropdowns
Examine API endpoints that return deployment key data - ensure responses are properly escaped in frontend
Look for similar patterns in other GitLab features using deprecated_jquery_dropdown
Check if access_dropdown.js has other vulnerable rendering functions
Test other resource types (Deploy tokens, SSH keys) for identical vulnerability patterns
Review if other maintainer-only features have similar privilege escalation through data injection

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1059

## Notes
This is a high-impact vulnerability because: (1) It affects authenticated users with maintainer roles, (2) CSP bypass is a critical factor allowing script execution despite security headers, (3) jQuery's HTML rendering is a common pitfall, (4) The vulnerability is triggered in a commonly-accessed settings page, (5) An attacker with lower privileges could add themselves as maintainer to inject the payload. The reporter properly identified that this is not self-XSS since maintainers can add other maintainers. The direct example URL showing the vulnerability was provided, demonstrating reproducibility.

## Full report
<details><summary>Expand</summary>

### Summary

This javascript [function](https://gitlab.com/gitlab-org/gitlab/-/blob/85fbd72dc08bcedcb9fe80fad4df798e9527ded8/app/assets/javascripts/projects/settings/access_dropdown.js#L534) is vulnerable:


```javascript
  deployKeyRowHtml(key, isActive) {
    const isActiveClass = isActive || '';

    return `
      <li>
        <a href="#" class="${isActiveClass}">
          <strong>${key.title}</strong>
          <p>
            ${sprintf(
              __('Owned by %{image_tag}'),
              {
                image_tag: `<img src="${key.avatar_url}" class="avatar avatar-inline s26" width="30">`,
              },
              false,
            )}
            <strong class="dropdown-menu-user-full-name gl-display-inline">${escape(
              key.fullname,
            )}</strong>
            <span class="dropdown-menu-user-username gl-display-inline">${key.username}</span>
          </p>
        </a>
      </li>
    `;
  }
```

It is used to render a deployment key in a dropdown item. Because the deployment title is controlled by users, it can be any html content, such as, `<script>alert(document.domain)</script>`. Furthermore, the html content will be [rendered](https://gitlab.com/gitlab-org/gitlab/-/blob/85fbd72dc08bcedcb9fe80fad4df798e9527ded8/app/assets/javascripts/deprecated_jquery_dropdown/gl_dropdown.js#L396) using jQuery, so the `<script>` tag will be executed despise of CSP with `script-src ` having  `'strict-dynamic'`  value:

```javascript
  renderMenu(html) {
    if (this.options.renderMenu) {
      return this.options.renderMenu(html);
    }
    return $('<ul>').append(html);
  }
```

### Steps to reproduce

1. In an existing project or create a new one, goto `Settings`/`Repository`. Then fill the form in `Deploy keys` as the following:

- `Title`:  `test <script>alert(document.domain)</script>`
- `Key`:  `ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCkhkyrQJvb30Q5lLZzxeALqCyBrLOh+QzRYWh+gPGpqi2efyGMf5beN2zda66OI6DaclB31SJ0jYzaYKgKXQw7rzu/IYazONdy5lz5O2iUB2BkDzJYZ+BObTaTCjyDgSvNNuezUqNXXqoXftEMa1l0+FRSkTusH5F2P3JCV3Tf1BBQImrbDIpdc6ps+UxsiX7S/dT+7bNIVXblC8s8k+AK4CWsC2KmfMToK35pk+sa9JI+rb26hzv8IHA8n7cqXOmR5qAj2qX962p1kOLNXCyHJAKAIfRXCuDPbXiB+kjnu478eIcudOPveo3CK3G6hBI0hPSRfoyAUIubcddnnbhR `
- `Grant write permissions to this key`:  Checked

Then click `Add key` button to save the form.

{F1752821}


__NOTE__: 

- `Title` can be any HTML content that represents the attack payload. In the example above, we just show an alert containing the current domain.
- `Key` can be any valid SSH public key. In the example above, I give you a random key so that you can copy-paste into the form without the need to generate a key

2. Always in the `Settings`/`Repository` page, click on `Protected branches` link to expand its form
3. Click on the dropdown box under `Allowed to push `, you should see an alert that was generated when the payload above being executed

{F1752822}

__NOTE__:

- This is not self-XSS as any project maintainer can access to the settings page. Furthermore a victim can be added as a project maintainer without their explicit acceptation
- The Step 2 can be ignored by accessing directly within `#js-protected-branches-settings` on the url, for example, `https://gitlab.com/yvvdwf/xss/-/settings/repository#js-protected-branches-settings`

### Impact

XSS with CSP bypass allows attacks to perform arbitrary malicious requests on behalf of victims on HTTP client side, such as, do an API request to access to private resources, etc.

### Examples

https://gitlab.com/yvvdwf/xss/-/settings/repository#js-protected-branches-settings

### What is the current *bug* behavior?

Deployment title is not sanitized

### What is the expected *correct* behavior?

Deployment title should be sanitized

### Output of checks

This bug happens on GitLab.com

## Impact

XSS with CSP bypass allows attacks to perform arbitrary malicious requests on behalf of victims on HTTP client side, such as, do an API request to access to private resources, etc.

</details>

---
*Analysed by Claude on 2026-05-12*
