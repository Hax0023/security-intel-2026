# Reflected Xss  https://██████/

## Metadata
- **Source:** HackerOne
- **Report:** 759418 | https://hackerone.com/reports/759418
- **Submitted:** 2019-12-16
- **Reporter:** 0xelkomy
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hello security all teams
**Relevant Products/Components:**
last version

**Detailed Description:**
Reflected XSS so have high impact.

**Steps To Reproduce:**

1-go in subdomain
2-and check url if tableau uses
3-Uses you can add this redirect dir in url with Authentication redirect:-
/en/embeddedAuthRedirect.html?auth=javascript:alert(%22xElkomy%22)

**Such as**

 https://████████/en/embeddedAuthR

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

Hello security all teams
**Relevant Products/Components:**
last version

**Detailed Description:**
Reflected XSS so have high impact.

**Steps To Reproduce:**

1-go in subdomain
2-and check url if tableau uses
3-Uses you can add this redirect dir in url with Authentication redirect:-
/en/embeddedAuthRedirect.html?auth=javascript:alert(%22xElkomy%22)

**Such as**

 https://████████/en/embeddedAuthRedirect.html?auth=javascript:alert(%22xElkomy%22)

**Browsers Verified In:**
all browsers supporting javascript

**Supporting Material/References:**
███

**Access Vector Required for Exploitation:**

no required any access but need only web access :)

**Vulnerability Exists in Default Configuration?:**
yes

**Exploitation Requires Authentication?:**
no need anything



#xElkomy

## Impact

The need for an external delivery mechanism for the attack means that the impact of reflected XSS is generally less severe than stored XSS, where a self-contained attack can be delivered within the vulnerable application itself.

</details>

---
*Analysed by Claude on 2026-05-24*
