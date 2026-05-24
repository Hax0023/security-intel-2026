# SSRF via webhook

## Metadata
- **Source:** HackerOne
- **Report:** 243277 | https://hackerone.com/reports/243277
- **Submitted:** 2017-06-26
- **Reporter:** cablej
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

There exists an SSRF vulnerability with the account webhook feature, allowing an attacker to verify the existence of the EC2 metadata url and enumerate URL's.

POC:

1. Create a webhook at https://app.mixmax.com/dashboard/settings/rules with url `http://169.254.169.254/latest/meta-data/`.
2. Trigger this webhook by sending/receiving an email. Wait a few hours.
3. Note that an email is not sen

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

Hi,

There exists an SSRF vulnerability with the account webhook feature, allowing an attacker to verify the existence of the EC2 metadata url and enumerate URL's.

POC:

1. Create a webhook at https://app.mixmax.com/dashboard/settings/rules with url `http://169.254.169.254/latest/meta-data/`.
2. Trigger this webhook by sending/receiving an email. Wait a few hours.
3. Note that an email is not sent saying the webhook failed. I tried for other internal urls such as 'http://localhost', but they sent a failure email, indicating that `http://169.254.169.254/latest/meta-data/` is open to the webhook.
4. In addition to verifying that this endpoint exists, an attacker could enumerate endpoints on this domain. For example, an attacker could enumerate MAC addresses at `http://169.254.169.254/latest/meta-data/network/interfaces/macs/xx:xx:...`.

Suggested fix:

Blacklist the AWS metadata url and any other sensitive internal urls.

Thanks.

</details>

---
*Analysed by Claude on 2026-05-24*
