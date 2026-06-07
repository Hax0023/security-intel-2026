# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Code Execution, Docker Escape, Path Traversal, Insufficient Input Validation, Unsafe Deserialization
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers demonstrated a critical attack chain leveraging indirect prompt injection to trick Auto-GPT into executing arbitrary code when processing attacker-controlled content from websites. The vulnerability combined LLM manipulation, console output injection, and docker escape techniques to achieve remote code execution and host system compromise. Multiple attack vectors were identified affecting docker and non-docker versions through versions 0.4.1-0.4.2.

## Attack scenario (step by step)
1. Attacker hosts a malicious website containing color-coded console messages or crafted text designed to appear as Auto-GPT instructions
2. Victim uses Auto-GPT to perform seemingly harmless task such as summarizing text from the attacker-controlled website
3. Auto-GPT's LLM processes the injected content and interprets hidden attacker instructions as legitimate commands
4. In non-continuous mode, attacker injects visual deception (color-coded messages or false planned action statements) to trick user into approving malicious commands
5. Auto-GPT executes arbitrary Python code via execute_python_code command with user's approved authorization
6. Attacker leverages docker escape vulnerability or path traversal exploit to break out of container/sandbox and compromise host system

## Root cause
Auto-GPT's LLM processes user input and externally-fetched content without sufficient sanitization before passing to command execution pipeline. The system trusts LLM interpretation of all text in conversation context, including attacker-controlled web content. Insufficient separation between instruction content and data content allows prompt injection. Docker container misconfiguration and non-docker sandbox implementation had trivial escape routes.

## Attacker mindset
Exploit the implicit trust in LLM-generated commands combined with cognitive biases in user approval process. Leverage web content fetching capabilities to inject instructions that appear legitimate within LLM's response format. Abuse console output rendering to deceive users via visual deception. Target weakly-configured containerization as final privilege escalation vector.

## Defensive takeaways
- Implement strict output validation and sanitization for all LLM-generated commands before execution, not just user input
- Separate data context from instruction context when feeding external content to LLM; clearly mark untrusted sources
- Disable or heavily restrict browse_website and similar functions that fetch attacker-controllable content in agent loops
- Implement signed/verified command schemas that cannot be manipulated by LLM output tampering
- Use principle of least privilege for process execution; run agents with minimal required permissions
- Properly configure docker containers with read-only filesystems, restricted capabilities, and user namespace isolation
- Implement sandboxing at OS level (seccomp, AppArmor) rather than relying on application-level isolation
- Add human-in-the-loop verification for all code execution commands with clear display of actual command to be run
- Implement rate limiting and anomaly detection for command sequences that suggest compromise
- Regular security audits of LLM prompt injection attack surface

## Variant hunting
Search for other autonomous agent frameworks (LangChain agents, ReAct implementations, custom tool-using LLM systems) for similar indirect prompt injection vulnerabilities. Look for other tools that fetch and process web content in LLM loops. Examine other docker escape vectors in containerized LLM applications. Test path traversal in file write operations of code generation tools. Investigate visual deception vectors in other CLI tools with approval workflows.

## MITRE ATT&CK
- T1190
- T1195
- T1202
- T1548
- T1059
- T1610
- T1611
- T1027
- T1578

## Notes
This represents a significant class of vulnerabilities in autonomous AI agent systems - the inability to distinguish between legitimate instructions and attacker-injected content when processing external data. The attack chain demonstrates how multiple moderate vulnerabilities (prompt injection + UI deception + weak containerization) combine to achieve critical impact. Versions 0.4.3+ addressed the console injection and docker escape, but the fundamental prompt injection vulnerability remains a design concern for similar systems. The path traversal in non-docker versions highlights how sandbox escapes can occur through file system operations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
