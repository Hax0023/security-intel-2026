# DoS: Type Confusion in mrb_no_method_error

## Metadata
- **Source:** HackerOne
- **Report:** 181871 | https://hackerone.com/reports/181871
- **Submitted:** 2016-11-13
- **Reporter:** raydot
- **Program:** mruby
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Type Confusion, Memory Corruption, Denial of Service, Arbitrary Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
A type confusion vulnerability exists in mruby's NoMethodError handling where overwriting the 'new' method of the NoMethodError singleton class to return a non-exception object causes memory corruption and potential arbitrary code execution. The vulnerability is triggered when code path expects an exception object but receives an arbitrary value instead.

## Attack scenario
1. Attacker identifies that NoMethodError.new can be overridden via define_singleton_method
2. Attacker redefines NoMethodError.new to return a string or other non-exception object
3. Code path attempts to call Object.q which triggers the no method error handler
4. Handler expects exception object and calls methods on the returned string
5. Type confusion occurs as the mruby runtime tries to interpret string data as exception object
6. Memory corruption or arbitrary code execution occurs during subsequent operations

## Root cause
The mruby runtime creates a NoMethodError exception without proper type validation of the object returned by NoMethodError.new. The code assumes the return value is always an exception object and proceeds to manipulate it without checking its actual type, leading to out-of-bounds memory access or interpretation of arbitrary data as exception metadata.

## Attacker mindset
An attacker within a sandboxed mruby environment seeks to escape sandbox constraints by exploiting type confusion. By hijacking exception creation, they can force the runtime to treat uncontrolled data as exception objects, enabling memory corruption that could lead to arbitrary code execution despite sandbox protections.

## Defensive takeaways
- Always validate return types from methods that are expected to produce specific object types, especially in core error handling paths
- Restrict or prevent overriding of critical singleton methods like Exception.new, NoMethodError.new, or other core exception constructors
- Implement type checks (e.g., rb_obj_is_kind_of) on exception objects before dereferencing their fields
- Use static analysis to identify code paths that assume specific types without validation
- Consider making exception class constructors non-overridable or add assertions in exception handling code
- Apply additional validation in sandboxed environments to prevent modification of core exception handling mechanisms

## Variant hunting
Search for similar patterns where other Exception subclasses (StandardError, RuntimeError, etc.) could be overridden to return non-exception objects. Look for other code paths that assume specific return types from 'new' methods without validation. Examine any place where rb_*_error functions are called to see if they validate exception object types.

## MITRE ATT&CK
- T1190
- T1203

## Notes
This is a sandbox escape vulnerability that exploits type confusion in exception handling. The patch likely adds type validation to ensure NoMethodError.new returns a proper exception object. The issue demonstrates how allowing modification of core language constructors can break fundamental assumptions in language runtimes. Similar issues may exist in other exception classes.

## Full report
<details><summary>Expand</summary>

Overwriting the 'new' method of the NoMethodError singleton to not return an exception object leads to memory corruption and possibly arbitrary code execution.

Running the following code under the mruny-engine sandbox script results in a native crash:
    NoMethodError.define_singleton_method(:new) do "waat" end
    Object.q

Attached is a patch to mitigate the issue.


</details>

---
*Analysed by Claude on 2026-05-24*
