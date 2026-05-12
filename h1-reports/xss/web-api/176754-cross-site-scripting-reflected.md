# Reflected Cross-Site Scripting (XSS) in Twitter Cards

## Metadata
- **Source:** HackerOne
- **Report:** 176754 | https://hackerone.com/reports/176754
- **Submitted:** 2016-10-19
- **Reporter:** linkks
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (Reflected), Improper Output Encoding, Unvalidated Parameter Reflection
- **CVEs:** None
- **Category:** web-api

## Summary
The Twitter Cards endpoint (/i/cards/tfw/v1/) fails to properly sanitize the 'scribe_context' query parameter, allowing injection of arbitrary JavaScript code. An attacker can craft malicious URLs that execute JavaScript in the victim's browser by breaking out of the JavaScript string context using </script><script> tags.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the scribe_context parameter: twitter.com/i/cards/tfw/v1/...?scribe_context=l4tqu</script><script>alert(1)</script>o7gyv
2. Attacker shares the URL via social media, email, or embeds it in a website
3. Victim clicks the malicious link or loads a page embedding the URL
4. Browser renders the Twitter Cards endpoint response containing unescaped user input
5. The injected <script> tag is executed in the victim's browser context with their session privileges
6. Attacker can steal cookies, session tokens, perform actions on behalf of the user, or redirect to phishing pages

## Root cause
The application copies the scribe_context parameter value directly into a JavaScript string without proper HTML entity encoding or JavaScript string escaping. The parameter is placed within double quotes in JavaScript code but not escaped, allowing an attacker to break out of the string context using </script><script> sequences.

## Attacker mindset
An attacker would identify this endpoint through reconnaissance of Twitter's card system. They would recognize the pattern of user-controlled input being reflected in responses and test for encoding bypasses by attempting to break out of the JavaScript string context. The low barrier to entry (simple URL manipulation) and high-value target (Twitter users) would make this attractive for phishing or session hijacking campaigns.

## Defensive takeaways
- Always apply context-appropriate output encoding: use JavaScript string escaping for values inserted into JavaScript context
- Implement Content Security Policy (CSP) headers to restrict inline script execution and limit exfiltration vectors
- Use templating engines with automatic contextual auto-escaping rather than manual string concatenation
- Validate and sanitize all user input, including query parameters, regardless of usage context
- Implement a Web Application Firewall (WAF) to detect and block common XSS patterns like </script><script>
- Conduct regular security code reviews focusing on output handling in dynamically generated content
- Perform comprehensive testing of all user-controllable parameters with both encoding variations and tag breakout techniques

## Variant hunting
Look for similar patterns in other Twitter endpoints that accept query parameters and inject them into JavaScript (e.g., analytics parameters, tracking parameters). Test other card-related endpoints, embed parameters, and any widgets that accept context-related parameters. Check for similar issues in:     https://twitter.com/i/web/status endpoints, widget.twitter.com embed functionality, and any other endpoints accepting 'lang', 'theme', 'width', 'height', or analytics parameters.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing
- T1566: Phishing
- T1185: Man in the Browser

## Notes
This is a classic reflected XSS vulnerability in a high-traffic endpoint. The use of </script><script> as a breakout sequence is a standard technique when values are inserted into JavaScript string literals. The presence of authenticated cookies in the request headers indicates the attacker could leverage this to perform authenticated actions. The report lacks specific bounty amount but given Twitter's bug bounty program and the severity, this likely resulted in a significant reward. The vulnerability demonstrates the importance of treating user input as untrusted regardless of the context (even technical parameters like 'scribe_context').

## Full report
<details><summary>Expand</summary>

hi Twitter team

https://twitter.com/i/cards/tfw/v1/788663483873263617?cardname=player&autoplay_disabled=true&forward=true&earned=true&lang=en&card_height=130&scribe_context=l4tqu%3c%2fscript%3e%3cscript%3ealert(1)%3c%2fscript%3eo7gyv

The value of the scribe_context request parameter is copied into a JavaScript string which is encapsulated in double quotation marks. The payload l4tqu</script><script>alert(1)</script>o7gyv was submitted in the scribe_context parameter. This input was echoed unmodified in the application's response.

GET /i/cards/tfw/v1/788663483873263617?cardname=player&autoplay_disabled=true&forward=true&earned=true&lang=en&card_height=130&scribe_context=l4tqu%3c%2fscript%3e%3cscript%3ealert(1)%3c%2fscript%3eo7gyv HTTP/1.1
Host: twitter.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://twitter.com/
Cookie: guest_id=v1%3A146255384359384655; _ga=GA1.2.178796086.1467670836; kdt=qU1PQNfIb0sNg6vhmvMkEIe1zla3g5clz7cCgLds; remember_checked_on=1; twid="u=4092731777"; auth_token=b4a4eb0642ec5579bf2f58a98d1eca87ad9552a7; moments_profile_moments_nav_tooltip_self=true; eu_cn=1; mp_c3de24deb6a3f73fba73a616bb625130_mixpanel=%7B%22distinct_id%22%3A%20%22ce74a9d62a1e8a572a472095b248ab3f4167e8341d603b9d689bf497fca88101%22%2C%22isAdmin%22%3A%20false%2C%22isAccountSpending%22%3A%20false%2C%22serviceLevel%22%3A%20%22null%22%2C%22goalBased%22%3A%20true%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fads.twitter.com%2Fnew_campaign%2F18ce54aqb54%2Fstart%22%2C%22%24initial_referring_domain%22%3A%20%22ads.twitter.com%22%7D; mbox=check#true#1476741932|session#dd4f8eba87774a26834c0ce387200a8a#1476743732|PC#dd4f8eba87774a26834c0ce387200a8a.26_5#1477951472; SSESS3c8b2bbd5af1180dab341c61a9900084=krekirm43u81j7g7bqbt9uij76; lang=it; moments_user_moment_profile_create_moment_tooltip=true; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCH3hdNxXAToMY3NyZl9p%250AZCIlZWRlZWQyYzFhYjMwYWYwOTJjMDEwZGM0NzM0NDIxMTk6B2lkIiU3MGQ4%250AMWY5MDI3Y2RjZWQyYmY3OGI2NTEwZTQxOGVkZQ%253D%253D--c5e4969a1a90f82f0db9ffa1991f7a2da912bfba; lang=en
Connection: close



</details>

---
*Analysed by Claude on 2026-05-12*
