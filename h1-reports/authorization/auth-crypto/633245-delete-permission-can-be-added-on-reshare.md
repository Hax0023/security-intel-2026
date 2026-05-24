# Delete Permission Can Be Added on Reshare in Nextcloud

## Metadata
- **Source:** HackerOne
- **Report:** 633245 | https://hackerone.com/reports/633245
- **Submitted:** 2019-07-01
- **Reporter:** phil-davis
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Privilege Escalation, Improper Access Control, Permission Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A user receiving a folder share with read+share permissions can reshare that folder to others with delete permissions they don't possess, allowing unauthorized file deletion. The vulnerability stems from an 'implied delete' permission mechanism that was designed to allow users to unshare received folders, but this permission is incorrectly propagated through resharing.

## Attack scenario
1. Attacker (user1) receives a folder share from the owner (user0) with read and share permissions only, no delete permission
2. Attacker uses the sharing API to reshare the folder to user2 or a group, explicitly setting the delete permission (bit 8) in the permissions bitmask
3. The system fails to validate that user1 lacks delete permission on the original share before allowing the reshare with elevated permissions
4. Attacker or group members (user2) gain delete capability on files within the reshared folder
5. Attacker uses delete permission to remove critical files from the original owner's folder
6. Original owner's data is compromised without authorization

## Root cause
The codebase implements 'implied delete' permission on share roots (in lib/private/Files/View.php line 1389) to allow users to unshare received shares. However, this permission is incorrectly included in the permission bitmask when resharing, and the reshare API does not validate that the resharing user actually possesses delete permission on the original share before allowing it to be granted downstream.

## Attacker mindset
An attacker with minimal permissions on shared content seeks to escalate privileges by exploiting the resharing mechanism. They recognize that permission validation occurs at reshare time rather than enforcing a maximum permission ceiling based on what they received, allowing them to grant themselves or allies permissions they never legitimately possessed.

## Defensive takeaways
- Implement permission ceiling validation: reshare permissions must be a subset of the resharing user's actual permissions on the original share
- Separate 'implied delete' (unshare capability) from actual delete permission in the permission model
- Audit all permission checks in sharing APIs to ensure they validate the source of permissions before propagation
- Implement permission inheritance chains that prevent escalation at each reshare level
- Add integration tests covering multi-level resharing scenarios with varying permission combinations
- Log and alert on permission escalation attempts during reshare operations

## Variant hunting
Check if other permissions (write, share) can be similarly escalated through resharing chains
Test resharing to groups where the resharer is a member - can they gain permissions they shouldn't have?
Examine if the same issue affects public link shares with resharing enabled
Investigate whether the 'implied delete' mechanism is also applied to other share root operations beyond unsharing
Test permission escalation through transitive group memberships and dynamic group changes
Check if the vulnerability affects federated shares across Nextcloud instances

## MITRE ATT&CK
- T1190
- T1548
- T1078

## Notes
This is a logic flaw in permission propagation rather than an authentication bypass. The vulnerability demonstrates the importance of implementing permission ceilings in collaborative systems. The reporter correctly identified the root cause in the codebase comments. The issue affects Nextcloud server master and likely 16.* release series. The attack can be executed via either API or web UI, making it practical and accessible.

## Full report
<details><summary>Expand</summary>

user0 creates folder /test
user0 creates file /test/file.txt
user0 shares folder /test with user1 with read+share permissions (17)
user1 receives the folder /test and can read-download /test/file.txt but not delete - good
user1 uses the sharing API to share folder /test with user2, and specifies read(1)+reshare(16)+delete(8)=permissions 25 e.g.

curl --user user1:user1 "http://172.17.0.1:8081/ocs/v1.php/apps/files_sharing/api/v1/shares" -H "OCS-APIRequest: true"  -X POST --data 'path=/test&shareType=0&shareWith=user2&permissions=25'

user2 deletes /test/file.txt

curl --user user2:user2 "http://172.17.0.1:8081/remote.php/dav/files/user2/test/file.txt" -H "OCS-APIRequest: true" -X DELETE

or with the webUI.

This seems to be a side-effect of https://github.com/nextcloud/server/blob/master/lib/private/Files/View.php#L1389 

```
			if ($mount instanceof MoveableMount && $internalPath === '') {
				$data['permissions'] |= \OCP\Constants::PERMISSION_DELETE;
			}
```
which seems to be there so that a user that receives a share gets "implied delete" access to the share "root" so that they can unshare. (They cannot really delete the whole received share, when they "delete" they are actually just "unsharing". But when they reshare on to `user2` then this "implied delete" is able to be passed on.

The problem also happens if user1 shares with a group, and adds the delete permission. Users in the group can delete files. user1 can share with a group that they are already a member of. That gives user1 delete access to the files in the folder.

## Impact

A malicious user can reshare any received share, adding the delete permission to the reshare. Thus giving themselves (if they are in the group) or the end-user the ability to delete files of the first user.

The scenario works with current server master. I guess it will work with 16.* release...

</details>

---
*Analysed by Claude on 2026-05-24*
