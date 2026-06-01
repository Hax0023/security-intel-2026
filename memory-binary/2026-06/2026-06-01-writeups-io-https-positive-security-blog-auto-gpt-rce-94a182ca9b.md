# Auto-GPT Remote Code Execution and Docker Escape via Indirect Prompt Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Unknown/Not specified
- **Severity:** critical
- **Vuln types:** Indirect Prompt Injection, Arbitrary Code Execution, Container Escape, Path Traversal, Insufficient Input Validation, Unsafe Deserialization
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers demonstrated a critical attack chain against Auto-GPT that leverages indirect prompt injection to trick the LLM into executing arbitrary code when processing attacker-controlled content from websites. The attack combines console message spoofing, social engineering of user approval, and container escape techniques to achieve RCE on the host system.

## Attack scenario (step by step)
1. Attacker hosts a malicious website containing color-coded messages or hidden instructions designed to be processed by Auto-GPT
2. Victim instructs Auto-GPT to perform a seemingly harmless task (e.g., summarize text) from the attacker-controlled website
3. Auto-GPT's LLM processes the attacker-injected content and interprets it as legitimate instructions
4. Attacker uses console message spoofing or exploits Auto-GPT's unreliable action predictions to make malicious commands appear legitimate
5. Victim approves the command in non-continuous mode, unaware of the malicious intent
6. Attacker leverages docker escape vulnerabilities or path traversal bugs to break out of containerization and compromise the host system

## Root cause
Auto-GPT processes attacker-controlled text from external sources (websites) through its LLM without sufficient sanitization, treating user-provided content and LLM outputs equivalently in the conversation context. The system relies on user approval as a security boundary, but insufficient visual validation and the LLM's tendency to produce unreliable predictions enable attackers to obtain approval for malicious commands. Additionally, the docker image configuration and path handling in file operations contained exploitable weaknesses.

## Attacker mindset
An attacker would recognize that LLMs are inherently vulnerable to prompt injection when processing untrusted input. They would identify that the approval mechanism is a weak security control due to usability constraints and user inattention. They would methodically craft payloads that appear benign while injecting commands that the LLM will recognize and execute, then exploit the trust users place in the approval interface.

## Defensive takeaways
- Never allow LLMs to process untrusted external data without explicit data sanitization and isolation boundaries
- Implement strict sandboxing of LLM-suggested commands with explicit allowlisting rather than denylist approaches
- Do not rely on user approval as a primary security control when users cannot reasonably validate command safety
- Visually clearly separate LLM-generated content from system output to prevent spoofing
- Use principle of least privilege for containerized applications and ensure proper docker security hardening
- Implement strict input validation and path traversal protections for all file operations
- Separate the LLM reasoning context from external data processing pipelines
- Require cryptographic signing or other strong validation for critical operations rather than implicit approval

## Variant hunting
Hunt for similar injection vulnerabilities in: (1) Other autonomous AI frameworks that process external data through LLMs, (2) Applications using Claude, Llama, or other LLMs in feedback loops where output becomes input, (3) Systems combining LLM suggestions with privilege escalation mechanisms, (4) Container escape vectors in other sandboxed environments using similar privilege models, (5) Path traversal issues in code execution sandboxes following restart operations

## MITRE ATT&CK
- T1190
- T1059
- T1598
- T1566
- T1027
- T1548
- T1021
- T1611

## Notes
This represents a fundamental class of vulnerabilities in LLM-based autonomous agents: the inability to distinguish between system-generated output and attacker-controlled input within the conversation context. The attack is particularly dangerous because it targets the approval mechanism itself, making it appear to users that they are authorizing safe actions. The researchers responsibly disclosed and the maintainers patched v0.4.3. This vulnerability class will likely recur in other autonomous AI systems unless specifically designed against.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
