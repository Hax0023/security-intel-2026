# Prevent XSS when passing a parameter directly into link_to 

## Metadata
- **Source:** HackerOne
- **Report:** 755354 | https://hackerone.com/reports/755354
- **Submitted:** 2019-12-10
- **Reporter:** speleding
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - DOM
- **CVEs:** None
- **Category:** web-api

## Summary
*Note: I would say this is perhaps more of a feature request than an actual vulnerability, but Rafael França deleted this from GitHub and asked to submit it here instead*

In a rails views it's easy to accidentally create an XSS vulnerability by using the following in a template:
`<%= link_to 'Back', params[:back] %>`

Doing this exposes the app to an attack that can easily be demonstrated by simp

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

*Note: I would say this is perhaps more of a feature request than an actual vulnerability, but Rafael França deleted this from GitHub and asked to submit it here instead*

In a rails views it's easy to accidentally create an XSS vulnerability by using the following in a template:
`<%= link_to 'Back', params[:back] %>`

Doing this exposes the app to an attack that can easily be demonstrated by simply adding this to URL of that view:
`?back=javascript%3Aalert%28boom%29%3B`

I think it would be good if rails detects this situation and filters the link_to parameter if it's from an untrusted source. The attached two-line patch does this by only allowing the HTTP(S) protocol in that case.

## Impact

If a programmer inadvertently passes a parameter directly into link_to then this would leave his site open to an XSS attack. Since rails filters untrusted parameters in many other situations it may not be apparent to the casual observer that link_to does not filter javascript.

</details>

---
*Analysed by Claude on 2026-05-24*
