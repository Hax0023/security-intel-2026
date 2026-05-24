# IDOR leads to Leakage an ██████████ Login Information

## Metadata
- **Source:** HackerOne
- **Report:** 1093908 | https://hackerone.com/reports/1093908
- **Submitted:** 2021-02-03
- **Reporter:** sleepnotf0und
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insufficiently Protected Credentials
- **CVEs:** None
- **Category:** web-api

## Summary
Hi security team,
According to my report #1092618, The VDP team agreed that ***█████████*** and it's subdomains is in the scope of the DoD program
I continue testing that domain
.
.

##Issue Description:
There is an IDOR in██████.███████ that connected with ████████.███████ 
(highly protected encryption chat app)
.
This IDOR leaks only the usernames 
When I used this IDOR in my account it leaks my

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

Hi security team,
According to my report #1092618, The VDP team agreed that ***█████████*** and it's subdomains is in the scope of the DoD program
I continue testing that domain
.
.

##Issue Description:
There is an IDOR in██████.███████ that connected with ████████.███████ 
(highly protected encryption chat app)
.
This IDOR leaks only the usernames 
When I used this IDOR in my account it leaks my username which is required for the login authentication
So I tried to  get the █████████ username in order to use this credential to access to the ██████████ panel in██████.██████
And It Worked I get the ███ username which is required for the login authentication
```displayname	"█████"```
.
.
With the correct ██████████ username an attacker can easily make a successful Bruteforce attack by using simple bruteforce tools to get access the █████████ panel as there is no rate limit in the login page
.
.
.

##Expected Behavior
403 forbidden

## Impact

With the correct █████████ username an attacker can easily make a successful Bruteforce attack by using simple bruteforce tools to get access the ███████ panel as there is no rate limit in the login page

## System Host(s)
██████.██████████.████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1 - Visit██████████.██████ 
2 - Sign in ( You can my test account ***username:███*** and  ***password: ███████████████*** )
3 - Now you logged in████.████████ 
4 - Visit█████.████/████.█████████
5 - After that try replace the username ***█████████*** with ***████*** /█████@***██████***:█████.████████
6 - Final link███.███████/████@████████:███████.██████
7 - Notice the █████████ username

## Suggested Mitigation/Remediation Actions
***██████████.███████.███████*** Should use HTTP Authorization header or 
The directory ***/████████/*** should not be accessed by any one



</details>

---
*Analysed by Claude on 2026-05-24*
