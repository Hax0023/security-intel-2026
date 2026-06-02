# Auto-GPT Remote Code Execution and Docker Escape via Indirect Prompt Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Auto-GPT (Open Source Project)
- **Bounty:** Not specified - appears to be security research disclosure
- **Severity:** critical
- **Vuln types:** Indirect Prompt Injection, Arbitrary Code Execution, Docker Escape, Path Traversal, Insufficient Input Validation, Console Output Injection
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
An attacker can inject malicious instructions into content that Auto-GPT processes (e.g., from a website), causing the LLM to interpret them as legitimate commands and execute arbitrary code. The vulnerability chains multiple issues: indirect prompt injection to trick GPT-4, social engineering of user approval via console injection, and trivial docker escape or path traversal for full system compromise.

## Attack scenario (step by step)
1. Attacker creates a malicious website containing specially crafted text with hidden instructions designed to be interpreted as Auto-GPT commands
2. Victim uses Auto-GPT to perform innocent task like summarizing content from the attacker's website
3. Auto-GPT fetches and processes the attacker-controlled website content through its LLM context
4. Injected instructions trick GPT-4 into planning malicious commands (e.g., reverse shell, credential theft) as part of task completion
5. Attacker uses console color codes or fabricated 'planned actions' to deceive user into approving malicious commands in review prompt
6. Approved malicious code executes, escaping docker container or sandboxing via path traversal to compromise host system

## Root cause
Auto-GPT processes untrusted external data (website content, file outputs) within the LLM context without adequate sanitization or isolation. The LLM is instructed to output JSON with commands to execute, making it a natural target for prompt injection. Additionally, insufficient validation of user-facing output (console colors) and weak sandboxing assumptions (docker permissions, path traversal checks) enable escalation.

## Attacker mindset
A sophisticated attacker recognizing that AI agents processing external data are inherently vulnerable to indirect prompt injection. By understanding Auto-GPT's architecture (command schema, execution flow, user approval process), the attacker crafts contextual payloads that appear natural to the LLM while containing hidden directives. Social engineering the user approval step via visual deception (console injection) or exploiting trust in 'planned actions' demonstrates understanding of human-machine interaction weaknesses.

## Defensive takeaways
- Implement strict input sanitization and validation for all external data before inclusion in LLM context; consider separate contexts for untrusted vs. trusted data
- Never rely on LLM outputs as trustworthy for security decisions; implement independent validation of commands before execution
- Use sandboxing layers with minimal privileges; avoid docker containers running as root or with excessive capabilities
- Implement output filtering to prevent injection attacks in console/user-facing output (e.g., strip color codes, escape special characters)
- Require explicit, unambiguous user approval for sensitive operations; avoid approval mechanisms exploitable via console manipulation
- Add monitoring and anomaly detection for unexpected command sequences or execution patterns
- Apply principle of least privilege for code execution environments and file system access; use read-only mounts where possible

## Variant hunting
['Test other AI agent frameworks (LangChain, BabyAGI, etc.) for similar indirect prompt injection vulnerabilities in external data processing', 'Investigate whether other commands beyond code execution (file operations, web requests) can be weaponized via prompt injection', 'Check if other LLM models (GPT-3.5, Claude, Llama) are susceptible or if prompt injection requires specific model behaviors', 'Examine plugins and custom command integrations for additional attack surface in Auto-GPT ecosystem', 'Test approval mechanisms in other AI tools for console injection or social engineering bypasses', 'Search for path traversal variants in non-docker setups and alternative sandboxing approaches (systemd, seccomp, apparmor)']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1203: Exploitation for Client Execution
- T1098: Valid Accounts
- T1021: Remote Service Session Initiation
- T1552: Unsecured Credentials
- T1055: Process Injection
- T1611: Escape to Host

## Notes
This writeup exemplifies emerging attack surface in AI-powered applications: the combination of LLM-based decision making with system-level execution capabilities creates a critical vulnerability class. The attack is particularly insidious because it doesn't require compromising the LLM itself—only manipulating the context it processes. The docker escape component highlights how automation tooling often trades security for convenience. Fixed in v0.4.3; disclosure timeline suggests responsible coordination with maintainers.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
