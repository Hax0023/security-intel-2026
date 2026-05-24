# XSS due to incomplete JS escaping

## Metadata
- **Source:** HackerOne
- **Report:** 474262 | https://hackerone.com/reports/474262
- **Submitted:** 2019-01-03
- **Reporter:** jessecampos
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
`ActionView::Helpers::JavaScriptHelper` inside ` rails/actionview/lib/action_view/helpers/javascript_helper.rb` provides JS escaping in Rails, but fails to protect template literal strings. As such, there are two ways XSS can occur:

###XSS via template literal break out:
1) Create a view with the following code: 
```
<script>let a = `<%= j '`+alert`' %>`</script>
```
2) The alert will execute bec

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

`ActionView::Helpers::JavaScriptHelper` inside ` rails/actionview/lib/action_view/helpers/javascript_helper.rb` provides JS escaping in Rails, but fails to protect template literal strings. As such, there are two ways XSS can occur:

###XSS via template literal break out:
1) Create a view with the following code: 
```
<script>let a = `<%= j '`+alert`' %>`</script>
```
2) The alert will execute because backticks aren't escaped.

###XSS via template literal placeholder evaluation:
1) Create a view with the following code:
```
<script>let a = `<%= j '${alert()}' %>`</script>
```
2) The alert will execute because `${expression}` isn't escaped
(escaping `$` with `\$` seems sufficient)

## Impact

Attackers can leverage this weakness to [steal private information, hijack accounts and distribute malware](https://chefsecure.com/blog/the-12-exploits-of-xss-mas-infographic) by injecting malicious code instead of an alert.

</details>

---
*Analysed by Claude on 2026-05-24*
