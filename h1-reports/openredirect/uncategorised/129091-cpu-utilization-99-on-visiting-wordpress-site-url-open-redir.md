# CPU Utilization 99% DoS via Invalid Post ID & Open Redirect Vulnerability in WordPress.com

## Metadata
- **Source:** HackerOne
- **Report:** 129091 | https://hackerone.com/reports/129091
- **Submitted:** 2016-04-07
- **Reporter:** csanuragjain
- **Program:** WordPress.com (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service (CPU Exhaustion), Open Redirect, Input Validation Failure, Infinite Loop
- **CVEs:** None
- **Category:** uncategorised

## Summary
WordPress.com suffers from a Denial of Service vulnerability where extremely large post IDs cause unhandled exceptions, triggering unlimited pixel tracking requests that consume 99% CPU resources. Additionally, the wp-login.php redirect_to parameter fails to validate redirect destinations, enabling open redirects to arbitrary external sites.

## Attack scenario
1. Attacker crafts malicious URLs with astronomically large post IDs (e.g., 20000000000000000000000...) and sends them to victim users via social engineering or phishing
2. Victim clicks the link appearing legitimate as it originates from wordpress.com domain
3. WordPress backend attempts to process the oversized post ID which exceeds variable capacity, triggering an exception
4. Exception causes a loop in pixel tracking logic that continuously sends requests to pixel.wp.com/g.gif without termination
5. Browser processes unlimited requests, consuming 99% CPU and rendering system unresponsive
6. For open redirect: Attacker includes redirect_to parameter pointing to attacker-controlled or malicious site in login URL; victim logs in and is silently redirected to external site, enabling credential harvesting or malware distribution

## Root cause
Insufficient input validation on post ID parameters allowing integer overflow/exception conditions to trigger exception handlers that enter infinite loops. Lack of whitelist validation on redirect_to parameter permitting arbitrary external domain redirects.

## Attacker mindset
Opportunistic attacker seeking to degrade user experience and potentially combine open redirect with phishing. Likely discovered through fuzzing with large numbers and parameter manipulation during reconnaissance.

## Defensive takeaways
- Implement strict input validation with bounds checking on all numeric ID parameters before processing
- Use try-catch blocks with proper exception handling rather than allowing exceptions to propagate into pixel tracking loops
- Implement whitelist-based validation for redirect_to parameters, only allowing internal WordPress.com domains
- Add rate limiting and request throttling to pixel.wp.com to prevent request floods
- Implement client-side timeout mechanisms for tracking pixel requests to prevent infinite request loops
- Add server-side monitoring for anomalous tracking request patterns from single sessions
- Use proper type casting and overflow detection for integer parameters
- Implement Content Security Policy headers to restrict redirect targets

## Variant hunting
Test all user-facing ID parameters (post, page, user, comment IDs) with: extremely large numbers, negative numbers, non-numeric strings, special characters. Test all redirect parameters (return, redirect_to, next, goto, continue) for external domain validation bypasses using URL encoding, protocol-relative URLs, and data URIs.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1561 - Disk Wipe (DoS impact)
- T1499 - Endpoint Denial of Service
- T1598 - Phishing (open redirect variant for credential harvesting)

## Notes
Report demonstrates compound vulnerability where input validation failure cascades into two distinct issues. The pixel tracking loop is particularly severe as it's an unintended consequence of exception handling. Open redirect severity elevated by combination with legitimate login flow increasing victim click-through rates. Report quality could be improved with: specific WordPress.com version, reproduction timeframes, affected user percentages, and whether vulnerability persists after reported issues.

## Full report
<details><summary>Expand</summary>

**Working POC for making CPU 99% for wordpress user**
+ Login to wordpress account
+ Visit any of the below url's which are sent by attacker to victim (since these are wordpress url so victim will accept & open)
1.https://wordpress.com/post/20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
2.https://wordpress.com/design/1000000000000000000000
3.https://wordpress.com/pages/anurag.wordpress.com/-10000000000000000000000000000000000000000000000
+ Check your CPU usage in task manager. It would go to 99% as shown in attached.
+ This happens since these pages continues to send unlimited requests to https://pixel.wp.com/g.gif?v=wpcom-no-pv&x_newdash_pageviews=route&t=0.1642450245826501
+ Unlimited request are send since I think the variable holding the Post id cannot hold a value as long as 20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 which throws an exception.
+ **Problem:** User CPU goes 99% causing the browser to go very very slow & unresponsive. Negative impact on customer.

**Working POC for open redirect**
+ Access wordpress using url https://wordpress.com/wp-login.php?redirect_to=https%3A%2F%2Fgoogle.com%2Fsearch?q=myFakeSite&reauth=1
+ After login you will be redirected to https://www.google.co.in/search?q=myFakeSite&gws_rd=cr&ei=WLYGV8fUHIq8uATj56uIBA which is incorrect. Wordpress should not allow redirecting to external websites like google,yahoo.
+ **Problem:** In future if there is any bug in these external site then this open redirect from wordpress could cause harm to users.

</details>

---
*Analysed by Claude on 2026-05-24*
