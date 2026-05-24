# Information Disclosure: Private Program Count Enumeration via GraphQL Query

## Metadata
- **Source:** HackerOne
- **Report:** 310946 | https://hackerone.com/reports/310946
- **Submitted:** 2018-01-31
- **Reporter:** haxta4ok00
- **Program:** HackerOne
- **Bounty:** Unknown
- **Severity:** Medium
- **Vuln:** Information Disclosure, Authorization Bypass, Enumeration
- **CVEs:** None
- **Category:** web-api

## Summary
A researcher discovered that the HackerOne GraphQL endpoint allows querying soft_launch_invitations for any user by username, revealing the total_count of private programs they have been invited to. This information leakage exposes invitation metrics that should be private and could enable enumeration attacks against researchers' private program participation.

## Attack scenario
1. Attacker identifies a target HackerOne user (e.g., @jobert)
2. Attacker crafts a GraphQL query to the /graphql endpoint specifying the target username in the user field
3. Attacker requests the soft_launch_invitations field with total_count aggregation
4. GraphQL API returns the total_count of invitations (e.g., 27) without proper authorization checks
5. Attacker can enumerate multiple users to map their private program participation
6. Attacker gains intelligence about private programs and researcher involvement

## Root cause
Insufficient authorization validation on the GraphQL soft_launch_invitations query. The API allows querying invitation metadata for any user by username without verifying that the requesting user has permission to view that information. The total_count field is exposed without access control checks.

## Attacker mindset
Reconnaissance and information gathering to understand private program distribution, identify high-value targets, or map researcher participation across confidential programs for targeted attacks.

## Defensive takeaways
- Implement proper authorization checks on all GraphQL queries to ensure users can only query their own data
- Add authentication context validation before returning any user-specific invitation data
- Consider field-level security to restrict sensitive aggregated fields like total_count
- Audit GraphQL schema for other queries that may expose unintended user information
- Implement rate limiting on GraphQL queries to prevent enumeration attacks
- Use GraphQL permission directives consistently across all resolvers

## Variant hunting
Query other user-specific fields in GraphQL schema with arbitrary usernames
Test if other invitation states expose additional metadata
Attempt to enumerate team/program data through GraphQL by varying parameters
Check if profile data, bounty metrics, or other sensitive fields are similarly exposed
Test REST API endpoints for similar authorization bypass patterns
Query historical invitation data or pagination to extract full datasets

## MITRE ATT&CK
- T1534 - Internal Spearphishing (reconnaissance for target identification)
- T1589 - Gather Victim Identity Information
- T1591 - Gather Victim Org Information
- T1592 - Gather Victim Host Information

## Notes
The reporter used the example username 'jobert' to demonstrate the vulnerability. The query shows that the GraphQL endpoint accepts arbitrary usernames without proper authorization, revealing invitation counts for the new /invite/token system. This is a classic case of missing access control on a query that returns aggregated user data. The old invitation system may have had similar exposure, but the new token-based system made the vulnerability more apparent through the GraphQL interface.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hi team.
The old version of the invite program, looks simple. A link to the program in which you need to log in.Now this looks through token.So my PoC I think you can count work since you have changed the system to a new, token

**Description:**

### Steps To Reproduce

1. https://hackerone.com/graphql

POST:
`{"query":"query Directory_invitations_page($state_0:[InvitationStateEnum]!,$state_3:[InvitationStateEnum]!,$first_1:Int!,$size_2:ProfilePictureSizes!) {\\n`***user(username:\\\"jobert\\\")***` {\\n    id,\\n    ...F5\\n  }\\n}\\nfragment F0 on User {\\n  _soft_launch_invitations259p9N:soft_launch_invitations(state:$state_0,first:$first_1) {\\n    total_count\\n  },\\n  id\\n}\\nfragment F1 on InvitationsSoftLaunch {\\n  id,\\n  team {\\n    handle,\\n    url,\\n    name,\\n    about,\\n    bug_count,\\n    base_bounty,\\n    offers_bounties,\\n    currency,\\n    _profile_picture2rz4nb:profile_picture(size:$size_2),\\n    id\\n  },\\n  expires_at,\\n  state,\\n  token\\n}\\nfragment F2 on Node {\\n  id,\\n  __typename\\n}\\nfragment F3 on InvitationInterface {\\n  __typename,\\n  ...F1,\\n  ...F2\\n}\\nfragment F4 on User {\\n  _soft_launch_invitations1WD3Qk:soft_launch_invitations(state:$state_0,first:$first_1) {\\n    total_count,\\n    edges {\\n      node {\\n        id,\\n        ...F3\\n      },\\n      cursor\\n    },\\n    pageInfo {\\n      hasNextPage,\\n      hasPreviousPage\\n    }\\n  },\\n  _soft_launch_invitations2FRMOR:soft_launch_invitations(state:$state_3,first:$first_1) {\\n    total_count\\n  },\\n  id\\n}\\nfragment F5 on User {\\n  id,\\n  ...F0,\\n  ...F4\\n}","variables":{"state_0":["pending_terms","open","accepted"],"state_3":["pending_terms","open","accepted","cancelled","rejected"],"first_1":100,"size_2":"large"}}`


I take username:\\\"jobert\\\" , hi @jobert

`Result "total_count":27`

You have 27 private programs in which you have added through the new system - using /invite/token

Yes , most likely you have more number of private programs, but those that are missing, you most likely added by the old system.

Sorry i bad speak english
I hope you understand me
Thank you,haxta4ok00

F259145

## Impact

total count Private programs in order to add the system /invite/token

</details>

---
*Analysed by Claude on 2026-05-24*
