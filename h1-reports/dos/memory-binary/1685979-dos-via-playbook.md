# Denial of Service via Unbounded Playbook Template Attributes

## Metadata
- **Source:** HackerOne
- **Report:** 1685979 | https://hackerone.com/reports/1685979
- **Submitted:** 2022-08-31
- **Reporter:** vultza
- **Program:** Mattermost
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Input Validation Bypass, Lack of Rate Limiting
- **CVEs:** CVE-2022-4019
- **Category:** memory-binary

## Summary
A normal authenticated user can create a playbook with unbounded string attributes (run_summary_template, retrospective_template, description) allowing injection of up to 50MB of data. Executing such a playbook triggers excessive server resource consumption, crashing the application and denying service to all users.

## Attack scenario
1. Attacker authenticates as a normal user and obtains MMAUTHTOKEN
2. Attacker crafts a malicious playbook payload with run_summary_template field containing 50MB of data
3. Attacker sends POST request to /plugins/playbooks/api/v0/playbooks endpoint with the oversized payload
4. Playbook is successfully created without size validation
5. Attacker navigates to playbook and clicks 'Run' button to execute it
6. Server enters resource exhaustion state processing the massive template, becoming unresponsive and eventually crashing, affecting all users

## Root cause
The playbook creation API endpoint lacks input validation and size constraints on string attributes. Template processing during playbook execution does not implement resource limits or streaming, forcing the server to load and process the entire massive payload into memory simultaneously.

## Attacker mindset
An authenticated user with malicious intent seeks to disrupt service availability. The attacker exploits the trust model that assumes authenticated users are non-malicious. This is a low-effort, high-impact attack requiring only basic API knowledge and a valid account.

## Defensive takeaways
- Implement strict input validation with maximum length constraints on all user-supplied string fields, especially template attributes
- Enforce rate limiting on resource-intensive operations like playbook execution
- Implement server-side size checks before processing templates, rejecting oversized payloads early
- Add resource quotas and timeout mechanisms for template rendering and playbook execution
- Monitor resource consumption during playbook runs and gracefully terminate runaway processes
- Implement pagination and streaming for large data processing instead of full in-memory loading
- Add authentication-level access controls to restrict who can create playbooks with resource-intensive operations
- Implement comprehensive logging and alerting for abnormal resource consumption patterns

## Variant hunting
Check for similar unbounded input fields in other plugin features and core Mattermost functionality
Test workflow/automation creation endpoints for identical DoS vectors
Examine message templates, notification templates, and other template-based features for size validation
Audit webhook payload handlers for input size limits
Investigate custom field creation and modification endpoints for similar vulnerabilities
Test integration configuration endpoints for unbounded data acceptance

## MITRE ATT&CK
- T1190
- T1499
- T1499.1
- T1499.4

## Notes
This is a critical infrastructure vulnerability despite medium CVSS because it affects availability for all users. The persistent nature (playbook remains after restart) and the UI rendering failure post-crash indicate the severity extends beyond simple DoS. The vulnerability leverages the implicit trust of authenticated users which is often overlooked in security models.

## Full report
<details><summary>Expand</summary>

## Summary:
A normal user can create a playbook, that has some attributes like the `run_summary_template`, `retrospective_template` and `description`,that don't have any size check or validation, which allows an attacker to set an unlimited number of characters as their values.

In a production environment is possible to set up to 50MB of data, due to the default nginx configuration, as the `run_summary_template` value. The creation of the playbook for itself is not sufficient to trigger an DoS attack in the application, but once this playbook is executed(run) the server  starts to consume a large amount of computing resources, which causes to the server to stop responding to users requests and ultimately leads to server crash.

This attack is even worst because after the application is restarted, its not possible to the user who created the playbook run to finish its execution via the Web Portal, because both the channel created by the playbook run, and the run dedicated management page, don't properly load, showing only a blank screen.

## Steps To Reproduce:
1.  Log in as a normal user in the platform.
2. Grab the user `MMAUTHTOKEN` authentication token.
3. Generate the playbook payload, that contains 50000000(50MB) characters as the `run_summary_template` attribute value. Use F1893243
4. Send the following `POST` request to the `plugins/playbooks/api/v0/playbooks` API endpoint:
```bash
curl -X POST "http://<domain>/plugins/playbooks/api/v0/playbooks" -H 'Content-Type: application/json' -d @payload --cookie "MMAUTHTOKEN=<user-auth-token>" -H "X-CSRF-TOKEN: <csrf-token>"
```
5. Go to the playbooks page, and click on the newly created playbook.
6. Click in the "Run" button and then set an name for the run.
7. After the run is initiated, the server will start to consume an abnormal quantity of computing resources, and crashes after some seconds.
8. The application becomes unavailable for all its users.

## Supporting Material/References:

  * PoC Video
{F1893242}

## Impact

A user can cause a full denial of service attack in the application server, making the application server unavailable to all its users.

</details>

---
*Analysed by Claude on 2026-05-24*
