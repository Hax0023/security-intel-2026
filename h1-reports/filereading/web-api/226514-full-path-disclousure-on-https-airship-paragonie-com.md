# Full Path Disclosure via Unhandled Exception on https://airship.paragonie.com

## Metadata
- **Source:** HackerOne
- **Report:** 226514 | https://hackerone.com/reports/226514
- **Submitted:** 2017-05-06
- **Reporter:** ruisilva
- **Program:** Paragon Initiative Enterprises (Airship Framework)
- **Bounty:** undisclosed
- **Severity:** low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Exception Handling Error
- **CVEs:** None
- **Category:** web-api

## Summary
An unhandled exception in the routing mechanism exposes the full server file path structure when accessing non-existent cabin classes. The error message reveals sensitive directory information including /var/www/paragonie/ and framework structure, allowing attackers to map internal application architecture.

## Attack scenario
1. Attacker accesses https://airship.paragonie.com/my/cabins endpoint expecting a valid cabin
2. Router attempts to instantiate class '\ParagonIE\Airship\Cabins' which does not exist
3. Exception is thrown but not properly caught or sanitized before output
4. Raw stack trace is displayed in HTTP response containing full filesystem paths
5. Attacker extracts absolute path information: /var/www/paragonie/framework/, /var/www/paragonie/public_html/
6. Attacker uses path disclosure to identify application structure and potential entry points for further exploitation

## Root cause
Missing or inadequate exception handling in the Router class that fails to catch ClassNotFoundException or similar errors. Error display is not sanitized for production environments, allowing detailed stack traces with absolute filesystem paths to be rendered to unauthenticated users.

## Attacker mindset
Information gathering during reconnaissance phase. Path disclosure is a low-impact but valuable vulnerability for mapping internal structure, identifying framework versions, and planning subsequent attacks. Useful as part of OSINT pipeline for larger campaigns.

## Defensive takeaways
- Implement global exception handlers that catch and sanitize error messages before output
- Configure error reporting to log detailed traces server-side while displaying generic messages to users
- Use relative paths or symbolic identifiers internally instead of absolute filesystem paths in error messages
- Disable debug mode in production environments; ensure display_errors is off
- Implement custom error pages that do not leak framework or path information
- Validate routing parameters and return proper HTTP 404 responses instead of revealing class instantiation attempts
- Use web application firewalls to strip path information from error responses

## Variant hunting
Search for similar path disclosure in other Paragon Initiative frameworks (Paseto, Halite, etc.). Check for unhandled exceptions in class loaders, autoloaders, and dependency injection containers. Look for database connection errors, file inclusion failures, or configuration loading that might expose paths. Test custom routing implementations and plugin systems for similar issues.

## MITRE ATT&CK
- T1018 - Remote System Discovery (reconnaissance via path enumeration)
- T1087 - Account Discovery (mapping application structure)
- T1580 - Cloud Infrastructure Discovery (identifying framework components)

## Notes
Low severity finding but valuable for security hardening. Paragon Initiative Enterprises is known for strong cryptographic libraries (libsodium bindings), so this disclosure is somewhat surprising. The specific path /var/www/paragonie/ suggests shared hosting or standardized deployment. This vulnerability likely already patched in current versions. Classic example of information disclosure vulnerability that should be caught during secure SDLC processes.

## Full report
<details><summary>Expand</summary>

Hi , i found an full path disclousure vulnerability on https://airship.paragonie.com

For reproduce this vulnerability go to: https://airship.paragonie.com/my/cabins
You will see something like this : Class '\ParagonIE\Airship\Cabins' not found #0 /var/www/paragonie/framework/Router.php(236): ParagonIE\Tuner\Router::passArgs(Array, Array, Array) #1 /var/www/paragonie/framework/Router.php(150): ParagonIE\Tuner\Router::serve(Array, Array, Array) #2 /var/www/paragonie/framework/Router.php(107): ParagonIE\Tuner\Router::site(Array) #3 /var/www/paragonie/public_html/index.php(26): ParagonIE\Tuner\Router::route(Array) #4 {main}

See attached file 
Thanks 

</details>

---
*Analysed by Claude on 2026-05-24*
