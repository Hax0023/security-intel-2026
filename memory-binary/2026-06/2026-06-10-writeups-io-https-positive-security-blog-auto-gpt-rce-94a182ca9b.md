# Auto-GPT Remote Code Execution and Docker Escape via Indirect Prompt Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Remote Code Execution, Container Escape, Path Traversal, Sandbox Bypass
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers demonstrated a critical attack chain leveraging indirect prompt injection to trick Auto-GPT into executing arbitrary code through attacker-controlled website content. The vulnerability chain allows an attacker to obtain user approval for malicious commands via console message spoofing and subsequently escape Docker containers or bypass sandboxing via path traversal exploits.

## Attack scenario (step by step)
1. Attacker creates a malicious website with color-coded console messages or fake future action statements injected into the content
2. Attacker tricks Auto-GPT user into asking the system to summarize or process content from the attacker's website via indirect prompt injection
3. Auto-GPT's LLM processes the injected instructions and interprets them as legitimate commands to execute
4. Attacker manipulates console output or leverages unreliable LLM statements to convince the user to approve execution of arbitrary Python code
5. Once code execution is achieved, attacker escalates to Docker escape on self-built images through minimal interaction (container restart) or path traversal sandbox bypass on non-Docker versions
6. Attacker gains code execution on the host system with full system access

## Root cause
Auto-GPT fails to properly sanitize and isolate attacker-controlled text that is processed by the LLM, allowing indirect prompt injection attacks. The approval mechanism relies on user review of console output which can be spoofed. The Docker container and sandbox implementations lack proper isolation boundaries and privilege restrictions.

## Attacker mindset
A security researcher or sophisticated attacker recognizes that autonomous AI systems process untrusted user-supplied data through powerful LLMs without adequate input validation. By crafting specially formatted malicious content, they exploit the LLM's tendency to follow instructions embedded in processed text, combined with weak approval mechanisms and container misconfiguration to achieve arbitrary code execution and host system compromise.

## Defensive takeaways
- Implement strict input sanitization and validation for all user-supplied and fetched content before LLM processing
- Design approval mechanisms that cannot be spoofed through console output manipulation or message formatting
- Run autonomous AI systems in properly hardened containers with minimal privileges and restricted syscalls
- Implement defense-in-depth with multiple isolation layers between LLM execution and host system
- Use output encoding and structural validation to prevent prompt injection through fetched web content
- Disable continuous mode by default and implement robust approval workflows
- Apply principle of least privilege to code execution sandboxes with no path traversal capabilities
- Regular security audits of LLM prompt templates and command execution interfaces

## Variant hunting
['Search for other autonomous AI agents that process user-supplied URLs or external content without sanitization', 'Identify other systems using LLM-based command execution with similar JSON schema approval mechanisms', 'Test other Docker-based AI applications for similar privilege escalation and escape vulnerabilities', 'Examine other tools allowing LLM-guided code execution for sandbox bypass via path traversal or similar techniques', 'Look for systems combining web fetching with LLM processing that lack output encoding/validation']

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1611
- T1548
- T1036
- T1202

## Notes
This vulnerability demonstrates the security risks of autonomous AI systems processing untrusted data. The attack chain requires multiple weak points (prompt injection → user deception → container misconfiguration) but each is individually achievable. Fixes were implemented in v0.4.3. The research highlights the inadequacy of relying on user review of AI-generated commands as a security control when that review can be manipulated through output spoofing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
