# Reflected XSS in m.imgur.com Username Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 149855 | https://hackerone.com/reports/149855
- **Submitted:** 2016-07-07
- **Reporter:** logue
- **Program:** Imgur
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Input Validation Bypass, Output Encoding Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the mobile version of imgur (m.imgur.com) where the username parameter in the account/messages endpoint fails to sanitize angle bracket characters. An attacker can inject arbitrary JavaScript that executes in the victim's browser within the m.imgur.com domain context by crafting a malicious URL and tricking users into clicking it.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload embedded in the username parameter: https://m.imgur.com/account/testcatplzignore">\<img src=x onerror=prompt(document.domain)>/messages
2. Attacker tricks an authenticated imgur user into clicking the link via social engineering on platforms like Reddit or direct messaging
3. Victim's mobile browser loads m.imgur.com with the mobile User-Agent, bypassing any desktop-only protections
4. Server reflects the unencoded username parameter into the HTML response without sanitization
5. Browser parses the injected HTML/JavaScript and executes the onerror event handler in the victim's session context
6. Attacker's malicious script can steal session cookies, credentials, or perform actions on behalf of the authenticated user

## Root cause
The application fails to perform proper output encoding (HTML entity encoding) on user-supplied input reflected in the response. The username parameter is directly inserted into the HTML markup without escaping angle brackets and quotes, allowing the browser to interpret the attacker's injected tags as legitimate HTML elements.

## Attacker mindset
An opportunistic attacker seeking to compromise imgur user accounts to gain access to private images, messages, or to leverage the account for further malicious activities. The attacker exploits the mobile site as a bypass vector, recognizing that mobile user agents may receive different validation logic than desktop browsers.

## Defensive takeaways
- Implement consistent output encoding: HTML-encode all user input reflected in HTML context (< becomes &lt;, > becomes &gt;, " becomes &quot;)
- Apply input validation on both client and server side, but rely on output encoding as the primary defense
- Ensure the same security controls are applied across all versions of the application (mobile, desktop, API)
- Use a Content Security Policy (CSP) to restrict inline script execution and mitigate XSS impact
- Implement automatic security testing that specifically tests mobile user agents and URL parameter injection points
- Use security libraries and templating engines that auto-escape output by default
- Conduct regular security reviews of all user-facing endpoints, particularly those accepting usernames or identifiers

## Variant hunting
Search for similar URL parameter reflection vulnerabilities in: other Imgur subdomains (api.imgur.com, www.imgur.com), other endpoints handling usernames or identifiers, any custom parameter that might be reflected in page content. Test with various User-Agent strings to identify platform-specific bypasses. Check comment sections, album descriptions, and any user-generated content fields that might reflect usernames.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The vulnerability specifically affects mobile browsers due to User-Agent detection differences. Desktop requests with standard User-Agent received a 302 redirect to the main site that resulted in a 404, suggesting the mobile site may have had different code paths or less mature security controls. The proof-of-concept used a prompt() dialog, but in a real attack, this would be replaced with credential-stealing or session-hijacking code. The vulnerability demonstrates the importance of maintaining consistent security across all application variants.

## Full report
<details><summary>Expand</summary>

There is a reflected XSS vulnerability in https://m.imgur.com as shown below:

https://m.imgur.com/account/testcatplzignore%22%3E%3Cimg%20src=x%20onerror=prompt(document.domain)%3E/messages

It appears that the username field in the url does not sanitize angle bracket characters on the mobile version of the site, allowing an attacker to execute arbitrary Javascript on the m.imgur.com domain.

I have attached several screenshots demonstrating this attack in the mobile context. While this attack affects devices loading the mobile site, I did notice that requests made with the standard User-Agent would issue a 302 redirect to the standard site, throwing a 404 error. This attack does execute on browsers that load the mobile version of the site.

The impact of this vulnerability is variable, depending on how it is used. An attacker could use this vulnerability to target a specific victim or post it on a site such as reddit, which is frequented by users of this application. If an authenticated imgur user could be tricked into clicking the link it may result in malicious JavaScript executing in the context of the user's session and could result in credential/session theft or other targeted attacks. This could result in multiple compromised accounts.

This vulnerability was tested in Google Chrome Version 51.0.2704.103 using the following User-Agent from the developer tools to load the mobile site:

User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36

To mitigate this vulnerability, consider encoding any angle brackets (< >) reflected back to the user when handling user input.

</details>

---
*Analysed by Claude on 2026-05-12*
