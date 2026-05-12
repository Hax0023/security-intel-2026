# Stored XSS in Merge Request Creation Page via Approval Rule Name with CSP Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1342009 | https://hackerone.com/reports/1342009
- **Submitted:** 2021-09-16
- **Reporter:** joaxcar
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), CSP Bypass, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab's merge request creation page where approval rule names are not properly sanitized before display in the Reviewers dropdown. An attacker with premium features can create a malicious approval rule with JavaScript/HTML payload as the name and attach it to a user, which executes when victims view the Reviewers dropdown during MR creation. The vulnerability includes a CSP bypass technique using iframe srcdoc injection.

## Attack scenario
1. Attacker with premium subscription creates a project and adds an approval rule with XSS payload (e.g., <iframe/srcdoc=...>) as the rule name
2. Attacker selects a user as the approver for the malicious rule to ensure the payload appears in user information
3. Attacker invites victim user to the project with Developer role, gaining access to the infected project
4. Victim user creates or views a merge request in the project and clicks the Reviewers dropdown
5. Malicious JavaScript payload in the approval rule name is rendered and executed in victim's browser context
6. Attacker can steal session tokens, exfiltrate data, or perform actions on behalf of the victim

## Root cause
Approval rule names are inserted into the DOM without proper HTML encoding or sanitization when displaying user information in the Reviewers dropdown. The application fails to escape special characters or validate the content before rendering it in the merge request creation page interface.

## Attacker mindset
Attacker recognizes that approval rules are a premium feature that can be weaponized against free users by inviting them to infected projects. They leverage the assumption that user-generated names are safe and exploit the gap between CSP policies and actual execution contexts to craft a polyglot payload that bypasses security controls.

## Defensive takeaways
- Implement strict output encoding for all user-controlled data, especially rule names, using context-aware escaping (HTML entity encoding for HTML context)
- Apply Content Security Policy directives more strictly, particularly disabling inline scripts and restricting iframe srcdoc attributes
- Sanitize user input at creation time in addition to output encoding for defense-in-depth
- Validate that approval rule names match expected patterns (alphanumeric, common punctuation only)
- Test XSS payloads across all UI surfaces where user-controlled data is displayed, including dropdowns and popovers
- Implement automatic scanning for reflected and stored XSS in premium features before general availability
- Consider restricting dangerous HTML/JavaScript patterns in approval rule names regardless of encoding

## Variant hunting
Test other rule-based features (branch protection rules, security policies) for similar injection points
Check if other user-controlled metadata fields in merge requests are similarly vulnerable
Test approval rule descriptions, custom fields, and other text input areas for XSS
Verify if the vulnerability exists in merge request editing and viewing modes
Test payload injection in other premium-only features accessible via invited users
Check if similar vulnerabilities exist in issue templates, board names, or label descriptions

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1078

## Notes
The reporter noted that the XSS does not fire when editing MRs, suggesting context-dependent rendering. The CSP bypass using iframe srcdoc indicates the application's CSP policy contains exceptions that allow iframe srcdoc execution. The vulnerability specifically affects the Reviewers dropdown which has different rendering logic than the MR edit view. Premium subscription requirement doesn't protect free users since attackers can invite them to infected projects. The reporter provided a live test case in a private project (ultimate-joaxcar-test3/xss) for verification.

## Full report
<details><summary>Expand</summary>

### Summary

Hi GitLab team, I found a stored XSS in merge request creation page caused by a payload in the name of an "approval rule".

Adding approval rules is a feature that is unlocked for premium subscriptions or above. This does not seem to block it from being used against regular users on for example Gitlab.com by inviting them into the "infected project".

This occurs when adding an "Approval rule" to a project and giving it a javascript/html payload as the name and attaching the rule to an approver. When a user tries to create a merge request in the project and opens the "Reviewers" dropdown, information about the user with the attached rule will be shown and the rule name will be injected underneath.

With the payload
```
<iframe/srcdoc='<script/src=/joaxcar_group/first/-/jobs/1415515489/artifacts/raw/data/alert.js></script>'></iframe>
```
this XSS bypasses the current CSP on Gitlab.com (tried it with an Ultimate trial and inviting a user without a trial to the project)

As I got the impression that all XSS are treated equal when reporting a similar issue, I have not made any deeper analysis of the reason for this firing. Thought I just report it right away. Please reach back to me if you need me to research the impact deeper! As an example, it does not fire when one "edits" a MR which is a bit odd...

### Steps to reproduce

1. Create two user accounts, `attacker_user` and `victim_user` (`attacker_user` must have at least premium features enabled)
2. Log in as `attacker_user`
3. Create a project `xss_project` by going to https://gitlab.com/projects/new#blank_project
4. Go to projects settings on https://gitlab.com/attacker_user/xss_project/edit and scroll down to and expand "Merge request approvals"

{F1450906}

5. Click "Add approval rule"
6. Put the payload as the name, If on Gitlab.com use
```
<iframe/srcdoc='<script/src=/joaxcar_group/first/-/jobs/1415515489/artifacts/raw/data/alert.js></script>'></iframe>
```
if this is tested on a server without CSP feel free to use the payload
```
<script>alert(document.domain)</script>
```
7. Search for and select `attacker_user` as approver and click create rule.

{F1450905}

8. Invite `victim_user` to the project as `Developer` on https://gitlab.com/attacker_user/xss_project/-/project_members
9. Log out and log back in as `victim_user`
10. Go to https://██████████/user_01/pub/-/branches/new and create a branch `new`
11. Directly click on "Create merge request" (which will appear on the screen)

{F1450903}

12. Click on the dropdown at "Reviewers"
13. Payload will trigger

{F1450904}


### Impact

Stored XSS with CSP bypass. Full Javascript functionality without restrictions, so everything from stealing data to generating and exfiltrating access tokens.

### Examples

If you access my private project at Gitlab.com (https://gitlab.com/ultimate-joaxcar-test3/xss) as an admin, you should be able to create an MR and trigger payload. (Just an alert box)

### What is the current *bug* behavior?

Approver rule name is injected in the user information without proper sanitization.

### What is the expected *correct* behavior?

The name should be sanitized


### Output of checks

This bug happens on GitLab.com

## Impact

Stored XSS with CSP bypass. Full Javascript functionality without restrictions, so everything from stealing data to generating and exfiltrating access tokens.

</details>

---
*Analysed by Claude on 2026-05-12*
