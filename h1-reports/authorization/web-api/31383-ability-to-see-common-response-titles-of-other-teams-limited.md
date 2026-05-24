# Ability to see common response titles of other teams (limited)

## Metadata
- **Source:** HackerOne
- **Report:** 31383 | https://hackerone.com/reports/31383
- **Submitted:** 2014-10-14
- **Reporter:** prakharprasad
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Insufficient Access Control, Information Disclosure, Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
A user can enumerate and view common response titles belonging to other teams by modifying the `common_response_id` parameter in trigger creation requests. By tampering with the JSON payload and changing the ID value, attackers can discover response templates and metadata from other organizations.

## Attack scenario
1. Attacker authenticates to their own HackerOne team/program dashboard
2. Attacker navigates to the triggers creation page (/team-name/triggers/new)
3. Attacker starts an intercepting proxy (Burp Suite, etc.) to capture the trigger creation request
4. Attacker creates a trigger with default settings and a common response
5. Attacker intercepts the JSON payload before it's sent to the server
6. Attacker increments the `common_response_id` value (e.g., 24, 18) and forwards the request, revealing response titles from other teams

## Root cause
The application does not properly validate that the `common_response_id` belongs to the user's team. The server accepts any valid ID without checking team ownership, allowing enumeration of resources across organizational boundaries.

## Attacker mindset
An attacker seeks to discover what response templates and communication strategies other competing bug bounty programs use, potentially for competitive intelligence or social engineering preparation. The low barrier to entry (simple parameter tampering) encourages exploration of the ID space.

## Defensive takeaways
- Implement server-side validation to ensure `common_response_id` references belong to the authenticated user's team only
- Use indirect object references or non-sequential IDs to prevent easy enumeration
- Log and alert on suspicious ID enumeration patterns
- Return generic error messages when accessing unauthorized resources rather than confirming existence
- Implement rate limiting on trigger creation requests to slow enumeration attacks
- Audit all object references in API endpoints for similar authorization bypass issues

## Variant hunting
Look for similar patterns where users can specify IDs for shared resources (templates, responses, policies, workflows) in team settings. Check other CRUD operations on team-scoped resources that may accept user-supplied IDs without proper authorization checks.

## MITRE ATT&CK
- T1526 - Reconnaissance (Resource Enumeration)
- T1087 - Account Discovery
- T1580 - Cloud Infrastructure Discovery

## Notes
This is a limited information disclosure vulnerability with low practical impact since response titles are relatively non-sensitive. However, it demonstrates a systemic authorization flaw that could be exploited more seriously in other features. The researcher properly disclosed the vulnerability with reproduction steps and included screenshots. The response IDs are redacted in the report but the vulnerability principle is clear.

## Full report
<details><summary>Expand</summary>

Hello guys,

Not sure what's happening exactly but when I go to my team (program) dashboard add a new Trigger and then tamper the request and change JSON variable `common_response_id` to say **24** and after trigger gets added I see a title of ████████ which is not in my default team template nor added by someone else of the team. Similarly if I set `common_response_id` to **18**, I get a trigger title of ████████ in the trigger (refer screenshots).This certainly seems to be of some other team.

**JSON (which gives trigger title as ████████):**
`{"title":"hackerone","criteria":[{"field":"any","type":"inclusion","inverse":false,"data":"agfagasga"}],"actions":[{"type":"request-needs-more-info","common_response_id":24}],"disabled":false}`

**Steps to Reproduce**

1. Login to Program/Team Dashboard 
2. Goto https://hackerone.com/<team-name>/triggers/new
3. Leave all options default and add text to criteria and select any common response.
4. Start the intercepting proxy and configure it to intercept the request
5. Now add title and enable the trigger then hit **Save**
6. Modify `common_response_id` to 24 for ████████ title or 18 for ████████ title

Kindly refer to screenshots as well.Revert back if you have any further query.

Thanks,
Prakhar Prasad

</details>

---
*Analysed by Claude on 2026-05-24*
