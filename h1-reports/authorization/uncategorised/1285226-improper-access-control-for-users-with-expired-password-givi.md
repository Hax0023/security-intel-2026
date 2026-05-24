# Improper Access Control for Users with Expired Password via API and Git

## Metadata
- **Source:** HackerOne
- **Report:** 1285226 | https://hackerone.com/reports/1285226
- **Submitted:** 2021-07-30
- **Reporter:** joaxcar
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Authentication, Improper Access Control, Insufficient Authorization Validation, Authentication Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
Users with expired passwords could bypass authentication controls and maintain full API access (REST, GraphQL) and Git HTTP access through valid personal access tokens. This vulnerability was a regression introduced by a LDAP-compatibility fix that inadvertently reopened access for non-LDAP accounts with expired passwords.

## Attack scenario
1. Administrator resets a user's password, setting password expiration timestamp to current time
2. User is blocked from web UI login and forced to change password upon next login attempt
3. Attacker uses previously generated personal access token to authenticate to REST API endpoint
4. Attacker retrieves private project data via API that should be inaccessible
5. Attacker clones private Git repositories using HTTP access with the expired password account
6. Attacker maintains persistent access through token-based authentication while being locked out from interactive sessions

## Root cause
A merge request (MR-63466) intended to fix LDAP compatibility issues with expired password handling inadvertently removed expiration validation checks for non-LDAP user accounts. The fix failed to maintain the security control that blocks token-based API/Git access when passwords expire, only checking for this condition in web UI authentication paths.

## Attacker mindset
An insider threat or compromised account holder with expired credentials could leverage previously-issued personal access tokens to maintain unauthorized data access while appearing locked out to administrators monitoring login attempts. This is particularly valuable for persistence and lateral movement.

## Defensive takeaways
- Implement consistent authentication validation across all access vectors (web UI, REST API, GraphQL, Git) rather than per-protocol implementations
- Apply expired password checks at a centralized authentication middleware layer before token validation
- Maintain security controls when implementing compatibility fixes; use feature flags to gradually roll out changes and test across all user types
- Revoke or invalidate personal access tokens when password expiration is triggered
- Implement comprehensive test coverage for authentication regression scenarios across all affected protocols
- Use integration tests that specifically validate expired password blocking across REST, GraphQL, and Git simultaneously
- Apply principle of least privilege: tokens should respect same constraints as session-based auth

## Variant hunting
Check if other authentication mechanisms (OAuth tokens, deploy tokens, CI/CD tokens) respect expired password restrictions
Verify if LDAP-synced users with external password expiration are properly enforced
Test if read-only API scopes bypass expiration checks differently than write scopes
Examine SSH key-based Git access for similar expired password bypass
Review if Webhook tokens and integration tokens enforce expiration validation
Test if admin-impersonation tokens bypass password expiration checks

## MITRE ATT&CK
- T1078.001 - Valid Accounts: Default Accounts
- T1078.002 - Valid Accounts: Domain Accounts
- T1110.004 - Brute Force: Credential Stuffing
- T1556 - Modify Authentication Process
- T1550.001 - Use Alternate Authentication Material: Application Access Token

## Notes
This report demonstrates a critical regression pattern where security patches for one authentication path inadvertently weaken another. The vulnerability required a previously-issued token combined with an expired password state—a scenario that should be impossible but became possible due to incomplete mitigation. The reporter's reference to two prior fixes (13.12.2 and 14.0.2) shows this was a repeat issue, suggesting inadequate regression testing procedures.

## Full report
<details><summary>Expand</summary>

### Summary

Users with an "expired password" can still access the full API with tokens. This includes the REST API, GraphQL API and Git HTTP access. The same issue was mitigated in [13.12.2](https://about.gitlab.com/releases/2021/06/01/security-release-gitlab-13-12-2-released/#insufficient-expired-password-validation) as "Insufficient Expired Password Validation". That patch blocked users with expired passwords from accessing the REST API. My report [1192460](https://hackerone.com/reports/1192460) led to a patch [14.0.2](https://about.gitlab.com/releases/2021/07/01/security-release-gitlab-14-0-2-released/#a-deactivated-user-can-access-data-through-graphql) that also blocked access through GraphQL.

It seems that these patches caused some problem for users accessing GitLab instances using LDAP. And a [merge request](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/63466) trying to address this problem got merged in one of the latests releases. Unfortenetly this new "fix for LDAP" also seems to have opened up access for regular user accounts with expired passwords again.

__Images showing access through REST, GraphQL and Git with a account with expired password:__

{F1394654}

{F1394656}

{F1394657}

### Steps to reproduce
(tested on 14.1.0 self-hosted)

1. Create a user user01, and log in
2. Create a new project at https://gitlab.domain.com/projects/new#blank_project make sure to put it as `private`. Take a note of the ID of the project
3. Go to https://gitlab.domain.com/-/profile/personal_access_tokens and create a personal access token
4. Log in as an administrator
5. Go to the admin page for editing the user https://gitlab.domain.com/admin/users/user01/edit and change the users password. This triggers `password expired at` to be set to the current time. Effectively putting the user01 in the state of "expired password""
6. Trying to log in as user01 with old password will now fail, using the new password will trigger "enter a new password" page. __Do not enter a new password here as this will put the user in a unexpired state again__

{F1394655}

7. Now instead try to use the user01 token from step 2 in a REST request such as
```
curl --request GET \
  --url https://gitlab.domain.com/api/v4/projects/:ID \
  --header 'Authorization: Bearer <TOKEN>' \
```
This should show the `private` project that should not be accessible.

### Impact

A user that should not have access to the instance as the password has expired can still access the API and Git with tokens.

### What is the current *bug* behavior?

Requests to the API and Git is not blocked for users with expired password

### What is the expected *correct* behavior?

Requests to the API and Git by users with expired password should be blocked and presented with a message like `403 Forbidden - Your password expired. Please access GitLab from a web browser to update your password.` as before.

## Impact

Users with expired passwords can still access the full API and Git using tokens

</details>

---
*Analysed by Claude on 2026-05-24*
