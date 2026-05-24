# Store Admin Page Accessible Without Authentication at http://www.grouplogic.com/ADMIN/store/index.cfm

## Metadata
- **Source:** HackerOne
- **Report:** 1164854 | https://hackerone.com/reports/1164854
- **Submitted:** 2021-04-14
- **Reporter:** ub3rsick
- **Program:** Unknown
- **Bounty:** $250
- **Severity:** medium
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
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
Navigate to 

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

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
