# Insufficient Type Check in DeleteAnnotation Mutation Allows Unauthorized Project/Repository Deletion

## Metadata
- **Source:** HackerOne
- **Report:** 960244 | https://hackerone.com/reports/960244
- **Submitted:** 2020-08-17
- **Reporter:** ledz1996
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Insufficient Type Validation, Authorization Bypass, Insecure Direct Object References (IDOR), Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A GraphQL mutation endpoint for deleting dashboard annotations lacks proper type checking on the input ID parameter, allowing a developer-level user to delete arbitrary objects including projects and repositories by passing their global IDs. The vulnerability exists because the `find_object` method in the Base mutation class uses `GitlabSchema.object_from_id()` without validating that the returned object is actually an Annotation, combined with overly permissive permission checks that only require developer role.

## Attack scenario
1. Attacker (User B) is added as a Developer to a target project (Project A) by the project owner (User A)
2. Attacker enumerates or discovers the global ID (gid) of the project itself or other sensitive objects like repositories or groups
3. Attacker crafts a GraphQL mutation calling `deleteAnnotation` with the target project's gid instead of an annotation gid
4. The mutation bypasses type validation in `find_object()` which returns any object matching the gid without checking if it's an Annotation
5. The authorization check only verifies if user has developer role (`:delete_metrics_dashboard_annotation` permission), which passes for the attacker
6. The DeleteService deletes the project/repository/group object instead of an annotation, causing data loss

## Root cause
The vulnerability has two complementary causes: (1) The `find_object` method in the Base mutation class uses `GitlabSchema.object_from_id(id)` which returns any object type matching the provided ID without type validation; (2) The `authorized_find!` method does not verify that the returned object is actually an Annotation before passing it to the delete service; (3) The permission check in DeleteService uses a generic permission that doesn't validate object type, allowing deletion of non-annotation objects.

## Attacker mindset
An insider threat or low-privileged collaborator seeking to sabotage projects or competitors' work by deleting critical infrastructure. The attacker leverages their legitimate developer access as a stepping stone to escalate privileges and delete objects far beyond their intended scope.

## Defensive takeaways
- Always validate that objects returned from ID deserialization match the expected type before proceeding with mutations
- Implement strict type checking in GraphQL mutations: cast to expected class and raise error if type mismatch occurs
- Use specific, granular permission checks that validate both the user's role AND the object type being operated on
- Apply the principle of least privilege: ensure permission names and checks directly correspond to the specific resource and action
- Add integration tests that verify mutations reject IDs of incorrect object types, especially from lower-privileged users
- Implement consistent patterns across all mutation base classes to enforce type validation before authorization
- Consider using GraphQL's type system more strictly to prevent ID confusion attacks

## Variant hunting
Search for similar patterns in other GitLab GraphQL mutations that: (1) use `GitlabSchema.object_from_id()` without type validation; (2) call `authorized_find!()` on mutations that accept generic ID parameters; (3) implement permission checks that don't verify object type; (4) have loose permission requirements (developer-level) for deletion operations. Check other mutation base classes and delete/update mutations across metrics, issues, merge requests, and other features.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1078 - Valid Accounts
- T1531 - Account Access Removal

## Notes
This is a critical privilege escalation vulnerability similar to #858671 mentioned in the report. The bug affects GitLab 13.2.3-ee and likely multiple versions. The attacker needs only valid developer-level access to one project to potentially delete any object in the system if they can construct valid GIDs. The fact that this is a duplicate of a similar bug suggests systemic issues with how GraphQL mutations handle object deserialization and authorization across the codebase.

## Full report
<details><summary>Expand</summary>

### Summary

Similar bug to #858671, but this time with annotations mutation: `DeleteAnnotation`

in ***app/graphql/mutations/metrics/dashboard/annotations/base.rb***

```ruby
module Mutations
  module Metrics
    module Dashboard
      module Annotations
        class Base < BaseMutation
          private

          # This method is defined here in order to be used by `authorized_find!` in the subclasses.
          def find_object(id:)
            GitlabSchema.object_from_id(id)
          end
        end
      end
    end
  end
end

```

There is no type check for `find_object` in ***app/graphql/mutations/metrics/dashboard/annotations/delete.rb***
```ruby
    annotation = authorized_find!(id: id)

            result = ::Metrics::Dashboard::Annotations::DeleteService.new(context[:current_user], annotation).execute
```

And luckily, Developer is sufficient for the permission check 

***app/services/metrics/dashboard/annotations/delete_service.rb***
```ruby
Ability.allowed?(user, :delete_metrics_dashboard_annotation, annotation)
```

### Steps to reproduce

1. For User A, Create project A Private adding User B as Developer
2. For User B, execute the following mutation in `http://gitlab.example.vm/-/graphql-explorer`

```graphql
mutation {
  deleteAnnotation(input: {id: "gid://Gitlab/Project/<project-id>"}) {
    clientMutationId
  }
}
```
3. Project disappear along with Repository

███████

#### Results of GitLab environment info

```
System information
System:     
Proxy:      no
Current User:   git
Using RVM:  no
Ruby Version:   2.6.6p146
Gem Version:    2.7.10
Bundler Version:1.17.3
Rake Version:   12.3.3
Redis Version:  5.0.9
Git Version:    2.27.0
Sidekiq Version:5.2.9
Go Version: unknown

GitLab information
Version:    13.2.3-ee
Revision:   640e2695514
Directory:  /opt/gitlab/embedded/service/gitlab-rails
DB Adapter: PostgreSQL
DB Version: 11.7
URL:        http://gitlab.example.vm
HTTP Clone URL: http://gitlab.example.vm/some-group/some-project.git
SSH Clone URL:  git@gitlab.example.vm:some-group/some-project.git
Elasticsearch:  no
Geo:        no
Using LDAP: no
Using Omniauth: yes
Omniauth Providers: 

GitLab Shell
Version:    13.3.0
Repository storage paths:
- default:  /var/opt/gitlab/git-data/repositories
GitLab Shell path:      /opt/gitlab/embedded/service/gitlab-shell
Git:        /opt/gitlab/embedded/bin/git
```

## Impact

Unauthorized deleting of repository/project by maintainers, developers

</details>

---
*Analysed by Claude on 2026-05-24*
