# Possible SSRF in email server settings(SMTP mode)

## Metadata
- **Source:** HackerOne
- **Report:** 222667 | https://hackerone.com/reports/222667
- **Submitted:** 2017-04-21
- **Reporter:** xifengweiyu
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Description:
vul address `https://demo.nextcloud.com/xxx/settings/admin/additional`,when you change `smtp server address` ,you will get some different hints.

Reproduce steps:

1.Go to `https://demo.nextcloud.com/xxx/settings/admin/additional`,choose `SMTP` mode

2.Set server address to "172.17.1.0`,then you will get screenshot(nextcloud1.png),it means not on the same network segment

3.Set server

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

Description:
vul address `https://demo.nextcloud.com/xxx/settings/admin/additional`,when you change `smtp server address` ,you will get some different hints.

Reproduce steps:

1.Go to `https://demo.nextcloud.com/xxx/settings/admin/additional`,choose `SMTP` mode

2.Set server address to "172.17.1.0`,then you will get screenshot(nextcloud1.png),it means not on the same network segment

3.Set server address to "172.17.0.0`,then you will get screenshot(nextcloud2.png),it means the address not exists or doesn't open any port to access

4.Set server address to "172.17.0.1` and port to empty,then the test email will send successfully!
it means this host exists and opens a smtp port

5.Set server address to "172.17.0.1` and port to `22`,then you will get screenshot(nextcloud3.png),it means the address exists,but can not access to the port


</details>

---
*Analysed by Claude on 2026-05-24*
