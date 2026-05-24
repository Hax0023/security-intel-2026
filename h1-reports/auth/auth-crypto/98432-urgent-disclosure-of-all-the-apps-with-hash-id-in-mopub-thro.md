# Urgent : Disclosure of all the apps with hash ID in mopub through API request (Authentication bypass) 

## Metadata
- **Source:** HackerOne
- **Report:** 98432 | https://hackerone.com/reports/98432
- **Submitted:** 2015-11-07
- **Reporter:** indoappsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi Team,

This looks like a very critical issue so you should fix it ASAP.

Steps to reproduce :
1.Go to your mopub account and create a segment in your network.
2.You will get a segment ID now.
3.Now Go to the API link : https://app.mopub.com/networks/v2/api/segment/[Segment_id]
Note : page will take lot of time to open and your browser may crash because the response will have all the Apps in moh

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

Hi Team,

This looks like a very critical issue so you should fix it ASAP.

Steps to reproduce :
1.Go to your mopub account and create a segment in your network.
2.You will get a segment ID now.
3.Now Go to the API link : https://app.mopub.com/networks/v2/api/segment/[Segment_id]
Note : page will take lot of time to open and your browser may crash because the response will have all the Apps in mohub with there hash key.
4.When the page will be opened you can see all the Apps in App section.

Providing the video POC for more understanding :
https://youtu.be/QiiEiEeErGU

Kindly Fix the issue ASAP and Let me know if you need any other help from my side.
Best Regards !
Vijay Kumar 

</details>

---
*Analysed by Claude on 2026-05-24*
