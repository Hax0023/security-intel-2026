# Privilege Escalation via Unprotected Activity Feed Endpoint - Shopify Admin

## Metadata
- **Source:** HackerOne
- **Report:** 95589 | https://hackerone.com/reports/95589
- **Submitted:** 2015-10-24
- **Reporter:** egrep
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Broken Access Control, Privilege Escalation, Horizontal Access Control Bypass, Missing Authorization Checks
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A limited access user without permission to view shop activities could bypass access controls by directly accessing an alternative dashboard endpoint that lacked proper permission validation. The vulnerable endpoint `/admin/dashboard/activity_feed` failed to enforce the same authorization checks present on the primary activity viewing interface, allowing unauthorized data exposure.

## Attack scenario
1. Attacker creates a Shopify account with limited access permissions (e.g., Sales Channels Overview only) on a target shop
2. Attacker observes that direct access to `/admin/activity` is properly blocked due to insufficient permissions
3. Attacker discovers through browser testing or reconnaissance that the shop admin uses alternative URLs like `/admin/dashboard/activity_feed?activity_pages=X&activity_filter=all` to load paginated activities
4. Attacker constructs the same URL pattern with varying `activity_pages` parameter values to enumerate all activity pages
5. Attacker successfully retrieves complete activity logs showing all shop owner actions, sensitive business operations, and administrative changes
6. Attacker leverages exposed information for business intelligence, fraud detection evasion, or social engineering attacks

## Root cause
Insufficient authorization validation on the `/admin/dashboard/activity_feed` endpoint. The development team implemented permission checks on the primary activity page but failed to apply identical authorization logic to an alternative endpoint serving the same data. This represents incomplete security implementation across multiple code paths accessing the same protected resource.

## Attacker mindset
An attacker with limited access would naturally probe for alternative endpoints and URL patterns, especially when observing legitimate functionality being used by admins. The discovery of pagination parameters suggests systematic enumeration of API patterns. The attacker recognized that different endpoints for the same feature often have inconsistent security controls—a common vulnerability pattern in web applications.

## Defensive takeaways
- Implement centralized authorization checks at the data access layer rather than at individual endpoint handlers to ensure consistent enforcement across all code paths
- Use a consistent permission middleware/decorator that validates user capabilities before processing any request accessing protected resources
- Conduct authorization control reviews across all endpoints that serve the same data (activity feeds, reports, dashboards) to identify inconsistencies
- Test all user permission levels against every endpoint, not just primary UI paths; attackers will find and exploit alternative data access routes
- Implement deny-by-default authorization: explicitly grant permissions rather than assuming unauthenticated access is blocked
- Use automated security testing to verify that permission restrictions are applied uniformly across all related endpoints
- Log and monitor access attempts to restricted endpoints for anomaly detection

## Variant hunting
Similar vulnerabilities likely exist in other Shopify admin endpoints serving user-specific data (order history, customer activities, staff logs, audit trails). Search for patterns where pagination, filtering, or alternative URL schemes bypass parent endpoint authorization. Check API endpoints (`/admin/api/*/`) serving activity data for identical authorization gaps. Test report generation endpoints which often access historical data through separate code paths.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1078: Valid Accounts
- T1087: Account Discovery
- T1526: Enumerate permission levels

## Notes
This is a classic authorization bypass pattern where different endpoints accessing the same protected resource have inconsistent security controls. The vulnerability affects data confidentiality of shop administrative activities. The fix likely involves applying the same permission check to `/admin/dashboard/activity_feed` that exists on `/admin/activity`. The report demonstrates good security research methodology by clearly documenting user roles, showing blocked vs. unblocked behavior, and providing reproducible steps.

## Full report
<details><summary>Expand</summary>

Scenario:
Test shopify shop : https://elamaranhack.myshopify.com/admin
User1 : elamaran+hackerone@shopify.com(X) - Account Owner(Shop Admin)
User2 : elamaran619@gmail.com(Y) - Limited access user(access to Sales Channels Overviews only)

Limited access user(Y) who don't have permission to access home page activities is able to see all shop owner activities using the request 
"https://elamaranhack.myshopify.com/admin/dashboard/activity_feed?activity_pages=XXXX&activity_filter=all" where XXXX is page number

Steps to reproduce:
1) Created users X & Y with above mentioned permissions(X1.png,X2.png)
2) Shop admin X views his activities using url "https://elamaranhack.myshopify.com/admin/activity" (X3.png,X4.png)
3) If limited access user Y tried to view shop admin activities, the system blocks the url rightly (Y1.png)
4) There is one option for shop admin X to load more activities using url "https://elamaranhack.myshopify.com/admin/dashboard/activity_feed?activity_pages=XXXX&activity_filter=all" where XXXX is page number (X5.png, X6.png)
5) If the limited access user Y use the url "https://elamaranhack.myshopify.com/admin/dashboard/activity_feed?activity_pages=XXXX&activity_filter=all" , he can able to view all shop admin activities (Y2.png, Y3.png)

Error screenshots attached for reference.

</details>

---
*Analysed by Claude on 2026-05-24*
