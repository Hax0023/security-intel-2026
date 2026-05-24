# Denial of Service via Large Numeric Input in Reward Settings

## Metadata
- **Source:** HackerOne
- **Report:** 63865 | https://hackerone.com/reports/63865
- **Submitted:** 2015-05-27
- **Reporter:** ashesh
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Input Validation Flaw
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can cause a denial of service condition by submitting an excessively large numeric value (over 1 million digits) to the base_bounty parameter in the reward settings endpoint. The application fails to validate input size constraints, causing the server to hang for 76+ seconds and ultimately return an Error 522 (Connection Timeout), indicating backend resource exhaustion.

## Attack scenario
1. Attacker authenticates to a HackerOne program they control or have access to
2. Attacker navigates to the program's reward_settings endpoint
3. Attacker crafts a malicious request with base_bounty parameter containing over 1,000,000 digits
4. Attacker sends the POST request with the oversized numeric payload
5. Backend server attempts to process the massive number, consuming excessive CPU/memory
6. Server hangs for 76+ seconds before timing out and returning Error 522 to the attacker and potentially other users

## Root cause
Missing input validation on the base_bounty parameter. The application does not implement reasonable size constraints or type validation before processing user-supplied numeric values, allowing arbitrarily large integers to be submitted and processed by the backend system.

## Attacker mindset
An attacker would recognize that financial/bounty parameters are often processed without strict validation. By submitting an unreasonably large value, they can exploit the backend's computational overhead in parsing, validating, or storing massive numbers. This creates a simple DoS vector requiring minimal sophistication—just a single request can impact service availability for legitimate users.

## Defensive takeaways
- Implement strict input validation on all numeric fields, including maximum value constraints and string length limits before type conversion
- Define reasonable business logic bounds for bounty amounts (e.g., maximum $1,000,000 or similar cap) and enforce validation before backend processing
- Add timeout controls and resource limits on parameter processing to prevent single requests from consuming excessive CPU
- Sanitize and validate input size before attempting to parse large numbers or perform mathematical operations
- Implement rate limiting on the reward_settings endpoint to limit repeated abuse attempts
- Monitor for unusual request patterns, such as extremely large numeric payloads, and flag or reject them automatically
- Use secure integer parsing libraries that have built-in overflow/size protections

## Variant hunting
Test other numeric fields (min_bounty, max_bounty, payout_thresholds) with oversized inputs
Attempt negative or special numeric values (infinity, NaN, scientific notation with large exponents)
Submit extremely long decimal representations in currency fields
Test array/object parameters that accept numeric values with bulk oversized data
Check if other program settings endpoints share the same validation flaw
Attempt floating-point payloads with thousands of decimal places
Test API endpoints vs web interface for differential handling of large numbers

## MITRE ATT&CK
- T1498 - Network Denial of Service
- T1499 - Endpoint Denial of Service
- T1190 - Exploit Public-Facing Application

## Notes
This is a relatively straightforward DoS vulnerability stemming from inadequate input validation. The 76+ second response time suggests the backend is attempting to perform expensive operations on the malicious input (parsing, conversion, storage). The Error 522 indicates a cloudflare/proxy timeout, meaning the origin server exceeded processing time. This type of vulnerability is common in web applications that accept numeric parameters without proper bounds checking. The report lacks specific bounty amount information but demonstrates clear denial of service impact.

## Full report
<details><summary>Expand</summary>

While setting the bounty for the program, if I set the bounty to a large value (over 1,000,000 digits) and send the request the website hangs for about a minute and a half, then pops up an error page saying there is an error on Hackerone's Host end.

Time taken to repsond : 76856 Millisecond = 76.856 Seconds
Error Code: `Error 522`
URL: https://hackerone.com/<program>/reward_settings

The Request and response is attached in this Report.

Vulneurabe paramater `base_bounty`

Request parameters format:

    {"handle":"<program>","errors":{},"offers_bounties":true,"advertise_bounties":true,"base_bounty":"1111....till 1,000,000 digits","hide_bounty_amounts":false,"team_state":"sandboxed","allowed_to_disable_bounties?":true}

</details>

---
*Analysed by Claude on 2026-05-24*
