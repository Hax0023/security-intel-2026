# Store Admin Page Accessible Without Authentication

## Metadata
- **Source:** HackerOne
- **Report:** 1164854 | https://hackerone.com/reports/1164854
- **Submitted:** 2021-04-14
- **Reporter:** ub3rsick
- **Program:** Group Logic
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Missing Authentication, Broken Access Control, Inadequate Authorization
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The store administration interface at /ADMIN/store/index.cfm is directly accessible without any authentication mechanism, allowing unauthenticated users to access sensitive administrative functionalities. An attacker can perform privileged operations including product management, order manipulation, and promotional code creation without valid credentials.

## Attack scenario
1. Attacker identifies the admin panel URL structure through directory enumeration or public disclosure
2. Attacker navigates directly to http://www.grouplogic.com/ADMIN/store/index.cfm in a web browser
3. Access is granted without presenting any credentials or authentication tokens
4. Attacker exploits admin functions to modify products, prices, or inventory
5. Attacker creates fraudulent promotional codes or manipulates existing orders
6. Attacker exfiltrates sensitive business and customer data accessible through admin panel

## Root cause
Complete absence of authentication and authorization checks on the admin page. The application fails to validate user credentials before serving administrative functionality, likely due to insufficient implementation of access control mechanisms in the ColdFusion-based application.

## Attacker mindset
Low-hanging fruit reconnaissance revealing critical administrative access. Attacker would recognize this as trivial unauthorized access to sensitive business operations with potential for financial fraud, data manipulation, and competitive advantage.

## Defensive takeaways
- Implement mandatory authentication on all administrative pages using secure session management
- Enforce role-based access control (RBAC) with explicit authorization checks before serving admin content
- Implement HTTP authentication headers and session validation on server-side
- Apply principle of least privilege to admin resources
- Use Web Application Firewall (WAF) rules to restrict /ADMIN paths to authenticated users
- Implement rate limiting and suspicious access logging for admin pages
- Regular security audits of publicly exposed admin interfaces
- Move admin interface to non-standard paths and implement IP whitelisting where feasible

## Variant hunting
Search for other ColdFusion (.cfm) files in /ADMIN/, /ADMINISTRATOR/, /ADMIN_PANEL/ directories that may lack authentication. Check for similar patterns in other endpoints handling sensitive operations (user management, settings, reports). Examine client-side only authentication implementation.

## MITRE ATT&CK
- T1190
- T1133
- T1110

## Notes
This is a basic but critical finding representing fundamental security failure. The vulnerability appears to be unauthenticated path traversal to protected resources. ColdFusion applications frequently suffer from improper authentication implementation. The presence of HTTP (non-HTTPS) protocol further compounds the risk through potential credential interception.

## Full report
<details><summary>Expand</summary>

## Summary
The store admin page is accessible without authentication at below URL:
```
http://www.grouplogic.com/ADMIN/store/index.cfm
```

The store admin page provides functionalities such as the following:
- Add Edit Items
- Search Products
- Search Results
- Search Orders
- Orders Search Results
- Add New Promo Code
- Promo Code
- Add New How Hear
- How Hear

## Steps To Reproduce
Navigate to below URL from a browser to access the store admin page.

```
http://www.grouplogic.com/ADMIN/store/index.cfm
```

## Recommendations
It is highly recommended to implement proper access controls on administrator functionalities. Only authenticated admin users are to be allowed to access admin pages.

## Impact

Access to admin functionalities without authentication.

</details>

---
*Analysed by Claude on 2026-05-24*
