# Full Path Disclosure in EasyDB

## Metadata
- **Source:** HackerOne
- **Report:** 115337 | https://hackerone.com/reports/115337
- **Submitted:** 2016-02-08
- **Reporter:** supernatural
- **Program:** EasyDB
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Full Path Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A Full Path Disclosure (FPD) vulnerability exists in EasyDB where server file paths are exposed in error messages. The researcher proposes validating input parameters to be one-dimensional arrays before execution to prevent nested array exploitation that could trigger unhandled exceptions.

## Attack scenario
1. Attacker identifies the EasyDB application uses an execute() function with parameter handling
2. Attacker crafts a request with multidimensional array parameters (nested arrays)
3. The application fails to validate parameter structure before processing
4. An unhandled exception is triggered during execution
5. Error message or stack trace is displayed containing full file paths
6. Attacker gains information about server directory structure and application architecture

## Root cause
Insufficient input validation on the $params variable before passing it to execute() function. The application does not check if $params is a one-dimensional array, allowing nested arrays to be processed and potentially triggering exceptions that leak path information.

## Attacker mindset
An attacker would recognize that multidimensional arrays bypass expected parameter handling, causing exceptions. By analyzing error messages, they could map the server's file structure and identify sensitive paths useful for further exploitation.

## Defensive takeaways
- Implement strict input validation on all function parameters, checking both type and structure
- Validate that array parameters are one-dimensional unless explicitly required to be nested
- Never expose file paths in error messages displayed to users; log internally instead
- Implement comprehensive exception handling to prevent stack traces from reaching end users
- Use error suppression or custom error pages for production environments
- Apply the proposed validation check before processing untrusted input

## Variant hunting
Search for other execute() or query() functions that don't validate parameter structure
Test all database abstraction layers for similar nested array handling issues
Look for other instances where COUNT_RECURSIVE comparison could be beneficial
Check for similar path disclosure in logging, caching, or serialization functions
Audit error handling across the entire EasyDB codebase for information leaks

## MITRE ATT&CK
- T1592
- T1526

## Notes
The researcher provided a concrete fix suggestion using COUNT_RECURSIVE comparison. This is a low-severity but valid issue as FPD can aid reconnaissance. The vulnerability likely requires no authentication and is easily discoverable through fuzzing or parameter manipulation.

## Full report
<details><summary>Expand</summary>

Hi

as reported in email,
there is a full path disclosure in EasyDB

you fixed some of them in last commit
add this code before and "execute($params)" function call!

    if(count($params) != count($params,COUNT_RECURSIVE)){
                throw new \InvalidArgumentException("Invalid params");
    }

this will check $params to be 1d array,


Regards

</details>

---
*Analysed by Claude on 2026-05-24*
