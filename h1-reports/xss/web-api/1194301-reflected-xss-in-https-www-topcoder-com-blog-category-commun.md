# Reflected XSS in TopCoder Blog Category Filter Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 1194301 | https://hackerone.com/reports/1194301
- **Submitted:** 2021-05-12
- **Reporter:** c0mbo
- **Program:** TopCoder
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the TopCoder blog category pages where the 'o' and 'so' URL parameters are reflected unsanitized into hidden input fields. An attacker can craft malicious URLs to inject arbitrary HTML and JavaScript, enabling phishing attacks and content spoofing by redirecting users to attacker-controlled sites.

## Attack scenario
1. Attacker identifies that the 'o' parameter in the blog category URL is reflected into a hidden input without sanitization
2. Attacker crafts a malicious URL with XSS payload: ?s=123&so=&o=1%22%3E%3Ch1%3EXSS payload%3C/h1%3E
3. Attacker embeds the malicious URL in a phishing email or forum post appearing legitimate
4. Victim clicks the link believing it's legitimate TopCoder content
5. Attacker's HTML/JavaScript executes in victim's browser within TopCoder's origin, displaying fake 'site moved' message
6. Victim is redirected to attacker's phishing site where credentials or sensitive data is harvested

## Root cause
The application fails to properly sanitize or encode user-supplied input from the 'o' and 'so' query parameters before reflecting them into HTML attributes within hidden input fields. The output context (HTML attribute) requires proper escaping but none is applied.

## Attacker mindset
The attacker demonstrates methodical testing by identifying hidden parameters, crafting multiple payloads for different attack scenarios (credential harvesting via fake login prompts, phishing redirects), and documenting the vulnerability clearly for the security team.

## Defensive takeaways
- Implement strict input validation and allowlisting for all query parameters
- Apply context-appropriate output encoding: HTML entity encoding for HTML context, JavaScript escaping for JS context
- Use security libraries/frameworks that auto-escape output by default
- Apply Content Security Policy (CSP) headers to mitigate XSS impact
- Implement HTTPOnly and Secure flags on sensitive cookies
- Regularly scan for reflected parameters in all user-controlled input
- Use automated security testing to catch reflected XSS in hidden fields and non-obvious locations

## Variant hunting
Test all URL parameters for reflection, including hidden ones (s, so, o, p, page, etc.)
Check other blog category pages and archive pages for similar filtering mechanisms
Examine admin/dashboard filters for same vulnerable patterns
Test POST parameters if pagination/filtering uses POST requests
Check if vulnerability exists in other TopCoder subdomains (forums, profiles, etc.)
Test parameter pollution attacks combining multiple parameters
Look for DOM-based XSS variants where parameters are processed client-side

## MITRE ATT&CK
- T1190
- T1598.003
- T1114

## Notes
The report correctly identifies this as reflected XSS despite superficial similarity to content spoofing. The vulnerability's persistence in hidden input fields makes it particularly dangerous as users may not notice the injected content. The reporter provided multiple payload examples demonstrating practical attack scenarios including phishing redirection, which significantly increases the real-world impact assessment.

## Full report
<details><summary>Expand</summary>

## Summary:
Reflected XSS in https://www.topcoder.com/blog/category/community-stories/
Note: This is a reflected XSS vulnerability in a hidden input.
With that vulnerability, an attacker could write his own code on the website.
But with this vulnerability, an attacker also could lead a user, to go on his attacker's website.

## Steps To Reproduce:

  1. go to the website https://www.topcoder.com/blog/category/community-stories/
  2. in the search field search 123 
  3. The request URL should look like this:https://www.topcoder.com/blog/category/community-stories/?s=123&so=&o=
  4. The &so=&o= after 123 it's the hidden input value, which is vulnerable to reflected XSS
  5. At the end of the URL (at the end of the &so=&o=) write 1"><h1>DOM XSS by c0mbo</h1>
  6. Request URL: https://www.topcoder.com/blog/category/community-stories/?s=123&so=&o=1%22%3E%3Ch1%3EREFLECTED%20XSS%20by%20c0mbo%3C/h1%3E

## Other payloads:
1. https://www.topcoder.com/blog/category/community-stories/?s=123&so=&o=1%22%3E%3Cbutton%3Eclick%20me!%3C/button%3E
2. https://www.topcoder.com/blog/category/community-stories/?s=123&so=&o=1%22%3E%3Ch1%3E!!!ATTENTION!!!%20this%20site%20has%20moved%20to%20[www.attackerssite.com]%20if%20you%20want%20to%20login,%20please%20visit%20[www.attackerssite.com]%3C/h1%3E
3. https://www.topcoder.com/blog/category/community-stories/?s=123&so=&o=1%22%3E%3Ctextarea%3E

## Supporting Material/References:
I made some screenshots :)

Contact me, if you need more info!

Best regards,
@c0mbo

## Impact

With that vulnerability, an attacker can write his own code on the website.
So with that, he could write a message on the website, that this site moved and he has to visit the attacker's site and send the victim the link.
That could for example be a phishing site. This is similar to content spoofing. 
NOTE: Some people would count it as content spoofing, but than it is still in scope, because an attacker can implement / modify HTML on the website, but in my opinion, that's definitly reflected XSS.

</details>

---
*Analysed by Claude on 2026-05-12*
