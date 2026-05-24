# Missing Rate Limiting on Contact Form Endpoint Enables Spam and DoS

## Metadata
- **Source:** HackerOne
- **Report:** 223542 | https://hackerone.com/reports/223542
- **Submitted:** 2017-04-24
- **Reporter:** khalidamin
- **Program:** Weblate
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Missing Rate Limiting, Denial of Service (DoS), Spam/Abuse of Functionality
- **CVEs:** None
- **Category:** uncategorised

## Summary
The contact form endpoint at POST /contact/ on demo.weblate.org lacks rate limiting controls, allowing attackers to submit unlimited requests and spam the application with contact form submissions. This can result in email bombing to the application operators and potential service degradation through resource exhaustion.

## Attack scenario
1. Attacker visits the contact form at https://demo.weblate.org/contact/?t=reg
2. Attacker fills out the form with arbitrary data and intercepts the POST /contact/ request using a proxy tool like Burp Suite
3. Attacker captures the request including CSRF token and form parameters
4. Attacker uses Burp Intruder or similar tool to rapidly replay the request hundreds or thousands of times without delays
5. Server processes each request without validation checks and generates outbound emails for each submission
6. Application operators are flooded with spam emails and backend email systems become overwhelmed, potentially causing DoS

## Root cause
The contact form endpoint was implemented without rate limiting controls, allowing an unauthenticated attacker to submit unlimited requests from the same source. No per-IP, per-email, or per-session throttling mechanism was implemented to protect the endpoint.

## Attacker mindset
An attacker with basic technical skills (ability to use Burp Suite) can discover and exploit this vulnerability with minimal effort. The attacker may be motivated by causing disruption/annoyance to the application operators, testing DoS capabilities, or using it as part of a larger attack campaign. The low barrier to exploitation makes this attractive for script kiddies and automated scanning.

## Defensive takeaways
- Implement rate limiting on all user-facing endpoints, especially those that trigger server-side actions like email sending
- Use multiple rate limiting strategies: per-IP address, per-email address, and per-session tokens
- Consider implementing CAPTCHA or email verification challenges on forms to add friction against automated abuse
- Monitor and alert on abnormal contact form submission patterns (e.g., sudden spike in requests from single IP/email)
- Implement exponential backoff or temporary IP blocking after threshold violations
- Use established rate limiting libraries/middleware appropriate to the framework (Django has django-ratelimit)
- Throttle email sending operations to prevent backend email system overwhelm
- Log all form submissions with source IP and email for forensic analysis and abuse tracking

## Variant hunting
Check other user-submitted form endpoints (newsletter signup, feedback, support tickets) for identical rate limiting gaps
Test authenticated endpoints that perform server actions (file uploads, API calls, exports) for rate limiting
Examine API endpoints that send notifications or emails for missing rate limits
Look for password reset, account recovery, or email verification endpoints that could be abused for spam/enumeration
Review any endpoint that triggers external communications (webhooks, notifications, emails) for rate limiting controls
Test for bypass techniques like X-Forwarded-For header manipulation, distributed requests, or timing-based evasion

## MITRE ATT&CK
- T1190
- T1499
- T1499.1
- T1499.4

## Notes
This is a straightforward missing control vulnerability rather than a complex logic flaw. The report demonstrates clear exploitation steps and practical impact. The suggested fix in the report mentions CSRF tokens and account banning, but the core issue is absence of any rate limiting mechanism. CSRF tokens alone would not prevent this attack since the attacker can obtain valid tokens for each request. The vulnerability affects availability and reputation rather than confidentiality or integrity, which is why severity is Medium rather than High. This type of issue is common in web applications and should be caught during secure code review or security testing phases.

## Full report
<details><summary>Expand</summary>

##Summary:
In your sub-domain: https://demo.weblate.org/ , there's an endpoint that doesn't have any rate limit on it to prevent spamming you by filling the contact you form multiple times to bomb you with tons of emails.

##Description:
Spamming and Possible DOS is being possible due to missing rate limit on this endpoint.

**Request**
POST /contact/ HTTP/1.1
Host: demo.weblate.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://demo.weblate.org/
Cookie:XXX
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 334

csrfmiddlewaretoken=XXX&subject=&name=&email=asd%40yahoo.com&message=&content=

**Suggested Fix**
Implement additional checking per API request such as a unique token or identifier that changes per request to prevent mass spamming, additional Rate limiting measures can be implemented such as IP blacklisting, or account banning if a certain amount of requests are made.

##Steps To Reproduce:
1- Visit https://demo.weblate.org/contact/?t=reg
2- Fill the form, send it and intercept the request
3- Using burp intruder mass replay the request.

Thank you.

</details>

---
*Analysed by Claude on 2026-05-24*
