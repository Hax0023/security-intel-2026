# Denial of Service (Segmentation Fault) due to Null Pointer Dereference in mrb_vm_exec

## Metadata
- **Source:** HackerOne
- **Report:** 202584 | https://hackerone.com/reports/202584
- **Submitted:** 2017-02-01
- **Reporter:** d4nny
- **Program:** mruby-engine
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Null Pointer Dereference, Denial of Service, Memory Safety
- **CVEs:** None
- **Category:** memory-binary

## Summary
A null pointer dereference vulnerability in the mrb_vm_exec function of mruby causes a segmentation fault when executing specially crafted Ruby code. The crash occurs during method resolution in the VM execution loop, leading to immediate process termination and denial of service.

## Attack scenario
1. Attacker identifies that mruby-engine is used in a sandboxed environment or application
2. Attacker crafts malicious Ruby code that triggers method_missing on specific objects during range creation
3. Attacker provides the malicious code to the vulnerable application for execution
4. The mruby VM attempts to execute the code and encounters an undefined method during range initialization
5. Error handling code attempts to call mrb_no_method_error which dereferences a null pointer
6. The mrb_vm_exec function crashes with a segmentation fault, terminating the process

## Root cause
The vulnerability stems from insufficient null pointer validation in the mrb_vm_exec function during method resolution and error handling. When method_missing is triggered during certain operations (particularly range creation), the error handling path dereferences a null pointer without proper validation, likely in the mrb_no_method_error or mrb_method_missing functions.

## Attacker mindset
An attacker would leverage this vulnerability to deny service to applications relying on mruby for sandboxed code execution. The simplicity of triggering the crash makes it attractive for denial-of-service attacks against embedded scripting environments, game engines, or other systems using mruby.

## Defensive takeaways
- Implement comprehensive null pointer checks before dereferencing pointers in VM execution paths
- Add defensive validations in error handling and method resolution code paths
- Use static analysis tools to detect potential null pointer dereferences in C code
- Implement exception handling boundaries to gracefully handle VM errors rather than crashing
- Add fuzzing tests to the mruby test suite targeting method resolution edge cases
- Consider using sanitizers (ASan, UBSan) during development to catch memory safety issues
- Implement process-level isolation for untrusted mruby code execution

## Variant hunting
Look for similar null pointer dereferences in other VM execution paths, particularly around: method resolution (mrb_method_search), function calls (mrb_funcall_with_block), error handling mechanisms (mrb_raise, mrb_exc_new), and object initialization (mrb_range_new, other constructor functions). Check for improper handling of edge cases where objects might be in partially initialized states.

## MITRE ATT&CK
- T1499
- T1190

## Notes
The crash backtrace shows a recursive call chain through method_missing and VM execution, suggesting the vulnerability may be triggered through carefully crafted method chains. The PoC file (vm_exec.rb) is referenced but not fully detailed in the writeup. The vulnerability appears to exist in the mruby standard library, not in a custom extension. Patch should be applied to the upstream mruby project.

## Full report
<details><summary>Expand</summary>

Introduction
============

Provided PoC segfaults at mrb_vm_exec due to null pointer dereference.

Proof of concept
================
Attached the poc.

