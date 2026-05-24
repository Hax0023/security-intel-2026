# Denial of Service in Strapi Framework via Argument Injection in Plugin Installation/Uninstallation

## Metadata
- **Source:** HackerOne
- **Report:** 768574 | https://hackerone.com/reports/768574
- **Submitted:** 2020-01-05
- **Reporter:** princechaddha
- **Program:** Strapi
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Argument Injection, Improper Input Validation, Denial of Service
- **CVEs:** CVE-2020-8123
- **Category:** memory-binary

## Summary
The Strapi admin panel's installPlugin and uninstallPlugin handlers use insufficient regex validation (allowing hyphen characters) before passing user input to the execa() function for npm commands. An attacker can inject npm arguments like '-h', '--help', '-v', or '--version' to trigger unintended server restarts without actually installing or uninstalling valid plugins.

## Attack scenario
1. Attacker accesses the Strapi admin marketplace at /admin/marketplace
2. Attacker initiates a plugin download request and intercepts it with a proxy tool
3. Attacker modifies the 'plugin' parameter from a legitimate plugin name to '-h', '--help', '-v', or '--version'
4. The input passes the insufficient regex validation /^[A-Za-z0-9_-]+$/ which allows hyphens
5. The malicious argument is passed to npm command: 'npm run strapi -- install -h' which triggers npm help output
6. Strapi's strapi.reload() function executes unconditionally, restarting the server and causing denial of service

## Root cause
The regex pattern /^[A-Za-z0-9_-]+$/ was intended to prevent command injection but inadvertently allows hyphen characters, which are valid npm command-line option prefixes. The code subsequently calls strapi.reload() without verifying that a legitimate plugin was actually processed, triggering server restart on any npm argument injection.

## Attacker mindset
An attacker seeks to disrupt service availability by discovering that the input validation's allowlist for hyphens creates an unintended bypass. By understanding npm's argument structure, the attacker realizes that even failed plugin operations trigger a mandatory reload, enabling trivial DoS without authentication or complex payloads.

## Defensive takeaways
- Use positive allowlists strictly matching expected plugin naming conventions (e.g., alphanumeric, underscores only - no hyphens) or validate against a registry of known plugins
- Separate input validation logic from business logic; validate that a plugin was successfully installed/uninstalled before calling reload()
- Implement exit code checking from execa() to ensure the npm command succeeded before triggering side effects
- Consider using a whitelist of approved plugins rather than regex on user-supplied names
- Add rate limiting or authentication checks on marketplace operations to mitigate DoS impact
- Log and alert on unusual plugin installation patterns or npm argument injection attempts

## Variant hunting
Test other special characters in allowlist regex (dots, slashes, colons) in similar plugin/module handlers across the codebase
Search for other execa()/spawn() calls preceded by insufficient regex validation patterns
Audit npm script handlers in package.json for unintended side effects from argument injection
Check if similar patterns exist in theme installation/uninstallation handlers
Review any user-supplied input passed to shell commands with character-based whitelisting

## MITRE ATT&CK
- T1190
- T1485
- T1561

## Notes
The reporter correctly identified that while server restart is intended behavior for valid plugin operations, the insufficient validation enables forced restarts without legitimate plugin activity. The fix should be layered: stricter regex (no hyphens), validation that the plugin exists and was processed successfully, and conditional reload() execution. This is a lower-severity DoS since it requires admin panel access but effectively requires no authentication if admin panel is exposed. The issue demonstrates how security controls meant to prevent code injection can have unintended bypasses when design intentions are not fully considered.

## Full report
<details><summary>Expand</summary>

I would like to report Denial Of Service in Strapi Framework.It allows attacker to force restart the server using argument injection.

# Module

**module name:** strapi
**version:** 3.0.0-beta.18.3 and earlier
**npm page:** `https://www.npmjs.com/package/strapi`

## Module Description

> The Strapi HTTP layer sits on top of Koa. Its ensemble of small modules work together to provide simplicity, maintainability, and structural conventions to Node.js applications.

## Module Stats

[1] weekly downloads 8,508

# Vulnerability

## Vulnerability Description

>  While reviewing source code i found that "installPlugin" and "uninstallPlugin" handler functions for the admin panel (https://github.com/strapi/strapi/blob/master/packages/strapi-admin/controllers/Admin.js) is using regex on line 70 & 110 i.e `/^[A-Za-z0-9_-]+$/` before passing user input to `execa()` on line 77 & 117 to prevent command injection but the regex allows `-` character.Using this attacker can pass valid arguments like "-h" "-v" "--help" which will add after the command `npm run strapi -- install <user-input>` & `npm run strapi -- uninstall <user-input>` and leads the serve to restart.

## Steps To Reproduce:

> Create a new strapi project and start the server by using yarn.
> Login to admin panel by visiting http://172.16.129.155:1337/admin/
> Goto http://172.16.129.155:1337/admin/marketplace & click on download while intercepting the request.
> Change value of plugin to "-h",  "--help", "-v" or "--version"
> Check console the server will restart everytime we send the request using valid strapi arguments. 

## Patch

> Instead of `strapi.reload();` after executing the command there should be a check to validate if a valid plugin is installed or uninstalled.Many user uses `_` & `-` in plugin names so blacklisting the above 4 inputs will fix this issue instead of removing `_` & `-` from the regex

# Wrap up

> Select Y or N for the following statements:

- I contacted the maintainer to let them know: [Y/N] N
- I opened an issue in the related repository: [Y/N] N


#####Also, It looks like an intented behaviour to restart server after uninstalling or installing a valid plugin but by just passing the valid arguments we can restart the server.

## Impact

Attacker can cause the server to restart even without installing or uninstalling a valid plugin.

</details>

---
*Analysed by Claude on 2026-05-24*
