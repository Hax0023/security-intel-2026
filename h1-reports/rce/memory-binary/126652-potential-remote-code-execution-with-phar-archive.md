# Remote Code Execution via PHAR Archive Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 126652 | https://hackerone.com/reports/126652
- **Submitted:** 2016-03-29
- **Reporter:** vah13
- **Program:** PHP
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Buffer Overflow, Memory Corruption, Arbitrary Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
A vulnerability in PHP's PHAR archive handling allows manipulation of the EIP register through crafted archive files, leading to remote code execution. The vulnerability enables attackers to control program execution flow by corrupting memory during PHAR file processing.

## Attack scenario
1. Attacker crafts a malicious PHAR archive file with specific payload structure
2. Victim application processes the PHAR file using PHP's file/archive functions
3. Memory corruption occurs during PHAR parsing, overwriting the EIP register
4. Attacker gains control of program execution pointer and directs it to payload code
5. Malicious code executes with privileges of the PHP process
6. Remote code execution achieved on the victim system

## Root cause
Improper bounds checking or unsafe memory operations in PHP's PHAR archive parsing code, allowing attacker-controlled data to overwrite critical stack/heap memory regions containing return addresses or function pointers

## Attacker mindset
An attacker would identify that many web applications process archives (uploads, installations, updates) without sufficient validation. By crafting a weaponized PHAR file, they could achieve code execution on vulnerable systems through a simple file upload or if the application automatically processes archives.

## Defensive takeaways
- Implement strict PHAR file format validation before processing
- Use Address Space Layout Randomization (ASLR) and Data Execution Prevention (DEP/NX) at OS level
- Disable PHAR stream wrapper if not required (phar.readonly=1)
- Restrict file_exists(), is_file(), and similar functions from accepting PHAR URIs (open_basedir)
- Implement sandboxing for archive processing operations
- Keep PHP updated with security patches
- Avoid processing user-supplied PHAR files; validate file types strictly
- Use memory-safe alternatives for archive handling where possible

## Variant hunting
Test other compression format handlers (ZIP, TAR, RAR) for similar memory corruption
Investigate PHAR metadata parsing for additional overflow vectors
Examine all PHAR file structure operations for unsafe memory access
Review other PHP stream wrapper implementations for similar issues
Test PHAR with nested/recursive archive structures

## MITRE ATT&CK
- T1190
- T1203
- T1499

## Notes
Report is minimal with limited technical details provided. Researcher references external PoC and crash logs (300+) not included in the writeup, suggesting significant vulnerability impact. The mention of EIP manipulation indicates 32-bit x86 architecture target. Related to PHP bug tracker #71860. Buffer overflow severity indicates potential for local privilege escalation or remote code execution depending on execution context.

## Full report
<details><summary>Expand</summary>

https://bugs.php.net/bug.php?id=71860
I can manipulate EIP register.
https://drive.google.com/file/d/0B7gu5bbuZn2ITk54ZGl5SzVWNlk/view
more PoC and full crash list (around 300) will send later.


tnx

</details>

---
*Analysed by Claude on 2026-05-12*
