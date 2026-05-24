# Unauthorized File Access via Direct URL Bypass - Shopify Admin Panel

## Metadata
- **Source:** HackerOne
- **Report:** 97452 | https://hackerone.com/reports/97452
- **Submitted:** 2015-11-03
- **Reporter:** h3xr
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Broken Access Control, Insecure Direct Object References (IDOR), Authorization Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Staff members without explicit permissions to access the Files/Settings section could view and download all files uploaded by administrators by directly accessing the /admin/rte/assets endpoint. The authorization check on the Files section failed to protect the underlying asset storage API, allowing permission-bypassing via direct URL manipulation.

## Attack scenario
1. Attacker creates or obtains staff account with limited permissions (e.g., only Products access)
2. Attacker navigates to product image upload feature, observes admin-uploaded files in the picker dialog
3. Attacker notes the uploaded images reference API endpoint /admin/rte/assets
4. Attacker directly navigates to https://[store].myshopify.com/admin/rte/assets in browser
5. Attacker views complete list of all administrator-uploaded files without any permission checks
6. Attacker downloads or links sensitive files that should have been restricted from their access level

## Root cause
Authorization checks were implemented on the Settings->Files UI page but not on the underlying /admin/rte/assets API endpoint. The asset picker component used across the admin panel (in product descriptions, image uploads, etc.) directly queried this unprotected endpoint, bypassing permission restrictions. Direct URL access circumvented the intended access control layer.

## Attacker mindset
Opportunistic insider threat or compromised staff account. Low-privilege user testing boundaries of their access, discovering that UI-level restrictions don't extend to APIs. Motivation could range from curiosity to data exfiltration of sensitive marketing assets, design files, or confidential product information.

## Defensive takeaways
- Implement authorization checks at API endpoint level, not just UI layer - all backend endpoints must validate permissions
- Use consistent permission model across all components accessing same resource (asset picker, direct API calls, UI pages)
- Apply principle of least privilege - restrict API access based on staff role for file listings and downloads
- Conduct API security audit to identify endpoints exposed without proper auth checks
- Log and monitor direct API access attempts, especially by low-privilege accounts
- Implement proper role-based access control (RBAC) matrix that covers all asset operations
- Test with low-privilege accounts to verify permission boundaries hold across all access paths

## Variant hunting
Check other /admin/rte/* endpoints for similar authorization bypasses
Test asset picker in other admin sections (email templates, themes, etc.) for file disclosure
Look for similar patterns in other Shopify admin APIs where UI restrictions might not extend to backend
Investigate /admin/api endpoints for unauthenticated or under-authenticated file listing/download capabilities
Test with different staff role combinations to map inconsistent permission enforcement
Check for cached/archived file endpoints (/admin/rte/assets/archive, /admin/rte/assets/deleted)
Review GraphQL endpoints for file query capabilities without permission checks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1526 - Enumerate Cloud Resources
- T1613 - Sensitive Data Discovery
- T1087 - Account Discovery
- T1566 - Phishing

## Notes
Classic broken access control vulnerability where authorization enforcement was incomplete - proper only on UI layer rather than at data/API layer. The vulnerability was discoverable through basic enumeration and direct URL manipulation. High impact due to potential exposure of all administrator-uploaded assets including potentially sensitive business files, product mockups, or confidential materials.

## Full report
<details><summary>Expand</summary>

Staff members with no permission can access to the files, uploaded by the administrator

### Test #1 
If the member has access only to the section  Products, Inventory, & Collections
1. Go to the Products -> Product Name -> Description
2. Click the button -> Add Image
3. In the section Uploaded images are all files uploded by the admin, so we can simply add them or download (screenshot attached)
4. Uploded images are in the section Settings -> Files (but we don't have access there)

### Test #2
If the member has NO access to the ALL sections
1. So we can not go to the page Products but....
2. Lets go here https://*.myshopify.com/admin/rte/assets
3. And we will see all files uploaded by admin (screenshot attached)
4. On this page we can simply find links for admin files


</details>

---
*Analysed by Claude on 2026-05-24*
