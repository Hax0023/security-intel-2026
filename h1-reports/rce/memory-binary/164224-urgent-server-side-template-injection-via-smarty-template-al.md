# Server Side Template Injection (SSTI) in Smarty Template Engine Leads to Remote Code Execution

## Metadata
- **Source:** HackerOne
- **Report:** 164224 | https://hackerone.com/reports/164224
- **Submitted:** 2016-08-29
- **Reporter:** yaworsk
- **Program:** HackerOne (specific program not named in report)
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln:** Server Side Template Injection (SSTI), Remote Code Execution (RCE), Arbitrary Code Execution, Information Disclosure
- **CVEs:** None
- **Category:** memory-binary

## Summary
The application uses Smarty templating engine to process user-supplied input from profile fields (firstname, lastname, nickname) without proper sanitization or escaping. Attackers can inject Smarty template syntax including {php} tags to execute arbitrary PHP code, leading to complete server compromise and sensitive file access.

## Attack scenario
1. Attacker identifies the application uses Smarty by injecting test payload {7*7} and observing template evaluation in email responses
2. Attacker confirms Smarty version and {php} tag support by injecting {$smarty.version} and {php}print 'test'{/php}
3. Attacker crafts malicious payload using {php} tags containing PHP functions like file_get_contents('/etc/passwd')
4. Attacker injects payload into profile fields (firstname, lastname, or nickname) during profile edit
5. Attacker triggers template rendering by inviting another user, causing email generation with injected payload
6. Attacker receives email with executed code output, successfully extracting sensitive system files and confirming RCE capability

## Root cause
User-supplied input from profile fields is directly embedded into Smarty templates and processed without sanitization, validation, or disabling dangerous template functions. The {php} tag processor is enabled in Smarty configuration, allowing direct PHP code execution within templates.

## Attacker mindset
Methodical reconnaissance through incremental payload testing (math expressions → version detection → code execution). Attacker demonstrated restraint by not creating webshells, instead reporting vulnerability responsibly while proving impact through file disclosure.

## Defensive takeaways
- Disable {php} tag processing in Smarty configuration immediately (set allow_php_tag = false)
- Never process user input directly as template code; use separate data structures for template variables
- Implement strict input validation and sanitization for all user-supplied data before template processing
- Use parameterized/safe template engines or template sandboxing to prevent injection
- Apply principle of least privilege to template processing - disable all unnecessary functions
- Implement output encoding appropriate to context (HTML, JavaScript, etc.)
- Deploy Web Application Firewall (WAF) rules to detect and block template injection patterns
- Conduct security code review of all template implementations
- Implement Content Security Policy headers to limit damage from template injections

## Variant hunting
Search for other user-input fields processed through Smarty (comments, descriptions, custom fields, form submissions). Check for similar SSTI vulnerabilities in other templating engines (Twig, Jinja2, FreeMarker, Velocity). Look for secondary template processing in email generation, PDF creation, or document rendering features.

## MITRE ATT&CK
- T1190
- T1059
- T1587.001
- T1083
- T1040

## Notes
Classic high-impact SSTI vulnerability with clear exploitation path. The attacker's methodical approach demonstrates good security research methodology. Email functionality as attack vector is common in SSTI bugs. Report predates significant Smarty security improvements. Smarty {php} tags were deprecated and eventually removed in Smarty 3.1+ specifically due to such vulnerabilities.

## Full report
<details><summary>Expand</summary>

Hi All,
I've found an issue which has allowed me to execute file_get_contents and extract your /etc/passwd file.

##Description
It appears as though you are using smarty on the backend for templating. Entering a malicious payload as my firstname, lastname and nickname and then inviting a user to join the site results in the code being executed.

To start, I began with the payload {7*7} and received a template error in the email I received {F115749} Recognizing the injection, I then was able to confirm the version of smarty used via {$smarty.version} {F115750} Next I was able to test {php} tags by using ```{php}print "Hello"{/php}``` {F115751}. Finally I used file_get_contents to begin extracting the etc/pass file ```{php}$s = file_get_contents('/etc/passwd',NULL, NULL, 0, 100); var_dump($s);{/php}``` {F115752}

##Steps to reproduce
1. Edit your profile
2. Add the payload ```{php}$s = file_get_contents('/etc/passwd',NULL, NULL, 0, 100); var_dump($s);{/php}``` as your first name, last name and user name (I'm not sure which field is vulnerable)
3. Invite a friend using another email of yours
4. View the email and you will see part of the etc file dumped

##Vulnerability
Since the {php} tags are being parsed and executed, we can execute php functions. In this case, you'll see I'm able to extract the etc/passwd file. While I haven't tried, an attacker can more than likely create a shell on the server.

Please let me know if you have any questions.
Pete

</details>

---
*Analysed by Claude on 2026-05-11*
