# Blind SSRF due to img tag injection in career form

## Metadata
- **Source:** HackerOne
- **Report:** 236301 | https://hackerone.com/reports/236301
- **Submitted:** 2017-06-03
- **Reporter:** encrypt
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
There is SSRF vulnerability due to img tag injection in career form. Attacker can inject multiple tags and perform multiple requests on remote hosts.

**POC**
1. Visit https://mixmax.com/careers.
2. Click on `Apply now`.
3. Insert img tag `<img src=https://your_choice.com>` in all the fields.
4. Click on `Send Application`.
5. Check server logs.

I got the following ip and user-agent headers.


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
There is SSRF vulnerability due to img tag injection in career form. Attacker can inject multiple tags and perform multiple requests on remote hosts.

**POC**
1. Visit https://mixmax.com/careers.
2. Click on `Apply now`.
3. Insert img tag `<img src=https://your_choice.com>` in all the fields.
4. Click on `Send Application`.
5. Check server logs.

I got the following ip and user-agent headers.
IP: 66.249.84.213
User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
