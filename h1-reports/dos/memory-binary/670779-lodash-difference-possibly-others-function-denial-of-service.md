# Lodash Denial of Service via Unvalidated Input to difference() Function

## Metadata
- **Source:** HackerOne
- **Report:** 670779 | https://hackerone.com/reports/670779
- **Submitted:** 2019-08-09
- **Reporter:** spengietz
- **Program:** Lodash
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Improper Input Validation, Heap Memory Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Lodash difference() function fails to validate that input parameters are actual arrays, accepting any object with a length property. An attacker can supply a malicious object with an arbitrarily large length value, causing the function to attempt allocating massive memory arrays, exhausting the JavaScript heap and crashing the Node.js process or freezing browser tabs.

## Attack scenario
1. Attacker identifies that the target application uses Lodash and passes user-supplied data to the _.difference() function
2. Attacker crafts a malicious object with a length property set to an extremely large number (e.g., 99999999999)
3. Attacker supplies this object as input to _.difference() either directly or through application input vectors
4. The baseDifference() function accepts the object as an array-like without validation
5. Lodash attempts to allocate an array matching the specified length, consuming gigabytes of memory
6. JavaScript heap memory is exhausted, triggering a fatal out-of-memory error and crashing the process

## Root cause
The difference() function and its underlying baseDifference() helper lack proper type checking. They accept any object with a length property as an array-like object without validating it is an actual Array, relying on duck-typing that can be exploited by supplying arbitrary objects with large length values.

## Attacker mindset
An attacker pentesting an application discovers it accepts user input and passes it to Lodash utility functions without sanitization. Recognizing that Lodash performs loose type checking, the attacker crafts a small payload (a simple JSON object) that exploits this to crash the application, demonstrating a denial of service vulnerability with minimal effort.

## Defensive takeaways
- Always validate and sanitize user input before passing to third-party library functions, especially utility libraries
- Implement input type checking at application boundaries—verify inputs are actual Arrays, not just array-like objects
- Use strict mode and TypeScript to catch type mismatches at development time
- Apply resource limits and timeout protections to prevent unbounded memory allocation
- Monitor memory usage and implement circuit breakers to detect and halt resource exhaustion attacks
- Keep dependencies updated and review security advisories for widely-used libraries like Lodash
- Consider using alternative libraries or implementing custom array comparison logic with proper validation

## Variant hunting
Test all Lodash array manipulation functions (intersection, union, xor, etc.) for similar unvalidated array-like input handling
Check if other utility functions that accept multiple array arguments have the same vulnerability
Investigate whether Lodash's handling of array-like objects is exploitable in other contexts (map, filter, reduce wrappers)
Test with objects containing length properties set to negative numbers, NaN, or Infinity values
Examine other npm packages with similar array utility functions for identical patterns of loose type checking

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1499: Endpoint Denial of Service
- T1561: Disk Wipe
- T1499.004: Application Exhaustion Flood

## Notes
This vulnerability affects Lodash 4.17.15 and potentially other versions. It was discovered during a penetration test of a production application, making it a real-world exploitable issue. The vulnerability is particularly dangerous in Node.js server environments where a single request can crash an entire process. Browser environments are also affected but with less severe consequences (tab freeze/crash rather than process termination). The fix would require Lodash to implement proper Array type checking using Array.isArray() or similar validation before processing array arguments.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

I would like to report a denial of service in Lodash.
It allows excessive usage of the NodeJS process's memory, leading to a "JavaScript heap out of memory" crash. The same vulnerability exists in the browser version of Lodash and causes Firefox's tab to crash and restart and causes Chrome's tab to completely freeze and become uncloseable (from my testing at least).

# Module

**module name:** Lodash
**version:** Only tested in 4.17.15
**npm page:** `https://www.npmjs.com/package/lodash`

## Module Description

> Copy description from npm page

A modern JavaScript utility library delivering modularity, performance & extras.
The Lodash library exported as Node.js modules.

## Module Stats

> Replace stats below with numbers from npm’s module page:

24,853,923 downloads in the last week
I can't find where it lists the daily/monthly downloads

# Vulnerability

## Vulnerability Description

