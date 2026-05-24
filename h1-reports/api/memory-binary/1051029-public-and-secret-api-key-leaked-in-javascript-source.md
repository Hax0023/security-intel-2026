# Public and secret api key leaked in JavaScript source

## Metadata
- **Source:** HackerOne
- **Report:** 1051029 | https://hackerone.com/reports/1051029
- **Submitted:** 2020-12-05
- **Reporter:** lmhu
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** memory-binary

## Summary
**Summary: [Summary the vulnerabilities]**
I am surfing on the bb3jobboard.topechelon.com website. I found a sensitive data including authentication key written in public accessible javascript file.

**URL Vulnerability**
  * https://bb3jobboard.topechelon.com/#!/search?page=1

###Steps To Reproduce:
  * Open bb3jobboard.topechelon.com and add payloads javascript-fuzz
  * Directory sensitive is ``

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

**Summary: [Summary the vulnerabilities]**
I am surfing on the bb3jobboard.topechelon.com website. I found a sensitive data including authentication key written in public accessible javascript file.

**URL Vulnerability**
  * https://bb3jobboard.topechelon.com/#!/search?page=1

###Steps To Reproduce:
  * Open bb3jobboard.topechelon.com and add payloads javascript-fuzz
  * Directory sensitive is ``//job_board.js//`` parse this json files using jsonparseronline
  * and look response bytes In response you can see Sensitive ApiKey Disclosure
  * Sensitive Information has been leaked on this source page job_board.js
  * Open your network browser , this javascript source has high files can leads to (DoS)

**Proof On Concept**
```javascript
}]), angular.module("jb").config(["lkGoogleSettingsProvider", function(e) {
    e.configure({
        apiKey: "██████████",
        clientId: "██████t.apps.googleusercontent.com",
        scopes: ["https://www.googleapis.com/auth/drive.readonly"],
        features: ["MULTISELECT_DISABLED"]
    })
}]), angular.module("jb.factories").factory("BoardSettingsFactory", ["railsResourceFactory", "PathToResourceRoute", function(e, t) {
    var n = e({
        url: t.convert(JBRoutes.jobBoardBoardSettingsPath),
        name: "boardSettings"
    });
```
**Screenshots Proof**
████

## Impact

Information disclosure

</details>

---
*Analysed by Claude on 2026-05-24*
