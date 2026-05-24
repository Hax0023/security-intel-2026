# Information Disclosure - Sensitive Domain Leaked in Scope Change History

## Metadata
- **Source:** HackerOne
- **Report:** 313075 | https://hackerone.com/reports/313075
- **Submitted:** 2018-02-07
- **Reporter:** eqbang
- **Program:** Technology Transformation Service (TTS) - bug bounty program
- **Bounty:** not specified
- **Severity:** low
- **Vuln:** information_disclosure, privacy_violation, sensitive_data_exposure
- **CVEs:** None
- **Category:** web-api

## Summary
The HackerOne report history page exposed a sensitive government domain (https://ci.fr.cloud.gov) in scope change activity logs, despite moderators redacting it from the public summary. This violated the program's confidentiality requirements by revealing infrastructure details meant to remain private.

## Attack scenario
1. Attacker views a publicly disclosed HackerOne report that was modified by moderators
2. Moderators redacted sensitive domain information from the report summary and set it to example.gov
3. Attacker scrolls to the activity/changelog section at the bottom of the page
4. Attacker discovers the unredacted domain (https://ci.fr.cloud.gov) in the scope change history showing 'britta changed the scope from https://ci.fr.cloud.gov to None'
5. Attacker gains information about TTS infrastructure despite confidentiality measures
6. Attacker uses this domain information for reconnaissance or targeting

## Root cause
Inconsistent redaction controls - while report content was sanitized, the activity history/changelog feed was not subject to the same redaction rules, allowing sensitive information to leak through audit logs visible to report readers.

## Attacker mindset
Reconnaissance-focused attacker looking for unintended information disclosures in public reports. Understands that organizations often overlook historical logs and metadata when redacting sensitive content, making changelog sections valuable reconnaissance targets.

## Defensive takeaways
- Apply consistent redaction policies across all report sections including activity logs, changelogs, and metadata
- Audit log entries should undergo the same sensitivity review as report content before publication
- Implement a system-level redaction mechanism that applies to all historically visible activities
- Use generic messages for scope changes when specific URLs are sensitive (e.g., 'scope modified' instead of revealing domains)
- Regular security review of what information is exposed in activity feeds and audit trails
- Consider making detailed change histories visible only to authorized parties, not all report viewers

## Variant hunting
Check for sensitive information in activity logs/changelogs of other disclosed reports
Look for unredacted details in version history, edit history, or modification timestamps
Examine metadata fields (timestamps, modifier names, IP addresses) for information leaks
Review other public disclosure platforms for similar changelog redaction bypasses
Check if attachment upload/deletion histories expose sensitive filenames
Look for similar issues in program policy documents or scope pages that may have revision histories

## MITRE ATT&CK
- T1589.001
- T1598.004
- T1598.003

## Notes
Low severity but important for maintaining program confidentiality. The issue demonstrates that redaction efforts must be comprehensive across all UI elements. Related to report 311289. The reporter correctly identified that domain-specific information should never appear in activity logs for sensitive programs.

## Full report
<details><summary>Expand</summary>

**Summary:**
please refer to the following report:
https://hackerone.com/reports/311289

It was noticed that TTS changed the summary and set the domain to example.gov as not to reveal to the public. But at the bottom of the page, "britta changed the scope from https://ci.fr.cloud.gov to None."

Recommendation:
Should only provide general message for such situation: "britta changed the scope"

## Impact

not much of impact. but violate Confidentiality of the program.

</details>

---
*Analysed by Claude on 2026-05-24*
