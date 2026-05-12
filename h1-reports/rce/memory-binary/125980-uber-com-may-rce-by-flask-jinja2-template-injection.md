# Remote Code Execution via Flask Jinja2 Server-Side Template Injection in Uber Profile Name

## Metadata
- **Source:** HackerOne
- **Report:** 125980 | https://hackerone.com/reports/125980
- **Submitted:** 2016-03-25
- **Reporter:** orange
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Server-Side Template Injection (SSTI), Remote Code Execution, Insufficient Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A Flask Jinja2 template injection vulnerability was discovered in rider.uber.com where user-controlled profile names were directly rendered in email templates without proper sanitization. Attackers could inject Jinja2 template expressions to achieve arbitrary code execution, though exploitation was constrained by a length limit on the name field.

## Attack scenario
1. Attacker sets their profile name to a Jinja2 template expression like {{ '7'*7 }}
2. Attacker modifies account profile through rider.uber.com web interface
3. System generates 'account updated' notification email to attacker
4. Email template renders the profile name field without escaping Jinja2 syntax
5. Template expression is evaluated server-side, executing arbitrary Python code
6. Attacker exfiltrates data or escalates attack through Python object introspection (e.g., accessing __subclasses__, __base__)

## Root cause
User-supplied profile name input was directly embedded into Flask/Jinja2 email templates without proper escaping or sandboxing. The application trusted user input in a context where template evaluation occurs, allowing expression injection.

## Attacker mindset
Opportunistic vulnerability discovery - researcher identified that user input reflected in email notifications could contain template syntax. Limited by length constraints, they demonstrated proof-of-concept through expression evaluation rather than pursuing full RCE, showing responsible disclosure approach.

## Defensive takeaways
- Always escape/sanitize user input before rendering in template contexts, especially emails
- Use Jinja2 auto-escaping enabled by default in templates: autoescape=True
- Implement strict input validation and sanitization on profile fields - reject or strip template syntax characters
- Apply principle of least privilege - use sandbox mode or restricted Jinja2 environment for user-controlled content
- Implement content security for email rendering - parse templates with user data as context variables, never as template code
- Add length limits and character whitelisting on user profile fields
- Conduct security code review of all email template generation code
- Implement WAF rules to detect common SSTI/template injection patterns

## Variant hunting
Search for other user input fields rendered in emails (bio, address, preferences)
Test all templated outputs across Uber platform (receipts, confirmations, notifications)
Check for similar patterns in driver app or other Uber services
Investigate other template engines (Jinja, Mako, etc.) used in codebase
Test if length limits can be bypassed through encoding or chunking
Attempt polyglot payloads targeting multiple template engines

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1203: Exploitation for Client Execution

## Notes
This report demonstrates a critical but length-constrained SSTI vulnerability. While full RCE was limited by field length restrictions, the ability to execute arbitrary Python code (accessing __subclasses__, performing arithmetic) proves the vulnerability is exploitable. The researcher responsibly disclosed without attempting bypass techniques. This is a classic example of insufficient input validation in templating contexts.

## Full report
<details><summary>Expand</summary>

Hi, Uber Security Team

I found an RCE in rider.uber.com.
First, if you change your profile name to {{ '7'*7 }}, and you will receive a mail
"Your Uber account information has been updated"
sent by support@uber.com

And in mail body, you can see your name become '7777777'

This is a vulnerability about Flask Template Engine(Jinja2) Injection , more detail can be seen in these blogs
https://nvisium.com/blog/2016/03/09/exploring-ssti-in-flask-jinja2/
https://nvisium.com/blog/2016/03/11/exploring-ssti-in-flask-jinja2-part-ii/

I think it can be a Remote Code Execution vulnerability but there is a length limit :(
But I still can "write" some Python code in "name" filed, there are more examples in attachments and bellow are my payloads

{{ '7'*7 }}
{{ [].__class__.__base__.__subclasses__() }} # get all classes
{{''.__class__.mro()[1].__subclasses__()}} 
{%for c in [1,2,3] %}{{c,c,c}}{% endfor %}
...

Thanks for your patience for reading my report. : )

</details>

---
*Analysed by Claude on 2026-05-11*
