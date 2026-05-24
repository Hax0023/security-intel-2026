# Full Path Disclosure in PasswordLock Library via Type Validation Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 115422 | https://hackerone.com/reports/115422
- **Submitted:** 2016-02-08
- **Reporter:** supernatural
- **Program:** HackerOne (specific program not disclosed in excerpt)
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Full Path Disclosure, Type Error Handling, Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The PasswordLock library fails to validate that password input is a string before passing it to the hash() function, allowing attackers to trigger a PHP warning that discloses the full file path. This information disclosure occurs when non-string values are supplied to the hashAndEncrypt() or decryptAndVerify() functions.

## Attack scenario
1. Attacker identifies a password input field that uses the vulnerable PasswordLock library
2. Attacker sends a non-string value (array, object, integer, etc.) as the password parameter
3. The application passes this non-string value to hashAndEncrypt() or decryptAndVerify() method
4. The hash() function is called with a non-string parameter, triggering a PHP warning
5. The warning message is displayed or logged, revealing the full file system path
6. Attacker uses the disclosed path information for reconnaissance or to plan further attacks

## Root cause
Insufficient input validation in the PasswordLock library's hashAndEncrypt() and decryptAndVerify() methods. The code does not verify that the password parameter is a string type before passing it to the hash() function, which expects a string as its second parameter.

## Attacker mindset
Information gathering - exploiting poor error handling to extract system path information that aids in reconnaissance and vulnerability mapping.

## Defensive takeaways
- Implement strict type validation for all input parameters before processing
- Use type hints and strict mode in PHP to catch type mismatches early
- Suppress or sanitize error messages to prevent information disclosure
- Log detailed errors server-side while showing generic messages to users
- Add unit tests for edge cases including type mismatches and invalid inputs
- Use try-catch blocks to handle exceptions gracefully without exposing paths

## Variant hunting
Check other cryptographic libraries (bcrypt, Argon2, scrypt wrappers) for similar type validation gaps; search for other hash() function calls without parameter type validation; audit password verification logic across the codebase.

## MITRE ATT&CK
- T1592.004
- T1592.001

## Notes
Low severity issue as it primarily leaks non-sensitive path information, but can aid attackers in reconnaissance. The actual password hashing logic may still be secure; the vulnerability is in error handling and validation. PHP configuration (error_reporting, display_errors) can mitigate exposure.

## Full report
<details><summary>Expand</summary>

Hi,

Password input must be string but not checked in PasswordLock lib,
It will throw an exception on `hash` function call

    Warning: hash() expects parameter 2 to be string

So you must validate it in `hashAndEncrypt` and `decryptAndVerify`

Regards

</details>

---
*Analysed by Claude on 2026-05-24*
