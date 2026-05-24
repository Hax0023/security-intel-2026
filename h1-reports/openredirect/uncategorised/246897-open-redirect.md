# Open Redirect via URL Parameter Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 246897 | https://hackerone.com/reports/246897
- **Submitted:** 2017-07-07
- **Reporter:** malcolmx
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, URL Redirection to Untrusted Site
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability was discovered in Twitter's live video stream authorization endpoint (t.lv.twimg.com) where the 'url' parameter is not properly validated. By manipulating the 'noredirect' parameter from true to false, attackers can redirect users to arbitrary external websites, enabling phishing and credential harvesting attacks.

## Attack scenario
1. Attacker crafts a malicious URL containing Twitter's live_video_stream endpoint with a controlled 'url' parameter pointing to a phishing site
2. The 'noredirect' parameter is set to 'false' to enable automatic redirection
3. Attacker distributes the malicious link via social engineering, appearing legitimate due to the twitter.com domain
4. Victim clicks the link, trusting the Twitter domain in the URL
5. The application automatically redirects the victim to the attacker-controlled phishing site
6. Attacker captures credentials or performs other malicious actions on the redirected domain

## Root cause
Insufficient input validation on the 'url' parameter combined with a conditional redirect mechanism controlled by the 'noredirect' parameter. The application fails to validate that redirect destinations are within allowed domains, and the noredirect parameter can be manipulated to bypass security controls.

## Attacker mindset
An attacker would leverage this vulnerability for phishing campaigns by creating convincing spear-phishing emails with Twitter-branded links that appear legitimate. The attacker understands that users trust well-known domains and can exploit this to redirect them to credential harvesting sites or malware distribution endpoints.

## Defensive takeaways
- Implement strict whitelist-based validation for all redirect parameters, allowing only internal Twitter URLs
- Never trust user-supplied redirect parameters without comprehensive validation
- Use allowlist approach rather than blacklist for URL validation
- Implement proper URL parsing and domain verification to ensure redirects stay within trusted domains
- Consider removing or restricting the ability to control redirect behavior via user parameters
- Log and monitor unusual redirect patterns for security analysis
- Educate users about verifying final destination URLs in browser address bar before interacting with content

## Variant hunting
Search for other endpoints accepting 'url' or 'redirect' parameters across Twitter infrastructure
Test variations: 'return_url', 'callback_url', 'next', 'goto', 'forward', 'target' parameters
Check if 'noredirect' or similar boolean parameters exist on other endpoints that can bypass protections
Test URL encoding bypasses: %2f%2f, double encoding, protocol variations (javascript:, data:)
Examine other Twitter shortened URL services and redirects (t.co ecosystem)
Test if redirect validation can be bypassed with domain trickery (subdomains, similar domains)

## MITRE ATT&CK
- T1598
- T1598.002
- T1566
- T1566.002
- T1605

## Notes
This vulnerability is particularly dangerous on a high-trust platform like Twitter where users are conditioned to click links from the domain. The presence of legitimate-looking parameters (live_video_stream, authorization status, context tokens) adds to the social engineering effectiveness. The very long URL with numerous parameters and checksums may provide false legitimacy to victims. The vulnerability demonstrates the importance of default-deny approaches to redirects rather than relying on boolean flags that can be toggled.

## Full report
<details><summary>Expand</summary>

Hello,

i found Open Redirect 

#POC : 
- go to 
https://t.lv.twimg.com/live_video_stream/authorized_status/883213898672783361/LIVE_PUBLIC/DEHOXIMUQAEbRFW?url=https://google.com/&ctx=27_883213898672783361:AAAAEIDslSPDE_gV-wU3Opzr9YAPswhkTvPilFsbz0m-QHi4zZGjkDktKKAldYW9vrXUzlTimnrcBaI0_UMq0VTZFEGi2y28FMWT_64G3uUalicaPAIdaxPuqr-K_5kADwxgi-2kQyrU1R4eh-u73RIpcIAcppkOk6JXBfkoRYNYfUpNiAC6wHtW9j97pYVZtSm-ZTOvx_IWbh26eiHUASipHu8CMTvWPby1Apb8tFpu9L9kIs2KTqNutqTk2cnFeSFVbpS1sCqHsAWCtprwiatM-dFger3FzGLnRTcrxgrbcvOhHUqryeUMq1trAekNsazL8lThiV1ig6f49SUizYIg9sEZq4Wqh5qAi4q1d9nOL8cCRBMVd-qgkvCxl41gjpDO70gHiBnNsreuN5MzcrKZxT7fY0cf0EMrVekTJPELycfBKq0HiwJubeo8tBebB_fFt-cqmFB7PflKdgA22yu4mN_NrvG7vCA5OzAYZIIA5vK7-fdmgkn34abSFKj680-zhHqx2IVLK4zmdeq4SRBSxWbFn-iC5x7HNhogriP3coQc4N1_31d6XOOtexkktpSGVsWZ-Y63xbpN&evt=38617099&exp=1499428143990&checksum=nwUP-VQZpwIBcWj-&noredirect=false

- by converting  ``` &noredirect= ```  from   ``` true ```   to  ``` false ```   i was able to redirect users to any site 
- by clicking on this link you will get redirect to https://google.com  as you can see it on  ``` ?url= ```

{F201033}

Thanks 

</details>

---
*Analysed by Claude on 2026-05-24*
