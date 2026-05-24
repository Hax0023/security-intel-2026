# DoS via Large Console Messages in Mattermost

## Metadata
- **Source:** HackerOne
- **Report:** 1243724 | https://hackerone.com/reports/1243724
- **Submitted:** 2021-06-25
- **Reporter:** thesecuritydev
- **Program:** Mattermost
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A denial of service vulnerability exists in Mattermost where submitting commands larger than 64KB via the `/api/v4/commands/execute` endpoint causes the server to crash when console logging is enabled. The error message logging mechanism attempts to log the entire invalid command without size restrictions, causing buffer overflow or resource exhaustion that renders the server unresponsive until restarted.

## Attack scenario
1. Attacker enables or verifies console logging with DEBUG level is active on target Mattermost server
2. Attacker crafts a POST request to `/api/v4/commands/execute` endpoint with a deliberately malformed/non-existent slash command
3. Attacker replaces the command value with a payload exceeding 64KB (66,000+ characters of repeated data like zeros)
4. Server receives request and determines the command is invalid
5. Server attempts to log the error message including the full payload to the console without size validation
6. The logging operation exceeds buffer limits (~65,535 bytes), causing the server process to crash or hang, making it unresponsive to all users

## Root cause
The application lacks input size validation on the command parameter before logging it to console. When an invalid command is detected, the entire command (including attacker-controlled payload) is included in the error log message without truncation or length checks. Console logging has lower buffer capacity than file logging, making it vulnerable to overflow conditions.

## Attacker mindset
An attacker with basic API knowledge can exploit this to disable a Mattermost instance. The vulnerability is trivial to trigger repeatedly via automation, enabling continuous DoS attacks. The attacker recognizes that debug logging settings are often enabled in production environments and that the logging subsystem doesn't sanitize user input.

## Defensive takeaways
- Implement strict input size limits on all API parameters, enforced at the validation layer before processing
- Truncate or summarize user-controlled data before including in log messages (e.g., log first 100 chars only with ellipsis)
- Apply separate size limits for console vs file logging output, or cap total log entry size regardless of destination
- Implement circuit breakers or rate limiting on error logging to prevent log flooding attacks
- Use structured logging that separates command metadata from payload content, allowing independent size limits
- Add monitoring/alerting for abnormally large log entries or logging exceptions that could indicate attacks
- Disable or restrict DEBUG console logging in production environments by default
- Validate command string length at API layer with clear error messages for oversized inputs

## Variant hunting
Similar pattern in SQL query logging when enabled - attacker could inject large payloads into queries that get logged
Search for other endpoints that accept unbounded string inputs and log them (webhooks, message content, file names, user input fields)
Check if other log levels (INFO, WARN, ERROR) have similar vulnerabilities with different buffer sizes
Test file logging with extremely large payloads to verify claimed immunity - could cause disk exhaustion DoS
Look for similar patterns in audit logging, webhook logging, or third-party integrations
Test with different character encodings (UTF-8 multibyte chars) to potentially exceed byte limits with fewer visible characters)

## MITRE ATT&CK
- T1499.4 - Denial of Service: Application Exhaustion
- T1583.004 - Acquire Infrastructure: Content Delivery Network

## Notes
Report indicates multiple attack vectors exist exploiting the same root cause (including SQL query logging). Console logging appears more vulnerable than file logging due to buffer size differences. Requires knowledge of API endpoints but no authentication bypass needed if endpoint accepts unauthenticated requests. Automation of attacks is trivial, making this particularly dangerous for unmaintained or poorly monitored instances.

## Full report
<details><summary>Expand</summary>

## Summary:
When server console logging is enabled, it's possible to cause a complete denial of service to the server by submitting large text (>64KB) that gets output in the console log. This causes the server to become unavailable for all users.

## Steps To Reproduce:
_I set up my environment following the steps at https://developers.mattermost.com/contribute/server/developer-setup/windows-wsl/_

  1. Create a test server and team.
2. Make sure console logging is enabled in the server settings, with debug level.
  3. Visit the server via Burp Suite for the next step.
 4. Go to a channel, and type some non-existing slash command like`/command` that doesn't exist, and execute it while intercepting the request in Burp Suite.
5. You should get a POST request to `/api/v4/commands/execute` with a JSON body with a `command` value.
6. Send the request to the Repeater in Burp Suite.
7. _The vulnerability comes from the fact that if you type a non-existent command, it will log an error that includes the command you gave. There is no size limit on the command value in the API directly (only in the text box)._
8. Replace the command value with `/000000000000000000000000000000000000000000000000000000000000000...`, where you use more than ~64KB of text (66,000+ characters will do nicely). _You can copy and paste, select all, and copy-paste repeatedly to generate a large text size._
9. If you send the request with this super large payload, the server will see the command is invalid, and try to log the error message to the console. The error message contains the large payload, and **will cause the server to become unresponsive if the log message is over ~64KB** (65,535 bytes) (The size includes the rest of the error message, so the exact payload size required will be a bit less, but 66,000 bytes ensures it will always work without adding too many unnecessary characters).
10. The server will not connect now until you restart with the `make run-server` command, and will be unavailable for all users and all teams.

This only works when CONSOLE logging is enabled (file logging doesn't seem to be affected). And for this attack vector, it is required to have DEBUG logging enabled, but it might be possible to find a vector that works via a different log type.

I will say I also found another vector abusing this same issue via SQL query logging, which I will submit later depending on the status of this report. But obviously, since it requires SQL query logging to be enabled it's not as big of an issue as this one, and it has the same root cause.

## Impact

Complete Denial of Service to all users of a server. It would be trivial to execute a script that automatically sends the payload whenever the server is available, to make sure it continually crashes.

</details>

---
*Analysed by Claude on 2026-05-24*
