# Auto-GPT Arbitrary Code Execution and Docker Escape via Indirect Prompt Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Auto-GPT (Open Source Project)
- **Bounty:** Not specified (appears to be security research disclosure)
- **Severity:** critical
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Arbitrary Code Execution, Container Escape, Path Traversal, Privilege Escalation
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers discovered a critical vulnerability chain in Auto-GPT that allows attackers to achieve arbitrary code execution through indirect prompt injection on attacker-controlled websites, combined with social engineering of user approval mechanisms. The vulnerability extends to docker container escape on self-built images and path traversal sandbox bypass on non-docker versions.

## Attack scenario (step by step)
1. Attacker hosts a website containing color-coded console messages or crafted text designed to appear as legitimate Auto-GPT output
2. Victim uses Auto-GPT to perform an innocuous task (e.g., text summarization) on the attacker-controlled website
3. Auto-GPT fetches and processes the content, which is then fed to GPT-4 as part of the conversation context
4. The injected prompt manipulation causes GPT-4 to interpret attacker instructions as legitimate commands, generating code execution requests
5. In non-continuous mode, the attacker's crafted messages trick the user into approving the malicious command via visual spoofing or ambiguous command descriptions
6. Once approved, Auto-GPT executes arbitrary Python code, leading to container escape or sandbox bypass depending on deployment model

## Root cause
Auto-GPT processes untrusted external content (from websites) directly into the LLM context without sanitization. The LLM then interprets this attacker-controlled text as legitimate instructions within its command schema. The approval mechanism in non-continuous mode relies on user review of potentially spoofed console output. Additionally, the python execution sandbox and docker configurations lack proper isolation boundaries.

## Attacker mindset
An attacker would recognize that autonomous AI agents create a new attack surface where indirect prompt injection can be more potent than traditional prompt injection—the LLM's own reasoning and tool-use capabilities amplify the attacker's influence. By compromising a website that a user might ask Auto-GPT to analyze, the attacker can achieve code execution with minimal interaction. The attacker exploits the trust users place in visual feedback and Auto-GPT's decision-making to obtain approval for malicious actions.

## Defensive takeaways
- Implement strict input sanitization and HTML/console output escaping for all external content before LLM processing
- Design approval UX to prevent visual spoofing attacks; use clear, non-ambiguous command summaries that cannot be confused with system output
- Enforce sandboxing at OS level (seccomp, AppArmor) for Python execution, not just language-level restrictions
- Use capability-dropping in docker to prevent container escape; run with minimal required privileges
- Implement content security policies and validate URLs against known safe domains before fetching
- Add per-command approval with detailed reasoning display to make injection attacks more visible
- Consider using separate isolated environments for each command execution to limit blast radius
- Implement integrity checks on file paths and reject symbolic links to prevent directory traversal

## Variant hunting
Look for similar patterns in other LLM-based autonomous agents (e.g., LangChain agents, custom GPT wrappers). Investigate other commands that accept external input (browse_website, analyze_code, read_file). Test approval bypass techniques in other AI orchestration platforms. Examine how other sandbox implementations (JavaScript eval, shell command execution) handle prompt injection. Search for similar container escape vectors in other Python-based containerized applications.

## MITRE ATT&CK
- T1190
- T1059
- T1609
- T1548
- T1578
- T1021
- T1564

## Notes
This vulnerability was patched in v0.4.3. The writeup is an excellent example of chained vulnerabilities creating a critical impact—prompt injection alone would be concerning, but combined with approval spoofing and container escape, it becomes a full RCE. The research highlights the unique security challenges of LLM-based autonomous systems where the LLM's reasoning becomes part of the attack surface. The timeline shows responsible disclosure was followed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
