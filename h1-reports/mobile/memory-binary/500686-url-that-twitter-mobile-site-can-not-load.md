# Invalid Hex Characters in URL Parameter Causes Mobile Site Crash

## Metadata
- **Source:** HackerOne
- **Report:** 500686 | https://hackerone.com/reports/500686
- **Submitted:** 2019-02-25
- **Reporter:** seifelsallamy
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Denial of Service, Client-Side Parsing Error, Input Validation Failure
- **CVEs:** None
- **Category:** memory-binary

## Summary
Invalid hex characters in URL parameters (e.g., ?%xx) cause the Twitter mobile site to crash and become unusable. When such URLs are shared via direct messages or tweets, they prevent all users (sender and followers) from loading content on mobile.twitter.com.

## Attack scenario
1. Attacker crafts a malicious URL containing invalid hex characters: https://mobile.twitter.com/?%xx
2. Attacker sends the URL via direct message to a victim
3. Victim attempts to load the conversation, triggering the crash
4. The mobile site fails to parse the invalid parameter and throws an unhandled error
5. Conversation/timeline becomes inaccessible to the victim
6. Alternatively, attacker tweets the URL, affecting all followers viewing the tweet

## Root cause
Client-side JavaScript attempts to decode or process the URL parameter without proper validation. When encountering %xx (incomplete/invalid hex sequence), the parser likely fails to find a valid character mapping, causing an unhandled exception that crashes the page rendering.

## Attacker mindset
Malicious user seeks to disrupt communication and content visibility on Twitter's mobile platform. Attack requires minimal technical sophistication and can affect multiple users through social distribution of the malicious link.

## Defensive takeaways
- Implement strict URL parameter validation and sanitization before processing
- Use try-catch blocks around URL decoding/parsing operations with graceful fallback
- Validate hex sequences during URL parameter extraction (must be %HH where H is valid hex)
- Implement error boundaries in React/JavaScript to prevent full page crashes from component errors
- Add CSP headers and input validation at network boundary
- Test edge cases with malformed URL parameters in QA process
- Consider using URL.parse() or established URI parsing libraries with error handling

## Variant hunting
Test other invalid percent-encoding sequences: %gg, %zz, %, %%
Try incomplete hex: %a, %1
Test in query parameters vs hash fragments: ?param=%xx vs #%xx
Test URL encoding in different parameter positions
Try nested encoding: %25xx (encoded percent sign)
Test on other Twitter endpoints and web properties
Check if other character parameters are similarly vulnerable

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1499 - Endpoint Denial of Service

## Notes
Report indicates this DoS vector only affects mobile.twitter.com (web), not native iOS/Android apps or desktop site. This suggests platform-specific client-side parsing vulnerability. The impact is limited to mobile web users, but represents a service disruption vector for that user segment.

## Full report
<details><summary>Expand</summary>

**Summary:** 
A url that twitter mobile site can not load, crushes any page containing this url

**Description:** 
Invalid hex characters crushes twitter mobile site as example go to ```https://mobile.twitter.com/?%xx``` 
twitter won't load.

1) Sending such url on a direct message, twitter will no longer be able to load the conversation,
F429765
2) Tweet such url, anyone following you won't be able to load any tweets
F429766

I think Twitter on the client side trying to find a value for %xx which is not possible so it raises an error

## Steps To Reproduce:

  1. Go to https://mobile.twitter.com/
  2. Send or tweet this url ```https://mobile.twitter.com/?%xx```
  3. You and your followers won't be able to see any tweets on the mobile site

## Impact

This issue works only on https://mobile.twitter.com/
(not working on IOS, Android and https://twitter.com/ )
however, all twitter mobile users with no twitter app should be affected

</details>

---
*Analysed by Claude on 2026-05-24*
