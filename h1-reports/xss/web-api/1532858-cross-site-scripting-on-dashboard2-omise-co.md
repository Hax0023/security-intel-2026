# Cross-site scripting on dashboard2.omise.co

## Metadata
- **Source:** HackerOne
- **Report:** 1532858 | https://hackerone.com/reports/1532858
- **Submitted:** 2022-04-06
- **Reporter:** oblivionlight
- **Program:** Unknown
- **Bounty:** $200
- **Severity:** critical
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Cross-site scripting (XSS) is an attack vector that injects malicious code into a vulnerable web application.
Stored XSS, also known as persistent XSS, is the more damaging of the two. It occurs when a malicious script is injected directly into a vulnerable web application.

Steps To Reproduce:
1. Log in to your account.
2. Visit https://dashboard.omise.co/test/settings 
3. Under Expor

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

## Summary:
Cross-site scripting (XSS) is an attack vector that injects malicious code into a vulnerable web application.
Stored XSS, also known as persistent XSS, is the more damaging of the two. It occurs when a malicious script is injected directly into a vulnerable web application.

Steps To Reproduce:
1. Log in to your account.
2. Visit https://dashboard.omise.co/test/settings 
3. Under Export - Specify the metadata that you want to include in your export option. Enter <script>alert(2)</script> in all four parameters including Charge, Transfer, Refund, Dispute.
4. Click on Update settings.
5. Click on Try our new dashboard, XSS will Trigger or log out and log in again, and XSS will Trigger.

POC:
Attached Video.

## Impact

Code injected into a vulnerable application can exfiltrate data or install malware on the user's machine. Attackers can masquerade as authorized users via session cookies, allowing them to perform any action allowed by the user account.

</details>

---
*Analysed by Claude on 2026-05-24*
