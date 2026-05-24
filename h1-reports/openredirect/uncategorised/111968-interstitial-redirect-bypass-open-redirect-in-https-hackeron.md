# Interstitial Redirect Bypass via Open Redirect Chaining

## Metadata
- **Source:** HackerOne
- **Report:** 111968 | https://hackerone.com/reports/111968
- **Submitted:** 2016-01-21
- **Reporter:** zombiehelp54
- **Program:** HackerOne (Zendesk)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Redirect Chain/Bypass, Security Control Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can bypass Zendesk's interstitial warning page by chaining an open redirect vulnerability in the zendesk_session endpoint with another redirect mechanism. The attacker crafts a malicious return_to parameter that points to an intermediate redirect endpoint, which then redirects to an attacker-controlled domain without displaying the security warning.

## Attack scenario
1. Attacker identifies that the zendesk_session endpoint has an open redirect vulnerability in the return_to parameter
2. Attacker discovers that support.hackerone.com/ping/redirect_to_account endpoint also performs redirects
3. Attacker crafts a URL where return_to points to the intermediate redirect endpoint instead of directly to evil.com
4. Victim clicks the malicious link which goes to zendesk_session endpoint
5. The interstitial check sees return_to as support.hackerone.com (first-party domain) and doesn't warn the user
6. The intermediate endpoint then redirects to attacker's evil.com domain, bypassing the interstitial warning

## Root cause
The interstitial redirect validation only checks the immediate return_to parameter value rather than validating the final destination after following redirect chains. The security control assumes one-hop redirects and fails to detect multi-stage redirect chains to malicious domains.

## Attacker mindset
The attacker recognizes that security controls can often be bypassed by chaining multiple legitimate-looking redirects. By using an internal endpoint as an intermediary, they exploit the trust relationship between domains and defeat the interstitial warning mechanism designed to protect users from phishing.

## Defensive takeaways
- Implement redirect chain analysis - follow and validate all redirect destinations, not just the immediate target
- Whitelist only specific endpoints/paths for redirect operations, not entire domains
- Apply the same validation rules to redirect endpoints as you do to user-facing redirect parameters
- Consider implementing Content Security Policy headers to restrict where pages can navigate users
- Log and monitor redirect chains to detect suspicious patterns (internal to external redirects)
- Use DNS/domain-based validation for redirect targets, not just path/parameter inspection
- Implement rate limiting on redirect endpoints to prevent abuse

## Variant hunting
Look for other intermediate redirect endpoints that could be abused (e.g., /api/redirect, /ping/*, /track/*)
Check if other authentication flows (OAuth, SAML endpoints) have similar redirect chain bypasses
Test whether the validation can be bypassed with encoded URLs or case variations in the intermediate endpoint
Investigate if subdomain redirects can similarly bypass the interstitial (e.g., redirect.support.hackerone.com)
Check if the return_to parameter accepts multiple values or array-like syntax to chain redirects
Test redirect endpoints with various encoding schemes (double encoding, Unicode, URL fragments)

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (using bypass to deliver phishing without warning)
- T1598.002 - Phishing: Spearphishing Link (social engineering with trusted-looking domain)
- T1021.007 - Remote Services: Cloud Service Web Portals (exploiting Zendesk session handling)
- T1566.002 - Phishing: Phishing - Link (leveraging redirect bypass for delivery)

## Notes
This is a security control bypass rather than a traditional open redirect. The vulnerability chained two separate issues: (1) the known open redirect in return_to parameter and (2) trust-based validation of intermediate endpoints. The researcher demonstrated sophisticated understanding of redirect mechanics and security control design. The suggested fix (blocklisting /ping/redirect_to_account) is a patch but not a comprehensive solution - a better approach would be recursive redirect validation.

## Full report
<details><summary>Expand</summary>

Hi guys , I have found a way to use the open redirect vulnerability that zendesk refused to fix and we discussed it in #101146 to bypass intristial redirect. 
in #101146 , @bencode said : 
> I tend to agree with Zendesk, we don't really see any security issues with it. We use our interstitial to warn the user and it's clear you are on a separate site.

Well , using this issue I could bypass the interstitial redirect.
#PoC:
[Clicking here will bypass interistial redirect and get you on evil.com](https://hackerone.com/zendesk_session?locale_id=1&return_to=https://support.hackerone.com/ping/redirect_to_account?state=compayn:/)
 
The link is `https://hackerone.com/zendesk_session?locale_id=1&return_to=https://support.hackerone.com/ping/redirect_to_account?state=compayn:/` which is used to redirect to generate a zendesk session.
This can be fixed from your end , by detecting the `/ping/redirect_to_account` in the `return_to` parameter. 
Thanks  

</details>

---
*Analysed by Claude on 2026-05-24*
