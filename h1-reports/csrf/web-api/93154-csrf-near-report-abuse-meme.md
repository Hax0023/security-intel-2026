# Csrf near report abuse meme 

## Metadata
- **Source:** HackerOne
- **Report:** 93154 | https://hackerone.com/reports/93154
- **Submitted:** 2015-10-09
- **Reporter:** oroborus
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hey team i would like to report a real csrf threat which allows attacker to make report abuse to any meme on behalf of the users 

how i found this bug :-

lets visit to any meme example :-

1> http://imgur.com/t/memes/ieTEJEd 
2> i clicked on post options 
3> i got an option called report i clicked on it
4> i selected a option of abusive/offensive 
5>started my intercept and click on report 
6> a

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

Hey team i would like to report a real csrf threat which allows attacker to make report abuse to any meme on behalf of the users 

how i found this bug :-

lets visit to any meme example :-

1> http://imgur.com/t/memes/ieTEJEd 
2> i clicked on post options 
3> i got an option called report i clicked on it
4> i selected a option of abusive/offensive 
5>started my intercept and click on report 
6> after intercepting i saw the post request having a unique token like ''Sid'' which maybe for form validations
7>i managed to delete the value of sid and still get a 200 ok status code and it was report abused 

below i will attach the snapshot of the original request edited and response :)

i ve attached images of original request and i have stripped off the formvalidation tokens and session values and passed the request i could still get a 200 ok status which means the vaidations are not properly checked server side  



</details>

---
*Analysed by Claude on 2026-05-24*
