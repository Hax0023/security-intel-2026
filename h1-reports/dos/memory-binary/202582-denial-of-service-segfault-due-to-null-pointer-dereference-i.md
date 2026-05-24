# Denial of Service (Segmentation Fault) due to Null Pointer Dereference in mrb_obj_instance_eval

## Metadata
- **Source:** HackerOne
- **Report:** 202582 | https://hackerone.com/reports/202582
- **Submitted:** 2017-02-01
- **Reporter:** d4nny
- **Program:** mruby
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Null Pointer Dereference, Denial of Service, Memory Safety Violation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A null pointer dereference vulnerability exists in the mrb_obj_instance_eval function in mruby's VM implementation that can be triggered by crafted Ruby code, causing a segmentation fault. The vulnerability crashes the interpreter by dereferencing a null pointer during the evaluation of instance_eval with specific arguments, leading to complete denial of service of any application using the affected mruby version.

## Attack scenario
1. Attacker crafts a malicious Ruby script containing a call to instance_eval with specific arguments designed to trigger the null pointer dereference
2. Attacker submits or executes this script through an application that uses mruby for code evaluation (such as a sandbox environment)
3. The mruby interpreter processes the instance_eval call and reaches the vulnerable code path in eval_under function
4. A null or invalid pointer is dereferenced at memory address 0x41b236 without proper validation
5. The segmentation fault occurs, crashing the interpreter process and the host application
6. Service becomes unavailable until the application is restarted, achieving denial of service

## Root cause
The mrb_obj_instance_eval function in vm.c fails to properly validate or handle null pointers before dereferencing them. The eval_under function attempts to dereference a pointer without confirming it has been properly initialized, likely when processing instance context or evaluating the block parameter for instance_eval.

## Attacker mindset
An attacker targeting a mruby-based sandbox or interpreter service would craft minimal PoC code to crash the service. The attacker seeks to achieve denial of service with low complexity - simply providing a malformed instance_eval call that causes the interpreter to crash, demonstrating the vulnerability and potentially making the service unavailable.

## Defensive takeaways
- Implement null pointer checks before all pointer dereferences, especially in VM instruction handlers and evaluation functions
- Add input validation for all arguments to built-in evaluation functions like instance_eval
- Use static analysis tools (ASan, UBSan) during development to catch null pointer dereferences early
- Implement fuzzing of VM instruction sequences to identify crash conditions
- Add bounds checking and guard clauses around pointer operations in critical VM functions
- Consider using safer languages or memory management techniques for VM core implementation
- Implement exception handling to gracefully handle invalid evaluation contexts instead of dereferencing null pointers

## Variant hunting
Search for similar null pointer dereferences in: mrb_obj_class_eval (similar evaluation function), other instance method evaluation paths, block evaluation functions, context switching code in vm.c, and any function calling eval_under with potentially null context pointers.

## MITRE ATT&CK
- T1190
- T1499

## Notes
The crash occurs at line 522 in vm.c within mrb_obj_instance_eval. The PoC file (eval.rb) referenced in the report would contain the specific instance_eval call sequence triggering the crash. The vulnerability affects mruby versions from Jan 31, 2017 and earlier. ASAN (Address Sanitizer) would detect this issue, suggesting proper sanitizer integration in CI/CD pipelines could have prevented this. The issue is in mruby (not Ruby/MRI), which is a lightweight embeddable Ruby implementation often used in constrained environments.

## Full report
<details><summary>Expand</summary>

Introduction
============

Provided PoC segfaults at mrb_obj_instance_eval due to null pointer dereference.

Proof of concept
================
Attached the poc.

