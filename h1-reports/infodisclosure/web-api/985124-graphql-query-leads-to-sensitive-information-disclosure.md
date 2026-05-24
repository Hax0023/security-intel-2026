# GraphQL Query leads to sensitive information disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 985124 | https://hackerone.com/reports/985124
- **Submitted:** 2020-09-18
- **Reporter:** chroduath
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Privacy Violation
- **CVEs:** None
- **Category:** web-api

## Summary
> NOTE! Thanks for submitting a report! Please replace *all* the (parenthesized) sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

### Summary

Graphql Query mentioned below disclosed emails of profiles which are not visible on their public pages in gitlab




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

> NOTE! Thanks for submitting a report! Please replace *all* the (parenthesized) sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

### Summary

Graphql Query mentioned below disclosed emails of profiles which are not visible on their public pages in gitlab


### Steps to reproduce

1> Go to Gitlab Graphql Explorer (https://gitlab.com/-/graphql-explorer)
2>  Use the query to fetch the information 

    {
    users {
    edges {
      node {
        username
        email
        avatarUrl
        status {
          emoji
          message
          messageHtml
         }
        }
       }
      }
     }

3> Navigate through any of the public profile of the usernames  fetched  with url : https://gitlab.com/username
4> Email information is not displayed in the public profile while the graphql query fetches it 

### Impact

This can be abused since email address is not publicly visible through gitlab profile. Any person can access user emails and try to hack their accounts using brute-force etc.

### What is the current *bug* behavior?

It displays sensitive information about the user which is not available in their public profile 

### What is the expected *correct* behavior?

it should only display public profile information such as username but not email

### Relevant logs and/or screenshots

Screenshot attached

## Impact

This can be abused since email address is not publicly visible through gitlab profile. Any person can access user emails and try to hack their accounts using brute-force etc

</details>

---
*Analysed by Claude on 2026-05-24*
