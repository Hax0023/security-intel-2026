# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Remote Code Execution, Docker Escape, Path Traversal, Improper Input Validation, Insufficient Access Controls
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
An attacker can inject malicious instructions into web content that Auto-GPT processes, tricking the LLM into executing arbitrary code. Combined with social engineering to obtain user approval (via color-coded console messages) and docker escape techniques, this allows complete system compromise from a seemingly harmless task like text summarization.

## Attack scenario (step by step)
1. Attacker hosts a malicious website containing color-coded console-like messages or misleading statements about future actions
2. User instructs Auto-GPT to summarize or analyze content from the attacker-controlled website
3. Auto-GPT fetches and processes the website content, passing it to the LLM for analysis
4. Injected instructions in the website content trick GPT-4 into generating commands for arbitrary code execution
5. Attacker uses social engineering (fake console output) or leverages LLM's unreliable statements to convince user to approve malicious commands
6. Auto-GPT executes the approved code, and attacker leverages docker escape via container restart or path traversal to compromise the host system

## Root cause
Auto-GPT fails to properly sanitize attacker-controlled input from external sources (websites) before passing it to the LLM. The LLM then interprets injected instructions as legitimate commands. Additionally, insufficient isolation between the application sandbox and container/host system allows privilege escalation.

## Attacker mindset
An attacker recognizes that LLMs process all input equally, including content from external sources. By crafting convincing prompts disguised as legitimate console output or leveraging the LLM's tendency to make speculative statements, they can manipulate both the AI and human users into executing malicious code. The attacker exploits the trust users place in the sandboxing mechanisms and the assumption that reviewing commands provides adequate protection.

## Defensive takeaways
- Implement strict input validation and sanitization for all external data sources before LLM processing
- Use prompt injection detection and filtering mechanisms to identify suspicious instruction patterns
- Never directly surface LLM-generated commands to users without clear, unambiguous formatting that cannot be spoofed by external input
- Require explicit, structured confirmation for sensitive operations (code execution, file writes) using out-of-band confirmation methods
- Implement proper containerization and privilege separation; run applications with minimal required permissions
- Use immutable container configurations and disable container restart capabilities or require manual host confirmation
- Apply strict path validation to prevent traversal attacks that bypass sandboxing
- Log and audit all LLM-to-command translations for security monitoring
- Consider using a separate, unprivileged user account for running auto-execution features
- Implement network segmentation to restrict Auto-GPT's access to external resources

## Variant hunting
Search for similar indirect prompt injection vulnerabilities in other LLM-based automation tools (Langchain agents, LlamaIndex applications, etc.). Look for command-and-control interfaces that accept external data without proper sanitization. Test other containerized AI applications for escape conditions via application-triggered failures. Investigate path traversal possibilities in any application using dynamic file operations based on LLM suggestions.

## MITRE ATT&CK
- T1190
- T1059
- T1053
- T1203
- T1611
- T1021
- T1567
- T1548

## Notes
This vulnerability chain demonstrates the intersection of multiple security domains: prompt injection, social engineering, containerization, and privilege escalation. The fixes in v0.4.3 addressed console message spoofing and docker escape, but the fundamental issue of processing untrusted external input through an LLM without proper boundaries remains a critical risk in AI automation systems. The reliance on user approval as a security control is undermined by the attacker's ability to manipulate the approval interface itself.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
