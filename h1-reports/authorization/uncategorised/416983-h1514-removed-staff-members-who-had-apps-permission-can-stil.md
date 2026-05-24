# Removed Staff Members with Apps Permission Can Modify Flow App Connections via Stateless HMAC

## Metadata
- **Source:** HackerOne
- **Report:** 416983 | https://hackerone.com/reports/416983
- **Submitted:** 2018-10-01
- **Reporter:** zombiehelp54
- **Program:** Shopify
- **Bounty:** $500-$2000 (estimated based on Shopify H1 historical payouts)
- **Severity:** High
- **Vuln:** Broken Authentication, Authorization Bypass, Insufficient Session Management, Predictable Token/HMAC Reuse
- **CVEs:** None
- **Category:** uncategorised

## Summary
Removed staff members retain ability to modify flow app connections (Google Sheets, Trello, Asana) because authorization relies solely on a static, non-expiring HMAC value that doesn't include session state or user identity. The HMAC is deterministic and based only on shop parameters, making it reusable indefinitely even after staff member removal.

## Attack scenario
1. Attacker is added as staff member with Apps permission and captures the path_hmac value during connector setup
2. Attacker saves the HMAC-based URLs for Google Sheets, Trello, and Asana connection settings before being removed
3. Shop owner removes the attacker from staff roster, assuming all access is revoked
4. Attacker uses saved URLs containing the valid path_hmac to bypass authentication checks on flow-connectors.shopifycloud.com
5. Attacker modifies connector settings to link their own Google Sheets/Trello/Asana accounts to the shop's workflows
6. Attacker intercepts shop data being synced to their accounts through modified workflow connections

## Root cause
Authorization check relies entirely on HMAC of static path parameters (shop_domain, shop_id) without incorporating: (1) current session tokens, (2) user identity, (3) expiration timestamps, or (4) backend validation of staff member status. The HMAC is deterministic and long-lived, defeating its intended security purpose.

## Attacker mindset
Disgruntled or malicious staff member who anticipates removal gathers authorization tokens/HMACs beforehand. Post-removal, they maintain data exfiltration capability by pivoting through workflow connections to their own accounts. Minimal effort required once HMAC is captured.

## Defensive takeaways
- Never use authorization tokens/HMACs as the sole authorization mechanism; always validate current session and user permissions on the backend
- Include user identity and expiration timestamps in sensitive HMACs or tokens
- Implement session-based authorization checks that verify user still has required permissions before granting access
- Use short-lived tokens with refresh mechanisms for cross-service authentication
- Upon staff removal, immediately invalidate all tokens/sessions issued to that user across all connected services
- Consider nonce-based challenges alongside HMACs for state-changing operations
- Audit and rotate HMACs when user permissions are modified or access is revoked

## Variant hunting
Check other Shopify apps/services using HMAC-only authorization without session validation
Look for other connectors (Slack, Stripe, etc.) that may have similar stateless authorization patterns
Search for similar authorization bypass in partner API endpoints that accept HMAC parameters
Test whether HMAC parameters can be guessed/brute-forced or reused across different shops
Verify if removing admin access revokes HMACs for other integration points (webhooks, API apps, data exports)

## MITRE ATT&CK
- T1078 - Valid Accounts (reuse of legitimate authorization tokens)
- T1550 - Use Alternate Authentication Material (HMAC reuse post-removal)
- T1190 - Exploit Public-Facing Application (targeting flow-connectors endpoint)
- T1556 - Modify Authentication Process (bypass of session/permission validation)

## Notes
The vulnerability is particularly impactful because: (1) Flow app integrations handle sensitive business data (customer info, sales data), (2) attacker maintains persistent access even after staff removal, (3) the attack requires zero technical sophistication post-HMAC capture, (4) Shopify did not implement refresh of authorization tokens upon staff permission changes. The public PoC link in the report demonstrates the ease of exploitation. This is a classic case of confusing authentication with authorization.

## Full report
<details><summary>Expand</summary>

**Summary:** 
It's been found that removed staff members who had "Apps" permission can still modify flow app connection settings due to improper authorization.

**Description:**
Flow app (https://apps.shopify.com/flow) allows users to connect their Google Sheets, Trello and Asana accounts to their flow accounts to be used later in workflows (e.g storing new customer information to google spreadsheet).

It's been found that when a user tries to connect his google account, he is redirected to `https://flow-connectors.shopifycloud.com/gsheet/connect?shop_domain=[shop].myshopify.com&shop_id=[shop-id]&path_hmac=[path_hmac]`, the parameter `path_hmac` is the only way the application determines whether the user can modify the connection settings for that shop or not and it's the same for all staff members and doesn't depend on any session as it's hmac of the path `/gsheet/connect?shop_domain=[shop].myshopify.com&shop_id=[shop-id]`  

With that said, it's possible for a staff member who had "Apps" permission then was removed to modify the connection settings for Google SpreadSheets, Trello and Asana by just saving the `path_hmac`.

## Steps To Reproduce:

1. Login to your shop as the shop owner and add a staff member with only "Apps" permission.
2. Install flow app: https://apps.shopify.com/flow
3. Login with the new user you added and navigate to `https://[Your-Shop].myshopify.com/admin/apps/flow/connectors`
4. Click All **Settings** links next to Google Sheets, Trello and Asana and save them
5. Login with the shop owner and remove the user you added
6. You can now use the links you saved to modify connectors settings.

**Live PoC:**
You can modify my shop's google spread sheet connection by navigating to `https://flow-connectors.shopifycloud.com/gsheet/connect?shop_id=24615823&path_hmac=%2BPnVhhFIC49KrHZGqwC08LoSMSkieG7UHWgtnriV2vQ%3D`

## Impact

Through this vulnerability a removed staff member will be able to modify google spread sheet, trello and asana connections to connect his own accounts so that workflow actions regarding the connections go to his accounts and therefore he can still access the shop data.

</details>

---
*Analysed by Claude on 2026-05-24*