> Description about how the vulnerability was found and how it can be exploited, how it harms package users (data modification/lost, system access, other.

The vulnerability was discovered while pentesting a web application for a client. The Lodash "difference" function (https://github.com/lodash/lodash/blob/4.17.15/lodash.js#L6947) uses the "baseDifference" function (https://github.com/lodash/lodash/blob/4.17.15/lodash.js#L2764) to perform what it needs to. "difference" is supposed to accept two arrays (`_.difference(array, [values])`) but it does not actually verify whether it is dealing with valid arrays before processing the data. This means a custom malicious Object can be supplied and the function will think it is an array, allowing excessive memory consumption that ends up in a crash of the Node.js process (or crash/freeze of the browser tab in Firefox/Chrome).

It was found to be exploitable in the clients application because they were passing user-supplied data into the "difference" function, which allowed me to crash their application with this vulnerability.

## Steps To Reproduce:

> Detailed steps to reproduce with all required references/steps/commands. If there is any exploit code or reference to the package source code this is the place where it should be put.

Benign example:
```
const _ = require('lodash')

user_supplied_array = [1, 2, 3]
values_to_compare_to = {'length': 5} // An object with the "length" property defined to an integer will be accepted as an array by the _.difference function

_.difference(values_to_compare_to, user_supplied_array) // This will output a new array of length 5 where each value is "undefined"
```

Because Lodash is essentially creating a new array of the length that we specify in "values_to_compare_to", we can provide a large value that will cause the Node.js process to crash before it can successfully create the array.

Will crash Node.js example:
```
const _ = require('lodash')

user_supplied_array = [1, 2, 3]
values_to_compare_to = {'length': 99999999999} // This could be any huge value

_.difference(values_to_compare_to, user_supplied_array) // The Node.js process will crash, saying that the JavaScript heap ran out of memory
```

When the Node.js process crashes, a stack trace similar to the following is output:
```
[5515:0x55aa82652700]    41959 ms: Mark-sweep 580.0 (585.7) -> 580.0 (585.7) MB, 201.8 / 0.0 ms  allocation failure GC in old space requested
[5515:0x55aa82652700]    42169 ms: Mark-sweep 580.0 (585.7) -> 579.9 (584.2) MB, 209.7 / 0.0 ms  last resort GC in old space requested
[5515:0x55aa82652700]    42372 ms: Mark-sweep 579.9 (584.2) -> 579.9 (584.2) MB, 203.2 / 0.0 ms  last resort GC in old space requested


<--- JS stacktrace --->

==== JS stack trace =========================================

Security context: 0x2eaefaca5729 <JSObject>
    1: baseDifference [/root/temp/tmp/node_modules/lodash/lodash.js:~2764] [pc=0x11aea9f0d272](this=0x28b6ba70c0f9 <JSGlobal Object>,array=0x3dd3a43ca4c9 <Object map = 0x1294fe65a571>,values=0x3dd3a43ca4a9 <JSArray[2]>,iteratee=0x3dd3a43822d1 <undefined>,comparator=0x3dd3a43822d1 <undefined>)
    2: arguments adaptor frame: 2->4
    3: /* anonymous */ [/root/temp/tmp/node_modules/lodash/lodash.j...

FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory
 1: node::Abort() [node]
 2: 0x55aa808c347e [node]
 3: v8::Utils::ReportOOMFailure(char const*, bool) [node]
 4: v8::internal::V8::FatalProcessOutOfMemory(char const*, bool) [node]
 5: v8::internal::Factory::NewUninitializedFixedArray(int) [node]
 6: 0x55aa80448b1d [node]
 7: v8::internal::Runtime_GrowArrayElements(int, v8::internal::Object**, v8::internal::Isolate*) [node]
 8: 0x11aea9d842fd
Aborted
```


## Patch

> If you're able to provide a patch with the fix please post it in this section

I don't know specifically, but it seems that proper verification that both inputs are arrays would fix this.

## Supporting Material/References:

> State all technical information about the stack where the vulnerability was found

Tested on two separate operating systems with the same end results.
Windows:
- Windows 10
- Node.js v8.9.4
- npm version 5.6.0
- Firefox 68.01 and Chrome 76.0.3809.100 when testing the browser version of Lodash

Linux:
- Kali Linux
- Node.js v9.0.0
- npm version 6.1.0
- Did not test in Firefox/Chrome on this operating system

# Wrap up

> Select Y or N for the following statements:

- I contacted the maintainer to let them know: N, it said to report it here
- I opened an issue in the related repository: N, it said not to publicly disclose it until after

## Impact

An attacker could cause excessive resource consumption which could slow down the server for other users or they could cause an outright crash of the Node.js process, denying service to all users of the application.

</details>

---
*Analysed by Claude on 2026-05-24*
