# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Indirect Prompt Injection, Arbitrary Code Execution, Docker Escape, Path Traversal, Privilege Escalation, Sandbox Bypass
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers discovered multiple critical vulnerabilities in Auto-GPT that allow attackers to achieve arbitrary code execution through indirect prompt injection attacks combined with Docker escape techniques. By injecting malicious instructions into attacker-controlled websites, attackers can trick Auto-GPT into executing arbitrary code and escape containerization to compromise the host system.

## Attack scenario (step by step)
1. Attacker hosts a malicious website containing color-coded console messages or crafted text designed to be processed by Auto-GPT's LLM
2. Victim uses Auto-GPT to perform a seemingly harmless task such as summarizing content from the attacker's website
3. Auto-GPT fetches and processes the attacker-controlled content, which contains embedded instructions interpreted by GPT-4
4. The LLM is deceived into generating malicious commands (e.g., execute_python_code) as part of its reasoning process
5. In non-continuous mode, the attacker-crafted visual formatting or unreliable statements trick the user into approving malicious commands
6. Attacker-controlled code executes within Auto-GPT, then exploits Docker misconfiguration or path traversal to escape to the host system

## Root cause
Auto-GPT processes user input and external website content through an LLM without sufficient input validation or sandboxing. The LLM interprets attacker-injected text as legitimate instructions within its JSON command schema. Additionally, insufficient access controls in Docker configurations and path traversal vulnerabilities in the Python sandbox allow escaping the intended execution environment.

## Attacker mindset
An attacker seeks to compromise systems running Auto-GPT by leveraging the trust users place in the application to safely handle external content. By exploiting the LLM's susceptibility to prompt injection and weak containerization practices, attackers can gain code execution and lateral movement capabilities with minimal user interaction.

## Defensive takeaways
- Implement strict input validation and sanitization for all content processed by LLMs, especially from external sources
- Design a robust approval mechanism that resists visual deception techniques and clearly distinguishes between expected and suspicious commands
- Enforce proper Docker security practices including read-only filesystems, restricted capabilities, and user privilege separation
- Implement comprehensive sandboxing for code execution with strict path restrictions and capability limitations
- Use prompt injection detection mechanisms and validate LLM outputs against expected command schemas before execution
- Maintain strict separation between container and host system with minimal escape vectors
- Regularly audit LLM-based applications for indirect injection attack vectors and test with adversarial inputs
- Implement command approval workflows that require explicit user confirmation without relying on visual/formatting tricks

## Variant hunting
['Test other LLM-powered automation tools (LangChain, agents, code executors) for similar indirect prompt injection vulnerabilities', 'Search for similar Docker escape vulnerabilities in self-built container images with permissive security configurations', 'Audit other applications that process untrusted content through LLMs without proper input validation', 'Investigate Python sandbox implementations in similar tools for path traversal and escape mechanisms', 'Test whether color-coding, ANSI escape sequences, or other formatting techniques can manipulate approval workflows in other systems', 'Examine other LLM-based code generation and execution frameworks for similar approval bypass techniques']

## MITRE ATT&CK
- T1190
- T1059
- T1040
- T1202
- T1610
- T1548
- T1027
- T1204

## Notes
This vulnerability chain demonstrates the inherent risks of autonomous agents that combine LLMs with code execution capabilities. The attack exploits multiple weaknesses: LLM susceptibility to prompt injection, weak user approval mechanisms, and inadequate containerization. Fixed in v0.4.3. The research highlights the critical need for security-first design when building LLM-powered automation tools with execution capabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
