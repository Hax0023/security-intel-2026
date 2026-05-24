# Privilege Escalation via IDOR in Group Sharing Feature - Private Group and Repository Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 131210 | https://hackerone.com/reports/131210
- **Submitted:** 2016-04-15
- **Reporter:** jobert
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR), Privilege Escalation, Information Disclosure, Broken Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An IDOR vulnerability in GitLab's group sharing feature allows an unauthenticated attacker to gain read access to private groups by modifying the link_group_id parameter during project-to-group sharing. Once access is obtained, the attacker can enumerate private repositories, issues, milestones, and team members via the GitLab API, exposing sensitive project metadata and descriptions.

## Attack scenario
1. Attacker creates a dummy project as an unprivileged user (jane)
2. Attacker navigates to the group_links endpoint to share the project with a public group
3. Attacker intercepts the POST request and modifies link_group_id parameter to target an unknown private group ID
4. Server accepts the modified request without authorization check, granting attacker read access to private group
5. Attacker uses GitLab API v3 endpoint /api/v3/groups/{id}/projects.json with their API token to enumerate all private repositories in the group
6. Attacker extracts sensitive data including repository names, descriptions, SSH/HTTP URLs, and project metadata

## Root cause
The Projects::GroupLinksController lacks proper authorization validation when processing group link requests. The controller accepts any link_group_id parameter without verifying that the authenticated user has permission to link their project to that specific group. The vulnerable code at line 11 of app/controllers/projects/group_links_controller.rb does not perform access control checks before establishing the group link relationship.

## Attacker mindset
An attacker would recognize that the group sharing feature is client-side trusted and that the server likely performs minimal validation on the group ID being linked. By manipulating this parameter to iterate through potential group IDs, they can discover private groups and leverage the API to systematically enumerate organizational assets without detection. The low barrier to entry (only requiring an account) makes this an attractive reconnaissance technique.

## Defensive takeaways
- Implement strict server-side authorization checks before creating group links - verify the user has permission to access the target group
- Use whitelist-based access control: only allow linking to groups where the user is already a member
- Validate that group visibility permissions are honored at the API endpoint level, not just the UI
- Implement rate limiting and logging on group link creation endpoints to detect enumeration attempts
- Audit API endpoints (/api/v3/groups/{id}/projects) to ensure they respect visibility settings and don't leak metadata to unauthorized users
- Implement comprehensive access control tests that verify users cannot access resources via direct ID manipulation
- Use consistent permission checks across all related endpoints (UI and API)

## Variant hunting
Check other sharing features (project links, member invitations) for similar IDOR vulnerabilities
Test if similar enumeration works for other API endpoints: /api/v3/groups/{id}/members, /api/v3/groups/{id}/issues
Verify if namespace IDs can be enumerated systematically to discover all private groups in an instance
Check if other controller actions in GroupLinksController lack proper authorization
Test whether read-only operations on private groups leak additional sensitive data through different API versions
Investigate if archived or deleted groups can be accessed through this vector

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate Cloud Resources
- T1087 - Account Discovery
- T1589 - Gather Victim Identity Information
- T1592 - Gather Victim Host Information
- T1110 - Brute Force

## Notes
This vulnerability demonstrates the critical importance of server-side authorization validation in multi-tenant applications. The attacker doesn't need to compromise credentials or exploit authentication; the vulnerability exists purely in authorization logic. The ability to chain this with API enumeration to systematically discover all private organizational resources makes this particularly dangerous. The fix should focus on the authorization check itself rather than hiding group IDs, as any identifier (sequential or UUID) can be enumerated if authorization is missing. This is a classic example of why client-side data should never be trusted without server-side validation.

## Full report
<details><summary>Expand</summary>

# Vulnerability details
There is an insecure direct object reference (IDOR) issue in the group sharing feature for a project. This allows an attacker to get access to the names of private repositories of a group, issues, milestones, and the group its team members.

# Proof of concept
First, lets set up the private group. Go to http://gitlab-instance/groups/new and fill in a name and set its visibility to private. In this example, lets call the group `private-group`. Lets also create a new project in the group at http://gitlab-instance/projects/new?namespace_id=7. The ID in the URL changes depending on the ID of the group that was just created. Lets call the project `secret-project`. Memorize this ID, you need it later in the PoC.

Now to get access to the group without being a member, sign in as some user (`jane`), create a new project and call it `dummy-project`. If Jane now goes to http://gitlab-instance/groups/private-group, a 404 is shown. This is good. Now go to http://gitlab-instance/jane/dummy-project/group_links. Now select a random public group from the dropdown list. Before clicking on the "Share" button , make sure you intercept your network traffic. The request that is being sent to the server will look something like this:

```
POST /jane/dummy-group/group_links HTTP/1.1
Host: 159.xxx.xxx.xxx
...

utf8=%E2%9C%93&authenticity_token=LKWaV6ekT0zFbfFJPKRG78OyIsUvCxObht2Dn1l7p02SEa9IrefoAtdtwX%2F890lUqS2HLCtASPQyvFWmCYtJwA%3D%3D&link_group_id=6&link_group_access=40
```

Now change the `link_group_id` in this request to the ID that you memorized in the first paragraph of this section and forward the request. Your page will now show the name of the private group. If Jane now goes to http://gitlab-instance/groups/private-group, to secret group page is shown. At this point, the private repositories are still hidden.

Since the attacker has read access to the group now, there are some endpoints that leak some private information. By sending a request to the http://gitlab-instance/api/v3/groups/7/projects.json?private_token=ZJirZUgh9QGSQfaGBHDL&search=&per_page=20 endpoint with Jane's API token, the private repositories are leaked. Here's an example response:

```json
[
  {
    "id":11,
    "description":"Super secret description of this project.",
    "default_branch":null,
    "tag_list":[],
    "public":false,
    "archived":false,
    "visibility_level":0,
    "ssh_url_to_repo":"git@gitlab-instance:super-private/secret-project.git",
    "http_url_to_repo":"http://gitlab-instance/super-private/secret-project.git",
    "web_url":"http://gitlab-instance/super-private/secret-project",
    "name":"secret-project",
    "name_with_namespace":"super-private / secret-project",
    "path":"secret-project",
    "path_with_namespace":"super-private/secret-project",
    "issues_enabled":true,
    "merge_requests_enabled":true,
    "wiki_enabled":true,
    "builds_enabled":true,
    "snippets_enabled":false,
    "created_at":"2016-04-15T20:55:19.228Z",
    "last_activity_at":"2016-04-15T20:56:24.988Z",
    "shared_runners_enabled":true,
    "creator_id":1,
    "namespace":{
      "id":7,
      "name":"super-private",
      "path":"super-private",
      "owner_id":null,
      "created_at":"2016-04-15T20:42:01.718Z",
      "updated_at":"2016-04-15T20:42:01.718Z",
      "description":"Super private group.",
      "avatar":
      {
        "url":null
      },
      "share_with_group_lock":false,
      "visibility_level":0
    },
    "avatar_url":null,
    "star_count":0,
    "forks_count":0,
    "open_issues_count":1,
    "public_builds":true
  }
]
```

The repository itself can't be accessed, but there's definitely some information disclosed that the attacker shouldn't have access to. In a real world scenario, someone could iterate over all namespace IDs and get access to all private groups. From there, it could send a request to the GitLab API to gain more knowledge about the private projects.

# Fix
This can be fixed by restricting which groups can be added to a project by a user. The issue itself originates from line 11 of the `Projects::GroupLinksController`, which can be found at `app/controllers/projects/group_links_controller.rb`.

</details>

---
*Analysed by Claude on 2026-05-24*
