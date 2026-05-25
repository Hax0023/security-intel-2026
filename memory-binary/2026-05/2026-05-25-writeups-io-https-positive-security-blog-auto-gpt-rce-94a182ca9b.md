# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Arbitrary Code Execution, Docker Escape, Path Traversal, Insufficient Input Validation, Unsafe Deserialization/Execution
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
An attacker can inject malicious instructions into Auto-GPT through attacker-controlled websites, tricking the LLM into executing arbitrary code. The vulnerability chains indirect prompt injection with insufficient user approval mechanisms and container escape techniques to compromise both the application and host system.

## Attack scenario (step by step)
1. Attacker creates a malicious website with color-coded console messages or crafted text that appears as legitimate Auto-GPT output
2. Victim uses Auto-GPT to perform a seemingly harmless task like summarizing text from the attacker's website
3. Auto-GPT fetches and processes the website content, which contains hidden instructions interpreted by GPT-4 as legitimate commands
4. The injected prompt causes Auto-GPT to decide to execute arbitrary Python code or system commands
5. In default mode, the console displays misleading or color-coded output making the malicious command appear legitimate, tricking the user into approving it
6. Once executed, the code either runs directly (non-docker) or enables a trivial docker escape via container restart to compromise the host system

## Root cause
Auto-GPT processes user-controlled input (website content) without sufficient sanitization before feeding it to the LLM. The LLM interprets this input as part of its instruction set rather than treating it as untrusted data. The approval mechanism relies on console output clarity, which can be spoofed with color codes. Additionally, the docker container and non-docker versions lack proper sandboxing or path traversal protections for code execution.

## Attacker mindset
An attacker would recognize that LLMs are vulnerable to prompt injection when processing untrusted data. By hosting a malicious website, they can influence Auto-GPT's behavior when users interact with it. The attacker would exploit the trust users place in the approval prompt and the ambiguity of LLM-generated commands. For container exploitation, the attacker would leverage the fact that users may restart containers without deep inspection of what caused termination.

## Defensive takeaways
- Implement strict input sanitization and validation for all user-controlled and externally-sourced content before processing by LLMs
- Create a robust command approval mechanism that cannot be spoofed—use structured, unambiguous display of planned actions rather than relying on console output clarity
- Implement true sandboxing for code execution with filesystem restrictions, no container escape vectors, and explicit whitelist of allowed operations
- Add rate limiting and anomaly detection for unusual command sequences or suspicious state transitions
- Use prompt engineering techniques to make the LLM more resistant to instruction injection (e.g., explicit markers for user data vs. system instructions)
- Apply principle of least privilege—restrict file system access, network access, and available commands to the minimum necessary
- Implement security logging and alerts for suspicious command approvals or container terminations
- Regular security audits of the interaction between LLM outputs and executable commands

## Variant hunting
['Search for other AI agent frameworks (LangChain agents, ReAct implementations) using similar LLM-command patterns without proper input validation', 'Identify other applications that fetch and process web content before LLM processing without sanitization', 'Hunt for similar approval mechanisms that rely on console output clarity or can be bypassed with ANSI codes', 'Test other containerized AI applications for similar docker escape vectors exploiting restart mechanisms', 'Look for path traversal vulnerabilities in sandboxed code execution environments that can escape restrictions', 'Examine other autonomous agent frameworks for indirect prompt injection via tool outputs (search results, file contents, API responses)']

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1611
- T1021
- T1027
- T1036

## Notes
This vulnerability demonstrates the inherent risks of autonomous LLM agents processing untrusted data. The attack chain requires multiple components: prompt injection capability, insufficient input validation, weak approval mechanisms, and container escape vectors. The fact that multiple escape paths existed (docker and non-docker) suggests systemic security issues in the sandboxing approach. Fixed in v0.4.3. This research highlights that AI safety must extend beyond the model itself to include secure system integration and user interface design.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
