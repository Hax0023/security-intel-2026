# IDOR leads to Edit Anyone's Blogs / Websites

## Metadata
- **Source:** HackerOne
- **Report:** 974222 | https://hackerone.com/reports/974222
- **Submitted:** 2020-09-03
- **Reporter:** ali
- **Program:** Intense Debate
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Missing Authorization Check
- **CVEs:** None
- **Category:** web-api

## Summary
An IDOR vulnerability in Intense Debate's edit-user-profile endpoint allows attackers to modify any user's blog or website information by manipulating the hidBlogID parameter. An authenticated attacker can intercept the request when saving blog settings and change the hidBlogID to target any victim's blog, enabling unauthorized modification of victim account blog metadata.

## Attack scenario
1. Attacker creates two accounts on Intense Debate (attacker and victim accounts)
2. Attacker logs into victim account and adds a blog/website to identify the victim's hidBlogID value
3. Attacker logs into their own account and navigates to edit-user-profile to add their own blog
4. When saving settings, attacker intercepts the HTTP request using Burp Suite
5. Attacker modifies the hidBlogID parameter from their own ID to the victim's ID
6. Attacker forwards the modified request, which updates the victim's blog information instead

## Root cause
The application fails to verify that the user making the request has authorization to modify the blog/website associated with the provided hidBlogID. The backend accepts any hidBlogID value without validating ownership, relying only on the user being authenticated rather than checking if they own that specific blog resource.

## Attacker mindset
An attacker with account access can systematically enumerate hidBlogID values to discover valid blog IDs. They could then mass-modify blog information across multiple victim accounts to deface sites, inject malicious URLs, or cause reputational damage. The simplicity of the attack (basic parameter manipulation) makes it highly exploitable.

## Defensive takeaways
- Implement proper authorization checks on all resource modification endpoints, verifying the requesting user owns/has permission to modify the specific resource
- Use indirect reference maps or UUIDs instead of sequential/predictable IDs to prevent enumeration
- Validate resource ownership before processing any modifications: verify hidBlogID belongs to authenticated user
- Apply principle of least privilege: extract user context from session/token rather than accepting client-provided identifiers
- Implement comprehensive access control testing as part of the SDLC, including IDOR-specific test cases
- Use security headers and logging to detect suspicious bulk modification attempts

## Variant hunting
Check other user-profile related endpoints (e.g., /edit-user-settings, /update-profile, /manage-blogs) for similar IDOR patterns
Test other resource identifiers (hidUserID, hidProfileID, etc.) for authorization bypass
Examine API endpoints that handle blog/website CRUD operations for missing ownership validation
Test batch operations or bulk update endpoints that might accept multiple resource IDs
Check if other authenticated actions (delete blog, share blog, transfer ownership) have the same vulnerability
Look for horizontal privilege escalation in admin/moderation panels if they exist

## MITRE ATT&CK
- T1190
- T1566
- T1134

## Notes
This is a textbook IDOR vulnerability demonstrating why client-supplied identifiers must never be trusted for authorization decisions. The vulnerability is trivial to exploit and has clear business impact (data tampering). The researcher provided clear reproduction steps making this high-quality submission. Intense Debate should have implemented object-level authorization checks at the application layer.

## Full report
<details><summary>Expand</summary>

Hello there,
I hope all is well!

Steps:
1. Go to `https://intensedebate.com/signup` and create 2 accounts.
2. Login as victim and go to `https://www.intensedebate.com/edit-user-profile`
3. Click `Add Blog / Website` text and fill the form > click `Save Settings` button
4. Go to `https://www.intensedebate.com/edit-user-profile`, again and search `radMainSite` text in page source and copy value.   
{F975085}
5. Then login as attacker.
6. Go to `https://www.intensedebate.com/edit-user-profile` > click `Add Blog / Website` text and fill the form > click `Save Settings` button
7. Go to `https://www.intensedebate.com/edit-user-profile`, again and click `Save Settings` button > open burp suite and change `hidBlogID` parameter with victim's `hidBlogID`.
8. Forward the request and go to victim's account. Check your website informations. You will see it's changed.

PoC:   
{F975096}

## Impact

Changing victim's website/blog informations.

Best Regards,
@mygf

</details>

---
*Analysed by Claude on 2026-05-11*