Crash report
============
```
./sandbox eval.rb 
./sandbox:20: [BUG] Segmentation fault at 0x00000000000003
ruby 2.3.1p112 (2016-04-26) [x86_64-linux-gnu]

-- Control frame information -----------------------------------------------
c:0003 p:---- s:0010 e:000009 CFUNC  :sandbox_eval
c:0002 p:0201 s:0005 E:000ef8 EVAL   ./sandbox:20 [FINISH]
c:0001 p:0000 s:0002 E:000950 (none) [FINISH]

-- Ruby level backtrace information ----------------------------------------
./sandbox:20:in `<main>'
./sandbox:20:in `sandbox_eval'

-- Machine register context ------------------------------------------------
 RIP: 0x00007f918a9e1761 RBP: 0x00007f918956dcb0 RSP: 0x00007f9189564a80
 RAX: 0x00007f918956dc80 RBX: 0x0000000000000003 RCX: 0x00007f9189572a00
 RDX: 0x00007f9189578fd0 RDI: 0x0000000000000082 RSI: 0x0000000000000004
  R8: 0x0000000000000002  R9: 0x0000000000000000 R10: 0x0000000000000020
 R11: 0x00007f9189586d50 R12: 0x00007f91895664e0 R13: 0x00007f9189578f80
 R14: 0x00007f91895664e0 R15: 0x00007f9189571610 EFL: 0x0000000000010213

-- C level backtrace information -------------------------------------------
/usr/lib/x86_64-linux-gnu/libruby-2.3.so.2.3 [0x7f918ec6dca5]
/usr/lib/x86_64-linux-gnu/libruby-2.3.so.2.3 [0x7f918ec6dedc]
/usr/lib/x86_64-linux-gnu/libruby-2.3.so.2.3 [0x7f918eb47944]
/usr/lib/x86_64-linux-gnu/libruby-2.3.so.2.3 [0x7f918ebf9c3e]
/lib/x86_64-linux-gnu/libc.so.6 [0x7f918e74f4b0]
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_obj_instance_eval+0x91) [0x7f918a9e1761] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:522
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_exec+0x3d8c) [0x7f918a9e5cac] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:1350
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mrb_vm_run+0x55) [0x7f918a9e8445] /home/dan/shpy/mruby-engine/ext/mruby_engine/mruby/src/vm.c:772
/home/dan/shpy/mruby-engine/lib/mruby_engine/mruby_engine.so(mruby_engine_monitored_eval+0x113) [0x7f918a9d3203] ../../../../ext/mruby_engine/eval_monitored.c:68
/lib/x86_64-linux-gnu/libpthread.so.0(start_thread+0xca) [0x7f918e5046ba]
/lib/x86_64-linux-gnu/libc.so.6(clone+0x6d) [0x7f918e82082d] ../sysdeps/unix/sysv/linux/x86_64/clone.S:109
```
MRuby analysis
==============
Code downloaded: 31-Jan-2017
Build: x64 Linux GCC with ASAN

```
Program received signal SIGSEGV, Segmentation fault.
───────────────────────────────────────────────────────────────────[registers]──
$rax     0x000002005fff8000 $rbx     0x00000ffffffff930 
$rcx     0x0000000000000000 $rdx     0x00000fff00000001 
$rsp     0x00007fffffffc8e0 $rbp     0x00007fffffffc940 
$rsi     0x0000000000000007 $rdi     0x000061400000fe40 
$rip     0x000000000041b236 $r8      0x00007fff00000003 
$r9      0x000062f0000076f0 $r10     0x0000000000000007 
$r11     0x00007ffff692c390 $r12     0x00007fffffffc980 
$r13     0x00007fffffffca60 $r14     0x00007fffffffc980 

0x41b224	 <eval_under+629>     rex.RB   call 0x49043b72
0x41b22a	 <eval_under+635>     mov   eax,edx
0x41b22c	 <eval_under+637>     shr   rax,0x3
0x41b230	 <eval_under+641>     add   rax,0x7fff8000
0x41b236	 <eval_under+647>     movzx   eax,BYTE PTR [rax] 		  <-  $pc
0x41b239	 <eval_under+650>     test   al,al
0x41b23b	 <eval_under+652>     setne   cl
0x41b23e	 <eval_under+655>     cmp   al,0x3
0x41b240	 <eval_under+657>     setle   al

g> bt
#0  0x000000000041b236 in eval_under ()
#1  0x000000000041bb80 in mrb_obj_instance_eval ()
#2  0x0000000000424544 in mrb_vm_exec ()
#3  0x000000000041d290 in mrb_vm_run ()
#4  0x0000000000433007 in mrb_top_run ()
#5  0x00000000004a2431 in mrb_load_exec ()
#6  0x00000000004a2592 in mrb_load_file_cxt ()
#7  0x0000000000403758 in main ()

```

</details>

---
*Analysed by Claude on 2026-05-24*
