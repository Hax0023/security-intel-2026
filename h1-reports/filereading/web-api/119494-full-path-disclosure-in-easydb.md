# Full Path Disclosure in EasyDB single() Function

## Metadata
- **Source:** HackerOne
- **Report:** 119494 | https://hackerone.com/reports/119494
- **Submitted:** 2016-02-29
- **Reporter:** supernatural
- **Program:** EasyDB
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Path Traversal Information Leak
- **CVEs:** None
- **Category:** web-api

## Summary
The single() function in EasyDB fails to properly validate input parameters, leaving it vulnerable to full path disclosure attacks. While similar issues were patched in other functions, the single() function was overlooked and remains vulnerable to the same attack vector.

## Attack scenario
1. Attacker identifies that the single() function accepts parameters without proper validation
2. Attacker crafts a multidimensional array as input to the single() function
3. The function processes the malformed input without proper error handling
4. An exception is thrown that reveals the full server file path in the error message
5. Attacker obtains sensitive information about the server's directory structure
6. This information can be used for subsequent reconnaissance or targeted attacks

## Root cause
Incomplete patching of a parameter validation vulnerability. While the same issue was fixed in related functions, the single() function at line 366 in EasyDB.php was not updated with the necessary recursive array depth check to ensure only single-dimensional arrays are accepted.

## Attacker mindset
An attacker seeks to gather reconnaissance information about the target server's file system structure and paths. By exploiting incomplete patches across similar code paths, they can map out the application's configuration to identify potential weaknesses for further exploitation.

## Defensive takeaways
- Apply security patches consistently across all similar code paths and functions
- Implement comprehensive input validation that checks for both structure (dimensionality) and content
- Use COUNT_RECURSIVE checks before processing array parameters to ensure expected data structure
- Configure error handling to avoid exposing file paths in exception messages
- Implement automated testing to verify patch completeness across the codebase
- Review related functions systematically when fixing a vulnerability to prevent similar issues

## Variant hunting
Search for other functions in EasyDB that accept array parameters without recursive depth validation. Review all database query functions (query, insert, update, delete) for similar information disclosure vulnerabilities. Check for any error handling that outputs file paths.

## MITRE ATT&CK
- T1087
- T1526
- T1592

## Notes
This is a follow-up report to issue #115337, indicating that the original patch was incomplete. The vulnerability is relatively low severity as it primarily discloses information rather than enabling direct compromise. However, it represents a security practice failure in thorough patch verification.

## Full report
<details><summary>Expand</summary>

Hi,

as reported in #115337
about a full path disclosure in EasyDB

you fixed some of them in last commits
but `single` function is vulnerable too and not fixed yet!

    if(count($params) != count($params,COUNT_RECURSIVE)){
                throw new \InvalidArgumentException("Invalid params");
    }
this will check $params to be 1d array,
add this code before line 366 in EasyDB.php


Regards

</details>

---
*Analysed by Claude on 2026-05-24*
