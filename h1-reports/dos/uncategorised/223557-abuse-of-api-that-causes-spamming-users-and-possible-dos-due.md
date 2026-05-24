# Missing Rate Limiting on Email API Endpoint Enables Spam and DoS

## Metadata
- **Source:** HackerOne
- **Report:** 223557 | https://hackerone.com/reports/223557
- **Submitted:** 2017-04-24
- **Reporter:** khalidamin
- **Program:** Weblate
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Missing Rate Limiting, Denial of Service, API Abuse, Spam
- **CVEs:** None
- **Category:** uncategorised

## Summary
The POST /accounts/email/ endpoint on demo.weblate.org lacks rate limiting protections, allowing attackers to spam arbitrary email addresses with unlimited requests. This vulnerability enables both user harassment through email flooding and potential service degradation through resource exhaustion.

## Attack scenario
1. Attacker identifies the unprotected POST /accounts/email/ endpoint on demo.weblate.org
2. Attacker crafts automated requests with victim email addresses and arbitrary content
3. Attacker sends hundreds or thousands of requests in rapid succession without authentication checks
4. Victim receives flood of unwanted emails from the Weblate service
5. Attacker can target multiple victims simultaneously or exhaust server resources
6. Service experiences degradation or unavailability due to email sending workload

## Root cause
The email endpoint was implemented without rate limiting middleware or request throttling mechanisms, allowing unauthenticated or authenticated users to submit unlimited requests without delay penalties.

## Attacker mindset
Opportunistic attacker seeking to cause harassment, disruption, or service abuse by exploiting lack of protective controls on publicly exposed endpoints. Focus on amplification attacks with minimal effort.

## Defensive takeaways
- Implement per-IP and per-user rate limiting on all user-facing API endpoints
- Apply stricter controls to endpoints that trigger external actions (email sending, notifications)
- Use CAPTCHA or additional verification on sensitive operations
- Implement request throttling with exponential backoff for repeated violations
- Monitor and alert on abnormal request patterns and email sending volumes
- Require authentication for endpoints that perform user-impacting actions
- Implement per-domain/per-email recipient rate limits to prevent targeted harassment
- Log all requests to email endpoints for forensic analysis and abuse detection

## Variant hunting
Search for similar unprotected endpoints performing resource-intensive operations: password reset endpoints, notification/alert APIs, webhook triggers, file processing endpoints, database query endpoints, and any POST/PUT operations lacking throttling controls. Check for inconsistent rate limiting across API surface.

## MITRE ATT&CK
- T1190
- T1499
- T1566

## Notes
This is a classic API abuse vulnerability commonly found in production systems. The demo environment increases severity as it represents the actual production codebase. Rate limiting should be layered (application-level, WAF, load balancer) rather than relying on single implementation point. Email-specific rate limits differ from general API rate limits due to external service costs and recipient impact.

## Full report
<details><summary>Expand</summary>

##Summary:
In your sub-domain: http://demo.weblate.org , another endpoint doesn't have any rate limit on it to prevent spamming you by posting a lot of questions.

##Description:
Spamming and Possible DOS is being possible due to missing rate limit on this endpoint.

**Request**
POST /accounts/email/ HTTP/1.1
Host: demo.weblate.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://demo.weblate.org/
Cookie: XXX
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 126

csrfmiddlewaretoken=&email=victim_email&content=



</details>

---
*Analysed by Claude on 2026-05-24*
