# Reflected Cross-Site Scripting (XSS) in /remote/error endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1799197 | https://hackerone.com/reports/1799197
- **Submitted:** 2022-12-10
- **Reporter:** 0xmr_b4rayz
- **Program:** Unknown (HackerOne Report 1799197)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the /remote/error endpoint where the 'errmsg' parameter is not properly sanitized or encoded before being reflected in the HTTP response. An attacker can inject malicious JavaScript code via a crafted URL that executes arbitrary scripts in a victim's browser when clicked.

## Attack scenario
1. Attacker crafts a malicious URL with JavaScript payload in the errmsg parameter: https://target/remote/error?errmsg=--><script>alert(document.domain)</script>
2. Attacker embeds the malicious link in a phishing email, social media post, or third-party website with enticing anchor text
3. Victim clicks on the seemingly legitimate link, triggering a request to the vulnerable application
4. The application reflects the unsanitized errmsg parameter value directly into the HTML response
5. Victim's browser parses the reflected script tag and executes the malicious JavaScript in the context of the application domain
6. Attacker's script gains access to victim's session cookies, can perform actions as the victim, or exfiltrate sensitive data

## Root cause
The application fails to properly validate and encode user-supplied input from the 'errmsg' query parameter before including it in the HTTP response. HTML special characters are not escaped, allowing attackers to break out of existing context and inject arbitrary HTML/JavaScript tags.

## Attacker mindset
An attacker seeks to compromise user sessions and perform unauthorized actions on behalf of authenticated users. By leveraging social engineering to distribute a malicious link, the attacker can bypass authentication mechanisms and gain the same privileges as the victim without knowing their credentials.

## Defensive takeaways
- Implement strict input validation on all user-supplied parameters, rejecting or sanitizing unexpected characters and patterns
- Apply context-appropriate output encoding (HTML entity encoding for HTML context) to all user-controlled data before reflection
- Use Content Security Policy (CSP) headers to restrict script execution and prevent inline scripts from running
- Implement HTTPOnly and Secure flags on cookies to prevent XSS from stealing session tokens
- Validate and sanitize on both client-side and server-side; never rely solely on client-side validation
- Use templating engines with auto-escaping enabled by default
- Conduct regular security code reviews focusing on data flow from input to output
- Implement Web Application Firewalls (WAF) with XSS detection rules

## Variant hunting
Search for similar parameter handling in other error pages, logging endpoints, or search functionality. Look for URL parameters like 'errmsg', 'error', 'message', 'msg', 'redirect', 'return', 'callback' that may reflect user input. Test endpoints returning HTML error messages, debugging information, or user-supplied data without encoding.

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1059.007

## Notes
The report provides clear reproduction steps with URL-encoded payload examples. The vulnerability is straightforward and requires minimal user interaction (simple click). The impact is severe as it can lead to complete user account compromise, session hijacking, and data theft. The vulnerability appears to be in a remote access or VPN-like application (based on /remote/error path), which typically handles sensitive authentication and authorization data.

## Full report
<details><summary>Expand</summary>

## Summary:
[Reflected XSS attacks, also known as non-persistent attacks, occur when a malicious script is reflected off of a web application to the victim’s browser.

The script is activated through a link, which sends a request to a website with a vulnerability that enables execution of malicious scripts. The vulnerability is typically a result of incoming requests not being sufficiently sanitized, which allows for the manipulation of a web application’s functions and the activation of malicious scripts.

To distribute the malicious link, a perpetrator typically embeds it into an email or third-party website (e.g., in a comment section or in social media). The link is embedded inside an anchor text that provokes the user to click on it, which initiates the XSS request to an exploited website, reflecting the attack back to the user.]

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. open the url [https://102.176.160.119:10443/remote/error?errmsg=]
  1.  in this pramiter  inject the xss pyload  in ?errmsg = [https://102.176.160.119:10443/remote/error?errmsg=ABABAB--%3E%3Cscript%3Ealert(1337)%3C/script%3E]
  1. final url ===    https://102.176.160.119:10443/remote/error?errmsg=--%3E%3Cscript%3Ealert(document.domain)%3C/script%3E

## Supporting Material/References: 
https://medium.com/@Steiner254/reflected-cross-site-scripting-xss-7aae0f4343c3
https://portswigger.net/web-security/cross-site-scripting
https://www.imperva.com/learn/application-security/reflected-xss-attacks/

## Impact

~ When attackers can control scripts that are executed in the victims’ browsers, then they stand at chances of typically compromising those users. These attackers can do the following:
a. Perform any kinds of actions within the applications that the users can perform.

b. View all kinds of data that the users have abilities to view.

c. Modify data that the users have abilities to modify.

d. Initiation of interactions with other application’ users.

</details>

---
*Analysed by Claude on 2026-05-12*
