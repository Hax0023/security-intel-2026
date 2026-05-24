# Stored self-XSS at m.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 134124 | https://hackerone.com/reports/134124
- **Submitted:** 2016-04-23
- **Reporter:** skavans
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
There is a stored self-XSS vulnerability at m.uber.com in displaying the uber invite code. If the user sets the invite code at `<script>alert(document.domain)</script>` value using the main personal area at the uber.com and then signs into the m.uber.com the XSS is fired.

Possible other user exploitation case can be the following:
The attacker sends messages to everyone with text:

```
I have wor

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

There is a stored self-XSS vulnerability at m.uber.com in displaying the uber invite code. If the user sets the invite code at `<script>alert(document.domain)</script>` value using the main personal area at the uber.com and then signs into the m.uber.com the XSS is fired.

Possible other user exploitation case can be the following:
The attacker sends messages to everyone with text:

```
I have worked at Uber and I know the secret invite code using by employees 
so invite friends using it gets you a $10000 discount for every invited friend. 
Set your invite code to this value:
EMPLOYEE_2016_04_oidkjnfkerjnoidkjnfkerjnoidkjnfkerjnoidkjnfkerjnoidkjnfkerjn<script>eval(atob('YWxlcnQoZG9jdW1lbnQuZG9tYWluKQ=='))</script>oidkjnfkerjnoidkjnfkerjnoidkjnfkerjnoidkjnfkerjnoidkjnfkerjn
```
The unlimited invite code length makes easier to hide a payload inside it. So user will set his invite code to this value and next time he will visit the m.uber.com the XSS will fire.

</details>

---
*Analysed by Claude on 2026-05-24*
