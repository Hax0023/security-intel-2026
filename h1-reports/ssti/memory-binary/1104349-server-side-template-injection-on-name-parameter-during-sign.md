# Server Side Template Injection on Name parameter during Sign Up process

## Metadata
- **Source:** HackerOne
- **Report:** 1104349 | https://hackerone.com/reports/1104349
- **Submitted:** 2021-02-16
- **Reporter:** battle_angel
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Code Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
## Summary:
Server-side template injection is when an attacker is able to use native template syntax to inject a malicious payload into a template, which is then executed server-side. 
In this scenario, when an attacker signs up on the platform and uses a payload in the **First Name** field, the payload is rendered server side and it gets executed in the promotional/welcome emails sent to the user

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
Server-side template injection is when an attacker is able to use native template syntax to inject a malicious payload into a template, which is then executed server-side. 
In this scenario, when an attacker signs up on the platform and uses a payload in the **First Name** field, the payload is rendered server side and it gets executed in the promotional/welcome emails sent to the user

## Steps To Reproduce:
Step 1: Navigate to [Glovoapp] (https://www.glovoapp.com/kg/en/bishkek/) and click on **Register**
Step 2: Now, in the ```First Name``` field, enter the value ```{{7*7}}```

{F1197322}


Step 3: Fill in the rest of the values on the Register page and register your account.

{F1197320}


Step 4: We have used the payload ```{{7*7}}``` here to verify that it is being evaluated at the backend
Step 5: Now, wait for the welcome/promotional email to arrive in your Inbox
Step 6: Notice that the email arrives with the Subject as ```49, welcome to Glovo!```

{F1197321}


Step 7: The attacker can now further exploit this issue by injecting malicious payloads in the Name field and gathering sensitive information from the application.


Note- After carrying out this attack, I didn't receive any welcome email for my other account maybe because the code broke.

## Impact

Template engines are widely used by web applications to present dynamic data via web pages and emails. Unsafely embedding user input in templates enables Server-Side Template Injection, which can be used to directly attack web servers' internals and often obtain Remote Code Execution (RCE), turning every vulnerable application into a potential pivot point.

</details>

---
*Analysed by Claude on 2026-05-24*
