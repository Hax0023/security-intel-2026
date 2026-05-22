# Auto-GPT Remote Code Execution via Indirect Prompt Injection and Docker Escape

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Auto-GPT
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Prompt Injection, Indirect Prompt Injection, Code Execution, Docker Escape, Path Traversal, Sandbox Bypass, Console Output Manipulation
- **Category:** memory-binary
- **Writeup:** https://positive.security/blog/auto-gpt-rce

## Summary
Researchers discovered a critical attack chain in Auto-GPT that combines indirect prompt injection to trick the LLM into executing arbitrary commands, combined with console manipulation to bypass user approval, and trivial container escape mechanisms. The vulnerability allows an attacker to achieve remote code execution and escape from Docker containers by injecting malicious instructions into attacker-controlled websites that Auto-GPT processes.

## Attack scenario (step by step)
1. Attacker hosts a malicious website containing hidden color-coded console messages or crafted text designed to be misinterpreted as LLM instructions
2. Victim instructs Auto-GPT to perform a benign task on the attacker's website (e.g., summarize content, browse website)
3. Auto-GPT fetches and processes the malicious content through its browse_website command, passing attacker-controlled text to the LLM
4. Indirect prompt injection causes GPT-4 to interpret the injected instructions as legitimate commands rather than website content
5. Color-coded messages or unreliable statements in LLM output trick the user into approving malicious commands before execution
6. Approved commands execute arbitrary Python code, then exploit path traversal or Docker mechanisms to escape sandbox and compromise host system

## Root cause
Auto-GPT processes attacker-controlled external content (from websites) through its LLM without proper sanitization, allowing indirect prompt injection. The LLM's output is not validated before user approval, enabling social engineering. Docker images run with excessive privileges, and sandboxing via path restrictions fails due to traversal vulnerabilities. The system trusts both the LLM's reasoning and user approval without defense-in-depth controls.

## Attacker mindset
An attacker recognizes that Auto-GPT is designed to autonomously execute commands based on LLM reasoning. They exploit the trust boundary between external content and LLM instruction processing, leverage human approval workflows as a weak point through visual/logical manipulation, and target the execution environment's weak isolation boundaries. The attacker weaponizes the system's own power (code execution capabilities) against it.

## Defensive takeaways
- Never trust LLM outputs as direct instructions; implement strict schema validation and command whitelisting with no exceptions
- Sanitize and escape all external content before passing to LLMs; treat web content as untrusted input
- Implement content Security Policy-style restrictions on what can be fetched and how it's displayed to prevent console injection attacks
- Require explicit command confirmation with full content display, not just summaries; prevent visual manipulation through standardized formatting
- Run autonomous agents in strict sandboxes with minimal privileges; use seccomp, AppArmor, or equivalent controls
- Implement path canonicalization and traversal prevention in file operations; validate all file paths against whitelist
- Use principle of least privilege for Docker containers; drop unnecessary capabilities and avoid running as root
- Add execution logging and monitoring with rate-limiting for dangerous commands like code execution
- Implement LLM instruction injection detection systems that recognize suspicious pattern shifts in LLM responses
- Segment network access; use egress filtering to prevent lateral movement if sandbox is compromised

## Variant hunting
['Test other LLM-based automation tools (LangChain, LlamaIndex, other agents) for similar indirect prompt injection via web content', 'Check if other media types (PDFs, images with OCR, audio transcripts) can inject prompts when processed by autonomous agents', 'Investigate whether custom plugins or extensions in Auto-GPT introduce additional injection vectors', 'Examine if API responses from third-party services (search results, API calls) can be weaponized for prompt injection', 'Test if file-based state or cache mechanisms can be exploited to persist injected instructions across restarts', 'Analyze other code execution sandboxes in AI tools for similar path traversal or capability escape methods', 'Research whether combining multiple benign commands in sequence can achieve harmful outcomes not possible individually', 'Investigate timing-based attacks where delayed command execution combined with state changes causes unintended behavior']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1086 - PowerShell (or equivalent: T1059 - Command and Scripting Interpreter)
- T1203 - Exploitation for Client Execution
- T1047 - Windows Management Instrumentation Command-line (or T1059 for general code execution)
- T1548 - Abuse Elevation Control Mechanism
- T1134 - Access Token Manipulation (privilege escalation context)
- T1027 - Obfuscation of Files or Information (color-coded messages, hidden injection)
- T1078 - Valid Accounts (leveraging user approval as bypass)
- T1574 - Hijack Execution Flow (path traversal)
- T1611 - Escape from Container

## Notes
This writeup demonstrates a sophisticated multi-stage attack leveraging the semantic gap between human intent and LLM interpretation. The vulnerability chain is particularly dangerous because each stage exploits a reasonable design decision (fetching web content, user approval, code execution capability) individually, but their combination creates critical risk. The attack was patched in v0.4.3 but affected earlier versions. The docker escape component is notable as it required only minimal user interaction (restart), making it practically exploitable. This research is highly relevant to the growing ecosystem of autonomous AI agents and highlights fundamental challenges in securing LLM-based systems.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
