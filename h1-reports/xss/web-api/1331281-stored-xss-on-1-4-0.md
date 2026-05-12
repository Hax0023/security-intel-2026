# Stored XSS in ImpressCMS 1.4.0 - AdSense and CustomTag Modules

## Metadata
- **Source:** HackerOne
- **Report:** 1331281 | https://hackerone.com/reports/1331281
- **Submitted:** 2021-09-06
- **Reporter:** tehwinsam
- **Program:** ImpressCMS
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** CVE-2020-17551
- **Category:** web-api

## Summary
ImpressCMS 1.4.0 contains stored XSS vulnerabilities in the AdSense and CustomTag admin modules that fail to properly sanitize user input. An authenticated admin can inject malicious JavaScript payloads into the 'ID of the adsense tag' and 'Name' fields, which are then executed in the browsers of other users viewing these pages.

## Attack scenario
1. Attacker authenticates as admin user to ImpressCMS 1.4.0 instance
2. Attacker navigates to modules/system/admin.php?fct=adsense&op=mod&adsenseid=4
3. Attacker injects payload <script>alert('AppleBois');</script> in the 'ID of the adsense tag to display this ad' field and saves
4. Attacker alternatively navigates to modules/system/admin.php?fct=customtag&op=mod and injects same payload in the 'Name' field
5. When other admins or users access the affected admin pages, the malicious script executes in their browser context
6. Attacker's JavaScript can steal session cookies, credentials, or perform unauthorized actions as the victim user

## Root cause
User-supplied input from the AdSense ID and CustomTag Name fields is stored in the database without sanitization and rendered in HTTP responses without proper HTML encoding, allowing arbitrary JavaScript execution

## Attacker mindset
Compromised admin account or insider threat seeking privilege escalation and lateral movement by capturing credentials of other administrators through cookie/session theft or keystroke logging via injected scripts

## Defensive takeaways
- Implement strict input validation and sanitization on all admin forms using allowlists for expected formats
- Apply context-aware output encoding (HTML entity encoding) when rendering user-controlled data in HTML context
- Utilize templating engines with automatic escaping enabled by default
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Apply principle of least privilege - restrict admin module access to necessary personnel only
- Conduct regular security code reviews focusing on data flow from input to output
- Implement automated SAST tools to detect XSS vulnerabilities during development

## Variant hunting
Search for similar patterns in other ImpressCMS modules accepting user input (news, articles, blocks, etc.). Check modules/system/admin.php for other ?fct= parameters that may accept user-controlled data without encoding. Review any custom field or metadata inputs across the system.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing: Spearphishing Link
- T1555 - Credentials from Password Stores
- T1539 - Steal Web Session Cookie

## Notes
CVE-2020-17551 assigned. Fixed in ImpressCMS 1.4.1. Issue originated on GitHub (AppleBois, Jun 2020), reported to HackerOne later. AdSense and CustomTag modules both vulnerable to same class of vulnerability, suggesting systemic lack of output encoding across admin interface. Admin-level access required for exploitation, limiting exposure but critical if admin accounts are compromised.

## Full report
<details><summary>Expand</summary>

## Summary:
The hacker (AppleBois) on Jun 19, 2020 has raise this Stored Stored Cross Site Scripting on GitHub and it has fixed on Jul 7, 2020. The hacker now raise the issue to Hackerone. Furthermore, this issue can now tracked under CVE-2020-17551.

## ImpressCMS branch :
[1.4.0 ]

## Steps To Reproduce:
  1. Navigate to modules/system/admin.php?fct=adsense&op=mod&adsenseid=4
  2. Look for the Textbar `"ID of the [adsense tag to display this ad]"`
  3. Input XSS PAYLOAD `<script>alert('AppleBois');</script>`

  1. Navigate to /modules/system/admin.php?fct=customtag&op=mod
  2. Look for the Textbar `"Name"`
  3. Input XSS PAYLOAD `<script>alert('AppleBois');</script>`

## Suggestions to mitigate or resolve the issue:
1 . Filter input on arrival. At the point where user input is received, filter as strictly as possible based on what is expected or valid input.
2 . Encode data on output. At the point where user-controllable data is output in HTTP responses, encode the output to prevent it from being interpreted as active content. Depending on the output context, this might require applying combinations of HTML, URL, JavaScript, and CSS encoding.

  Additional Reference
https://github.com/ImpressCMS/impresscms/issues/659
https://medium.com/@tehwinsam/impresscms-1-4-0-3aaf1825e6d5
https://nvd.nist.gov/vuln/detail/CVE-2020-17551
https://www.impresscms.org/modules/news/article.php?article_id=1034&title=impresscms-1-4-1-security-and-maintenance-release

## Impact

The impact of XSS, it could allow an attacker to execute malicious JavaScript so that the Cookies can send to attacker web via GET Method which could turn into account hijacking

</details>

---
*Analysed by Claude on 2026-05-12*
