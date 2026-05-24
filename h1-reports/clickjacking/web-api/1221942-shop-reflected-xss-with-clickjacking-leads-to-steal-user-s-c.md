# Reflected XSS with Clickjacking Protection Bypass Enables Cookie Theft

## Metadata
- **Source:** HackerOne
- **Report:** 1221942 | https://hackerone.com/reports/1221942
- **Submitted:** 2021-06-09
- **Reporter:** error201
- **Program:** Martha Stewart / Better Homes and Gardens (Meredith Corporation)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Clickjacking, Missing Security Headers, Cookie Theft
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability in the search parameter (?s=) combined with missing X-Frame-Options and clickjacking protections allows attackers to craft malicious URLs that execute arbitrary JavaScript and steal user cookies. By embedding these XSS payloads in an HTML POC that frames the vulnerable site, attackers can transparently overlay clickable elements to trick users into triggering the payload without awareness.

## Attack scenario
1. Attacker identifies the ?s= search parameter is vulnerable to XSS injection on both marthastewart.com/shop and bhg.com/shop domains
2. Attacker crafts a malicious URL with XSS payload like: https://bhg.com/shop/all.html?s=%E2%80%98);%3C/script%3E%3Cscript%3Ealert(document.cookie)%3C/script%3E
3. Attacker creates a POC.html file that iframes the vulnerable URL and overlays transparent clickable elements using CSS positioning
4. Attacker distributes the POC.html file via phishing email, social media, or other social engineering means to target users
5. Victim opens POC.html in browser; the vulnerable site loads in iframe and XSS payload executes due to reflected nature
6. Attacker's JavaScript exfiltrates victim's cookies and session tokens to attacker-controlled server, enabling account hijacking

## Root cause
The application fails to: (1) properly sanitize/encode user input in the search parameter before reflecting it in HTML context, (2) implement X-Frame-Options header to prevent clickjacking, (3) implement Content-Security-Policy headers to restrict script execution, and (4) use HttpOnly and SameSite flags on session cookies

## Attacker mindset
Opportunistic attacker leveraging publicly-known technique (Self-XSS to Good-XSS via clickjacking) against large e-commerce properties. The attacker actively researched the vulnerability class through Medium articles and prior HackerOne reports, indicating moderate sophistication. Target selection suggests motivation is either financial (account takeover for fraud) or reputational (bug bounty program participation).

## Defensive takeaways
- Implement input validation and output encoding for all user-supplied parameters, especially search queries
- Add X-Frame-Options: DENY or SAMEORIGIN header to all responses to prevent iframe-based clickjacking
- Implement Content-Security-Policy header with strict directives (script-src, frame-ancestors) to restrict code execution
- Set HttpOnly and Secure flags on all session cookies to prevent JavaScript access
- Add SameSite=Strict/Lax cookie attribute to mitigate CSRF attacks triggered via clickjacking
- Use a security-focused templating engine with automatic output encoding enabled by default
- Implement Web Application Firewall (WAF) rules to detect and block common XSS payloads
- Conduct regular security code reviews focusing on template injection and encoding gaps

## Variant hunting
Search for similar ?s= or query parameters across the Meredith Corporation domain portfolio; test other input parameters on both domains (filters, category, sort); check for stored variants if search history is saved; test similar patterns on mobile versions; investigate if third-party JavaScript libraries are being used that might have bypasses

## MITRE ATT&CK
- T1190
- T1566.002
- T1111
- T1005
- T1041
- T1598.003

## Notes
Report lacks technical depth in POC (HTML not included in excerpt), bounty amount unknown suggesting possible lower-tier resolution. The vulnerability represents a classic chaining of two separate weaknesses (XSS + missing framebusting) rather than a novel attack. Both domains affected suggests shared codebase or platform. Report references appropriate prior art but could have benefited from more detailed payload analysis and mitigation testing.

## Full report
<details><summary>Expand</summary>

Hii  Security Team ,

I am S Rahul MCEH(Metaxone Certified Ethical Hacker) and a Security Researcher I just checked your website and found Reflected XSS to Good XSS Clickjacking In Two Domain

Description:- As the search parameter is vulnerable to XSS and but the plus point is there is  no X-Frame-Header or Click-jacking Protection.So by combing this two methods the Attack Easier And Converted it to Well Working XSS on Other User’s . 

Vulnerable Urls:- https://marthastewart.com/shop/all.html?s=
                            https://bhg.com/shop/all.html?s=
		
Steps to reproduce :-
1. Navigate to  Vulnerable URLS and As we know that ?s= parameter is vulnerable to XSS 

2.As Reflected XSS Occurs on :-
	Example1 :-  https://bhg.com/shop/all.html?s=%E2%80%98);%3C/script%3E%3Cscript%3Ealert(document.cookie)%3C/script%3E
	Example2 :-  https://marthastewart.com/shop/all.html?s=%E2%80%98);%3C/script%3E%3Cscript%3Ealert(document.cookie)%3C/script%3E

3.The attacker can use different Payloads like document.domain etc 

4.Now as we know there is no X-Frame-Header or Click-jacking Protection that can leads to successful attack

5.Now we will create POC.html to send the victim and steal the cookies of the other users { POC.html is attached below }

6.Now as the victim opens the POC.html the attacker will get the cookies of the users or victim

Refernces:-
https://arbazhussain.medium.com/self-xss-to-good-xss-clickjacking-6db43b44777e
https://hackerone.com/reports/470206
https://hackerone.com/reports/892289

## Impact

Impact
By exploiting this Vulnerability
1.An attacker can force the customer to execute XSS and Steal user's cookie.
2.Launch advanced phishing attacks by rendering arbitrary HTML forms.
3.Force users to download malware/viruses.
4.Execute browser-based attacks etc.

</details>

---
*Analysed by Claude on 2026-05-24*
