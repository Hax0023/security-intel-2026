# XSS in ZenTao Integration via Unsanitized API Response URLs

## Metadata
- **Source:** HackerOne
- **Report:** 1542510 | https://hackerone.com/reports/1542510
- **Submitted:** 2022-04-16
- **Reporter:** joaxcar
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Unsafe URL Handling, Improper Input Validation, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's ZenTao issue integration (premium feature) fails to validate URLs returned from external ZenTao API responses, allowing attackers to inject javascript: protocol URLs that execute when clicked. The vulnerability affects self-hosted GitLab instances without strict Content Security Policy enforcement, as the web_url field is directly used in breadcrumb links without sanitization.

## Attack scenario
1. Attacker sets up a malicious ZenTao-compatible API server or compromises an existing ZenTao instance
2. Attacker crafts a malicious API response containing javascript:alert(document.domain) in the 'url' field and HTML injection in the 'id' field
3. Victim GitLab admin configures the ZenTao integration pointing to attacker's server
4. Victim visits the ZenTao issue details page (/-/integrations/zentao/issues/story-1)
5. Attacker uses HTML injection in 'id' field (e.g., large image tag) to make the malicious link prominent and clickable
6. Victim clicks the crafted link, triggering JavaScript execution in GitLab domain context

## Root cause
The ZenTao serializer (issue_entity.rb) exposes the 'url' field directly without validating that it contains a safe HTTP(S) URL, only sanitizing the 'id' field without HTML encoding. The web_url is then rendered in breadcrumb links without additional escaping.

## Attacker mindset
An attacker with network position (MITM) or control over the configured ZenTao server can perform supply-chain style attacks by poisoning API responses. The attack leverages trust in external integrations and the GitLab UI's incorporation of untrusted data.

## Defensive takeaways
- Always validate and whitelist URL schemes (http, https only) when rendering URLs from external APIs
- Implement URL validation at both serialization and rendering layers
- Apply HTML encoding/escaping consistently across all user-controllable and external data
- Use allowlist-based URL scheme validation (e.g., only allow http/https) rather than blacklist approaches
- Implement strict CSP as defense-in-depth, but do not rely on it as primary control for self-hosted instances
- Sanitize both the data field and the context where it's rendered (breadcrumbs, links, etc.)
- Consider using URL validation libraries that prevent javascript: and data: URLs

## Variant hunting
Check other integrations (JIRA, GitHub, etc.) for similar URL handling in serializers
Review all external API integrations that render user-facing URLs (issue trackers, CI/CD, monitoring tools)
Search for other uses of the pattern 'expose :web_url' or similar direct field exposure in serializers
Test data: URLs, vbscript: URLs, and other protocol-based XSS vectors in ZenTao and similar integrations
Check if comments, descriptions, or other fields from ZenTao API are also unsanitized
Review avatar URLs and other image sources for similar injection vectors

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
This is a follow-up to report 1533976 affecting a different integration. The vulnerability requires either a compromised external service or MITM capability. The CSP bypass potential is explicitly stated as unknown by the researcher. The attack is more practical on self-hosted instances due to relaxed CSP policies compared to GitLab.com. The combination of HTML injection in 'id' field with XSS in 'url' field demonstrates chaining of multiple weaknesses. Requires premium subscription to exploit on GitLab, limiting exposure.

## Full report
<details><summary>Expand</summary>

### Summary

The ZenTao issue integration (premium feature) is susceptible to an XSS attack by delivering modified API responses to GitLab.

This is related and similar to my report https://hackerone.com/reports/1533976 but this time affecting the ZenTao integration.

