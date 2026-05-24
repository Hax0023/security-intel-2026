# Blind SSRF in emblem editor (2)

## Metadata
- **Source:** HackerOne
- **Report:** 265050 | https://hackerone.com/reports/265050
- **Submitted:** 2017-08-31
- **Reporter:** alexbirsan
- **Program:** Unknown
- **Bounty:** $1,500
- **Severity:** medium
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

As per your recommendation in #233301, I'm submitting a PoC for another blind SSRF in the emblem editor.

To oversight here is allowing absolute `url()` values for the `fill` attribute:

`<path fill="url(https://requestb.in/15rxmgv1#test)" stroke="#a1a1a1"  ... `

Upon publishing an emblem containing such an element, a HTTP request to the given URL is sent from a Rockstar server. (`███`). 

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

Hello,

As per your recommendation in #233301, I'm submitting a PoC for another blind SSRF in the emblem editor.

To oversight here is allowing absolute `url()` values for the `fill` attribute:

`<path fill="url(https://requestb.in/15rxmgv1#test)" stroke="#a1a1a1"  ... `

Upon publishing an emblem containing such an element, a HTTP request to the given URL is sent from a Rockstar server. (`███`). The destination port can be easily modified. This doesn't seem to work without including a fragment in the URL (`#test` in the example above).

Further testing showed that, if a valid SVG is found at the given URL, the `fill` data is actually used in the final image. Fortunately, ████████ doesn't seem to support scripts, although the possibility of finding another way to exfiltrate data doesn't seem that out of reach.

I've attached the full body of the emblem I've used to confirm this bug for ease of reproduction.

</details>

---
*Analysed by Claude on 2026-05-24*
