# Public and secret api key leaked  in JavaScript source

## Metadata
- **Source:** HackerOne
- **Report:** 983331 | https://hackerone.com/reports/983331
- **Submitted:** 2020-09-16
- **Reporter:** lmhu
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cleartext Storage of Sensitive Information
- **CVEs:** None
- **Category:** memory-binary

## Summary
**Summary:** [Summary the vulnerabilities]
I am surfing on the stripo website. I found a sensitive data including authentication key written in public accessible javascript file.

**URL Vulnerability**
https://staging.empleio.stripo.email/main.c1965c58f39a0f4aadc3.js

###Steps To Reproduce:
  * Open staging.empleio.stripo.email and add payloads javascript-fuzz
  * Directory sensitive is ``main.c19

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

**Summary:** [Summary the vulnerabilities]
I am surfing on the stripo website. I found a sensitive data including authentication key written in public accessible javascript file.

**URL Vulnerability**
https://staging.empleio.stripo.email/main.c1965c58f39a0f4aadc3.js

###Steps To Reproduce:
  * Open staging.empleio.stripo.email and add payloads javascript-fuzz
  * Directory sensitive is ``main.c1965c58f39a0f4aadc3.js`` parse this json files using jsonparseronline
  * and look response bytes In response you can see Sensitive ApiKey Disclosure
  * Sensitive Information has been leaked on this source page ``main.c1965c58f39a0f4aadc3.js``
  * Open your network browser , this javascript source has high files can leads to (DoS)

**Proof On Concept**
```javascript
projectId: null,
userFullName: null,
unSubscribeLink: null,
viewInBrowserLink: null,
initialTab: i.TAB_NAME_CONTENT,
aviaryApiKey: "████████",
youtubeApiKey: "███████",
onChangeFromCodeEditor: null,
onSaveEmail: null,
onSaveTemplate: null,
onUnauthorized: function(e)
```
**Screenshots Proof**
F989906
F989907

## Impact

Information Disclosure & DoS json files

</details>

---
*Analysed by Claude on 2026-05-24*
