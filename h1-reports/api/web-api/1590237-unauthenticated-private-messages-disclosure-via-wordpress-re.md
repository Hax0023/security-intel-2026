# Unauthenticated Private Messages DIsclosure via wordpress Rest API

## Metadata
- **Source:** HackerOne
- **Report:** 1590237 | https://hackerone.com/reports/1590237
- **Submitted:** 2022-06-03
- **Reporter:** ghimire_veshraj
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Vulnearble Plugin: Senei LMS

Hi there,
Hope you are doing well,
So, i noticed that their is an option to contact teacher on Sensei LMS which is meant to private.
By default, other user can't see the question I asked to the teacher.
But using the  `/wp-json/wp/v2/sensei-messages/<numericID>` where numeric ID can be bruteforced.
Those private questions asked to teacher is still visible to any Unaut

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

Vulnearble Plugin: Senei LMS

Hi there,
Hope you are doing well,
So, i noticed that their is an option to contact teacher on Sensei LMS which is meant to private.
By default, other user can't see the question I asked to the teacher.
But using the  `/wp-json/wp/v2/sensei-messages/<numericID>` where numeric ID can be bruteforced.
Those private questions asked to teacher is still visible to any Unauthenticated User.
{F1754958}

Steps to reproduce:
Create any course then as a student, ask question on that course.
Now, the message is visible through `/wp-json/wp/v2/sensei-messages/<numericID>` 
Sensei LMS lacks authentication in a REST API endpoint, allowing unauthenticated users to discover private questions sent between teacher and student on the site.

## Impact

Disclosure of Private Questions to Unauthenticated User.

</details>

---
*Analysed by Claude on 2026-05-24*
