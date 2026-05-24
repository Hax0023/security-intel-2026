# Sign up CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 6872 | https://hackerone.com/reports/6872
- **Submitted:** 2014-04-10
- **Reporter:** cliantech
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Again sir,

There is no mitigation against CSRF attacks on the regsitration, I believe when not fixed you will be flooded with reports by researchers regarding this.

<form action="" method="post" class="signupForm" novalidate>
                <p>Sign up for a free account / <b><a href="/pricing" target="_blank">Pricing</a></b></p>
                <div class="userError"></div>
             

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

Again sir,

There is no mitigation against CSRF attacks on the regsitration, I believe when not fixed you will be flooded with reports by researchers regarding this.

<form action="" method="post" class="signupForm" novalidate>
                <p>Sign up for a free account / <b><a href="/pricing" target="_blank">Pricing</a></b></p>
                <div class="userError"></div>
                <div id="signupOrgInfo" class="userInfo">You’re signing up to join the <b id="signupOrgName"></b> team.</div>
                <p class="form"><input class="input" name="realname" placeholder="Name"></p>
                <p class="form"><input class="input" name="email" type="email" placeholder="Email"></p>
                <p class="form"><input class="input" name="password" type="password" placeholder="Password"></p>
                <input type="hidden" name="invite">
                <input type="hidden" name="org_invite">
                <p class="form"><button type="submit" class="signup"><span>Sign up</span></button></p>
                <p><small>By signing up, you agree to our <a href="/terms">Terms of Service</a></small></p>
            </form>

Kindly let me know if you needed more information.

Clifford

</details>

---
*Analysed by Claude on 2026-05-24*
