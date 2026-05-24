# Missing Back-end User Input Validation Leading to Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 361337 | https://hackerone.com/reports/361337
- **Submitted:** 2018-06-03
- **Reporter:** zuh4n
- **Program:** Liberapay
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Improper Input Validation, Denial of Service (DoS), Missing Server-Side Validation
- **CVEs:** None
- **Category:** business-logic

## Summary
The Liberapay application enforces maximum length validation (64 characters) only on the client-side for the public_name field, but lacks corresponding back-end validation. An attacker can bypass the front-end constraint by modifying the DOM and submitting extremely large payloads (10,000+ characters), causing significant server processing delays and potential resource exhaustion.

## Attack scenario
1. Attacker identifies the public_name input field on the Profile page with a 64-character client-side limit
2. Attacker uses browser developer tools to modify the HTML maxlength attribute from 64 to a larger value (e.g., 15000)
3. Attacker enters or pastes a 15,000-character string into the modified input field
4. Attacker submits the POST request with the oversized payload to the back-end
5. Server processes the request without validation, causing response time to increase from 150-200ms to several seconds
6. Multiple concurrent requests with large payloads can exhaust server resources, causing denial of service for legitimate users

## Root cause
Client-side input validation was implemented but not replicated on the server-side. The application relies solely on the maxlength HTML attribute for constraint enforcement, assuming users cannot modify it. The back-end accepts and processes arbitrarily large payloads without length checks, leading to computational overhead.

## Attacker mindset
The attacker approached this as a security researcher identifying business logic weaknesses that could be exploited for resource exhaustion. They methodically tested various payload sizes to demonstrate the performance degradation curve, then extrapolated the findings to show how this could enable a DDoS attack with minimal bot resources.

## Defensive takeaways
- Always implement server-side input validation independent of client-side constraints
- Define and enforce strict length limits at the API/back-end layer before processing user input
- Implement request size limits (Content-Length headers) to prevent oversized payloads from being processed
- Add rate limiting and request throttling to mitigate DoS attacks exploiting validation gaps
- Monitor response times and server resource consumption for anomalies indicating potential attack patterns
- Use input sanitization and validation libraries consistently across all endpoints
- Test security controls by bypassing client-side restrictions (browser DevTools, proxies) during code review

## Variant hunting
Check other profile fields (username, bio, description) for similar client-only validation patterns
Test other user-editable fields across the application (settings, preferences, comments) for back-end validation gaps
Examine file upload endpoints for missing size validation despite client-side restrictions
Search for other string/text input fields with maxlength attributes that may lack server-side enforcement
Test POST/PUT endpoints directly via API without browser to bypass all client-side controls
Investigate if other applications in the same ecosystem share similar validation patterns

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
While classified as a DoS vulnerability, the reporter emphasizes this is a business logic weakness rather than a critical security flaw. The impact depends on server architecture and resource constraints. The fix is straightforward: implement server-side validation matching or stricter than client-side limits. This is a canonical example of why front-end validation should never be trusted as a security control.

## Full report
<details><summary>Expand</summary>

Hello Team,

Usually such kind of reports are out of scope, however I still would like to report you the business logic weakness that should be eliminated, at least from my point of view. Due to missing user input validation it is can lead to application unavailability.

**_Details:_**
During brief review of Liberapay application I have noticed that under 'Profile' page it's allowed to change username + name data. The first thing that caught my eye - "Name (optional) Maximum length is 64 `<input name="public_name" class="form-control" value="zzzzz" maxlength="64" placeholder="Name">`". It means that application has front-end user input validation, but what about back-end?

In case when the user exceeds the specified limit, the application server will return a response with the following status: 400 Bad Request + entire string that was inserted by user. Having this information in mind it was decided to check how the application server will handle the POST request that contains 100, 500, 10000, ... public_name value length.

In my case I simply changed the `maxlength` value directly at the DOM.

**_PoC:_**
The usual response time for valid request is about ~150-200ms (65 public_name value length)
{F304705}

This one for 500 public_name value length
{F304706}

This one for 10000 public_name value length
{F304707}

This one for 15000 public_name value length
{F304708}

**_Remediation:_**
- The recommendation here is simple, before sending an actual processing request - the application need to double check the content-length at back end. _All_ user input input should be validated at back-end.

## Impact

This surface is a good base for a planning a DDoS attack Liberapay with a small bot-net asset, i.e. small number of machines may cause a consuming of server's RAM.

</details>

---
*Analysed by Claude on 2026-05-24*
