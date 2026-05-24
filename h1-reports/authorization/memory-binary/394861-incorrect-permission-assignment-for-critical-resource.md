# Incorrect Permission Assignment for Critical Resource - NULL DACL in Named Pipe Security Descriptor

## Metadata
- **Source:** HackerOne
- **Report:** 394861 | https://hackerone.com/reports/394861
- **Submitted:** 2018-08-14
- **Reporter:** dhiraj-mishra
- **Program:** MariaDB
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Improper Access Control, Insecure Permission Assignment, Windows Security Descriptor Misconfiguration
- **CVEs:** None
- **Category:** memory-binary

## Summary
MariaDB's named pipe implementation in mysqld.cc creates a NULL DACL (Discretionary Access Control List) when setting up the security descriptor, which allows unauthenticated access to the pipe. An attacker can exploit this by manipulating permissions to deny all access, including administrator access, potentially leading to privilege escalation or denial of service.

## Attack scenario
1. Attacker identifies MariaDB named pipe on Windows system with NULL DACL
2. Attacker gains local system access and connects to the exposed named pipe
3. Attacker modifies the security descriptor to set restrictive permissions (Everyone: Deny All)
4. Legitimate administrators and services lose access to the MariaDB named pipe
5. Attacker leverages elevated privileges or escalates to administrator level
6. System experiences denial of service or attacker achieves privilege escalation

## Root cause
The SetSecurityDescriptorDacl() function call with NULL DACL parameter creates an empty access control list, which by default grants full access to all users. The code at /server/blob/10.3/sql/mysqld.cc#L2761 fails to define explicit access control entries, violating secure coding practices for Windows named pipes.

## Attacker mindset
Local privilege escalation through Windows security descriptor manipulation; targeting database service access control to gain elevated privileges or deny service availability to administrators.

## Defensive takeaways
- Never use NULL DACLs for critical resources - always explicitly define access control entries
- Implement restrictive security descriptors with explicit allow/deny rules for named pipes
- Use least privilege principle: restrict pipe access to specific service accounts and administrators only
- Conduct mandatory security code review for all Windows API calls related to security descriptors
- Implement automated static analysis tools to detect NULL DACL patterns
- Test permission inheritance and ACL enforcement during development
- Document security requirements for inter-process communication mechanisms

## Variant hunting
Search for other SetSecurityDescriptorDacl() calls with NULL parameters in codebase
Identify other named pipes created by MariaDB or dependent services
Check for similar issues in CreateNamedPipe() implementations without proper SECURITY_ATTRIBUTES
Review other Windows services in codebase that use security descriptors
Audit registry permissions and other resource ACLs for similar misconfigurations

## MITRE ATT&CK
- T1548.001 - Abuse Elevation Control Mechanism: Setuid and Setgid
- T1548.002 - Abuse Elevation Control Mechanism: Bypass User Access Control
- T1547.014 - Boot or Logon Autostart Execution: Active Setup
- T1543.003 - Create or Modify System Process: Windows Service

## Notes
This vulnerability was identified through code review rather than active exploitation. The issue affects Windows installations of MariaDB 10.3 and potentially other versions. The fix requires proper DACL configuration restricting access to specific security principals. Coordinate with vendor before disclosure; MariaDB security team acknowledged and planned fix in subsequent release.

## Full report
<details><summary>Expand</summary>

Dear Team, 

Product Affected: https://github.com/MariaDB/server

File:
 /server/blob/10.3/sql/mysqld.cc#L2761

```
}
    if (!SetSecurityDescriptorDacl(&sdPipeDescriptor, TRUE, NULL, FALSE))
{
```

This was purely identified on code review, Never create NULL ACLs.

A mail was sent to security@mariadb.org and MariaDB team is working on this and a fix will be pushed in next version, attached mail headers for your reference.

## Impact

An attacker can set it to Everyone (Deny All  Access), which would even forbid administrator access and may lead to privilege escalation.

</details>

---
*Analysed by Claude on 2026-05-24*
