# Open Redirect Filter Bypass via Triple Slash Protocol Prefix

## Metadata
- **Source:** HackerOne
- **Report:** 76738 | https://hackerone.com/reports/76738
- **Submitted:** 2015-07-19
- **Reporter:** jayden
- **Program:** Zaption
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The logout endpoint's returnTo parameter implements a redirect filter that fails to properly validate URLs beginning with triple slashes (///). An attacker can bypass the filter by prepending three slashes to an external domain, causing the application to redirect users to arbitrary attacker-controlled sites. This vulnerability can be exploited in phishing attacks to deceive users into visiting malicious websites while appearing to come from the legitimate Zaption domain.

## Attack scenario
1. Attacker identifies the vulnerable logout endpoint at zaption.com/logout?returnTo=parameter
2. Attacker discovers the redirect filter rejects common bypass patterns like http://, //, and single-slash external URLs
3. Attacker crafts a payload using triple slashes: ///evil.com/ which is not caught by the filter
4. Attacker creates a phishing link: https://www.zaption.com/logout?returnTo=///evil.com/
5. Attacker distributes the link to victims via email or social engineering
6. When victim clicks the link, Zaption's server responds with HTTP 302 redirect to ///evil.com, which browsers interpret as a redirect to evil.com, successfully bypassing the filter

## Root cause
The redirect validation logic uses a blacklist or pattern-matching approach that fails to account for alternative URL schemes and protocol representations. The filter likely checks for 'http://', '//', or single-slash patterns but does not normalize or comprehensively validate the returnTo parameter, allowing the triple-slash variant (///) to bypass validation while still functioning as a valid redirect.

## Attacker mindset
An attacker exploiting this vulnerability seeks to abuse the trust users have in the legitimate Zaption domain to deliver them to malicious sites. By using the application's own logout flow, the attacker increases credibility and reduces user suspicion. The filter bypass demonstrates shallow security testing and provides an easy path for phishing infrastructure without domain registration costs.

## Defensive takeaways
- Implement whitelist-based URL validation: only allow redirects to explicitly approved domains or relative URLs
- Use URL parsing libraries to normalize and validate URLs before redirects, not regex patterns
- Validate the protocol scheme explicitly and reject any variation or absence of standard schemes
- Implement a strict allow-list of valid redirect destinations rather than attempting to block malicious patterns
- Test open redirect filters against comprehensive bypass payloads including //, ///, \\ variants, protocol-relative URLs, and encoded characters
- Log redirect attempts to external domains for security monitoring and anomaly detection
- Consider implementing POST-based redirects with CSRF tokens instead of GET parameters for sensitive operations like logout

## Variant hunting
Test with encoded slashes: %2f%2fevil.com and %5c%5cevil.com
Try protocol-relative URLs: //evil.com and ////evil.com
Test with backslashes: \\evil.com
Try mixed case variations and unicode homoglyphs in domain names
Test with data: URLs and javascript: URLs if the filter only blocks http/https
Try URL fragments: /path#//evil.com
Test with null bytes or line breaks to truncate validation: /path%00//evil.com
Test with alternative protocols: ftp://, ws://, gopher://

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1598.001 - Phishing: Spearphishing via Service

## Notes
This is a classic example of security through obscurity failure. The developers attempted to block common bypass patterns without understanding URL parsing mechanics. The triple-slash payload works because browsers normalize ///evil.com to //evil.com (protocol-relative URL) which resolves to http(s)://evil.com. Zaption's filter likely used a simple string search or regex that checked for specific patterns but failed to account for alternative representations. The response header 'Access-Control-Allow-Origin' appears blank, suggesting potential additional CORS misconfiguration. This vulnerability is particularly effective for phishing because the redirect originates from the legitimate zaption.com domain, increasing user trust.

## Full report
<details><summary>Expand</summary>

Hi  , 

An open redirect is an application that takes a parameter and redirects a user to the parameter value without any validation. This vulnerability is used in phishing attacks to get users to visit malicious sites without realizing it.

its possible to bypass your redirect filter using : 
https://www.zaption.com/logout?returnTo=///evil.com/

`HTTP/1.1 302 Moved Temporarily
Access-Control-Allow-Origin: 
Cache-Control: private, must-revalidate
Content-Type: text/html; charset=utf-8
Date: Sun, 19 Jul 2015 10:55:48 GMT
Location: ///evil.com
P3P: CP="Zaption does not have a P3P policy. See privacy policy at http://zapt.io/privacy"
Pragma: no-cache
Vary: Accept, Accept-Encoding
Content-Length: 78
Connection: keep-alive

<p>Moved Temporarily. Redirecting to <a href="///evil.com">///evil.com</a></p>`



</details>

---
*Analysed by Claude on 2026-05-24*
