# Apache HTTP Server mod_rewrite Path Traversal via Improper Output Escaping (CVE-2024-38475)

## Metadata
- **Source:** HackerOne
- **Report:** 2585378 | https://hackerone.com/reports/2585378
- **Submitted:** 2024-07-03
- **Reporter:** orange
- **Program:** Apache HTTP Server
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Improper Output Escaping, Arbitrary File Access, Code Execution
- **CVEs:** CVE-2024-38475
- **Category:** uncategorised

## Summary
Apache HTTP Server 2.4.59 and earlier contains a vulnerability in mod_rewrite where improper escaping of output allows attackers to map URLs to unintended filesystem locations when backreferences or variables are used as the first segment of rewrites. This can result in unauthorized access to files not directly reachable via URL, leading to source code disclosure or remote code execution.

## Attack scenario
1. Attacker identifies a vulnerable RewriteRule using backreferences or variables in the substitution target as the first segment
2. Attacker crafts a malicious URL containing path traversal sequences that get captured by the RewriteRule pattern
3. The mod_rewrite module fails to properly escape the substitution output, allowing path traversal sequences to be preserved
4. The rewrite rule maps the malicious URL to a filesystem path outside the intended directory structure
5. Attacker gains access to sensitive files (configuration files, source code, application files) or executable paths
6. If writable, attacker could potentially execute arbitrary code through uploaded or accessible script files

## Root cause
Insufficient input escaping/output encoding in mod_rewrite when backreferences or variables are used as the first segment of the substitution target. The module fails to sanitize path traversal sequences (../, etc.) in the substituted values before mapping them to filesystem paths.

## Attacker mindset
An attacker exploiting this would leverage known RewriteRule patterns in Apache configurations to bypass URL-based access controls. They would probe for unintended paths accessible through path traversal, targeting configuration files, source code repositories, or executable locations to achieve information disclosure or code execution.

## Defensive takeaways
- Update Apache HTTP Server to patched versions (2.4.60+)
- Audit existing RewriteRules that use backreferences or variables as the first segment of substitutions
- Apply strict input validation and sanitization for any dynamic components in rewrite targets
- Use the UnsafePrefixStat flag only after thoroughly validating that substitutions are properly constrained
- Implement defense-in-depth with filesystem permissions to restrict access to sensitive files regardless of URL mapping
- Use RewriteRule anchors and specific patterns to limit what can be captured in backreferences
- Consider using RewriteCond directives to whitelist safe substitution patterns
- Monitor logs for unusual rewrite patterns or path traversal attempts

## Variant hunting
Look for similar path traversal vulnerabilities in other Apache modules that perform URL-to-filesystem mapping (mod_alias, mod_userdir). Check for improper escaping in any module handling backreferences or variable substitution. Examine other web servers' rewrite engines (nginx, IIS) for similar output encoding gaps in dynamic path construction.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1005 - Data from Local System
- T1552 - Unsecured Credentials
- T1005 - Data from Local System

## Notes
CVE assigned July 1, 2024. This is a server-context configuration vulnerability requiring specific RewriteRule patterns. The vulnerability requires the attacker to understand the target's rewrite rules, making reconnaissance important. The UnsafePrefixStat mitigation flag indicates Apache's acknowledgment that some legitimate configurations may be affected by the fix.

## Full report
<details><summary>Expand</summary>

I reported this vulnerability through the official Apache HTTP Server security email on April 1, 2024, and received a fix along with a CVE number on July 1, 2024. You can check detailed information from there:
> https://httpd.apache.org/security/vulnerabilities_24.html

## Impact

Improper escaping of output in mod_rewrite in Apache HTTP Server 2.4.59 and earlier allows an attacker to map URLs to filesystem locations that are permitted to be served by the server but are not intentionally/directly reachable by any URL, resulting in code execution or source code disclosure.

Substitutions in server context that use a backreferences or variables as the first segment of the substitution are affected. Some unsafe RewiteRules will be broken by this change and the rewrite flag "UnsafePrefixStat" can be used to opt back in once ensuring the substitution is appropriately constrained.

</details>

---
*Analysed by Claude on 2026-05-24*
