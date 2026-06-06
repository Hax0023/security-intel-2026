# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Arbitrary Code Execution, Docker Escape, Path Traversal, Privilege Escalation, Authorization Bypass
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers discovered a critical vulnerability chain in Auto-GPT where attackers can inject malicious instructions through attacker-controlled websites to trick the LLM into executing arbitrary code. The vulnerability is compounded by insufficient user approval mechanisms (console color-code spoofing) and trivial container escape techniques that allow attackers to break out of Docker sandboxing to the host system.

## Attack scenario (step by step)
1. Attacker hosts a malicious website containing color-coded console messages or specially crafted text designed to be interpreted as legitimate Auto-GPT output
2. Attacker tricks a user into asking Auto-GPT to perform a seemingly harmless task like summarizing text from the attacker's website
3. Auto-GPT fetches content from the malicious site, and the LLM processes the injected instructions as part of the conversation context
4. Through indirect prompt injection, the LLM is convinced to execute arbitrary Python code or system commands
5. In non-continuous mode, the spoofed console messages or misleading LLM statements cause the user to approve malicious commands
6. Attacker leverages Docker escape techniques or path traversal exploits to break sandbox isolation and gain host system access

## Root cause
Auto-GPT's architecture processes all user input, fetched content, and LLM outputs within a single conversation context without proper isolation. The LLM cannot distinguish between legitimate system messages and attacker-injected content. Additionally, the approval mechanism relies on user interpretation of console output without cryptographic verification, and default Docker configurations lack proper privilege restrictions.

## Attacker mindset
An attacker recognizes that autonomous AI agents create a new attack surface where indirect inputs can influence code execution decisions. By poisoning web content that the agent will consume, attackers can manipulate the LLM's reasoning without direct access to the system. The attacker also understands that users may trust the approval prompts they see, especially if they appear to come from trusted sources or use visual elements that mimic legitimacy.

## Defensive takeaways
- Implement cryptographic verification and signing of all system messages to prevent spoofing via console output manipulation
- Isolate user-controlled input, system output, and LLM reasoning in separate contexts with clear boundaries
- Require explicit multi-step approval for sensitive operations like code execution, not just user confirmation of LLM suggestions
- Enforce strict sandboxing with minimal Docker capabilities (no privilege escalation, read-only filesystems where possible)
- Apply principle of least privilege - run containers as non-root users with restricted syscalls via seccomp
- Implement content sanitization and validation for all fetched external resources before feeding to LLM
- Add monitoring and logging for all code execution attempts with ability to detect unusual command patterns
- Use separate LLM contexts or dedicated safety models to validate whether command suggestions are legitimate

## Variant hunting
['Search for similar indirect prompt injection patterns in other autonomous AI agents (e.g., BabyAGI, AgentGPT, LangChain-based agents)', 'Test if other code execution sandboxes (Jupyter, Codex, custom execution environments) are vulnerable to similar path traversal attacks', "Investigate whether other containerized AI applications have weak privilege separation similar to Auto-GPT's Docker escape", 'Look for prompt injection vulnerabilities in AI systems that fetch external content (news aggregators, research tools, web crawlers)', 'Test console output spoofing techniques against other CLI tools that present user approval prompts', 'Examine if LLM-driven deployment tools (Ansible, Terraform interfaces) have similar authorization bypass mechanisms']

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1578
- T1610
- T1548
- T1070
- T1036

## Notes
This vulnerability chain is particularly dangerous because it targets the intersection of LLM reasoning, user trust, and container security. The attack requires minimal user interaction (just asking Auto-GPT to summarize a webpage) and exploits the human tendency to trust visual indicators and system prompts. The fixes were applied in v0.4.3 but the research highlights fundamental architectural challenges in making autonomous AI systems secure. The indirect prompt injection technique is likely to become more prevalent as AI agents become more widely deployed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
