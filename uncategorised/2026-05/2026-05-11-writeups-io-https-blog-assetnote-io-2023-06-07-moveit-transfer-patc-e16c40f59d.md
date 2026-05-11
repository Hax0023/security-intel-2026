# MOVEit Transfer Patch Diff Analysis - CVE-2023-34362

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Progress Software MOVEit Transfer
- **Bounty:** Unknown
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
Analysis of security patch differences in MOVEit Transfer revealing critical SQL injection vulnerability in file transfer functionality. The vulnerability allows unauthenticated attackers to execute arbitrary SQL commands and achieve remote code execution through improper input validation in transfer endpoints.

## Attack scenario (step by step)
1. Attacker identifies MOVEit Transfer instance exposed on internet
2. Attacker analyzes public patch files to understand vulnerability nature
3. Attacker crafts malicious SQL payload targeting file transfer parameters
4. Attacker sends HTTP request with injected SQL to vulnerable endpoint without authentication
5. SQL injection executes arbitrary queries allowing database access or command execution
6. Attacker achieves remote code execution and gains system access

## Root cause
Insufficient input validation and improper parameterization of SQL queries in MOVEit Transfer's file transfer handling functionality, allowing direct SQL injection through HTTP parameters

## Attacker mindset
Reverse engineer security patches by comparing patched vs unpatched versions to identify exact vulnerability location, then develop weaponized exploit before widespread patching occurs

## Defensive takeaways
- Implement strict input validation and use parameterized queries/prepared statements for all database operations
- Apply security patches immediately upon release, especially for critical vulnerabilities
- Implement Web Application Firewalls (WAF) with SQL injection detection rules
- Monitor file transfer applications for suspicious SQL syntax in logs
- Restrict network access to file transfer applications behind authentication layers
- Conduct security code reviews focusing on query construction patterns

## Variant hunting
Search for similar SQL injection patterns in other Progress Software products (Moveit Automation, MOVEit Managed File Transfer), other file transfer services (Accellion, Tresorit), and web applications using similar parameter-to-query construction patterns without parameterization

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1190 - Exploit Public-Facing Application
- T1505 - Server Software Component
- T1059 - Command and Scripting Interpreter
- T1548 - Abuse Elevation Control Mechanism

## Notes
Page content not fully accessible - appears to be blog index rather than full writeup. CVE-2023-34362 was a critical SQL injection in MOVEit Transfer that was actively exploited. The patch diff analysis approach is valuable for understanding vulnerability mechanics post-disclosure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
