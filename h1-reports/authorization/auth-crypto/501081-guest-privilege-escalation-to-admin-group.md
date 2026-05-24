# Guest Privilege Escalation to Admin Group via Improper ACL Validation

## Metadata
- **Source:** HackerOne
- **Report:** 501081 | https://hackerone.com/reports/501081
- **Submitted:** 2019-02-25
- **Reporter:** gronke
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Improper Access Control, Privilege Escalation, Insufficient Authorization Checks, Unsafe Deserialization/Code Execution in Integrations
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A guest user could escalate privileges to admin by exploiting improper ACL validation in the insertOrUpdateUser method. The vulnerability chain involved adding oneself to the 'bot' group (which has manage-own-integrations permission), then creating a malicious integration script that executes arbitrary code to add the user to the admin group.

## Attack scenario
1. Guest user logs in and extracts their own user _id from browser traffic
2. Guest user calls insertOrUpdateUser method to add themselves to the 'bot' group, bypassing insufficient permission checks
3. With 'bot' group permissions, guest user creates a custom Integration with a malicious script payload
4. Guest user triggers the integration, causing the script to execute in a privileged context
5. Malicious script uses Roles.addUserRoles() to add the guest user to the 'admin' role
6. Guest user now has full administrator privileges on the Rocket.Chat server

## Root cause
Two distinct authorization flaws: (1) insertOrUpdateUser method failed to properly validate that only administrators can modify user group memberships, allowing self-assignment to privileged groups, and (2) Integration script execution context was not properly isolated from server application, allowing scripts to invoke privileged Roles API calls.

## Attacker mindset
An attacker with guest-level access would recognize that the ACL validation is incomplete and can be bypassed through a two-stage escalation. By chaining weak authorization checks with unrestricted script execution in integrations, they can reach full admin access without direct detection of privilege escalation attempts.

## Defensive takeaways
- Implement strict authorization checks in all user modification endpoints - only administrators should be able to change user roles/groups
- Apply principle of least privilege to integration script execution - sandbox scripts with no access to sensitive APIs like Roles management
- Use whitelist-based permission model rather than blacklist - explicitly define what each role CAN do rather than what it CANNOT
- Audit all endpoints that modify security-critical attributes (roles, groups, permissions) for authorization flaws
- Implement server-side session validation to prevent privilege escalation attacks chained across multiple API calls
- Log and alert on suspicious role/group modifications from low-privileged users

## Variant hunting
Search for similar patterns: (1) Other endpoints using insertOrUpdateUser or similar methods that modify user attributes, (2) Other integration/webhook/plugin execution contexts that might have access to privileged APIs, (3) Other permission checks that use blacklist rather than whitelist approach, (4) Custom script execution in admin panels, chatbots, or workflow automation features

## MITRE ATT&CK
- T1548.002
- T1190
- T1078.001
- T1059.007

## Notes
This vulnerability demonstrates the danger of chaining multiple weak security controls. While the explicit check prevented direct admin group assignment, the incomplete authorization validation on insertOrUpdateUser combined with uncontrolled integration script execution created a viable escalation path. The fix requires both preventing unauthorized group assignment AND sandboxing integration scripts from sensitive APIs.

## Full report
<details><summary>Expand</summary>

Due to improper ACLs it was found possible to escalate privileges from a guest user to admin.

As first step the guest user adds itself to the `bot` group that holds the `manage-own-integrations` permission. With this permission it is possible to create a custom Integration with a script that, if triggered, adds the user to the `admin` group.

The `insertOrUpdateUser` method improperly validates a users permissions to change its groups. Because an explicit check prevents from adding itself to the `admin` group directly, the privileges of the `bot` group need to be used to further escalate to global admin.

## Releases Affected:

  * [develop@5f0180d](https://github.com/RocketChat/Rocket.Chat/commit/5f0180dc1500b4e37b8320b39869babadb5d01cd)

## Steps To Reproduce (from initial installation to vulnerability):

(Add details for how we can reproduce the issue)

  1. Login Guest user
  2. Determine own users `_id` from browser traffic
  3. Escalate to `bot` group
  4. Create malicious Integration script
  5. Trigger Integration

## Supporting Material/References:

### Bot group privilege escalation
```json
["{\"msg\":\"method\",\"method\":\"insertOrUpdateUser\",\"params\":[{\"_id\": \"<USER_ID>\", \"roles\": [\"user\", \"bot\"]}],\"id\":\"17\"}"]
```

### Malicious Integrations Script
```javascript
this.Roles.addUserRoles("9HN4Brdmo2Qc2wsiX", "admin")
class Script {
  process_incoming_request({ request }) {};
}
```

## Suggested mitigation

  * Only allow administrators to modify user groups
  * Isolate Integration script context from server application

## Impact

Guest users can become server administrator.

</details>

---
*Analysed by Claude on 2026-05-24*
