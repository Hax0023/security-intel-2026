# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Prompt Injection (Indirect), Arbitrary Code Execution, Docker Escape, Path Traversal, Insufficient Input Validation, Improper Output Sanitization
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers demonstrated a critical vulnerability chain in Auto-GPT that allows attackers to execute arbitrary code through indirect prompt injection by embedding malicious instructions in attacker-controlled websites. The vulnerability chain includes obtaining user approval through console message injection and subsequently escaping Docker containers to compromise the host system.

## Attack scenario (step by step)
1. Attacker hosts a malicious webpage containing color-coded console messages or specially crafted text designed to be processed by Auto-GPT's LLM
2. Victim user requests Auto-GPT to perform a seemingly harmless task like text summarization on the attacker's website
3. Auto-GPT's LLM processes the attacker-controlled content and interprets embedded instructions as legitimate commands
4. Attacker uses injected messages or exploits unreliable statement handling to trick the user into approving malicious commands during the review phase
5. Once approved, Auto-GPT executes arbitrary Python code or shell commands specified by the attacker
6. Attacker leverages Docker misconfiguration or path traversal vulnerabilities to escape the container and compromise the host system

## Root cause
The vulnerability stems from multiple design flaws: (1) insufficient isolation between attacker-controlled input and LLM instruction processing, (2) inadequate sanitization of console output allowing injection attacks, (3) user approval mechanisms that can be manipulated through visual/textual deception, and (4) insecure Docker image configurations and path traversal protections in the Python code execution sandbox.

## Attacker mindset
An attacker would recognize that Auto-GPT's strength (processing arbitrary text inputs and converting them to executable commands) is also its critical weakness. By crafting carefully formatted content hosted on attacker-controlled infrastructure, they can leverage the LLM's pattern-matching behavior to inject malicious instructions. The attacker understands that user approval mechanisms can be bypassed through social engineering (misleading console output) and that Docker escapes are trivial with improper configuration, making this a complete compromise chain.

## Defensive takeaways
- Implement strict input validation and sanitization for all attacker-controlled data before feeding to LLMs, not just output sanitization
- Design approval mechanisms that cannot be visually spoofed; use structured, cryptographically signed approval tokens rather than relying on console output review
- Never embed user-controlled content directly into LLM prompts; use separate, clearly-marked sections with explicit boundaries
- Apply principle of least privilege: restrict Python code execution to sandboxed environments with minimal OS access; use AppArmor, seccomp, or similar mandatory access controls
- Ensure Docker images run with minimal capabilities (drop CAP_SYS_ADMIN and other dangerous capabilities), use read-only root filesystems, and implement proper user namespacing
- Implement path traversal protections beyond simple string checking; use absolute paths and verify canonical paths
- Maintain a clear separation between LLM 'reasoning' output and actual command execution; require explicit human review of actual commands, not summaries
- Implement rate limiting and anomaly detection for command execution patterns
- Use code signing and attestation for any dynamically executed code

## Variant hunting
Look for similar vulnerabilities in other autonomous LLM agents (e.g., LangChain agents, other GPT wrapper tools). Test any application that: accepts user goals, uses LLMs to plan/execute commands, allows code execution, runs in containers, or processes web content. Examine how other projects handle user approval, input validation, and sandboxing. Test for variations like: JavaScript code execution contexts, SQL injection through LLM-generated queries, indirect command injection through file paths, and approval bypass through timing attacks or race conditions.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1203: Exploitation for Client Execution
- T1055: Process Injection
- T1548: Abuse Elevation Control Mechanism
- T1611: Escape to Host
- T1083: File and Directory Discovery
- T1070: Indicator Removal
- T1027: Obfuscation or Deception

## Notes
This vulnerability represents a critical class of AI safety issues where the capability to process natural language and convert it to executable actions becomes a direct attack surface. The writeup is particularly valuable because it demonstrates a complete exploitation chain from initial compromise to host system access. The fixes applied in v0.4.3 appear to address symptoms rather than root causes; organizations deploying LLM-based automation tools should conduct thorough security reviews of their architecture before production use. The vulnerability highlights the fundamental tension in autonomous agent design: flexibility for legitimate use cases directly enables malicious use cases.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
