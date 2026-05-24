# XSS in editor by any user

## Metadata
- **Source:** HackerOne
- **Report:** 18691 | https://hackerone.com/reports/18691
- **Submitted:** 2014-07-01
- **Reporter:** tunnelshade
- **Program:** Unknown
- **Bounty:** $1,000
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
# Steps 

+ Open any editor in phabricator where memes can be used (literally anywhere :P)
+ Enter the following and save it & **BOOM**

```
{meme, src= http://dummy//onerror=eval(prompt(1))// }
```

# Why ?

+ Nested parsing is causing the src value to be treated as a link which is automatically made link by fabricator. So, a whole mess-up of syntax happening there.
+ ```\\``` are bei

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

# Steps 

+ Open any editor in phabricator where memes can be used (literally anywhere :P)
+ Enter the following and save it & **BOOM**

```
{meme, src= http://dummy//onerror=eval(prompt(1))// }
```

# Why ?

+ Nested parsing is causing the src value to be treated as a link which is automatically made link by fabricator. So, a whole mess-up of syntax happening there.
+ ```\\``` are being used as space separators since those replaced.

# Fix ?

+ May be to avoid nested parsing, it messes up things. But the choice is yours since you have more knowledge of the application needs

</details>

---
*Analysed by Claude on 2026-05-24*
