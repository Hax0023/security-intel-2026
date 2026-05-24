# Google API Key Leak and Regex Misconfiguration Enables Open Redirect

## Metadata
- **Source:** HackerOne
- **Report:** 1066410 | https://hackerone.com/reports/1066410
- **Submitted:** 2020-12-25
- **Reporter:** br33z3
- **Program:** Clario (via HackerOne)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Credential Exposure, API Key Hardcoding, Open Redirect, Insufficient Input Validation, Security Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
A Google Firebase API key was exposed in client-side JavaScript, allowing unauthorized access to Firebase Dynamic Links URL shortening service. The backend regex validation for allowed domains was insufficiently configured, permitting attackers to craft shortened URLs redirecting to arbitrary malicious sites while maintaining the legitimate clario.co domain appearance.

## Attack scenario
1. Attacker examines client-side JavaScript files from account.clario.co and discovers hardcoded Google Firebase API key (AIzaSyAw-SpLHVTIP3IFEIkckCuEmIhnUrY9OrQ)
2. Attacker researches Firebase Dynamic Links API documentation and identifies the /v1/shortLinks endpoint accepts URL shortening requests with API authentication
3. Attacker discovers via testing that the backend regex validation for allowed domains is flawed, accepting any URL containing '/clario.co/' in the path component
4. Attacker constructs malicious URL: https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=[LEAKED_KEY] with payload containing 'https://malicious-site.com/clario.co/attack-path'
5. Attacker obtains shortened URL from lnk.clario.co appearing legitimate to victims
6. Attacker distributes shortened link via phishing campaigns; victims click trusting clario.co domain and are redirected to attacker-controlled malicious site

## Root cause
Multiple security failures: (1) API key embedded in client-side JavaScript without restriction/rotation, (2) Insufficient domain validation regex that checks for substring '/clario.co/' rather than domain boundary validation, (3) No URL allowlist enforcement or request signing to prevent unauthorized API usage

## Attacker mindset
Opportunistic credential harvesting combined with methodical API exploration. Attacker recognized exposed API key as valuable asset, researched legitimate API functionality, then identified and exploited weak validation logic to enable phishing at scale with trusted domain spoofing.

## Defensive takeaways
- Never hardcode API keys in client-side code; use server-side proxies with restricted API key scopes instead
- Implement proper domain validation using DNS lookups or strict whitelist matching against domain boundaries, not substring matching
- Rotate and revoke exposed API keys immediately; implement API key monitoring and alerting
- Apply principle of least privilege: restrict API keys to minimal required scopes and services
- Implement CORS and referrer validation on API endpoints to prevent unauthorized cross-origin requests
- Use URL allowlist/blocklist with proper canonicalization to prevent bypass via path tricks (e.g., clario.co/ substring attacks)
- Add rate limiting and behavioral analysis to detect abuse of Dynamic Links creation
- Audit all client-side assets regularly for hardcoded credentials using automated scanning

## Variant hunting
Search for similar patterns: (1) Other hardcoded Firebase/GCP API keys in JavaScript bundles across target assets, (2) Other URL shortening services with weak regex validation (bit.ly, tinyurl integrations), (3) Cloud Storage buckets or APIs exposed through client-side credentials, (4) Subdomain registration allowing arbitrary path injection (e.g., attacker-controlled.clario.co/ paths), (5) Admin APIs or internal service endpoints accessible via leaked API keys, (6) Analytics/event tracking APIs that log shortened URL creation without proper authentication

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (API key exposure)
- T1589 - Gather Victim Identity Information (credential harvesting)
- T1598 - Phishing (via legitimate-looking shortened URLs)
- T1566 - Phishing (delivery mechanism)
- T1621 - Multi-Stage Channels (shortened link redirects to secondary payload)

## Notes
Report demonstrates full kill chain from reconnaissance (JavaScript analysis) through exploitation (regex bypass) to attack delivery (phishing with spoofed legitimacy). The substring-based validation is particularly egregious as 'https://attacker.com/clario.co/' would pass validation. Firebase Dynamic Links API access should have been restricted to server-only authentication with IP allowlisting.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello, when i search your targets and javascript files I found an googleapikey leaks in url = [https://account.clario.co/js/main.044af6485f6b0cd90809.js](https://account.clario.co/js/main.044af6485f6b0cd90809.js "Url").
Part of the leak down below;
``` 
'https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=AIzaSyAw-SpLHVTIP3IFEIkckCuEmIhnUrY9OrQ';
```
{F1129971}

After that I do some research about that API key. I found how to use. This API shortening urls. API looks for key, company and regex rule for shortening urls.
Ref Link1 => [https://support.google.com/firebase/answer/9021429](https://support.google.com/firebase/answer/9021429 "Url")
Ref Link2 =>[https://firebase.google.com/docs/dynamic-links/rest](https://firebase.google.com/docs/dynamic-links/rest "Url")

While I was trying to test regex I was figured out i can short urls that redirect users whatever I want because of wrong regex leads security misconfiguration.  Also I found urls shortening from ```https://lnk.clario.co/?link=[URLHERE]```. I found that endpoint from same javascript file.
You can type anydomain and any urls only thing you need to do is add ```/clario.co/``` path to your url.

Here is an example PoC video; 

{F1130020}

You can redirect any website and any path to victims with that dynamic url.

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Get API key from javascript file.
  2. Find endpoint for shortening url from javascript file.
  3. Use postman or another tool for creating short url.
  4. Send url to victims. After that its up to your imagination :).

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

## Impact

Shortened link looks legit because its coming from clairo.co when we are looks from the victims perspective. Because of this victims can click the link easily and redirect to malicious websites.

</details>

---
*Analysed by Claude on 2026-05-24*
