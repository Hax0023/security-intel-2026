# Reflected XSS in chatbot

## Metadata
- **Source:** HackerOne
- **Report:** 1735622 | https://hackerone.com/reports/1735622
- **Submitted:** 2022-10-14
- **Reporter:** roland_hack
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Reflected XSS attacks, also known as non-persistent attacks, occur when a malicious script is reflected off of a web application to the victim's browser. The script is activated through a link, which sends a request to a website with a vulnerability that enables execution of malicious scripts
Proof of Concept
1)Go to the website https://mtn.com.gh/
2)click on the MTN chat and where it asks to ente

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

Reflected XSS attacks, also known as non-persistent attacks, occur when a malicious script is reflected off of a web application to the victim's browser. The script is activated through a link, which sends a request to a website with a vulnerability that enables execution of malicious scripts
Proof of Concept
1)Go to the website https://mtn.com.gh/
2)click on the MTN chat and where it asks to enter a number enter an xss payload
3)In my case I put the following payload:<button onClick="alert('xss')">Submit</button>

## Impact

If an attacker can control a script running in the victim's browser, they can usually completely compromise that user. Among other things, the attacker can: Perform any action in the application that the user can perform.

</details>

---
*Analysed by Claude on 2026-05-24*
