# Open Redirect Bypass via Path Traversal in Shopify Admin Theme Editor

## Metadata
- **Source:** HackerOne
- **Report:** 165046 | https://hackerone.com/reports/165046
- **Submitted:** 2016-09-01
- **Reporter:** zombiehelp54
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Open Redirect, Path Traversal, Improper Input Validation, iframe Content Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
A researcher discovered a bypass to a previous open redirect fix by using path traversal sequences (/../) to circumvent store ID validation in the return_url parameter. This allows attackers to redirect users to arbitrary domains via the victim's store, including injecting malicious content into theme editor iframes.

## Attack scenario
1. Attacker identifies that Shopify fixed a previous open redirect by validating the store ID in checkout.shopify.com URLs
2. Attacker discovers that path traversal sequences (/../) are not properly sanitized before validation occurs
3. Attacker crafts a malicious URL with format: https://checkout.shopify.com/<victim_store_id>/../<attacker_store_id> to bypass the store ID check
4. When victim visits this URL, the path traversal bypasses validation but attacker's 404 page loads
5. Attacker's 404 page contains malicious JavaScript that redirects to any domain or injects content
6. If used within theme editor iframe context, attacker can modify iframe content and potentially perform actions within admin context

## Root cause
The fix validated the store ID in the return_url parameter but performed validation before path normalization/canonicalization, allowing relative path traversal (/../) to be used to reference different store IDs. The application did not properly sanitize or resolve relative paths before security checks were applied.

## Attacker mindset
Methodical security researcher identifying incomplete patches and edge cases in validation logic. Demonstrates understanding that fixes often focus on direct cases and miss encoding/traversal variations. Shows persistence in finding bypass techniques after initial vulnerability is patched.

## Defensive takeaways
- Always normalize and canonicalize URLs before performing security validation checks
- Implement allowlist validation on full resolved URL paths, not partial string matching
- Apply input sanitization before any validation logic, removing or rejecting path traversal sequences
- Use URL parsing libraries that properly handle relative paths and resolve them to absolute paths
- Validate store IDs at multiple stages: during parameter extraction, after URL resolution, and before redirect execution
- Implement additional protections like frame-ancestors CSP headers to prevent iframe injection attacks
- Ensure 404 error pages cannot be used as redirect intermediaries or contain user-controllable content

## Variant hunting
Look for similar patterns: (1) Other Shopify redirect endpoints that may use incomplete validation, (2) Path traversal in other URL parameters beyond return_url, (3) Double-encoding variants (%2e%2e%2f), (4) URL scheme variations (javascript:, data:, etc.), (5) Case sensitivity bypasses in store ID validation, (6) Other admin endpoints that embed iframes with insufficient origin validation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1601 - Modify System Image
- T1566 - Phishing

## Notes
This is a follow-up to HackerOne #159522. The researcher demonstrates sophisticated understanding of how incomplete security patches can be bypassed. The vulnerability affects both user redirection and admin panel functionality through iframe manipulation. The attacker's 404 page acting as a redirect intermediary is a clever technique to avoid direct redirect from trusted domain while still achieving malicious goals.

## Full report
<details><summary>Expand</summary>

Hi ,

I managed to bypass the fix you deployed to the issue I reported in #159522.
Apparently this is what the fix does:

- Redirecting to `https://checkout.shopify.com/<exact_store_id> /` only is allowed.
- For example: `victim.myshopify.com/account/logout?return_url=https://checkout.shopify.com/<victim_store_id>/` will work 

- but `victim.myshopify.com/account/logout?return_url=https://checkout.shopify.com/<attacker_store_id>/` won't work 
- `https://checkout.shopify.com/<store_id>` no longer follows the 302 redirect rules added in the admin dashboard.

##Redirect bypass: 

`<victim>.myshopify.com/account/logout?return_url=https://checkout.shopify.com/<victim_store_id>/../14467660` 

Note that `14467660` is the attacker's store id.

The 302 redirect no longer works , but the attacker can still inject any HTML/JavaScript code in his store's 404 page that will redirect to any domain he wants.

##Change theme editor iframe content:

Here is the PoC:
`https://<your_store>.myshopify.com/admin/themes/<theme_id>/editor#/account/logout?return_url=https://checkout.shopify.com/<your_store_id>/../14467660`

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
