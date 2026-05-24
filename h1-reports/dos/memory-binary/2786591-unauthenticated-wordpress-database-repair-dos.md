# Unauthenticated WordPress Database Repair DoS via WP_ALLOW_REPAIR

## Metadata
- **Source:** HackerOne
- **Report:** 2786591 | https://hackerone.com/reports/2786591
- **Submitted:** 2024-10-17
- **Reporter:** wshadow
- **Program:** WordPress Core
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Missing Authentication, Denial of Service, Uncontrolled Resource Consumption, Improper Access Control
- **CVEs:** None
- **Category:** memory-binary

## Summary
WordPress database repair functionality at `/wp-admin/maint/repair.php` is accessible without authentication when `WP_ALLOW_REPAIR` is enabled in wp-config.php, allowing unauthenticated attackers to trigger resource-intensive repair operations. Repeated requests to the endpoint exhaust server resources, resulting in Denial of Service and site unavailability.

## Attack scenario
1. Attacker identifies target WordPress installation with `WP_ALLOW_REPAIR` set to true (often left enabled for maintenance purposes)
2. Attacker accesses `/wp-admin/maint/repair.php` without authentication and confirms the repair interface is publicly accessible
3. Attacker crafts automated script using curl or Python to send repeated GET requests to `/wp-admin/maint/repair.php?repair=1`
4. Each request triggers database repair operations, consuming CPU, memory, disk I/O, and database connections
5. Server resources become exhausted as repair operations accumulate, causing legitimate requests to timeout
6. Target website becomes unresponsive and inaccessible to legitimate users, achieving denial of service

## Root cause
WordPress fails to implement authentication checks for the database repair endpoint despite it being a critical administrative function. The repair functionality also lacks rate limiting, resource quotas, or operational safeguards when `WP_ALLOW_REPAIR` is enabled, treating it as a convenience feature without security boundaries.

## Attacker mindset
Low-effort DoS attack requiring minimal sophistication—attacker simply needs to loop HTTP requests against a publicly documented WordPress endpoint. The vulnerability is attractive because it requires no authentication, no exploitation of complex logic, and can be weaponized with a simple script. The long-standing nature of the vulnerability suggests it may be known in underground communities.

## Defensive takeaways
- Never enable `WP_ALLOW_REPAIR` in production environments; restrict it to maintenance windows only
- Require authentication checks for ALL critical administrative functions, regardless of configuration flags
- Implement rate limiting and request throttling on resource-intensive operations
- Use one-time tokens or temporary access mechanisms for maintenance endpoints instead of persistent flags
- Monitor and alert on repeated requests to maintenance endpoints from unauthenticated sources
- Apply IP-based access control lists to administrative endpoints at web server level
- Regularly audit wp-config.php for dangerous settings left enabled in production
- Consider disabling repair functionality entirely in favor of managed database maintenance

## Variant hunting
Check for similar unauthenticated access to other `/wp-admin/maint/*` endpoints (export, import, etc.)
Investigate other WordPress configuration flags that enable functionality without enforcing authentication
Review third-party plugins that implement maintenance features with `WP_ALLOW_REPAIR`-style conditional access
Examine upgrade/migration endpoints that may bypass authentication when certain conditions are met
Look for other database-heavy operations (optimize, backup, restore) exposed without proper access controls
Test for similar patterns in WordPress multisite functionality that grants bulk operations without auth

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1526: Exposure of Resource Through Query Parameters
- T1613: Obtain Information from Exposed Maintenance Endpoints
- T1499: Service Exhaustion Denial of Service

## Notes
Writeup references external GitHub script for weaponization, indicating functional proof-of-concept exists. Vulnerability affects WordPress Core <6.6, suggesting patch was issued in 6.6. The fact that `WP_ALLOW_REPAIR` is a common production misconfiguration makes this high-impact despite simplicity. Risk is heightened on shared hosting where resource contention magnifies impact.

## Full report
<details><summary>Expand</summary>

## Summary:

