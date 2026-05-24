# Stealing Users OAuth Tokens through redirect_uri parameter

## Metadata
- **Source:** HackerOne
- **Report:** 665651 | https://hackerone.com/reports/665651
- **Submitted:** 2019-08-01
- **Reporter:** manshum12
- **Program:** Unknown
- **Bounty:** $750
- **Severity:** high
- **Vuln:** Open Redirect
- **CVEs:** None
- **Category:** auth-crypto

## Summary
I found that https://login.fr.cloud.gov/oauth/authorize has vulnerability by open redirect on oauth redirect_uri which can lead to users oauth tokens being leaked to any malicious user.

Step : 
1, Clicked on link https://login.fr.cloud.gov/oauth/authorize?client_id=███&response_type=token&redirect_uri=https%3A%2F%2Fevil.com%2Fauth%2Fcallback&state=███

2, Choose any .gov account to login ( Screen

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

I found that https://login.fr.cloud.gov/oauth/authorize has vulnerability by open redirect on oauth redirect_uri which can lead to users oauth tokens being leaked to any malicious user.

Step : 
1, Clicked on link https://login.fr.cloud.gov/oauth/authorize?client_id=███&response_type=token&redirect_uri=https%3A%2F%2Fevil.com%2Fauth%2Fcallback&state=███

2, Choose any .gov account to login ( Screenshot ) then i believe you will got redirect to evil.com with oauth access token .

## Impact

Attacker can using this bug to stolen victim access token , that means he can takeover victim account .

</details>

---
*Analysed by Claude on 2026-05-24*
