# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Remote Code Execution, Docker Escape, Path Traversal, Insufficient Input Validation, Privilege Escalation
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
An attacker can inject malicious instructions into attacker-controlled websites that Auto-GPT processes, causing the LLM to execute arbitrary code through indirect prompt injection. The vulnerability chains RCE with trivial Docker escape and path traversal to achieve full host system compromise with minimal user interaction.

## Attack scenario (step by step)
1. Attacker hosts malicious content on a website with color-coded console messages or crafted instructions disguised as legitimate output
2. Victim uses Auto-GPT to perform seemingly harmless task such as summarizing text from attacker's website
3. LLM processes attacker's injected instructions from website content as legitimate system directives
4. Attacker uses color-coded messages or unreliable LLM statements about planned actions to deceive user into approving malicious commands
5. Auto-GPT executes arbitrary Python code or system commands with application privileges
6. For Docker: Attacker triggers container termination and user restart to escape; for non-Docker: Attacker exploits path traversal to execute code outside sandbox on restart

## Root cause
The LLM lacks proper distinction between user instructions and attacker-controlled content from external sources. The system trusts LLM-generated command sequences without sufficient validation. Console output manipulation and unreliable LLM reasoning about future actions allow social engineering of user approval. Docker and non-Docker versions lacked proper sandboxing isolation.

## Attacker mindset
Exploit the trust boundary between legitimate system output and attacker-injected content. Leverage LLM's natural language reasoning limitations to generate convincing but false statements about command execution. Use social engineering to gain user authorization for malicious actions. Chain multiple weaknesses (prompt injection + approval bypass + sandbox escape) to achieve maximum impact.

## Defensive takeaways
- Implement strict input validation and sanitization on all external content before LLM processing
- Establish explicit boundaries between user instructions, system output, and externally-sourced content
- Never rely on LLM reasoning alone for security-critical decisions; implement deterministic approval mechanisms
- Use actual command hashing/signing instead of text-based approval to prevent visual spoofing
- Implement proper sandboxing with immutable separation between container and host filesystem
- Add explicit approval requirements for code execution commands with human-readable diffs
- Disable continuous mode by default and require explicit per-command authorization
- Use restrictive system user accounts and capability dropping for code execution contexts
- Validate all file paths and prevent traversal attacks through canonical path resolution
- Monitor and log all LLM-generated commands before execution with anomaly detection

## Variant hunting
['Search for other LLM-based automation tools processing external content (Langchain agents, custom GPT plugins)', 'Look for approval workflows that rely on text-based validation or visual cues', 'Test web scraping tools that feed results to LLMs without sanitization', 'Examine chatbot systems accepting URLs or file uploads for processing', 'Audit containerized applications with insufficient privilege separation', 'Review systems with path traversal in file operations following user input', 'Check for environment variable injection through LLM output processing', 'Test approval bypass through ANSI color codes and terminal escape sequences in other applications']

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1552
- T1611
- T1574
- T1548
- T1027
- T1055
- T1021

## Notes
This vulnerability demonstrates a novel attack class combining LLM-specific risks (prompt injection via external content) with traditional security flaws (insufficient sandboxing, path traversal). The indirect prompt injection is particularly concerning because it occurs without explicit user instruction to process untrusted input. The attack requires relatively low interaction from users (just restarting a container or Auto-GPT application), making it highly practical. Fixed in v0.4.3 but highlights systemic design issues in LLM-based automation systems. The console color code bypass and unreliable LLM statements tricks are social engineering attacks that exploit human trust in visual/textual system output.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
