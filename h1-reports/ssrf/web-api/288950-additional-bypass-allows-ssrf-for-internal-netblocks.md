# Additional bypass allows SSRF for internal netblocks

## Metadata
- **Source:** HackerOne
- **Report:** 288950 | https://hackerone.com/reports/288950
- **Submitted:** 2017-11-09
- **Reporter:** edoverflow
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** CVE-2017-0909
- **Category:** web-api

## Summary
It turns out there is another bypass in the `private_address_check` gem. The gem does not include 0.0.0.0 in the exclusion list in the first place.

```
irb(main):001:0> require 'private_address_check'
=> true
irb(main):002:0> PrivateAddressCheck.private_address?("0.0.0.0")
=> false
```

I was able to bypass your filter by using http://0.0.0.0:22/ as you can see below:

{F238151}

Please find a ho

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

It turns out there is another bypass in the `private_address_check` gem. The gem does not include 0.0.0.0 in the exclusion list in the first place.

```
irb(main):001:0> require 'private_address_check'
=> true
irb(main):002:0> PrivateAddressCheck.private_address?("0.0.0.0")
=> false
```

I was able to bypass your filter by using http://0.0.0.0:22/ as you can see below:

{F238151}

Please find a hotfix for this issue attached to this report: {F238152}. The author of the gem has been notified and should hopefully provide a proper fix very soon.



</details>

---
*Analysed by Claude on 2026-05-24*
