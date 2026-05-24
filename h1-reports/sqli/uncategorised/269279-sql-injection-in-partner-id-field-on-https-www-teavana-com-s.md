# SQL injection in partner id field on https://www.teavana.com (Sign-up form)

## Metadata
- **Source:** HackerOne
- **Report:** 269279 | https://hackerone.com/reports/269279
- **Submitted:** 2017-09-18
- **Reporter:** bigbug
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
While signing up for "teavana" shopping account on it came to notice that the partner id validation fails and exists SQL injection.

So this is what I did:

1) Visit https://www.teavana.com/us/en/account
2) Click on signin > create shopping account
3) In the partnerno, gave an input of "1234" (1.PNG)
     Result :No issue as expected . Signup fails
     message: "We are unable to verify starbucks 

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

While signing up for "teavana" shopping account on it came to notice that the partner id validation fails and exists SQL injection.

So this is what I did:

1) Visit https://www.teavana.com/us/en/account
2) Click on signin > create shopping account
3) In the partnerno, gave an input of "1234" (1.PNG)
     Result :No issue as expected . Signup fails
     message: "We are unable to verify starbucks partner id" (2 .PNG)
4) Changed input to "1234' OR 1=1" (without double qoutes) (3.PNG)
    Result: This time signup succeeds!!! (4.PNG) 



</details>

---
*Analysed by Claude on 2026-05-24*
