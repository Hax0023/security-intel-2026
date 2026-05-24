# Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 121827 | https://hackerone.com/reports/121827
- **Submitted:** 2016-03-09
- **Reporter:** bugdisclose
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello this is regarding an account takeover via import image from facebook option, when we import fb photos a link with a token generated which is valid for any user and it can be use to replace user linked fb account to attacker fb account And then login via fb to takeover account

Note: I tested it on https://m.Badoo.com
-

Steps to reproduce :-
--

1 -Create two Badoo account attacker & victim 

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

Hello this is regarding an account takeover via import image from facebook option, when we import fb photos a link with a token generated which is valid for any user and it can be use to replace user linked fb account to attacker fb account And then login via fb to takeover account

Note: I tested it on https://m.Badoo.com
-

Steps to reproduce :-
--

1 -Create two Badoo account attacker & victim and link 2 diff fb account in each of them

2- Login as 'attacker' and go to import photos via fb and copy the link from URL bar 

3- Now login as 'victim' in diffrent browser and open the link and click cancel.

4- FB account of 'victim' is replaced with FB account of 'attacker' (Removed from 'victim' one)

5-Login via attacker FB account and you will be logged in 'User' account 

Congo u just hacked victim account 

More explanation
--
Suppose a user have an account of attacker 'A' with FB linked which 'FB-of-A' and a victim account 'B' with fb linked which is 'FB-of-B' now attacker create a link to import photos from his fb and give it to victim 'B' he opens it and press cancel but this have changed his FB account 'FB-of-B' to attacker's FB account 'FB-of-A', And now attacker can login with his fb account in victim's badoo account.

I have made a PoC video on mobile so if u need i will send it or please wait i will send u PC made within mext 24 hours

</details>

---
*Analysed by Claude on 2026-05-24*
