# Denial of Service in Report View via Comment Flooding

## Metadata
- **Source:** HackerOne
- **Report:** 140720 | https://hackerone.com/reports/140720
- **Submitted:** 2016-05-24
- **Reporter:** apok
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Server-Side Performance Issue
- **CVEs:** None
- **Category:** memory-binary

## Summary
The report view functionality loads all comments without pagination or limits, allowing attackers to cause server timeouts by posting hundreds of comments or large payloads to a single report. This prevents legitimate users from accessing reports and causes unnecessary server load through request amplification attacks.

## Attack scenario
1. Attacker identifies a report accessible to them on HackerOne
2. Attacker crafts and submits 450+ comments with test data or large high-entropy payloads to the same report
3. When a legitimate user attempts to view the report, the server attempts to load all comments into memory simultaneously
4. Server resource exhaustion occurs due to processing and serializing hundreds of comments without pagination
5. Server returns HTTP 524 (Origin Time-Out) error after 60 seconds, denying access to legitimate users
6. Attacker can repeat this pattern across multiple reports to amplify the DoS impact

## Root cause
The report view endpoint lacks pagination, comment count limits, or lazy-loading mechanisms. All comments (both user-generated and system-generated) are loaded and rendered in a single response without server-side resource constraints or client-side rendering optimizations.

## Attacker mindset
An attacker seeks to disrupt collaboration on vulnerability reports by making them inaccessible. The attack is low-effort (just posting comments), requires minimal technical sophistication, and can be weaponized across multiple reports simultaneously. The attacker recognizes that even rate-limiting would only delay, not prevent, the attack.

## Defensive takeaways
- Implement pagination or lazy-loading for comments (load N comments initially, provide 'load more' button)
- Set hard limits on comment count per report or maximum comment size
- Implement server-side timeouts for response generation with graceful fallback to paginated view
- Add request throttling and rate-limiting per user per report
- Monitor for abnormal comment activity patterns (many comments in short timeframe) and trigger CAPTCHA verification
- Implement database query optimization and caching for frequently accessed reports
- Consider implementing asynchronous comment loading with streaming responses
- Set maximum request payload size and response generation time budgets

## Variant hunting
Check if other resource listing views (activity feeds, comment threads on other objects) have similar pagination issues
Investigate whether comment size limits exist and if they can be bypassed
Test if system-generated comments (e.g., status updates) can also be created/exploited by attackers
Verify if the issue affects API endpoints differently than web interface
Check if the vulnerability applies to private vs public reports differently
Test attachment/media handling in comments as potential large-payload vectors

## MITRE ATT&CK
- T1498.001 - Flood with traffic (HTTP floods)
- T1499.4 - Protocol exhaustion
- T1561 - Disk wipe

## Notes
Reporter demonstrated responsible disclosure by testing on sandboxed team and provided three specific report IDs with different exploitation methods. Reporter correctly identified that rate-limiting alone is insufficient as a mitigation. The 524 gateway timeout is indicative of backend processing timeout rather than network timeout. This is a classic application-level DoS rather than infrastructure-level attack, making it more cost-effective for attackers while being easily preventable through proper pagination architecture.

## Full report
<details><summary>Expand</summary>

Hello Team!
First of all thank you for acknowledging my feature request, I know it will help a lot of users.

Description:
==========
I just wanted to report a potential vulnerability on the report view functionality.
For obvious reasons I'm using my sandboxed team on an alternate account to test it, but I'm pretty sure it can be still exploited on non-sandboxed teams.
I'm guessing that one of the main differences between sandboxed and non-sandboxed teams is that non-sandboxed have rate-limiting, but this wouldn't be a successfuly way of preventing this potential attack, but just a way of slowing it down, but not for long.

Basically the problem relies in that the view report functionality, tries to load every comment, either man made or system made, which, given enough comments, overloads the server and sends a 524 Origin Time-Out.

I was able to get this error by sending around 450 "test" messages on the same report, or by sending a few big messages. You can see it by yourself on reports 137508, 132450 and 138662 (Three different ways of exploiting this vulnerability)

Why is this a vulnerability?
======================
A malicious individual could very well leverage this vulnerability to prevent a legitimate user from accessing the report. In addition, it causes an unnecessary load on Hackerone's servers, since it can be used as a request amplification attack, by issuing a large amount of requests to the report, once it's filled with random info. Also, even though compression techniques can be used to reduce the amount of data transferred, this can by greatly bypassed by issuing high-entropy data (random), which would hinder the compression mechanisms.

How to fix this?
=============
Several ideas come to mind:
- Limit the amount of consecutive comments that can be seen at once in a report, providing a "see more" button which will at most overload the client interface, not the server.
- Limit the amount of data sent per comment, providing a "see more" button which loads the following chunk of data.
- When a high amount of comment load is detected (either because of a high amount of comments or big comments being sent), perform a CAPTCHA check.

As you can see on the following screenshot, the report failed to load: {F95556}

This is the request made by the Ajax controller: {F95557}

This is the response sent by the server, showing a gateway error after 60 seconds: {F95558}

</details>

---
*Analysed by Claude on 2026-05-24*