Crash report
============
```
./sandbox vm_exec.rb 
./sandbox:20: [BUG] Segmentation fault at 0x00000000000000
ruby 2.3.1p112 (2016-04-26) [x86_64-linux-gnu]

-- Control frame information -----------------------------------------------
c:0003 p:---- s:0010 e:000009 CFUNC  :sandbox_eval
c:0002 p:0201 s:0005 E:001568 EVAL   ./sandbox:20 [FINISH]
c:0001 p:0000 s:0002 E:001270 (none) [FINISH]

-- Ruby level backtrace information ----------------------------------------
./sandbox:20:in `<main>'
./sandbox:20:in `sandbox_eval'

-- Machine register context ------------------------------------------------
 RIP: 0x00007fe9d813e6ed RBP: 0x00007fe9d6cd4fd0 RSP: 0x00007fe9d6cbf0d0
 RAX: 0x0000000000000000 RBX: 0x00007fe9d6cc9170 RCX: 0x00007fe9d6cd4f80
 RDX: 0x00007fe9d6cd4b30 RDI: 0x00007fe9d6d28a80 RSI: 0x00007fe9d6ce57b0
  R8: 0x00007fe9d6cc23e0  R9: 0x0000000000000000 R10: 0x000000000000001f
 R11: 0x00007fe9d6cee1c0 R12: 0x0000000000000000 R13: 0x00007fe9d6cc24e0
 R14: 0x00007fe9d6cc9f80 R15: 0x0000000000804029 EFL: 0x0000000000010297

-- C level backtrace information -------------------------------------------
/usr/lib/x86_64-linux-gnu/libruby-2.3.so.2.3 [0x7fe9dc3c9ca5]
/usr/lib/x86_64-linux-gnu/libruby-2.3.so.2.3 [0x7fe9dc3c9edc]
/usr/lib/x86_64-linux-gnu/libruby-2.3.so.2.3 [0x7fe9dc2a3944]
/usr/lib/x86_64-linux-gnu/libruby-2.3.so.2.3 [0x7fe9dc355c3e]
/lib/x86_64-linux-gnu/libc.so.6 [0x7fe9dbeab4b0]
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_exec+0x7cd) [0x7fe9d813e6ed] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:1592
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_run+0x55) [0x7fe9d8144445] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:772
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_run+0x17) [0x7fe9d813c3f7] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:2480
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall_with_block+0x2fc) [0x7fe9d813c6fc] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:422
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall_argv+0xc) [0x7fe9d813cc5c] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:432
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall+0x258) [0x7fe9d813cec8] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:323
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_no_method_error+0x13b) [0x7fe9d816526b] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/error.c:510
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_method_missing+0x95) [0x7fe9d815f445] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/class.c:1477
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_bob_missing+0x5b) [0x7fe9d815f50b] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/class.c:1522
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall_with_block+0x263) [0x7fe9d813c663] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:415
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall_argv+0xc) [0x7fe9d813cc5c] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:432
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall+0x258) [0x7fe9d813cec8] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:323
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_range_new+0x75) [0x7fe9d814cee5] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/range.c:40
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_exec+0x28ea) [0x7fe9d814080a] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:2414
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_run+0x55) [0x7fe9d8144445] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:772
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_run+0x17) [0x7fe9d813c3f7] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:2480
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall_with_block+0x2fc) [0x7fe9d813c6fc] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:422
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall_argv+0xc) [0x7fe9d813cc5c] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:432
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall+0x258) [0x7fe9d813cec8] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:323
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_no_method_error+0x13b) [0x7fe9d816526b] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/error.c:510
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_method_missing+0x95) [0x7fe9d815f445] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/class.c:1477
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_bob_missing+0x5b) [0x7fe9d815f50b] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/class.c:1522
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_exec+0x680) [0x7fe9d813e5a0] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:1174
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_run+0x55) [0x7fe9d8144445] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:772
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_run+0x17) [0x7fe9d813c3f7] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:2480
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall_with_block+0x2fc) [0x7fe9d813c6fc] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:422
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall_argv+0xc) [0x7fe9d813cc5c] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:432
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_funcall+0x258) [0x7fe9d813cec8] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:323
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_no_method_error+0x13b) [0x7fe9d816526b] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/error.c:510
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_method_missing+0x95) [0x7fe9d815f445] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/class.c:1477
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_bob_missing+0x5b) [0x7fe9d815f50b] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/class.c:1522
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_exec+0x680) [0x7fe9d813e5a0] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:1174
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_run+0x55) [0x7fe9d8144445] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:772
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mruby_engine_monitored_eval+0x113) [0x7fe9d812f203] ../../../../ext/mruby_engine/eval_monitored.c:68
/lib/x86_64-linux-gnu/libpthread.so.0(start_thread+0xca) [0x7fe9dbc606ba]
/lib/x86_64-linux-gnu/libc.so.6(clone+0x6d) [0x7fe9dbf7c82d] ../sysdeps/unix/sysv/linux/x86_64/clone.S:109

```
MRuby analysis
==============
Code downloaded: 31-Jan-2017
Build: x64 Linux GCC with ASAN

```
Program received signal SIGSEGV, Segmentation fault.
──────────────────────────────────────────────────────────────────────────[registers]──
$rax     0x0000000000000000 $rbx     0x00007fffffff87d0 
$rcx     0x000061d00001e000 $rdx     0x0000000000000000 
$rsp     0x00007fffffff79f0 $rbp     0x00007fffffff87f0 
$rsi     0x0000000000000003 $rdi     0x000061400000fe40 
$rip     0x0000000000427fbf $r8      0x0000000000000000 
$r9      0x00007fffffff8c40 $r10     0x0000000000000009 
$r11     0x00007ffff692d550 $r12     0x00007fffffff8d80 
$r13   

</details>

---
*Analysed by Claude on 2026-05-24*
