# Null target_class Denial of Service in mruby Object#instance_exec

## Metadata
- **Source:** HackerOne
- **Report:** 183405 | https://hackerone.com/reports/183405
- **Submitted:** 2016-11-19
- **Reporter:** h72
- **Program:** mruby
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Null Pointer Dereference, Denial of Service, Missing Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Object#instance_exec method in mruby fails to validate that target_class is non-null before the OP_CLASS and OP_MODULE opcodes attempt to dereference it. When a singleton class cannot be created for an object (like Integer 1), executing class/module definitions within instance_exec causes a null pointer dereference, crashing the VM.

## Attack scenario
1. Attacker identifies that mruby's instance_exec sets target_class to NULL when singleton class creation fails for immutable objects
2. Attacker crafts a simple Ruby expression calling instance_exec on an integer primitive (1.instance_exec)
3. Within the block passed to instance_exec, attacker defines a class or module (class X; end)
4. The VM executes OP_CLASS opcode which dereferences the NULL target_class pointer without validation
5. Null pointer dereference triggers segmentation fault, crashing the mruby VM
6. Service relying on mruby interpreter becomes unavailable

## Root cause
The Object#instance_exec method in mrbgems/mruby-object-ext/src/object.c sets target_class to NULL when singleton class creation fails, but the OP_CLASS and OP_MODULE opcodes lack null pointer validation before dereferencing target_class. Missing defensive programming checks allow unchecked null dereference.

## Attacker mindset
An attacker with code execution capability or ability to submit Ruby code to an mruby interpreter seeks to trigger a denial of service by crashing the VM. This is trivial to exploit requiring only a single line of code, making it an attractive DoS vector for applications embedding mruby.

## Defensive takeaways
- Always validate pointer dereferences before use, especially in VM opcode implementations
- Add null pointer checks before accessing target_class in OP_CLASS and OP_MODULE opcode handlers
- Consider throwing an exception or returning an error code instead of allowing null dereference
- Implement defensive programming patterns for all VM state that could be null
- Add regression tests covering edge cases like class definition on immutable objects
- Document preconditions for VM state assumptions (e.g., target_class must be non-null)

## Variant hunting
Search for other opcodes or VM operations that assume non-null target_class; audit all singleton class creation paths for null returns; test method/constant definition operations on other immutable types (symbols, numbers); check module inclusion and method aliasing in instance_exec context; fuzz instance_exec with various object types to find similar crashes

## MITRE ATT&CK
- T1499.004
- T1190

## Notes
This is a classic VM crash bug with trivial reproducibility. The vulnerability exists in the VM implementation itself rather than in user code, making it critical for mruby embedders. The fix requires adding null checks in opcode handlers to gracefully handle the edge case of immutable objects passed to instance_exec.

## Full report
<details><summary>Expand</summary>

The `Object#instance_exec` method in `mrbgems/mruby-object-ext/src/object.c` executes a block in the context of an object. It sets the VM's `target_class` pointer to the singleton class of this object. `target_class` is used as the definition target for constants and methods.

If a singleton class cannot be created for an object, `target_class` is set to `NULL`. The `OP_CLASS` and `OP_MODULE` opcodes in the VM assume `target_class` is not null when defining new classes and modules.

This causes a null pointer dereference and segfaults the mruby VM.

Sample code:

```
1.instance_exec { class X; end }
```

</details>

---
*Analysed by Claude on 2026-05-24*
