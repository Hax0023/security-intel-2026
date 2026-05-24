# Improper Access Control on Adding Register to Outlet - Cross-Store Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 317332 | https://hackerone.com/reports/317332
- **Submitted:** 2018-02-18
- **Reporter:** al88nsk
- **Program:** Vend (vendhq.com)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, Insecure Direct Object Reference (IDOR), Cross-Store Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
A user with Cashier role in Store A can bypass authorization checks to add registers to outlets in Store A by leveraging their admin privileges in their own Store B. The application fails to validate that the outlet_id belongs to the store the user is currently acting within, allowing cross-store object manipulation.

## Attack scenario
1. Attacker creates two stores: Store A (victim) and Store B (attacker-controlled), both using attacker's email address
2. Attacker is assigned Cashier role in Store A, which lacks register creation permissions
3. Attacker logs into Store B where they have full admin privileges and creates an outlet
4. Attacker initiates register creation for their outlet in Store B and intercepts the HTTP request
5. Attacker modifies the outlet_id parameter in the POST request to reference a victim outlet from Store A
6. Attacker submits the modified request, successfully creating a register in the victim's Store A outlet despite lacking permissions

## Root cause
The application performs role-based authorization checks against the user's current store context but fails to validate that object IDs (outlet_id) belong to the authorized store before processing create/modify operations. The backend does not re-verify store ownership of the outlet when processing the register creation request.

## Attacker mindset
An attacker with legitimate low-privilege access to a target store can escalate their capabilities by establishing control over a secondary store where they hold admin rights. By leveraging direct object references and manipulating request parameters, they can circumvent authorization controls that should be store-scoped. This represents a classic privilege escalation through multi-tenancy bypass.

## Defensive takeaways
- Implement strict store-scoped authorization checks: verify that all object IDs (outlets, registers, etc.) belong to the user's current authorized store before processing any modifications
- Use indirect object references or UUIDs instead of sequential IDs to prevent trivial enumeration of cross-store objects
- Add server-side session validation that binds all operations to the current store context, not just at the UI/route level
- Implement comprehensive authorization middleware that checks store ownership for all resource operations, not just creation
- Log and alert on cross-store access attempts or parameter modifications that reference unauthorized stores
- Conduct security reviews of multi-tenant architectures to identify store-isolation bypasses
- Test authorization controls across tenant boundaries during security testing phases

## Variant hunting
Check other resource creation endpoints (payment_id, receipt_template_id, etc.) for similar outlet_id parameter manipulation
Test modifying outlet_id in register update/delete operations
Verify if users can manipulate other store IDs in URLs or parameters (e.g., change store subdomain in parameter values)
Check if users with low privilege in Store A can modify objects by sending requests from Store B context
Test if the CSRF token from Store B can be used to modify Store A resources
Examine other multi-tenant operations for similar store-boundary bypass opportunities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (improper authorization in web application)
- T1550 - Use Alternate Authentication Material (leveraging secondary store access to bypass primary store restrictions)
- T1078 - Valid Accounts (using legitimate account with elevated privileges in secondary context)

## Notes
This vulnerability demonstrates a critical multi-tenancy bypass where authorization context is not properly enforced across store boundaries. The attacker doesn't need to escalate privileges within a single store; instead, they exploit the ability to act as an admin in one store to modify resources in another. The report notes that Cashier role can discover outlet IDs from publicly accessible page source (Sales Ledger), reducing the attack complexity. The vulnerability is particularly severe because it affects core business functionality (register management) and appears to affect default roles.

## Full report
<details><summary>Expand</summary>

**Summary:** User without permissions to add a Register to an Outlet can bypass this restriction and add a Register to an Outlet.

**Description:** I do not know which permission exactly controls this action, I tested this against default `Cashier` role. User with default `Cashier` role has no permission to add registers.  If a user creates his own store on `vendhq.com` then he can add a Register to an Outlet.

## Steps To Reproduce:

  1. Add a user to store A with `Cashier` role. Assume the added user's email is attacker@attacker.com
  2. Go to `Setup` -> `Outlets and Registers`
  3. Create an outlet in store A
  4. Create a new store B using email attacker@attacker.com
  5. Log in to store B with attacker@attacker.com credentials
  6. Create an outlet in store B
  7. Run Burp Suite or any other proxy to intercept requests
  8. Add a register to outlet in store B and intercept outgoing POST request
  9. Replace id in `vend_register%5Boutlet_id%5D=<outlet id>` from the request with id of outlet from store A and process the request
  10. Check outlet from store A - a register should be added to it

Request example

```
POST /register/create/outlet_id/<outled id from B> HTTP/1.1
Host: <store B>.vendhq.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://<store B>.vendhq.com/register/<outled id from B>/new?confirmed=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 694
Cookie: <Cookie>
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1

vend_register%5Bid%5D=&vend_register%5Boutlet_id%5D=<outled id from A>&vend_register%5B_csrf_token%5D=<csrf token>&vend_register%5Bname%5D=6&vend_register%5Bcash_managed_payment_id%5D=<cash managed payment id>&vend_register%5Breceipt_template_id%5D=<receipt template id>&vend_register%5Binvoice_sequence%5D=1&vend_register%5Binvoice_prefix%5D=&vend_register%5Binvoice_suffix%5D=&vend_register%5Bask_for_user_on_sale%5D=0&vend_register%5Bemail_receipt%5D=1&vend_register%5Bprint_receipt%5D=1&vend_register%5Bask_for_note_on_save%5D=1&vend_register%5Bprint_note_on_receipt%5D=1&vend_register%5Bshow_discounts%5D=1&return=
```

Cashier can get id of interesting outlet from `Sales Ledger` page source.

## Impact

An attacker can add registers to outlets even if he has no permissions to do it.

</details>

---
*Analysed by Claude on 2026-05-24*
