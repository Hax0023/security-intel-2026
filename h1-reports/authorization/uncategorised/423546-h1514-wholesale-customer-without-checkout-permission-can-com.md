# Wholesale customer without checkout permission can complete purchases

## Metadata
- **Source:** HackerOne
- **Report:** 423546 | https://hackerone.com/reports/423546
- **Submitted:** 2018-10-13
- **Reporter:** cablej
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authorization Bypass, Business Logic Flaw, Insufficient Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
Shopify Wholesale customers without checkout approval permissions can bypass the manual approval requirement by intercepting and modifying the purchase order submission request. By changing the endpoint from /purchase_orders/submit to /purchase_orders/update_checkout, attackers can proceed directly to checkout and complete orders without store admin approval or respecting maximum checkout amount restrictions.

## Attack scenario
1. Attacker identifies themselves as a wholesale customer without immediate checkout permissions in a Shopify store
2. Attacker adds products to cart and attempts to submit a purchase order for manual approval
3. Attacker intercepts the PUT request to /purchase_orders/submit using a proxy tool (Burp Suite, etc.)
4. Attacker modifies the URL endpoint from /purchase_orders/submit to /purchase_orders/update_checkout
5. Attacker forwards the modified request, bypassing the approval workflow
6. Attacker gains access to checkout and completes the purchase without admin approval or amount validation

## Root cause
The application fails to properly validate authorization on the /purchase_orders/update_checkout endpoint. The endpoint does not verify that the user has checkout permissions enabled, instead relying on frontend restrictions and incorrect endpoint routing. The API accepts endpoint manipulation without validating business logic constraints.

## Attacker mindset
An attacker with basic security knowledge recognizes that restricting checkout through UI constraints and frontend validation is insufficient. By identifying alternative API endpoints that perform similar functions, they can circumvent approval workflows. This represents classic client-side security bypass thinking, testing for inconsistent authorization checks across different endpoints.

## Defensive takeaways
- Implement server-side authorization checks on every endpoint that affects checkout or order placement, not just UI restrictions
- Validate business rules (checkout permissions, maximum amounts) on the backend before processing any checkout-related request
- Use explicit endpoint routing that cannot be modified by attackers; avoid relying on URL manipulation for request handling
- Implement consistent authorization middleware across all related endpoints to ensure equivalent security policies
- Log and monitor unusual API endpoint usage patterns that suggest endpoint switching or API abuse
- Implement role-based access control (RBAC) that explicitly denies checkout functionality for restricted wholesale customers
- Validate that user state and permissions haven't changed between frontend submission and backend processing

## Variant hunting
Look for other Shopify endpoints that bypass intended workflows: /purchase_orders/cancel, /purchase_orders/approve endpoints that may accept unauthorized requests. Check for similar patterns in cart/checkout flow where endpoints like /cart/checkout, /checkout/submit might have inconsistent authorization. Investigate other wholesale-specific features (payment terms, credit limits) that may accept direct endpoint manipulation.

## MITRE ATT&CK
- T1190
- T1550
- T1578

## Notes
This is a critical business logic vulnerability affecting commerce platforms. The attacker requires account access as a wholesale customer but no special privileges. The impact includes financial loss through unauthorized purchases and circumvention of credit/approval controls. The fix requires comprehensive authorization auditing across all checkout-related endpoints, not just patching the identified endpoint manipulation.

## Full report
<details><summary>Expand</summary>

**Summary:**

By default, Shopify Wholesale customers are prevented from immediately checking out:

{F360280}

Instead, a store admin must approve each order before the customer can pay.

This restriction can be bypassed, allowing a customer to check out orders without prior approval. This also bypasses any maximum checkout amount that a store can set.

## Steps To Reproduce:

  1. As a Wholesale owner, ensure that a customer is disallowed from immediately checking out at https://your-store.myshopify.com/admin/apps/wholesale/admin/shops/x/accounts.
  1. As the customer, visit the Wholesale shop and fill your cart with products.
  1. Observe that the UI forces the user to submit a purchase order:

    {F360285}

  1. To bypass this restriction, intercept the request to `PUT /purchase_orders/submit` to submit the purchase order and change the url to `/purchase_orders/update_checkout`.
  1. Observe that executing the request will allow the customer to proceed through the checkout flow and place the order:

{F360296}

## Impact

This allows a customer to bypass manual approval restrictions for a Wholesale store and immediately check out.

</details>

---
*Analysed by Claude on 2026-05-24*
