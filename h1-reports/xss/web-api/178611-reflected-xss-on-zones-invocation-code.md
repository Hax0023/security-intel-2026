# Reflected XSS on Zones > Invocation Code

## Metadata
- **Source:** HackerOne
- **Report:** 178611 | https://hackerone.com/reports/178611
- **Submitted:** 2016-10-28
- **Reporter:** pavanw3b
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
**"Cricetinae"** :)

This report is similar to my earlier report: #170156.

### Short Description
The **Close text** parameter in *Inventory > Zone > Invocation Code* is vulnerable to Cross-Site Scripting vulnerability.

### Steps to Reproduce
1. Logon or Work as an agent.
2. Navigate to Inventory > Zones > Invocation Code. Create Websites & Zones records if empty.
3. Enter  `[Close]something'/><s

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

**"Cricetinae"** :)

This report is similar to my earlier report: #170156.

### Short Description
The **Close text** parameter in *Inventory > Zone > Invocation Code* is vulnerable to Cross-Site Scripting vulnerability.

### Steps to Reproduce
1. Logon or Work as an agent.
2. Navigate to Inventory > Zones > Invocation Code. Create Websites & Zones records if empty.
3. Enter  `[Close]something'/><script>alert(1);</script><span class='1` for **Close text**.
4. Note the javascript alert box triggered from the payload entered above.
Chrome's default XSS Protection blocks simple XSS payloads. Please use firefox for reproduction or disable Chrome's security.

### Vulnerability Details
Cross-Site Scripting issue let's one to run a javascript of choice. It helps most of the client side risks including but not limited to phishing, temporary deface, browser key-logger and others. Exploitation frameworks like BeEF eases the offensive attack.

### Attack Vector
Though this may be treated as a Self-XSS, the place where the issue is affecting is sensitive. If the user who is going to set up the Revive Adserver, follows an untrusted malicious guide which contains specially crafted XSS payload, can help in gaining access to the database by tricking him to enter the credential in attacker's site by redirecting or any other way.

###Test Environment Details
**Version**: Latest as on Oct 28: revive-adserver-4.0.0 downloaded from official website
**Setup type**: local
**Browser**: Firefox 47.0
**OS**: Mac OS X

Cheers,
Pavan

</details>

---
*Analysed by Claude on 2026-05-24*
