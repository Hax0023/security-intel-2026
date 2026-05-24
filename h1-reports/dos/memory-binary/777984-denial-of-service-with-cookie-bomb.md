# Denial of Service via Cookie Bomb on nordvpn.com

## Metadata
- **Source:** HackerOne
- **Report:** 777984 | https://hackerone.com/reports/777984
- **Submitted:** 2020-01-19
- **Reporter:** bihari_web
- **Program:** NordVPN
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Denial of Service, Cookie Bomb, Insufficient Input Validation, Unsanitized Cookie Values
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can craft malicious URLs with excessively long path parameters that are unsanitized and directly embedded into cookies (FirstSession, CurrentSession, and n_ref), accumulating to 8KB+ of cookie data. This exceeds typical web server cookie size limits, causing persistent denial of service for victims until cookies are manually cleared.

## Attack scenario
1. Attacker crafts a URL with a ~4KB random path parameter: https://nordvpn.com/[4KB_payload]
2. Victim visits the malicious link in a fresh incognito session
3. JavaScript sets FirstSession and CurrentSession cookies containing the unsanitized pathname as a parameter value (4KB each)
4. Attacker provides a second malicious link with n_ref parameter containing ~4KB payload: https://nordvpn.com/order/?2year&coupon=anything&ref=[4KB_payload]
5. Victim visits the second link, setting n_ref cookie with additional 4KB data
6. Total accumulated cookies exceed 8KB, exceeding server limits; requests fail and site becomes inaccessible until cookies are deleted

## Root cause
The application directly embeds unsanitized URL pathname values into cookie contents without size validation or sanitization. No server-side validation prevents cookie accumulation, and no maximum cookie size enforcement exists at the application level before transmission.

## Attacker mindset
Exploit lack of input validation on URL parameters that get stored in cookies. Understand HTTP cookie size limitations (typically 4-8KB per domain) and leverage cookie persistence to create a self-inflicted denial of service condition that persists across sessions.

## Defensive takeaways
- Implement strict input validation and sanitization for all URL parameters before storing in cookies
- Set maximum length limits on cookie values and enforce validation server-side
- Monitor and limit total cookie size per domain, rejecting requests that would exceed thresholds
- Use Content Security Policy headers to restrict cookie-setting behavior
- Implement cookie size warnings and automated cleanup of oversized cookies
- Avoid storing user-controlled URL paths directly in cookies; use encoded identifiers instead
- Educate users about clearing cookies if site becomes inaccessible

## Variant hunting
Test other URL parameters (query strings, fragments) for similar cookie injection
Check if other cookies can be manipulated via HTTP headers (Set-Cookie injection)
Test POST parameters for cookie bomb vectors
Look for other subdomains with similar vulnerable cookie-setting logic
Investigate if header-based attacks (X-Forwarded-For, User-Agent) can inflate cookies
Test if multiple simultaneous requests can accumulate cookies faster

## MITRE ATT&CK
- T1499.004
- T1190

## Notes
This is a classic cookie bomb attack combining path traversal concepts with cookie overflow. The report demonstrates good understanding of HTTP mechanics. The persistent nature (survives page reloads/new sessions) makes it particularly impactful. Report includes video PoC (F689645). Severity is medium rather than high because it requires victim interaction and can be easily remediated by clearing cookies.

## Full report
<details><summary>Expand</summary>

## Summary:
This is Denial of Service attack by using which an attacker can make an user unable to access nordvpn.com website.
For more information you can read this article.
[https://blog.innerht.ml/tag/cookie-bomb/]

## Steps To Reproduce:
This will usually work on  user's fresh session for which we can use inconginito tab.

  1. Open fresh user session to website (Or Incognito Tab)
  1. First visit this link 
https://nordvpn.com/xxxxx.....xxxxxxx_up_to_4kb_in_size

When we visit this link or the home page of the website two cookies are set i.e *FirstSession* and *CurrentSession*
For every session, **FirstSession** Cookie is only set once and the **CurrentSession** cookies keeps on updating based on some **path** values.
Note: These cookies are set by javascript.

Cookie format for both of them is like this 
**FirstSession: source=(direct)&campaign=(direct)&medium=(none)&term=&content=&hostname=nordvpn.com&pathname=/&date=20200119**
**CurrentSession: source=(direct)&campaign=(direct)&medium=(none)&term=&content=&hostname=nordvpn.com&pathname=/&date=202019**
Here the **pathname** parameter is path to the website that we are on.
Since the pathname is directly set into  these cookie from the visited url, and there is no size limit on the url path.
Hence we can make a request to long random path up to of 4 Kb (Max size of a cookie) and both of the cookies will contain 4kb of randome data.
But the **CurrentSession** cookies will change on each path followed, hence it will change it's payload size.
For this attack to be successful we need aprox 8Kb of Cookies size. (Atleast we have 4Kb now from *FirstSession*)


  3 . Now Visit this final link
https://nordvpn.com/order/?2year&coupon=anything&ref=xxxxx.....xxxxxxx_up_to_4kb_in_size
This will set a cookie **n_ref** with the value of **ref** parameter.
And Now we have appox 8Kb of cookies and most of the webservers don't accept this large size of request and hence we now have a persistent Denial Of Service Attack.

## Supporting Material/References:
  * F689645
  * https://drive.google.com/file/d/1bgLTJd3ZNK9S7gHAz3g0Ksiz78BYWXOV/view?usp=sharing 
Video PoC Link

## Impact

User will not we able to access the website, and will have persistent DoS attack untill he deletes all the cookies manually.

</details>

---
*Analysed by Claude on 2026-05-24*
