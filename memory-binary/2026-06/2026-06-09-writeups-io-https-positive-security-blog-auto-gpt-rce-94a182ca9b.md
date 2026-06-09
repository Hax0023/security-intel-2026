# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Arbitrary Code Execution, Docker Escape, Path Traversal, Insufficient Input Validation, Privilege Escalation
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers discovered that Auto-GPT could be exploited through indirect prompt injection to execute arbitrary code when processing attacker-controlled website content. The vulnerability chain combined LLM manipulation, user authorization bypass via console manipulation, and container escape techniques to achieve full system compromise.

## Attack scenario (step by step)
1. Attacker hosts a malicious website containing color-coded console messages or prompt injection payloads designed to be processed by Auto-GPT
2. Victim instructs Auto-GPT to perform a seemingly harmless task such as summarizing text from the attacker's website
3. Auto-GPT's LLM processes the attacker-controlled content and interprets embedded instructions as legitimate commands
4. Attacker uses console color codes or unreliable statement formatting to trick the user into approving malicious commands during review
5. Auto-GPT executes arbitrary Python code or shell commands with the container's privileges
6. In docker-based deployments, minimal user interaction (container restart) allows escape to the host system via container escape techniques

## Root cause
Auto-GPT lacked sufficient isolation between user-controlled external data and LLM instruction processing. The system trusted LLM outputs without adequately validating command intentions, combined with weak visual differentiation in command approval prompts and insecure docker container configuration allowing privilege escalation.

## Attacker mindset
An attacker would recognize that AI agents processing external data are inherently vulnerable to prompt injection. By crafting malicious websites and leveraging visual trickery in console output, the attacker exploits both the LLM's susceptibility to instruction injection and human psychology during the approval process. The docker escape represents an opportunistic exploitation of misconfiguration to achieve lateral movement.

## Defensive takeaways
- Implement strict sandboxing and capability restrictions for LLM-generated commands, not relying on user review as primary security control
- Sanitize and validate all external data before it reaches LLM processing pipelines
- Use clear, tamper-resistant visual formatting for security-critical approval prompts that cannot be manipulated by color codes or formatting tricks
- Implement execution whitelisting and principle of least privilege for code execution engines
- Run containers with minimal privileges and use read-only filesystems where possible
- Add explicit boundaries between user instructions and external data processing contexts
- Implement runtime monitoring and anomaly detection for unusual command sequences
- Consider using separate LLM instances or contexts for processing trusted vs untrusted data sources

## Variant hunting
['Similar LLM-based automation tools (Langchain agents, Custom GPT integrations) processing external data without input sanitization', 'Other tools using LLM-generated commands with insufficient validation mechanisms', 'Containerized applications with default or misconfigured security contexts', 'Systems with visual/console-based approval mechanisms vulnerable to formatting injection', 'Applications chaining multiple LLM calls where output of one serves as input to another']

## MITRE ATT&CK
- T1190
- T1059
- T1609
- T1548
- T1202
- T1566
- T1204

## Notes
This vulnerability exemplifies the emerging security challenges with autonomous AI systems. The attack required chaining multiple attack vectors (prompt injection, social engineering via UI manipulation, container escape). Fixed in Auto-GPT v0.4.3. The research highlights that user approval mechanisms alone cannot serve as security boundaries when the approval interface itself can be manipulated.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
