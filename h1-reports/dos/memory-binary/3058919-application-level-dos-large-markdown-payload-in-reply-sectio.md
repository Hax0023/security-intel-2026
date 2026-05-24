# Application Level DoS - Large Markdown Payload in Reply Section Leading to Resource Exhaustion

## Metadata
- **Source:** HackerOne
- **Report:** 3058919 | https://hackerone.com/reports/3058919
- **Submitted:** 2025-03-25
- **Reporter:** theteatoast
- **Program:** Discourse (try.discourse.org)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Insufficient Input Validation, Application-Level DoS
- **CVEs:** None
- **Category:** memory-binary

## Summary
An application-level DoS vulnerability exists in Discourse's reply section where submitting an excessively large markdown payload (~800,000 characters) causes the server to hang for 30 seconds before returning a 502 error. This vulnerability can be exploited through automated parallel requests to exhaust backend resources and cause widespread service disruption.

## Attack scenario
1. Attacker authenticates with valid credentials on the target Discourse instance
2. Attacker navigates to a reply section and crafts an HTTP POST request containing ~800,000 character markdown payload
3. Attacker intercepts the request and submits it, observing 30-second server response time followed by 502 error
4. Attacker automates the attack using tools like Burp Intruder, Python requests library, or custom botnet scripts
5. Attacker sends multiple parallel requests to overwhelm backend markdown processing service
6. Server resources become exhausted, causing legitimate users to experience timeouts and service unavailability

## Root cause
Lack of input validation and size restrictions on markdown payload processing in the reply endpoint combined with inefficient or unoptimized markdown rendering that consumes excessive CPU/memory for large payloads without early rejection mechanisms.

## Attacker mindset
An attacker recognizes that markdown processing is computationally expensive and that the application lacks input validation controls. By discovering the threshold where processing becomes prohibitively slow, they can craft automated attacks to exhaust server resources without requiring privileged access, merely valid credentials.

## Defensive takeaways
- Implement strict input length limits on user-submitted content (e.g., max 10,000-50,000 characters for replies) validated server-side
- Add request rate limiting and throttling per user/IP address to prevent automated parallel submission attacks
- Implement early rejection of oversized payloads before passing to markdown processing engine
- Add timeouts to markdown processing with graceful degradation (e.g., return plaintext if rendering takes >5 seconds)
- Monitor and alert on unusual processing times or resource spikes indicating potential DoS attacks
- Use async/queue-based processing for markdown rendering to prevent blocking HTTP handlers
- Implement CAPTCHA or additional validation for large payload submissions from new/low-reputation users

## Variant hunting
Similar vulnerabilities may exist in other user-input processing endpoints (comments, posts, direct messages), other markup formats (HTML, LaTeX, code blocks), file upload handlers with large file size limits, and search functionality with complex query payloads. Test endpoints accepting rich text, form submissions with unlimited field sizes, and any backend service that performs compute-intensive processing on user input.

## MITRE ATT&CK
- T1499.4 - Application Layer Distributed Denial of Service
- T1190 - Exploit Public-Facing Application
- T1499 - Endpoint Denial of Service

## Notes
The vulnerability requires authentication, reducing immediate blast radius but still exploitable by compromised accounts or insider threats. The 30-second response time indicates the backend is processing the payload rather than rejecting it early. The 502 error suggests a reverse proxy or load balancer timeout, implying the vulnerability likely affects upstream backend services as well. Video PoC and payload payload.txt link provided in original report substantiate the claim.

## Full report
<details><summary>Expand</summary>

## Summary:

An application level Denial of Service (DoS) vulnerability was identified in the reply section on https://try.discourse.org

By submitting an excessively large markup payload (~800,000 characters), the server takes 30 seconds to respond before returning an HTTP/2 502 Bad Gateway error. This indicates potential resource exhaustion or backend service failure, which could be exploited to degrade or disrupt website availability.

## Attack Scenario:

If an attacker automates this request using multiple parallel requests (e.g., via Burp Intruder, Python scripts, or a botnet), it can cause severe resource exhaustion.

The backend service will be overwhelmed, leading to widespread downtime, preventing legitimate users from accessing the forum.

## Steps To Reproduce:
1. Login with valid credentials on `https://try.discourse.org`

2. Navigate to the default discobot grettings message.
{F4182648}

3. Reply the message with the following paylod while intercepting the request: `https://github.com/theteatoast/theteatoast.github.io/blob/main/payload.txt`
{F4182646}

4. Repeat the request and observe that the server takes ~30 seconds before responding with 502.
{F4182647}

##Video POC:
{F4182629}

##Suggested Mitigation:

1. Implement input length restrictions on replies to prevent excessive payload sizes.

2. Introduce rate-limiting and request throttling to mitigate automated abuse.

3. Optimize backend request handling to reject large payloads early before processing.

##Note:

This Proof of Concept (PoC) was performed solely for demonstration purposes, with no intent to harm the system. I ensured minimal impact while testing.

## Impact

1. Attackers can exploit this to cause severe delays and temporary or prolonged service disruption.

2. The lack of input validation allows attackers to send multiple large requests in parallel, leading to backend resource exhaustion.

3. If automated, this attack could render the forum completely inaccessible.

</details>

---
*Analysed by Claude on 2026-05-24*
