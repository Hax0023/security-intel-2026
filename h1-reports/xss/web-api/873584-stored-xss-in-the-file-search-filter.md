# Stored XSS in the file search filter

## Metadata
- **Source:** HackerOne
- **Report:** 873584 | https://hackerone.com/reports/873584
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
3. Go to Dashboard >Files > Search
4. In the file search bar, click **Advanced**
5. In the window that appears, enter a phrase and click the save button, paste the following payload: `<img src=1 onerror=alert(1)>` and click the save button
6.  In the filter search bar, click **Edit** and wait for the malicious 

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
3. Go to Dashboard >Files > Search
4. In the file search bar, click **Advanced**
5. In the window that appears, enter a phrase and click the save button, paste the following payload: `<img src=1 onerror=alert(1)>` and click the save button
6.  In the filter search bar, click **Edit** and wait for the malicious code to execute

## Impact

If a user has been added to the administrators group, then he can create a malicious filter and wait for someone else to change this filter

</details>

---
*Analysed by Claude on 2026-05-24*
