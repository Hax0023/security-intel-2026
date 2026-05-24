# Stored XSS on express entries

## Metadata
- **Source:** HackerOne
- **Report:** 873474 | https://hackerone.com/reports/873474
- **Submitted:** 2020-05-13
- **Reporter:** solov9ev
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
1. Download Concrete5 8.5.2 and install it
2. Log into your Concrete5 instance as admin
3. Go to Dashboard > System settings > Express entities (/index.php/dashboard/system/express/entities) 
4. Сlick on the **Create** button
5. in the field **Name** paste the following text: `</h1><script>alert(1)</script><h1>`
6. Go to tab **View Objects**

## Impact

If the user was added to the group of admini

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

1. Download Concrete5 8.5.2 and install it
2. Log into your Concrete5 instance as admin
3. Go to Dashboard > System settings > Express entities (/index.php/dashboard/system/express/entities) 
4. Сlick on the **Create** button
5. in the field **Name** paste the following text: `</h1><script>alert(1)</script><h1>`
6. Go to tab **View Objects**

## Impact

If the user was added to the group of administrators, then he can create an express object with a payload in the name and give a link to another administrator to view the created object.

</details>

---
*Analysed by Claude on 2026-05-24*
