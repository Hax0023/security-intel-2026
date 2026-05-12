# Struct Type Confusion RCE in mruby

## Metadata
- **Source:** HackerOne
- **Report:** 181879 | https://hackerone.com/reports/181879
- **Submitted:** 2016-11-13
- **Reporter:** h72
- **Program:** mruby
- **Bounty:** Unknown
- **Severity:** Critical
- **Vuln:** Type Confusion, Memory Corruption, Instruction Pointer Control, Out-of-Bounds Access
- **CVEs:** None
- **Category:** memory-binary

## Summary
A type confusion vulnerability in mruby allows attackers to corrupt memory and gain control of the instruction pointer by exploiting improper struct type handling. The vulnerability enables jumping to arbitrary memory addresses and can be leveraged for full remote code execution when combined with arbitrary read/write primitives.

## Attack scenario
1. Attacker crafts a malicious mruby script that exploits struct type confusion
2. Script creates or manipulates struct instances to cause type confusion between different data structures
3. Memory layout corruption allows attacker to overwrite critical pointers or function references
4. Attacker controls the instruction pointer and directs execution to arbitrary memory address (0x0000133713371337 in PoC)
5. With additional arbitrary read/write primitives, attacker can write shellcode to executable memory region
6. Code execution achieved with attacker-controlled instructions

## Root cause
Improper type checking and validation when handling struct objects in mruby, allowing type confusion that corrupts memory layout and overwrites instruction pointers or function references

## Attacker mindset
Exploit memory safety weaknesses in the Ruby VM to achieve low-level code execution. Type confusion provides a bridge from high-level script control to low-level memory corruption.

## Defensive takeaways
- Implement strict runtime type checking for struct operations
- Add type guards before memory operations on struct fields
- Use memory tagging or type safety mechanisms to prevent type confusion
- Implement bounds checking on struct field access
- Enable ASLR and CFI (Control Flow Integrity) mitigations on mruby deployments
- Fuzz struct handling code paths with malformed inputs
- Sanitize and validate all struct instantiation and manipulation operations

## Variant hunting
Search for similar type confusion issues in: other struct/class field access mechanisms, array/hash type confusion, method dispatch on confused types, object initialization sequences, inheritance chains with type mismatches

## MITRE ATT&CK
- T1190
- T1203
- T1055

## Notes
This is a VM-level vulnerability with high impact. The PoC demonstrates instruction pointer hijacking (segfault at controlled address proves control). Actual RCE would require chainable primitives (arbitrary write). mruby is commonly embedded in applications, making this particularly dangerous. The annotation level in PoC suggests well-documented exploitation technique.

## Full report
<details><summary>Expand</summary>

Heya!

I've been poking at mruby a bit more and I've found a vulnerability that allows an attacker to take control of the instruction pointer.

I've attached a proof of concept script that when run in mruby will jump to `0x0000133713371337` and segfault.

While the proof of concept script just jumps to an attacker controlled address and crashes, it would almost certainly be possible to achieve full remote code execution, especially given an arbitrary read/write primitive (which is easily created using the same techniques as in the proof of concept)

The proof of concept script has detailed annotations throughout about how it works, but I'm also happy to clarify anything if need be :)

Cheers,

███████

</details>

---
*Analysed by Claude on 2026-05-12*
