# Curl parse_connect_to_string Heap-Overread Leading to Denial of Service via CURLOPT_CONNECT_TO

## Metadata
- **Source:** HackerOne
- **Report:** 3306456 | https://hackerone.com/reports/3306456
- **Submitted:** 2025-08-20
- **Reporter:** irene1hacker
- **Program:** curl/libcurl
- **Bounty:** Not specified in writeup
- **Severity:** Medium
- **Vuln:** Heap Buffer Overread, Out-of-Bounds Read, Input Validation Failure, Denial of Service
- **CVEs:** None
- **Category:** uncategorised

## Summary
A heap buffer overread vulnerability exists in libcurl's parse_connect_to_string function when processing malformed CURLOPT_CONNECT_TO strings containing unexpected characters like newlines. This flaw enables attackers to trigger a segmentation fault and crash applications using the vulnerable library, resulting in denial of service without requiring code execution or data access.

## Attack scenario
1. Attacker identifies an application using libcurl with CURLOPT_CONNECT_TO functionality enabled
2. Attacker crafts a malicious CURLOPT_CONNECT_TO string containing unexpected characters (e.g., embedded newlines or null bytes)
3. Attacker provides this string to the vulnerable application through user input, environment variables, or configuration files
4. The parse_connect_to_string function fails to properly validate the input and reads beyond allocated heap buffer boundaries
5. Address sanitizer or runtime detection catches the heap overread, triggering a segmentation fault
6. Application crashes, causing denial of service for legitimate users

## Root cause
Insufficient input validation in parse_connect_to_string function. The code does not properly sanitize or validate host strings before processing, allowing unexpected characters like newlines to bypass validation checks. String parsing logic assumes well-formed input and dereferences pointers without bounds checking, leading to out-of-bounds memory access.

## Attacker mindset
An attacker with the ability to influence CURLOPT_CONNECT_TO parameters (through user input, configuration, or network requests) seeks to disrupt service availability. The attacker recognizes that fuzzing with malformed input can expose memory safety issues in string parsing logic, particularly at boundary conditions where validation is weak or missing.

## Defensive takeaways
- Implement strict input validation for all CURLOPT_CONNECT_TO strings, rejecting inputs with invalid characters (newlines, null bytes, control characters)
- Use bounds checking and safe string functions to prevent buffer overreads during string parsing
- Employ fuzzing and sanitizer testing (ASAN, UBSAN) during development to catch memory safety issues early
- Validate string length and format before dereferencing pointers in parse functions
- Consider using safe parsing libraries or APIs that handle malformed input gracefully
- Implement comprehensive unit tests covering edge cases and malformed input scenarios
- Apply defense-in-depth: limit access to CURLOPT_CONNECT_TO functionality and validate configuration sources

## Variant hunting
Search for similar parse_* functions handling user-controlled strings without proper validation
Audit other CURLOPT_* options for similar input validation gaps
Check for heap overread vulnerabilities in URL parsing, hostname parsing, and other string processing functions
Fuzz additional string parsing code paths with control characters and boundary values
Review code handling custom connection routing and proxy configurations
Examine related functions in networking libraries that parse untrusted input

## MITRE ATT&CK
- T1190
- T1499
- T1499.1

## Notes
The vulnerability requires attackers to control CURLOPT_CONNECT_TO input, limiting exploitation scope to applications that accept user-controlled connection-to parameters. While the severity is medium (DoS only, no RCE/data exposure), the presence of heap overread suggests potential for escalation if exploitable for information disclosure. The development-branch version (8.16.0-DEV) indicates this was caught before stable release. Recommend updating to patched version and auditing other libcurl option handlers for similar patterns.

## Full report
<details><summary>Expand</summary>

## Summary:
A heap-buffer-overread occurs in Curl's parse_connect_to_string function when using the CURLOPT_CONNECT_TO option with crafted input. This can lead to a segmentation fault and crash of the application, resulting in a denial-of-service. The issue is triggered by malformed host strings containing unexpected characters, such as newline (\n), that are not properly validated before dereferencing.

## Affected version
curl 8.16.0-DEV (Linux) libcurl/8.16.0-DEV

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1.Compile libcurl with sanitizers enabled:
```
mkdir build && cd build
CC=clang CXX=clang++ cmake ..   -DCMAKE_BUILD_TYPE=Debug   -DCMAKE_C_FLAGS="-g -O1 -fsanitize=address"   -DBUILD_SHARED_LIBS=OFF   -DBUILD_STATIC_LIBS=ON   -DBUILD_TESTING=OFF   -DBUILD_EXAMPLES=OFF   -DENABLE_MANUAL=OFF
cmake --build . --config Debug
```
 2. Build the test target
```
clang++ -g -O1 -fsanitize=address     -I../include -I../src/include     minimal_curl_connect_crash.cpp ./lib/libcurl-d.a     -o minimal_curl_connect_crash     -lpsl -ldl -lpthread -lssl -lcrypto -lz
```
3. Run the test target
```
./minimal_curl_connect_crash
```
## Supporting Material/References:
{F4696730}
{F4696745}

## Impact

## Summary:
An attacker can cause a denial-of-service (DoS) by crashing the application using a specially crafted CURLOPT_CONNECT_TO string. No code execution or data leakage is known; the primary risk is service disruption.

</details>

---
*Analysed by Claude on 2026-05-24*
