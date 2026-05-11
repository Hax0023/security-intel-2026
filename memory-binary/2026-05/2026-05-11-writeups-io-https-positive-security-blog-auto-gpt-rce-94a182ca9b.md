# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Remote Code Execution, Container Escape, Path Traversal, Insufficient Input Validation, Console Output Injection
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers discovered a critical vulnerability in Auto-GPT that allows attackers to achieve remote code execution through indirect prompt injection by embedding malicious instructions in attacker-controlled websites. The attack leverages the LLM's processing of untrusted content to trick it into executing arbitrary code, combined with visual spoofing to gain user approval. Additionally, self-built Docker versions were vulnerable to trivial container escape.

## Attack scenario (step by step)
1. Attacker hosts a malicious website containing prompt injection payloads embedded in visible text or HTML comments
2. Victim is asked by Auto-GPT to summarize or analyze content from the attacker-controlled website using the browse_website command
3. Auto-GPT fetches the website content and the LLM processes the attacker-injected instructions as legitimate task directives
4. Attacker uses color-coded console messages or crafted statements about future actions to manipulate the user into approving malicious commands
5. Auto-GPT executes arbitrary Python code or system commands approved by the deceived user
6. In Docker environments, attacker terminates the container triggering a restart, which enables escape to the host system via misconfigured volume mounts or default permissions

## Root cause
Auto-GPT fails to properly sanitize and isolate untrusted input from external sources (websites, user-provided content) before feeding it to the LLM prompt context. The system trusts the LLM's output without sufficient validation, and insufficient sandboxing in Docker configurations combined with the ability to execute arbitrary Python code enables privilege escalation. Console output lacks proper escaping allowing visual manipulation attacks.

## Attacker mindset
Exploit the trust chain between the LLM, the application, and the user. Recognize that while the LLM cannot be directly jailbroken, it can be tricked through intermediate data sources. Use social engineering (console spoofing) to manipulate human approval mechanisms. Leverage automation weaknesses in containerization to achieve persistence and lateral movement.

## Defensive takeaways
- Implement strict input validation and sanitization for all external data sources before LLM processing
- Use separate sandboxed execution environments with minimal privileges and no host access
- Require explicit user confirmation with full command visibility, resistant to visual manipulation/console injection
- Implement output filtering and escaping to prevent console/UI spoofing attacks
- Use read-only file systems and drop unnecessary Linux capabilities in containers
- Apply path traversal protections with normalized path validation and chroot jails
- Maintain strict boundaries between LLM reasoning context and executable instructions
- Implement content security policies for website browsing to strip or neutralize prompt injection attempts
- Apply principle of least privilege to Python code execution sandboxes
- Regularly audit and restrict available commands exposed to the LLM

## Variant hunting
['Test indirect prompt injection via other data sources: email content, PDF metadata, image EXIF data, API responses', 'Search for similar LLM automation tools (LangChain agents, other GPT wrappers) with command execution capabilities', 'Investigate other containerization technologies (Kubernetes, systemd-nspawn) for similar escape paths', 'Test prompt injection in multi-stage LLM pipelines where output of one model feeds into another', 'Examine other approval/authorization bypass techniques in console-based UIs', 'Look for similar path traversal in configuration file loading or plugin systems']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1059.006 - Python
- T1610 - Deploy Container
- T1611 - Escape to Host
- T1027.001 - Obfuscated Files or Information: Steganography
- T1036.006 - Masquerading: Space after Filename
- T0845 - Spoof Command Output
- T1548.002 - Abuse Elevation Control Mechanism: Bypass User Account Control

## Notes
Reported via responsible disclosure; fixes implemented in v0.4.3. The vulnerability chain demonstrates how safety controls in AI systems can be bypassed through multiple weak points: (1) trust in external data sources, (2) insufficient LLM output validation, (3) user confusion through visual manipulation, (4) weak container isolation. This is representative of emerging attack patterns against LLM-powered automation systems where the 'weakest link' may be the human approver or the integration points rather than the LLM itself.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
