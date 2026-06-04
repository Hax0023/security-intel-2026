# Auto-GPT Remote Code Execution and Docker Escape via Indirect Prompt Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Indirect Prompt Injection, Arbitrary Code Execution, Docker Escape, Path Traversal, Console Injection, Privilege Escalation
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
An attacker can leverage indirect prompt injection to trick Auto-GPT into executing arbitrary code by injecting malicious instructions into attacker-controlled websites that Auto-GPT processes. The vulnerability chain includes bypassing user approval through console color-coding tricks, achieving arbitrary code execution, and escaping the Docker container to the host system through a trivial escape vector.

## Attack scenario (step by step)
1. Attacker hosts a malicious website containing color-coded console messages or crafted text that appears benign to users
2. Attacker tricks Auto-GPT user into performing a seemingly harmless task like summarizing content from the attacker's website
3. Auto-GPT fetches and processes the attacker-controlled content, which is then interpreted by the LLM as legitimate instructions
4. Through prompt injection, the LLM is convinced to execute malicious commands (e.g., python code execution, file operations)
5. In non-continuous mode, attacker-injected console messages or misleading LLM statements trick the user into approving malicious commands
6. Once code execution is achieved, attacker uses path traversal (non-docker) or trivial docker escape to break out of sandbox and compromise host system

## Root cause
Auto-GPT processes attacker-controlled external content (from websites) without sufficient sanitization before feeding it to the LLM's decision-making logic. The LLM, despite its sophistication, can be confused by indirect prompts embedded in data it processes. Additionally, the sandwich layer between LLM output and execution (user approval in non-continuous mode) can be bypassed through console injection and misleading statements. The docker and non-docker sandboxes contained insufficient isolation boundaries.

## Attacker mindset
An attacker would recognize that LLMs can be manipulated not just through direct prompts but through indirect injection via data they process. They would identify that user approval mechanisms rely on correct interpretation of console output and can be circumvented through visual tricks. They would exploit the trust users place in reviewing LLM-suggested actions, knowing users cannot easily verify complex command chains. Finally, they would target the weak containerization and path traversal protections as trivial post-exploitation escape mechanisms.

## Defensive takeaways
- Implement strict input sanitization and validation for all externally-sourced content before LLM processing
- Add explicit content-type validation and HTML/markup stripping for processed web content
- Use sandboxing mechanisms that are isolated from user approval workflows (console output should not be the source of truth for approval decisions)
- Implement cryptographic verification or digital signatures for sensitive command approvals
- Use properly-configured AppArmor, SELinux, or seccomp in Docker to prevent trivial container escapes
- Implement strict file system boundaries and prevent path traversal through chroot/pivot_root or read-only mounts
- Log all LLM reasoning and command decisions for audit trails and anomaly detection
- Disable or heavily restrict dangerous commands like arbitrary code execution by default
- Implement separate execution contexts with capability dropping to prevent privilege escalation
- Add anomaly detection for unusual command chains or when LLM reverses previous decisions

## Variant hunting
Researchers should examine: (1) Similar autonomous AI agent frameworks that process external data and look for identical indirect prompt injection vectors; (2) Other LLM-based tools that bridge natural language decisions to system commands; (3) Sandbox escapes in other containerized AI tools through similar path traversal or privilege escalation chains; (4) Console-based injection attacks in other approval workflows; (5) Variations of this attack against different LLM models that may be more or less susceptible to specific prompt injection techniques; (6) Supply chain attacks where LLM-based tools are compromised through their data sources rather than direct compromise.

## MITRE ATT&CK
- T1190
- T1059
- T1053
- T1611
- T1578
- T1021
- T1027
- T1036
- T1566
- T1091

## Notes
This vulnerability demonstrates the critical risk of autonomous AI agents that bridge language understanding to system command execution. The attack is particularly insidious because it creates a false sense of security through user approval mechanisms that are themselves vulnerable to manipulation. The timeline shows fixes were implemented in v0.4.3, but the fundamental risk of indirect prompt injection in LLM-based autonomous systems remains a class of vulnerabilities that deserves continued research. The docker escape was described as 'trivial,' suggesting minimal hardening was present. This case study is highly relevant for any system combining LLMs with privileged execution capabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
