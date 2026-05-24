# Password Reset emails missing TLS leads account takeover

## Metadata
- **Source:** HackerOne
- **Report:** 173251 | https://hackerone.com/reports/173251
- **Submitted:** 2016-09-30
- **Reporter:** c0rte
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi,

I saw that the email is sent in clear-text instead of TLS (Transport Layer Security) any Man-in-the-middle attacker is able to read these sensitive Emails and get the password reset link which lead to account takeover.

Email details:
from:	help@rubygems.org
to:	Victim@gmail.com
date:	Fri, Sep 30, 2016 at 10:31 PM
subject:	Change your password
mailed-by:	rubygems.org
encryption:	ec2-52-43-250

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

I saw that the email is sent in clear-text instead of TLS (Transport Layer Security) any Man-in-the-middle attacker is able to read these sensitive Emails and get the password reset link which lead to account takeover.

Email details:
from:	help@rubygems.org
to:	Victim@gmail.com
date:	Fri, Sep 30, 2016 at 10:31 PM
subject:	Change your password
mailed-by:	rubygems.org
encryption:	ec2-52-43-250-235.us-west-2.compute.amazonaws.com did not encrypt this message

Thanks,
Diogo Real




</details>

---
*Analysed by Claude on 2026-05-24*
