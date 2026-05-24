# Stored XSS in SupportFlow Ticket Subject

## Metadata
- **Source:** HackerOne
- **Report:** 145086 | https://hackerone.com/reports/145086
- **Submitted:** 2016-06-16
- **Reporter:** whitehatter
- **Program:** Unknown
- **Bounty:** $50
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
SupportFlow contains an XSS vulnerability in how it handles ticket subjects in the admin-side ticket form, because the subject is not escaped before being used in the `value` attribute of the subject input element.

This first requires wptexturize to be disabled (not that uncommon):

```add_filter( 'run_wptexturize', '__return_false' );```

Then, create a ticket with a subject like this:

```
"><s

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

SupportFlow contains an XSS vulnerability in how it handles ticket subjects in the admin-side ticket form, because the subject is not escaped before being used in the `value` attribute of the subject input element.

This first requires wptexturize to be disabled (not that uncommon):

```add_filter( 'run_wptexturize', '__return_false' );```

Then, create a ticket with a subject like this:

```
"><script>alert('hi');</script>
```

The next time someone views that ticket (any other user) in the admin area at _SupportFlow -> All Tickets -> [Ticket]_, XSS is triggered.

This is due to this line not using `esc_attr()` on the title value (core does not do this automatically):

https://github.com/SupportFlow/supportflow/blob/71a6053848c523f7b50b61a1f3770013badc76c0/classes/class-supportflow-admin.php#L905

I've attached a screenshot demonstrating the XSS `alert` - please let me know if you have any questions or if I can clarify anything.

</details>

---
*Analysed by Claude on 2026-05-24*
