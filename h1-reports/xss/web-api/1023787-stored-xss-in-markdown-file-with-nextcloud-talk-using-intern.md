# Stored XSS in markdown file with Nextcloud Talk using Internet Explorer

## Metadata
- **Source:** HackerOne
- **Report:** 1023787 | https://hackerone.com/reports/1023787
- **Submitted:** 2020-11-01
- **Reporter:** verg
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** CVE-2020-8294
- **Category:** web-api

## Summary
While editing a markdown file through the text app, users can create link elements that have a javascript URL such as `javascript:alert(1)`.

Steps to reproduce:
* While editing a markdown file, select some text and click the "Add Link"  button.
* Using a web proxy, intercept the request and change the href value to `javascript:alert(1)`.

{F1060394}

* Refresh the document and click the malicious

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

While editing a markdown file through the text app, users can create link elements that have a javascript URL such as `javascript:alert(1)`.

Steps to reproduce:
* While editing a markdown file, select some text and click the "Add Link"  button.
* Using a web proxy, intercept the request and change the href value to `javascript:alert(1)`.

{F1060394}

* Refresh the document and click the malicious link created to fire the payload.

{F1060397}

Note that CSP blocks the javascript from running, but browsers such as IE are still vulnerable.

{F1060402}

## Impact

An attacker could execute arbitrary JavaScript code on the web browser of a victim who opens the file and clicks the malicious link.

</details>

---
*Analysed by Claude on 2026-05-24*
