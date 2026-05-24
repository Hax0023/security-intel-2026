# Brave Browser Open Redirect via Improper URL Parameter Handling in Redirect Flow

## Metadata
- **Source:** HackerOne
- **Report:** 1579374 | https://hackerone.com/reports/1579374
- **Submitted:** 2022-05-24
- **Reporter:** kalkii
- **Program:** Brave Browser
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, Browser Security Policy Bypass, Improper Input Validation
- **CVEs:** CVE-2023-22798
- **Category:** uncategorised

## Summary
Brave browser bypasses Facebook's redirect validation mechanism (l.facebook.com/l.php) by directly following redirect parameters without consulting the origin server's security checks. This allows circumvention of Facebook's linkshim protection that filters malicious domains, affecting only Brave users while other browsers properly validate redirects through the origin server.

## Attack scenario
1. Attacker crafts a malicious URL: https://l.facebook.com/l.php?u=https://attacker-controlled-domain.com/phishing
2. Victim using Brave browser receives the link via Facebook post, message, or third-party site
3. Victim clicks the link expecting Facebook's server-side validation to filter malicious destinations
4. Brave intercepts the redirect parameter and directly requests the attacker domain without contacting l.facebook.com servers
5. Facebook's linkshim validation (malicious domain list check) is bypassed entirely
6. Victim is redirected to attacker's phishing page, believing Facebook has already validated it as safe

## Root cause
Brave browser implements aggressive redirect handling that directly follows URL parameters in redirect endpoints without respecting the origin server's security validation flow. The browser treats the redirect parameter as a direct instruction rather than data to be processed by the origin server, violating the intended security architecture where l.facebook.com validates destinations before issuing redirects.

## Attacker mindset
An attacker exploits browser-specific behavior to bypass established security controls. By understanding that Brave deviates from standard redirect handling, they can craft Facebook URLs that appear legitimate but actually bypass Facebook's server-side filtering. This is attractive because it maintains the illusion of Facebook's validation (using their official redirect domain) while circumventing protections, increasing social engineering effectiveness.

## Defensive takeaways
- Browser vendors should implement redirect handling that respects server-side validation requirements and not optimize by pre-following parameters
- Validate that redirect endpoints are actually being contacted by monitoring server-side logs for redirect requests
- Implement Content Security Policy (CSP) headers with frame-ancestors and form-action directives to restrict where users can be redirected
- Use opaque redirect URLs that cannot be parsed client-side to force server-side validation
- Add browser fingerprinting/behavior detection to identify when redirect validation is being bypassed
- Educate users about URL structure and the importance of server-side validation in security flows

## Variant hunting
Search for similar browser-specific redirect handling bypasses in: Chrome, Firefox, Safari, and Edge browsers with redirect endpoints from other platforms (bit.ly, tinyurl, URL shorteners). Test whether browsers follow 'next', 'return_to', 'redirect_uri', 'url', 'goto' parameters directly without origin server validation. Check if browsers optimize away intermediate redirects in other security contexts (OAuth flows, password reset links, email verification).

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (redirect bypass enables effective phishing)
- T1566.002 - Phishing: Phishing - Email (delivered via Facebook with bypassed validation)
- T1598.004 - Phishing: Spearphishing via Service (abuse of trusted Facebook redirect mechanism)

## Notes
This is a browser implementation bug rather than a Facebook vulnerability. The reporter correctly identified that other browsers follow proper flow while Brave deviates. The severity is Medium-High due to widespread Brave usage and the combination with trusted platform (Facebook) making social engineering more effective. The fix requires Brave to change redirect handling logic to contact the origin server rather than following parameters directly. This report demonstrates the importance of cross-browser testing for security features and that 'optimizations' in browser behavior can inadvertently bypass security controls.

## Full report
<details><summary>Expand</summary>

## Summary:

Brave browser is not following proper flow for redirection. Browser is directly redirecting to the site that is present in redirect parameter without confirming from the main site server.
I have found this vulnerability and this is affecting Facebook. Facebook use ```l.facebook.com/l.php?u=<redirect_site>``` for redirection and when server gets the request it check whether the redirect_site is in the list of there malicious(linkshim) list or not. If not then Facebook redirect  it properly.
But when we try to go to a site like https://l.facebook.com/l.php?u=https://test.facebook-whitehat.com/ then brave browser is directly requesting to https://test.facebook-whitehat.com/ (a domain resticted by facebook which can be used for testing prepose) without asking Facebook server  whether should I redirect or not. But other browser are properly following the flow. 

## Products affected: 

 Windows 11, Version 1.38.119 Chromium: 101.0.4951.67 (Official Build) (64-bit)

## Steps To Reproduce:

1. Open brave browser in windows
2.  Intercept the requests
3. Go to ```https://l.facebook.com/l.php?u=https://test.facebook-whitehat.com/``` and you will notice that it directly generating a request ```https://test.facebook-whitehat.com/``` not to ```l.facebook.com```

## Supporting Material/References:

 I also soon how other browser is responding and how brave is responder. POC video attached

## Impact

Brave has seen a massive growth in 2021 quarter and Facebook is the one of the largest used social media.
Due to this vulnerability users that are using Brave browser are directly affected which will affect brave reputation as only brave browser users are getting affect.
As well  this vulnerability in brave browser is affecting facebook's security also.

</details>

---
*Analysed by Claude on 2026-05-24*
