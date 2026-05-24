# Denial of Service via Malformed URL Parameter on twitter.com & mobile.twitter.com

## Metadata
- **Source:** HackerOne
- **Report:** 903740 | https://hackerone.com/reports/903740
- **Submitted:** 2020-06-20
- **Reporter:** try_to_hac
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service, Client-Side DoS, Browser Crash, Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
A browser-based DoS vulnerability exists on twitter.com and mobile.twitter.com where a crafted URL with a malformed port parameter causes the browser to freeze or crash when the page is viewed. The vulnerability affects Chrome on desktop and Firefox/Edge on mobile, allowing attackers to target any user or popular hashtag by sharing a malicious link.

## Attack scenario
1. Attacker crafts a malicious URL: http://twitter.com:627732462 (or similar with arbitrary port numbers)
2. Attacker shares the link on Twitter, in DMs, or embeds it in web pages targeting Twitter users
3. Victim clicks the link or navigates to a tweet/message containing this URL
4. Browser attempts to parse the malformed port parameter, triggering excessive resource consumption
5. Victim's browser becomes unresponsive and freezes or crashes, preventing access to Twitter
6. If targeting a popular hashtag or account, widespread users could be affected simultaneously

## Root cause
Improper input validation and parsing of URL port parameters in the Twitter web application. The browser's URL parsing logic combined with Twitter's page rendering fails to gracefully handle invalid or excessively large port numbers, leading to resource exhaustion or infinite loops during DOM manipulation or rendering.

## Attacker mindset
An attacker would recognize this as a low-effort, high-impact vulnerability. By poisoning URLs shared publicly (tweets, hashtags, DMs), they could cause widespread browser crashes affecting numerous users simultaneously. The ability to target specific accounts or trending topics makes this attractive for harassment, disruption, or competitive sabotage.

## Defensive takeaways
- Implement strict server-side and client-side URL validation before processing port parameters
- Sanitize and validate all URL components before rendering or parsing
- Add upper bounds checks on port numbers (valid range: 0-65535)
- Implement timeouts for page load operations to prevent infinite loops
- Use Content Security Policy (CSP) to restrict resource loading from suspicious sources
- Test edge cases and malformed URLs during development and QA
- Monitor for unusual URL patterns that might indicate DoS attempts
- Implement graceful error handling for invalid URLs instead of allowing browser crashes
- Consider using URL parsing libraries with robust validation rather than custom implementations

## Variant hunting
Test with other invalid port numbers (negative values, extremely large numbers, non-numeric)
Test with special characters in port parameter (%00, null bytes, Unicode characters)
Test with multiple port parameters in the same URL
Test with port parameter combined with other invalid URL components (fragments, query strings)
Test on other Twitter-related endpoints (api.twitter.com, cards.twitter.com, etc.)
Test with URL encoding variations of the payload
Check if other URL path parameters exhibit similar parsing vulnerabilities
Test if the vulnerability applies to Twitter embedded iframes or widgets

## MITRE ATT&CK
- T1190
- T1561
- T1499

## Notes
The vulnerability demonstrates browser-specific behavior (works on Chrome/Firefox/Edge differently), suggesting the issue may lie in how Twitter's frontend code interacts with browser APIs. The reporter's observation that it doesn't affect the mobile app indicates the vulnerability is specific to web rendering. A previous similar report was reportedly submitted, suggesting this may be a recurring issue with URL parsing logic. The public impact is high given Twitter's user base and the ease of distributing malicious URLs through the platform itself.

## Full report
<details><summary>Expand</summary>

Hi Team,

Detail:
I found a DoS that works on **twitter.com** and **mobile.twitter.com**, but it doesn't work on the mobile app. The user only needs to view the message or tweet in order to be exposed to this DoS. As far as I can remember, a report similar to this report has been sent to you before, but I think it's no longer public.

Note:
- If the user tries to view the DoS message or tweet from twitter.com, DoS will definitely work, but if it enters from Chrome and displays this DoS from **mobil.twitter.com**, this DoS will not work. This works without exception in Edge and Firefox.

- I think this is a browser-based DoS, so I think it won't work on Desktop Twitter. So I didn't test it.

- I did my tests on my own accounts. I haven't done a test for any tag. But I'm sure it will work.


PoC & Steps:
`http://twitter.com:627732462`



{F875527}

## Impact

An attacker could apply this DoS to any Twitter account or popular tag. It prevents a large audience or target user from accessing Twitter from the browser.

</details>

---
*Analysed by Claude on 2026-05-24*
