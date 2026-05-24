# Privilege Escalation: External Program Maintainer Can Edit Churned Public Programs

## Metadata
- **Source:** HackerOne
- **Report:** 411930 | https://hackerone.com/reports/411930
- **Submitted:** 2018-09-20
- **Reporter:** haxta4ok00
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Broken Access Control, Privilege Escalation, Authorization Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
A user with privileges to maintain External Programs was able to edit certain public (churned) programs due to improper authorization checks. The attacker could modify program metadata including about section, website, Twitter handle, cover color, and potentially logo despite lacking explicit permissions to edit public programs.

## Attack scenario
1. Attacker obtains or is assigned the 'External Program Maintainer' role within HackerOne
2. Attacker identifies a churned/inactive public program (e.g., @uzbey)
3. Attacker navigates to the public program profile and discovers an 'edit' button is accessible
4. Attacker modifies program metadata fields (about, website, Twitter handle, cover color)
5. Attacker successfully persists changes to the public program profile
6. Attacker realizes the vulnerability affects multiple churned programs with the same authorization flaw

## Root cause
Authorization logic fails to properly validate that users with 'External Program Maintainer' privilege should only edit External Programs, not public programs. The authorization check likely verifies role existence but not program_type matching or churned status, allowing privilege scope creep.

## Attacker mindset
Low-skill reconnaissance mindset - researcher stumbled upon this while exploring their own permissions rather than through targeted exploitation. Responsibly reported the issue and noted it affects potentially multiple programs. Demonstrated good faith by not escalating impact and offering to continue searching.

## Defensive takeaways
- Implement explicit authorization checks that verify both user role AND target resource type match before granting edit access
- Separate authorization logic for different program states (active, churned/inactive, external) with clear role-to-resource mappings
- Audit all role-based access control assignments for scope creep and unintended permission inheritance
- Add role-specific UI element visibility - hide 'edit' buttons for resources outside the role's authorized scope
- Implement comprehensive access control tests covering edge cases like inactive/churned programs
- Log and monitor unauthorized edit attempts on resources outside user's intended scope
- Review all 'External Program Maintainer' assignments for unintended access to public programs

## Variant hunting
Check if other privileged roles (e.g., Program Manager, Support) have similar scope creep to unintended resource types
Verify if archived/deleted programs have the same authorization bypass
Test if users can edit program settings through API endpoints that lack UI-level access controls
Examine if other program metadata fields beyond listed ones are editable (e.g., program policy, scope)
Check if role permissions escalate when programs transition between states (active → churned)
Verify similar vulnerabilities in other HackerOne resource types managed by role-based access

## MITRE ATT&CK
- T1190
- T1199
- T1078

## Notes
Researcher demonstrated responsible disclosure and acknowledged language barriers. The vulnerability's low exploitability in practice (requires existing elevated privileges) and limited business impact (metadata-only changes) supports the medium severity assessment. The fact that multiple programs may be affected increases concern. Report suggests this may be a known edge case in transitioning programs rather than a systemic authorization architecture flaw.

## Full report
<details><summary>Expand</summary>

**Summary:**
You wrote that some programs are behind, but you are trying to get them back (sorry maybe bad translation)

**Description:**
Apparently because of a system error, I have access to change information in the public program.
This option is given only for external programs.But here is a public program, so I create a report

### Steps To Reproduce

1. Go to @uzbey -- https://hackerone.com/uzbey
2. I can see button `edit`
F348953
3. Try to change `about`
4. I write -- `test @jobert`
F348952

Check about page
`The goal of Uzbey is to create the worlds largest selfie to be launched into space. test @jobert`
Hi @jobert :)


PS I understand that this is an old program, but it has the ability to return. Perhaps there are still such programs.I'm still searching. If I understood something wrong, then close the report as information, thank you!

fix: to change the program state

Sorry i bad speak english
I hope you understand me
Thank you,haxta4ok00

## Impact

Change fields:

`Website`
`Twitter handle`
`About`
`Cover color`
and i think , i can change `logo` ?
in public(public_mode) programs

</details>

---
*Analysed by Claude on 2026-05-24*
