# Stored XSS 

## Metadata
- **Source:** HackerOne
- **Report:** 2926 | https://hackerone.com/reports/2926
- **Submitted:** 2014-03-03
- **Reporter:** anandpingsafe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

Go to this URL https://sehacure.slack.com/account/preferences?updated_highlight_words=1
and in the highlight words option please fill the XSS vector as 

</textarea><script>prompt(document.cookie);</script>

Your cookie will be reflected.

Best regards,
Anand

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

Go to this URL https://sehacure.slack.com/account/preferences?updated_highlight_words=1
and in the highlight words option please fill the XSS vector as 

</textarea><script>prompt(document.cookie);</script>

Your cookie will be reflected.

Best regards,
Anand

</details>

---
*Analysed by Claude on 2026-05-24*
