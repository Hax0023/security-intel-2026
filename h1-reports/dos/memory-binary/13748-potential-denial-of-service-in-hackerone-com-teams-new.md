# Denial of Service via Large Bounty Value in Team Creation

## Metadata
- **Source:** HackerOne
- **Report:** 13748 | https://hackerone.com/reports/13748
- **Submitted:** 2014-05-28
- **Reporter:** idps
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Denial of Service (DoS), Algorithmic Complexity, Input Validation Weakness
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can cause a denial of service condition on the team creation endpoint by submitting an excessively large numeric value (over 1,000,000 digits) in the bounty field. The application lacks proper input validation and timeout mechanisms, causing the server to hang for approximately 90 seconds before returning an error.

## Attack scenario
1. Attacker navigates to hackerone.com/teams/new
2. Attacker fills in required team creation fields
3. Attacker enters a bounty value with over 1,000,000 digits (e.g., a string of zeros)
4. Attacker submits the form/request
5. Server attempts to process/validate the extremely large number, consuming significant CPU/memory
6. Application becomes unresponsive for ~90 seconds, then displays generic error page

## Root cause
Missing or insufficient input validation on the bounty field that fails to enforce reasonable numeric limits (max value, max digit length) before backend processing. Server-side logic attempts to parse/process the large number without proper bounds checking or timeout constraints.

## Attacker mindset
Resource exhaustion through arithmetic/parsing operations. Attacker discovers that unbounded numeric input triggers expensive computational operations, enabling trivial DoS with a single request.

## Defensive takeaways
- Implement strict input validation on numeric fields with enforced maximum values and digit lengths before backend processing
- Add request timeout mechanisms to prevent long-running operations from blocking server threads
- Validate bounty amounts against business logic constraints (e.g., 0 to $1,000,000 range)
- Implement rate limiting on form submissions to mitigate repeated DoS attempts
- Use secure numeric parsing libraries with overflow/bounds protection
- Add server-side request timeouts and circuit breakers for expensive operations
- Monitor for patterns of malformed input submissions

## Variant hunting
Test other numeric input fields (prize amounts, user IDs, amounts) with extremely large values
Try negative numbers with extreme magnitude
Test scientific notation (1e999999) to bypass length checks
Attempt similar payloads on other form endpoints (project creation, payment setup)
Test with decimal/float precision abuse (1.1111...repeated millions of times)
Check for similar issues in API endpoints vs web UI

## MITRE ATT&CK
- T1498 - Network Denial of Service
- T1499 - Endpoint Denial of Service
- T1190 - Exploit Public-Facing Application

## Notes
This is a simple but effective DoS vector requiring no authentication bypass or complex exploitation. The ~90 second hang time suggests the server may be attempting BigInteger arithmetic or string-to-number conversion on the massive input. This type of vulnerability is common in applications that don't validate numeric ranges before processing. The fix is straightforward: client-side and server-side validation of reasonable bounds.

## Full report
<details><summary>Expand</summary>

While creating a new team, if I set the bounty to a large value (over 1,000,000 digits) and send the request the website hangs for about a minute and a half, then pops up an error page saying there is an error on your end.

</details>

---
*Analysed by Claude on 2026-05-24*
