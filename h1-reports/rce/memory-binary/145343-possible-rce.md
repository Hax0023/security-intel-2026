# Possible RCE via Dynamic Function Call in LDAP Wizard

## Metadata
- **Source:** HackerOne
- **Report:** 145343 | https://hackerone.com/reports/145343
- **Submitted:** 2016-06-17
- **Reporter:** paulos__
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution (RCE), Unsafe Dynamic Function Call, Insufficient Input Validation, Unsafe Object Property Access
- **CVEs:** None
- **Category:** memory-binary

## Summary
A critical RCE vulnerability exists in /apps/user_ldap/ajax/wizard.php where user-controlled POST parameters are used to dynamically invoke functions on the $wizard object without proper validation. An attacker can execute arbitrary PHP functions by crafting a malicious POST request with a function name in the 'action' parameter.

## Attack scenario
1. Attacker identifies that the 'action' POST parameter directly controls which method is called on the $wizard object
2. Attacker discovers that 'ldap_test_loginname' parameter is passed as an argument to the dynamically called function
3. Attacker crafts a POST request with action=system&ldap_test_loginname=whoami to test code execution
4. Attacker leverages PHP built-in functions or magic methods (__wakeup, __construct) to achieve arbitrary code execution
5. Attacker executes system commands or includes malicious code to compromise the server
6. Attacker gains full control over the Nextcloud instance and underlying system

## Root cause
The application uses unsanitized user input from $_POST['action'] as a dynamic function/method name without whitelist validation or type checking. This is combined with passing unsanitized $_POST['ldap_test_loginname'] directly as a parameter, creating a two-stage exploitation vector.

## Attacker mindset
An attacker would recognize this as a classic dynamic function invocation vulnerability. They would first enumerate available methods on the $wizard object or try common PHP functions (eval, system, exec, passthru). If direct function calls fail, they would explore object deserialization or magic method exploitation to achieve RCE.

## Defensive takeaways
- Never use user input directly as function/method names - implement strict whitelist of allowed actions
- Validate and sanitize all user inputs, especially those used in dynamic code execution contexts
- Use switch/case statements or pre-defined action maps instead of dynamic function calls
- Implement proper access controls and authentication checks before executing sensitive operations
- Disable dangerous PHP functions (eval, system, exec, passthru, shell_exec) if not required
- Use static analysis tools to detect dynamic function calls in security-sensitive code paths
- Implement rate limiting and logging for LDAP wizard operations

## Variant hunting
Search for similar patterns in other AJAX endpoints handling 'action' parameters. Check user_shibboleth, user_sql, and other authentication modules. Look for any use of $_POST/$_GET variables in method_exists(), call_user_func(), or $object->$variable() constructs. Examine all wizard.php and setup.php files across Nextcloud codebase.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1202 - Indirect Command Execution

## Notes
The researcher explicitly states they didn't fully test the vulnerability but provided strong theoretical analysis. The vulnerability appears to be in the LDAP app's AJAX endpoint which may be accessible to unauthenticated users depending on Nextcloud configuration. The mention of arbitrary object wakeup and constructor exploitation suggests potential for even more severe exploitation chains. This should be treated as a critical issue requiring immediate patching.

## Full report
<details><summary>Expand</summary>

Hello,

I just quickly took a glance, I am not entirely sure or didn't get a chance to test it but it seems there are some serious bugs.

In */apps/user_ldap/ajax/wizard.php*: 
```php
36: $action = (string)$_POST['action']; 
```
and it is called in multiple places. including line 83 & 99. one being `$action($loginName);` & since 
`$loginName` is defined as:

```php
$loginName = $_POST['ldap_test_loginname'];
```
would mean an RCE is achievable when $result is called
```php
$result = $wizard->$action($loginName);
``` 
 
This is because userinput is used as dynamic function name. ergo, arbitrary functions may be called.

All an attacker have to send is a POST request with action parameter containing a function name like action=eval&ldap_test_loginname=stufftoexecute

There is a very little chance the $wizard will stop this because arbritary wakeup & constract objects may be exploitable. like I said, I didn't get a chance to test this but seems fairly feasible. please think about it and let me know.

Thanks,
P


</details>

---
*Analysed by Claude on 2026-05-12*
