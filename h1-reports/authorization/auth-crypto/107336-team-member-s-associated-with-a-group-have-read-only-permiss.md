# Team Members with 'Post Internal Comments' Permission Can Post Public Comments via is_internal Parameter Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 107336 | https://hackerone.com/reports/107336
- **Submitted:** 2015-12-29
- **Reporter:** dz_samir
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Broken Access Control, Authorization Bypass, Improper Input Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A team member with restricted 'Post internal comments' permission could bypass access controls by appending a comma to the is_internal parameter, allowing them to post comments visible to all report participants instead of only internal team members. This occurs due to improper validation of the is_internal boolean parameter which accepts malformed values.

## Attack scenario
1. Attacker is a team member with limited 'Post internal comments' permission on a HackerOne group
2. Attacker crafts a comment submission request with is_internal=, (comma instead of boolean)
3. The backend fails to properly validate the is_internal parameter and treats the malformed value as false/null
4. The comment is submitted as a public comment visible to all participants including the reporter
5. Reporter and other participants see the internal team comment, potentially revealing sensitive information
6. Attacker gains unauthorized visibility of their restricted comments to external parties

## Root cause
Insufficient input validation on the is_internal parameter. The application likely uses a simple boolean check that doesn't properly validate the parameter value, allowing malformed inputs like 'is_internal=,' to pass through and be interpreted as false/public rather than being rejected.

## Attacker mindset
A malicious or negligent team member seeking to expose internal comments to reporters and other participants, either to leak sensitive remediation details, coordinate attacks, or exfiltrate confidential information shared in internal discussions.

## Defensive takeaways
- Implement strict input validation for boolean parameters - reject any value that is not explicitly 'true' or 'false'
- Use server-side permission enforcement independent of client-supplied parameters
- Validate all security-critical parameters against a whitelist of acceptable values
- Apply role-based access control checks before processing comment visibility
- Log and audit access control failures for security monitoring
- Test parameter tampering and type coercion as part of security testing
- Use strongly-typed enums or constants for permission-related fields rather than relying on string parsing

## Variant hunting
Test other boolean parameters with comma injection (add_reporter_to_original=,)
Try alternative malformed values: is_internal=null, is_internal=undefined, is_internal=0x00
Test with spaces and special characters: is_internal= , is_internal=;
Check if other permission levels can be bypassed similarly (e.g., escalating to admin actions)
Test permission bypass on different report actions and endpoints
Attempt Type Juggling attacks with numeric/array values: is_internal[]=false

## MITRE ATT&CK
- T1190
- T1110
- T1548
- T1556

## Notes
This is a classic authorization bypass vulnerability arising from loose parameter validation. The use of a comma as a payload suggests the backend may be using string manipulation or CSV parsing that fails to properly handle edge cases. The PoC video referenced in the report would have provided visual confirmation of the bypass. The vulnerability affects information disclosure (internal comments exposed to reporters) which could lead to further attacks or operational security failures.

## Full report
<details><summary>Expand</summary>

Hello Hackerone,

I find bug with it 
team Member(s) associated with a  Group have only permission (Post internal comments) can post comment to all the participants 

Bypass it just with Add comma  ','      is_internal=, 


message=test&substate=&is_internal=,&reference=&add_reporter_to_original=false&reply_action=add-comment&reports_count=1&report_ids%5B%5D=107329

response 
{"flash":"Comment was created successfully.","reports":[{"latest_activity":"2015-12-29T13:35:34.210Z","id":107329,"url":"https://hackerone.com/reports/107329","title":"Demo report: XSS in \u003chttp://a\u003e home page","state":"open","substate":"new","readable_substate":"New","created_at":"2015-12-29T12:48:29.534Z","reporter":{"username":"demo-researcher","url":"https://hackerone.com/demo-researcher"},"team":{"id":1607,"url":"https://hackerone.com/testtest10","handle":"testtest10","name":"\u003chttp://a\u003e","profile_picture_urls":{"small":"https://profile-photos.hackerone-user-content.com/production/000/001/607/fe7b2a22db2cef08c85e527846ecffc358a396de_small.png?1430615268","medium":"https://profile-photos.hackerone-user-content.com/production/000/001/607/b6ddcfa6d5ff3f1b8703197372452b3278c61869_medium.png?1430615268"},"permissions":[]}}]}


PoC video:https://www.dropbox.com/s/sxvzyqlyz5silt7/Hackerone.mov?dl=0


Thanks 

Hadji Samir

</details>

---
*Analysed by Claude on 2026-05-24*