The WordPress Database Repair feature, accessible via the `/wp-admin/maint/repair.php` endpoint, is vulnerable due to improper access control and insecure design. When `WP_ALLOW_REPAIR` is set to `true` in the `wp-config.php` file, the repair page becomes publicly accessible without requiring any authentication. This vulnerability arises from two main issues: the absence of authentication for accessing the repair endpoint and the insecure nature of the WordPress repair feature, which lacks any limits or restrictions on access frequency or user verification. Consequently, an attacker can repeatedly trigger resource-intensive database repair operations, overwhelming server resources and resulting in a Denial of Service (DoS) condition. 
This vulnerability can be categorized under these two CWE's as it fails to impose necessary restrictions on who can access this critical functionality.

**CWE-306: Missing Authentication for Critical Function** 
 **CWE-400: Uncontrolled Resource Consumption**

## Platform(s) Affected:

Wordpress Core  <6.6
https://core.svn.wordpress.org/branches/6.6/

## Steps To Reproduce:

1. Ensure that `WP_ALLOW_REPAIR` is set to `true` in the `wp-config.php` file of the target WordPress installation.
   ```php
   define('WP_ALLOW_REPAIR', true);
   ```
2. Access the database repair endpoint directly by visiting the URL: `http://target-site.com/wp-admin/maint/repair.php`.
3. Note that the page allows access without authentication. Select either the "Repair Database" or "Repair and Optimize Database" button.
4. To exploit this vulnerability, repeatedly send GET requests to `http://target-site.com/wp-admin/maint/repair.php?repair=1` to trigger the database repair process.
   - You can use a simple bash script or a tool like `cURL` to automate the requests:
     ```bash
     while true; do curl -X GET "http://target-site.com/wp-admin/maint/repair.php?repair=1"; sleep 1; done
     ```
   - To be more practical, I have weaponized it with a simple python script that can bring the site down for as long as the attacker desires. The script is hosted at https://raw.githubusercontent.com/smaranchand/wreckair-db/refs/heads/main/wreckair-db.py?token=GHSAT0AAAAAACZBPSANBXQSCUVHV6JYC2LUZYQVXVQ

      Note: Let me know if it is not accessible.
5. Observe that the repeated requests will eventually exhaust server resources, causing the site to become unresponsive, results in a Denial of Service (DoS) condition, impacting the availability of the target WordPress site.

## Supporting Material/References:
{F3684807}

## Impact

The impact of this vulnerability is severe, as it allows an unauthenticated attacker to make the target WordPress site unresponsive through repeated use of the database repair functionality. This Denial of Service (DoS) condition disrupts the availability of the website, rendering it inaccessible to legitimate users. The lack of authentication and rate limiting on a critical function makes it easy for attackers to exploit, resulting in significant downtime, potential loss of business, and damage to the reputation of the affected website. Additionally, this vulnerability has been active for a long time, going unreported and unnoticed, making it a persistent threat to WordPress installations that enable the repair feature without proper security measures.

## Mitigations

To mitigate this vulnerability, the following actions are recommended:

1. **Require Authentication**: WordPress should require authentication for accessing the `/wp-admin/maint/repair.php` endpoint, even when `WP_ALLOW_REPAIR` is set to `true`. This would ensure that only authorized users can initiate database repair operations.

2. **Restrict Access**: Implement IP-based access control to limit access to the repair page only to trusted IP addresses. This would prevent unauthorized users from accessing the endpoint.

3. **Use a One-Time Token Mechanism**: Introduce a secure one-time token mechanism to allow temporary access to the repair page. This token should expire after a short period, reducing the risk of exploitation.

4. **Rate Limiting**: Apply rate limiting to the `/wp-admin/maint/repair.php` endpoint to restrict how frequently repair requests can be made. This will help mitigate the risk of resource exhaustion through repeated requests.

By implementing these mitigations, the risk associated with this vulnerability can be significantly reduced, ensuring that the database repair functionality is only used by authorized personnel and cannot be abused to create a DoS condition.

</details>

---
*Analysed by Claude on 2026-05-24*
