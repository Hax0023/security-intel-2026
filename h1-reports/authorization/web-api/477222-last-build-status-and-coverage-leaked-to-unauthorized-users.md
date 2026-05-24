# Last build status and coverage leaked to unauthorized users via CI badges

## Metadata
- **Source:** HackerOne
- **Report:** 477222 | https://hackerone.com/reports/477222
- **Submitted:** 2019-01-09
- **Reporter:** xanbanx
- **Program:** GitLab
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Authorization bypass, Information disclosure, Access control bypass
- **CVEs:** CVE-2019-5463
- **Category:** web-api

## Summary
GitLab CI badge endpoints for build status and coverage did not properly enforce authorization checks, allowing unauthorized users to view pipeline and coverage information despite restricted project access. The vulnerability affected public projects (unauthenticated access), internal projects (any authenticated user), and private projects (guest users).

## Attack scenario
1. Attacker identifies a target GitLab project with restricted pipeline access and disabled public builds
2. Attacker constructs a direct URL to the badge endpoint (e.g., /badges/master/pipeline.svg or /badges/master/coverage.svg)
3. For public/internal projects, attacker accesses the badge without authentication or with minimal privileges
4. SVG response reveals the actual build status or coverage percentage for the target branch
5. Attacker can enumerate multiple branches to map CI/CD pipeline status across the project
6. Leaked information could reveal build failures, security testing status, or code coverage metrics

## Root cause
Badge rendering endpoints did not implement proper authorization validation before returning build status or coverage information. The application treated badge requests as publicly available assets without verifying the requester's access level to pipelines.

## Attacker mindset
An attacker seeks to gather intelligence about a target organization's CI/CD pipeline health, code quality metrics, or build status without proper authorization. This could be reconnaissance for further attacks or competitive intelligence gathering.

## Defensive takeaways
- Implement authorization checks on all endpoints that expose sensitive information, including badge/status endpoints
- Apply the same access control rules to derived content (badges) as to the underlying resources (pipelines)
- Consider whether static assets should respect project visibility settings before rendering
- Audit all endpoints that return information about builds, tests, or deployments for proper permission validation
- Test authorization bypass scenarios including unauthenticated, authenticated, and guest user access levels

## Variant hunting
Check for similar bypass on other GitLab status endpoints (merge request status, job artifacts)
Test badge endpoints with different branch names and pipeline types
Examine other CI/CD platforms (Jenkins, GitHub Actions, GitLab CI) for similar badge authorization issues
Look for other endpoints that generate images/assets from restricted data without authorization checks
Test whether project export or archive features also bypass pipeline visibility restrictions

## MITRE ATT&CK
- T1190
- T1040
- T1526

## Notes
This is a classic authorization bypass where derived content (SVG badges) exposed sensitive information about restricted pipelines. The vulnerability demonstrated that security controls must be applied consistently across all endpoints, including those returning seemingly innocuous assets like status badges.

## Full report
<details><summary>Expand</summary>

GitLab CI supports creating badges for the latest build/coverage on a certain branches. However, with restricted access, where users do not have access to pipelines, users still have access to the build/coverage status of any branch.
This access works for different configurations:

1. For public projects with restricted pipeline access, any user (the user does not need to be signed in) has access to this information
2. For internal projects with restricted pipeline access, any authenticated user has access to this information
3. For private projects, any Guest user of that project has access to this information

## Steps to reproduce

1. Create a public repo, configure CI, and push some code. Consider the project namespace to be `test/cibadges` in these steps.
2. Restrict the visibility of whole repo to `Project Members Only` and disable `Public builds` in the CI settings
3. As a non-authenticated user visit the following page: `https://example.gitlab.com/test/cibadges/badges/master/pipeline.svg`

This will return a SVG image showing the build status of the `master` branch. This works for any other branch as well. The same thing also works with the coverage badge accessible via the following link `https://example.gitlab.com/test/cibadges/badges/master/coverage.svg`
The same works for the other configurations as mentioned above.

Even if repos and therefore also pipelines are completely disabled, the last build status/coverage still can be retrieved via the badges link.

## Steps to mitigate

Perform proper authorization check handling a badge request

## Impact

Users with restricted pipeline access can see the build/coverage status for different branches

</details>

---
*Analysed by Claude on 2026-05-24*
