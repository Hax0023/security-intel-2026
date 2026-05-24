# Internal API endpoint is accesible for everyone

## Metadata
- **Source:** HackerOne
- **Report:** 1066790 | https://hackerone.com/reports/1066790
- **Submitted:** 2020-12-26
- **Reporter:** arnonymous
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** uncategorised

## Summary
## Summary:
It looks like the endpoint **/internal/cron/refreshCaseStats** as configured in [cron.yaml]  (https://github.com/WorldHealthOrganization/app/blob/master/server/appengine/src/main/webapp/WEB-INF/cron.yaml#L3) is accesible for everyone. Since it is configured as a cronjob to run every 5 minutes and starts with internal, this should not be the case, and could worst case lead to DoS if it'

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

## Summary:
It looks like the endpoint **/internal/cron/refreshCaseStats** as configured in [cron.yaml]  (https://github.com/WorldHealthOrganization/app/blob/master/server/appengine/src/main/webapp/WEB-INF/cron.yaml#L3) is accesible for everyone. Since it is configured as a cronjob to run every 5 minutes and starts with internal, this should not be the case, and could worst case lead to DoS if it's a costly operation.

## Steps To Reproduce:

  1. Go to https://hack.whocoronavirus.org/internal/cron/refreshCaseStats
```time curl -v https://hack.whocoronavirus.org/internal/cron/refreshCaseStats```

{F1130894}
Show that it takes about 20 seconds, before a 200 OK response returns (with a single request).

## Supporting Material/References:
https://github.com/WorldHealthOrganization/app/blob/master/server/appengine/src/main/webapp/WEB-INF/cron.yaml#L3

## Impact

Depending on the impact / performance of the action 'refresh case stats'  this could lead to unnecesarry load on the backend (and charges) or even DoS.

</details>

---
*Analysed by Claude on 2026-05-24*
