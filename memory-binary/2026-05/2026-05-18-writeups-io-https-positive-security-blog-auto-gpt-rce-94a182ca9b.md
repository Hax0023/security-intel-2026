# Auto-GPT Remote Code Execution and Docker Escape via Indirect Prompt Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Prompt Injection, Remote Code Execution, Docker Escape, Path Traversal, Arbitrary Code Execution, Insufficient Input Validation
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
An attacker can leverage indirect prompt injection to trick Auto-GPT into executing arbitrary code by injecting malicious instructions into attacker-controlled web content that the LLM processes. The vulnerability chains user approval bypass (via console color-coding or unreliable statements) with multiple code execution paths, culminating in docker escape or sandbox breakout depending on deployment method.

## Attack scenario (step by step)
1. Attacker creates a malicious website containing color-coded console messages or crafted instructions formatted to appear as Auto-GPT's own planned actions
2. Attacker convinces a user to ask Auto-GPT to summarize or process content from the malicious website
3. Auto-GPT's LLM processes the injected content and interprets it as legitimate instructions rather than data
4. The injected payload instructs Auto-GPT to execute arbitrary Python code or commands via execute_python_code or similar functions
5. Either: (a) console injection tricks user into approving malicious commands in non-continuous mode, or (b) continuous mode executes immediately without approval
6. Attacker achieves RCE within container, then exploits docker misconfiguration or path traversal to escape to host system

## Root cause
Auto-GPT fails to properly separate data from instructions when processing user-supplied content through the LLM. The system treats all LLM outputs (including those influenced by attacker-controlled input) as trusted instructions without sufficient sandboxing. Additionally: (1) insufficient console output validation allows injection of approval-triggering messages, (2) Docker image misconfiguration enables container escape with minimal interaction, (3) Python sandboxing has path traversal weaknesses in restart scenarios.

## Attacker mindset
The attacker recognizes that LLMs process all text input similarly regardless of source, viewing prompt injection as a privilege escalation technique within the Auto-GPT architecture. They exploit the gap between data processing and instruction execution, understanding that users are likely to trust LLM-suggested commands. The attacker leverages social engineering (user approval) combined with technical exploits (docker/sandbox escape) to achieve full system compromise.

## Defensive takeaways
- Implement strict separation between LLM-generated instructions and user-supplied data; never allow untrusted input to influence command schema decisions
- Add cryptographic integrity verification for all console output and command suggestions to prevent injection attacks
- Enforce mandatory command execution sandboxing with whitelist-based authorization, not just approval prompts
- Use read-only mounted docker volumes and drop unnecessary capabilities; implement multi-layer container escape prevention
- Apply principle of least privilege to Python execution environments with chroot jails, AppArmor, or seccomp filtering
- Validate and canonicalize all file paths before execution; prevent symlink/traversal attacks in restart scenarios
- Rate-limit and monitor unusual command sequences; alert on suspicious patterns indicating injection attempts
- Never rely on user approval as sole security control when users cannot distinguish attacker-injected from legitimate messages

## Variant hunting
Search for similar indirect prompt injection in: (1) other LLM-based automation tools (Langchain agents, custom orchestrators), (2) systems that fetch and process untrusted web content through LLMs (web crawlers, RSS readers), (3) containerized applications with weak escape mitigations, (4) any system where user approval is gated by console output that can be manipulated. Test for prompt injection in email summarization tools, document processing pipelines, and code analysis platforms.

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1056
- T1566
- T1005
- T1552
- T1542
- T1611

## Notes
This writeup demonstrates a sophisticated attack chain combining multiple vulnerability classes. The indirect prompt injection vector is particularly noteworthy as it exploits the fundamental architecture of LLM-based systems rather than a discrete bug. The docker escape component shows supply chain risk in self-built images. Fixed in v0.4.3, but illustrates broader risks in all systems that delegate command execution decisions to LLMs processing untrusted data. The approval-bypass via console injection is especially dangerous as it exploits user trust in system output.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
