# Login CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 6871 | https://hackerone.com/reports/6871
- **Submitted:** 2014-04-10
- **Reporter:** cliantech
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi sir,

There is no mitigation of XCSRF in your login form. 

Kindly check the source code of login:

<form class="signin" action="" method="post" novalidate>
                    <p class="form">
                        <input class="input" name="email" type="email" placeholder="Email">
                        <input class="input" name="password" type="password" placeholder="Password">


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

Hi sir,

There is no mitigation of XCSRF in your login form. 

Kindly check the source code of login:

<form class="signin" action="" method="post" novalidate>
                    <p class="form">
                        <input class="input" name="email" type="email" placeholder="Email">
                        <input class="input" name="password" type="password" placeholder="Password">
                        <input type="hidden" name="org_invite">
                        <button type="submit"><span>Login</span></button>
                        <a class="forgotten" href="#?/password-reset">Forgotten your password?</a>
                    </p>
                    <div class="userError"></div>
                </form>

kindly let me know if you needed more information.

Clifford

</details>

---
*Analysed by Claude on 2026-05-24*
