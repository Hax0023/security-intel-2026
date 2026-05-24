# Hard-coded API keys at NordVpn Android App

## Metadata
- **Source:** HackerOne
- **Report:** 792850 | https://hackerone.com/reports/792850
- **Submitted:** 2020-02-11
- **Reporter:** dantt
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Use of Hard-coded Credentials
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hello NordVpn,

**APK Version : 4.6.2**
**API'S at res/values/strings.xml**

>**Google**
>google_api_key = ███
**Stripe**
>stripe_publishable_api_key = ██████████

**Referance;** 
>https://stripe.com/docs/keys

## Impact

Cleartext Storage of Sensitive Information

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

Hello NordVpn,

**APK Version : 4.6.2**
**API'S at res/values/strings.xml**

>**Google**
>google_api_key = ███
**Stripe**
>stripe_publishable_api_key = ██████████

**Referance;** 
>https://stripe.com/docs/keys

## Impact

Cleartext Storage of Sensitive Information

</details>

---
*Analysed by Claude on 2026-05-24*
