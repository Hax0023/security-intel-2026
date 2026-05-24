# Unprotected Api EndPoints

## Metadata
- **Source:** HackerOne
- **Report:** 511536 | https://hackerone.com/reports/511536
- **Submitted:** 2019-03-18
- **Reporter:** kaushalag29
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
## Summary:
I am able to automate the get/post requests of the following api end-points with a python script which can lead to heavy load to server resulting in dos attack or buffer overflow.
/internal_api/v0.2/getSuggestedProjects
/internal_api/v0.2/getLanguages
/internal_api/v0.2/getLoggedInUser
/internal_api/v0.2/getSecuritySettings
/internal_api/v0.2/getActiveOAuthGrants
/internal_api/v0.2/get

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

## Summary:
I am able to automate the get/post requests of the following api end-points with a python script which can lead to heavy load to server resulting in dos attack or buffer overflow.
/internal_api/v0.2/getSuggestedProjects
/internal_api/v0.2/getLanguages
/internal_api/v0.2/getLoggedInUser
/internal_api/v0.2/getSecuritySettings
/internal_api/v0.2/getActiveOAuthGrants
/internal_api/v0.2/getAccountEmails
/internal_api/v0.2/getExternalAccounts
/internal_api/v0.2/getAuthenticationProviders
/internal_api/v0.2/getActivePRIntegrations
/internal_api/v0.2/getProjectLatestStateStats
/internal_api/v0.2/getBlogPosts
/internal_api/v0.2/setUsername
/internal_api/v0.2/savePublicInformation

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Create an account  lgtm-com.pentesting.semmle.net.
  2. Get The cookie and nonce value of your logged in session by intercepting post/get requests with burpsuite.
  3. Use the cookie and nonce value in dos.py script(attached) inorder to execute endless api calls.
  4.Watch Video Attached as POC. 

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]
Video and Script is attached.

  * [attachment / reference]

## Impact

Leading to heavy load on server that can lead to dos attack or buffer overflow using post requests with no rate limit restriction.

</details>

---
*Analysed by Claude on 2026-05-24*
