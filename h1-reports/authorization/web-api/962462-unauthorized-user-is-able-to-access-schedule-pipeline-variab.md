# Unauthorized Access to Pipeline Schedule Variables via API

## Metadata
- **Source:** HackerOne
- **Report:** 962462 | https://hackerone.com/reports/962462
- **Submitted:** 2020-08-19
- **Reporter:** vaib25vicky
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Access Control, Information Disclosure, API Authorization Bypass
- **CVEs:** CVE-2020-13351
- **Category:** web-api

## Summary
GitLab's pipeline schedule API endpoints failed to enforce the documented access control model, allowing unauthorized users to read sensitive pipeline variables and their values. Users without proper permissions could access schedule details via the REST API that should have been restricted to project owners and masters only.

## Attack scenario
1. Attacker identifies a target GitLab project with scheduled pipelines containing sensitive variables
2. Attacker obtains or creates any valid GitLab account with API token access
3. Attacker uses the public API endpoint GET /projects/{id}/pipeline_schedules/{schedule_id} with their token
4. API returns full schedule details including custom variable names and values without validating user permissions
5. Attacker reads sensitive data like database credentials, API keys, or deployment tokens stored in variables
6. Attacker uses obtained credentials to hijack schedules, modify pipeline behavior, or access protected resources

## Root cause
The API endpoint implementation did not enforce the same permission checks that the UI enforced. The backend validated permissions for web interface access but the REST API handler skipped authorization validation, directly returning schedule objects including variables to any authenticated user.

## Attacker mindset
An attacker with basic GitLab access seeks to escalate privileges and access secrets. Pipeline variables often contain credentials for deployment, databases, or external services. By bypassing UI restrictions through API endpoints, the attacker discovers an authorization bypass that grants access to sensitive configuration data intended for restricted users only.

## Defensive takeaways
- Enforce consistent authorization checks across all API endpoints and UI handlers - authorization logic must be centralized and applied uniformly
- Never assume API endpoints inherit permission models from UI - explicitly validate permissions at API layer
- Treat sensitive data fields (passwords, tokens, keys) with extra scrutiny - require highest permission levels for retrieval
- Implement authorization checks before data serialization - redact sensitive fields before returning responses
- Add integration tests validating permission enforcement across both UI and API for the same operations
- Document the security model explicitly in code comments near authorization checks
- Use consistent permission checking middleware or decorators across all endpoints

## Variant hunting
Check other API endpoints in GitLab that return sensitive configuration data (variables, secrets, credentials)
Test LIST endpoints for pipeline schedules - do they also leak variable names/values?
Examine webhook configurations, environment variables, and protected branches APIs for similar bypasses
Review UPDATE/PATCH endpoints - can unauthorized users modify schedules they shouldn't access?
Test with different user roles (guest, developer, maintainer) to identify permission boundary failures
Check if the vulnerability exists in other scheduled/automated features (CI/CD templates, recurring tasks)

## MITRE ATT&CK
- T1190
- T1613
- T1526
- T1087

## Notes
This is a classic authorization bypass where the API layer failed to enforce the documented security model. The vulnerability demonstrates that UI-level access control provides false sense of security if not enforced at the API layer. GitLab's own documentation acknowledged the intended access restrictions, making this an implementation gap rather than design ambiguity. Pipeline variables frequently contain high-value secrets, making this vulnerability particularly dangerous for credential compromise.

## Full report
<details><summary>Expand</summary>

### Summary

The feature allows to add or overwrite variables that are passed to jobs  in order to modify the behavior just for that specific instance.
 
As per this https://gitlab.com/gitlab-org/gitlab-foss/-/issues/32568#note_32531510 , the current security model is
>If you are owner of schedule (as developer) or master => you can read, modify and delete,
If you are developer => you can just list, not read,

>This allows only owners and masters to read variables assigned to the schedule. It prevents other developers from hijacking schedules, but allows master to fully control them. Master already has access to Secret Variables.

But api endpoints are cleary showing this values to everyone even if the user is not part of the project. https://docs.gitlab.com/ee/api/pipeline_schedules.html#get-a-single-pipeline-schedule


### PoC

This is my test project https://gitlab.com/thevicc/trigg with schedule pipeline which custom variables you can't read.

Now, run this to read the variable and its value

`curl  --header "Private-Token: <your_access_token>"  https://gitlab.com/api/v4/projects/20618145/pipeline_schedules/69918`

Response
{F955402}

### Steps to reproduce

* Create a project and add a schedule pipeline with custom variables
*  Only you or owner can read variables
* As second account, use the api `https://docs.gitlab.com/ee/api/pipeline_schedules.html#get-a-single-pipeline-schedule`

## Impact

This bug allows unauthorized users to read scheduled pipeline custom variables and values. As per security model, this allows other devs to hijack schedules.

</details>

---
*Analysed by Claude on 2026-05-24*
