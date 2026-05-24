# The email API to test email-server settings is unlimited and can be used as a email bomb

## Metadata
- **Source:** HackerOne
- **Report:** 222660 | https://hackerone.com/reports/222660
- **Submitted:** 2017-04-21
- **Reporter:** xifengweiyu
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Description:**

The email-server settings test function in  `https://demo.nextcloud.com/xxx/settings/admin/additional` is unlimited and can be used as a email bomb.

And the test email API  is `https://demo.nextcloud.com/xxx/settings/admin/mailtest`

**Reproduce steps:**

1.Go to `https://demo.nextcloud.com/xxx/settings/personal` ,set your personal address to a email address which you want to at

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

**Description:**

The email-server settings test function in  `https://demo.nextcloud.com/xxx/settings/admin/additional` is unlimited and can be used as a email bomb.

And the test email API  is `https://demo.nextcloud.com/xxx/settings/admin/mailtest`

**Reproduce steps:**

1.Go to `https://demo.nextcloud.com/xxx/settings/personal` ,set your personal address to a email address which you want to attack .see screenshot(1)

2.Then go to `https://demo.nextcloud.com/xxx/settings/admin/additional`,`send test mail` ,then above email address will receive an test email.

3.So I can use chrome console network panel to `replay XHR` continuously,then my email box receive many email.see screenshot(2)



</details>

---
*Analysed by Claude on 2026-05-24*
