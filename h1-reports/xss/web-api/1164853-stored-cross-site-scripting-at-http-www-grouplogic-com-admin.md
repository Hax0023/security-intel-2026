# Stored Cross Site Scripting at http://www.grouplogic.com/ADMIN/store/index.cfm?fa=disprocode

## Metadata
- **Source:** HackerOne
- **Report:** 1164853 | https://hackerone.com/reports/1164853
- **Submitted:** 2021-04-14
- **Reporter:** ub3rsick
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary
The application exposes store ADMIN page at below URL and is accessible without authentication. 
```
http://www.grouplogic.com/ADMIN/store/index.cfm
```
The ADMIN page provides several functionalities.  Among them the below functionality is found to be vulnerable to stored XSS.
- View and Edit Promo Code (http://www.grouplogic.com/ADMIN/store/index.cfm?fa=disprocode)


## Steps To Repro

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
The application exposes store ADMIN page at below URL and is accessible without authentication. 
```
http://www.grouplogic.com/ADMIN/store/index.cfm
```
The ADMIN page provides several functionalities.  Among them the below functionality is found to be vulnerable to stored XSS.
- View and Edit Promo Code (http://www.grouplogic.com/ADMIN/store/index.cfm?fa=disprocode)


## Steps To Reproduce
1. Navigate to  below URL to access the store admin page without authentication.
```
http://www.grouplogic.com/ADMIN/store/index.cfm
```
2. Navigate to promo codes section. (http://www.grouplogic.com/ADMIN/store/index.cfm?fa=disprocode)
3. Edit any promo code.
4. Add any of below payload in the Promo Code field.
```
Payload 1:
----------
<h1 onmouseover=alert(document.domain)>XSS</h1>

Payload 2:
----------
<img src=x onerror=alert(1)>
```
5. Click the Edit Promo Code Button to save modified the promo code.
6. Navigating again to the promo code page, in case of payload 1, XSS string is rendered, hovering mouse over it triggers xss. In case of payload 2, as soon as the promo code page is opened, xss triggers.

## Recommendations
It is highly recommended to implement output encoding.  
Encode the following characters with HTML entity encoding to prevent switching into any execution context, such as script, style, or event handlers. Using hex entities is recommended in the spec. The 5 characters significant in XML``` (&, <, >, ", ')```:

```
 & --> &amp;
 < --> &lt;
 > --> &gt;
 " --> &quot;
 ' --> &#x27;
```
Reference: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

## Impact

XSS can be  used to :
- Steal cookies, password
- Website Defacement
- Redirect Victim to Malicious site 
- Log keystrokes etc.

</details>

---
*Analysed by Claude on 2026-05-24*