A user can create a project and configure ZenTao to be used as an external issue tracker. [ducumentation](https://docs.gitlab.com/ee/user/project/integrations/zentao.html). If this is done on a `premium` instance the integration will add an `issue list` to the project displaying ZenTao issues, and clicking one of these issues will display issue details for a single ZenTao issue. The URL for a single issue looks like

https://gitlab.example.com/GROUP/PROJECT/-/integrations/zentao/issues/story-1

Visiting this page will trigger the GitLab backend to make an API request to the configured ZenTao instance like this

https://zentao.example.net/api.php/v1/issues/story-1

and the response from such a request looks like

```json
{
    "issue": {
        "id": "story-1",
        "title": "story",
        "labels": [ ],
        "pri": 3,
        "openedDate": "2021-08-10T08:25:18Z",
        "openedBy": {
            "id": 1,
            "account": "admin",
            "realname": "admin",
            "avatar": "https://www.gravatar.com/avatar/21232f297a57a5a743894a0e4a801fc3?d=identicon&s=80",
            "url": "https://jihudemo.zentao.net/index.php?m=user&f=profile&userID=1"
        },
        "lastEditedDate": "2021-08-10T08:25:18Z",
        "lastEditedBy": "admin",
        "status": "opened",
        "url": "https://jihudemo.zentao.net/index.php?m=story&f=view&storyID=32",
        "desc": "",
        "assignedTo": [],
        "comments": [ ]
    }
}
```
 This response is serialized by [ee/app/serializers/integrations/zentao_serializers/issue_entity.rb](https://gitlab.com/gitlab-org/gitlab/-/blob/master/ee/app/serializers/integrations/zentao_serializers/issue_entity.rb)

The interesting part of this file is

```ruby
     expose :web_url do |item|
        item['url']
      end
```

and also 

```ruby
      expose :id do |item|
        sanitize(item['id'])
      end
```

The `:web_url` does not check for correctness of the URL and can thus be given a JavaScript URL such as `javascript:alert(document.domain)`. The `:id` is sanitized by ruby sanitizer, but is not HTML encoded. This will open up a "safe" HTML injection, which we can use to make the attack easier to pull of.

When viewing a ZenTao issue details page the `:web_url` and `:id` is used to create the last part of the breadcrumb links. By adding this to our API response

```json
{
   "id": "<img src=# height=10000 width=10000>",
   "url": "javascript:alert(document.domain)"
}
```

The details page will now display a giant image that on click will trigger the XSS.

Here I use an image tag just to prove that the injection. The `:id` HTML injection can be customized to have the victim more prone to clicking the link.

Infected page:
{F1695165}

Popup:
{F1695164}

### Steps to reproduce

Using my hosted server (see example further down for self hosting the attack):
1. Log in with a user on a self hosted GitLab instance with premium subscription (call the user `user1`)
2. Create a new project, call it `project1`
3. Go to https://gitlab.example.com/user1/project1/-/integrations/zentao/edit
4. Fill in the form. Put `https://joaxcar.com` in the server field. Leave the API field empty, add anything in the username and password.
5. Go to
https://gitlab.example.com/user1/project1/-/integrations/zentao/issues/story-1
6. Click the big white square
7. XSS triggered

To self host the API make sure to host a server that will deliver this payload with a `application/json` response to calls to `/api.php/v1/issues/story-1`

payload
```json
{
    "issue": {
        "id": "<img src=# height=10000 width=10000>",
        "title": "Attack",
        "labels": [],
        "pri": 3,
        "openedDate": "2021-08-10T08:25:18Z",
        "openedBy": {
            "id": 1,
            "account": "asd",
            "realname": "admin",
            "avatar": "https://www.gravatar.com/avatar/21232f297a57a5a743894a0e4a801fc3?d=identicon&s=80",
            "url": "https://example.com"
        },
        "lastEditedDate": "2021-08-10T08:25:18Z",
        "lastEditedBy": "asd",
        "status": "asd",
        "url": "javascript:alert(document.domain)",
        "desc": "description",
        "assignedTo": [],
        "comments": []
    }
}
```

### Impact

Full XSS on self hosted GitLab instances. A victim needs to visit the infected page and made to click a special link (can be made easy to click)

### What is the current *bug* behavior?

ZenTao issue URLs are not sanitized

### What is the expected *correct* behavior?

Javasript URLs should be filtered

### CSP
This attack does not work on GitLab.com as the CSP rules block any JavaScript URL. I don't know of any bypass to this. But it does affect self-hosted instances that have not configured CSP. I calculated my CVSS score as per attacking a self-hosted instance. GitLab team can modify this according to your current treatment of these issues!

### Ruby sanitation
The ZenTao issues uses a lot of `ruby sanatize` sanitization. This is strict enough to prevent any serious code injection but still allows for some HTML tags to be included where they are supposed not to be. Like in ID in this issue.

Best regards
Johan

## Impact

Full XSS on self hosted GitLab instances. A victim needs to visit the infected page and made to click a special link (can be made easy to click)

</details>

---
*Analysed by Claude on 2026-05-12*
