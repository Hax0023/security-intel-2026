# Stored XSS in app.lemlist.com

## Metadata
- **Source:** HackerOne
- **Report:** 928816 | https://hackerone.com/reports/928816
- **Submitted:** 2020-07-21
- **Reporter:** solov9ev
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
[add summary of the vulnerability]

## Steps To Reproduce:
  - Go to Company > Buddies-to-Be > Custom variables
  - Add malicious code: `" onmouseover="confirm(document.domain)" a="`

{F915718}

  -  Go to Company > Messages > Blank email
  - In the WYSIWYG  editor select `Custom variables`
  - Malicious code executed

{F915719}

## Impact

With this vulnerability, an attacker can for 

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
[add summary of the vulnerability]

## Steps To Reproduce:
  - Go to Company > Buddies-to-Be > Custom variables
  - Add malicious code: `" onmouseover="confirm(document.domain)" a="`

{F915718}

  -  Go to Company > Messages > Blank email
  - In the WYSIWYG  editor select `Custom variables`
  - Malicious code executed

{F915719}

## Impact

With this vulnerability, an attacker can for example steal users cookies or redirect users on malicious website.

</details>

---
*Analysed by Claude on 2026-05-24*
