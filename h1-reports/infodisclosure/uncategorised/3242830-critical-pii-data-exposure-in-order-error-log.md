# Critical PII Data Exposure in ORDER_ERROR_LOG via Unfiltered SQL Error Logging

## Metadata
- **Source:** HackerOne
- **Report:** 3242830 | https://hackerone.com/reports/3242830
- **Submitted:** 2025-07-09
- **Reporter:** xenion_
- **Program:** dlielc.edu
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Information Disclosure, Sensitive Data Exposure, Improper Error Handling, Inadequate Logging Controls, Data Minimization Violation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application's error logging system captures and persists complete SQL INSERT statements containing full customer PII (names, emails, phones, addresses, transaction amounts) in plaintext ORDER_ERROR_LOG files when database operations fail. This creates a high-value target for attackers and violates data minimization and privacy compliance requirements. The vulnerability allows any user with log file access to view sensitive customer records indefinitely.

## Attack scenario
1. Attacker gains unauthorized access to server filesystem or log file storage (via misconfigured permissions, compromised credentials, or directory traversal)
2. Attacker locates and reads the ORDER_ERROR_LOG file containing unfiltered SQL statements
3. Attacker extracts complete customer records including PII, transaction amounts, and addresses from INSERT statements
4. Attacker correlates multiple log entries to identify high-value targets or compile comprehensive customer databases
5. Attacker uses extracted PII for identity theft, account takeover, social engineering, or sale on dark markets
6. Organization discovers breach during audit or when customers report fraudulent activity, resulting in regulatory fines and reputational damage

## Root cause
The application logs complete SQL INSERT statements to error files without sanitizing or redacting sensitive data. Error handling mechanisms capture the full query context including parameterized customer data, and logging infrastructure lacks PII detection/filtering logic to prevent persistence of confidential information.

## Attacker mindset
Log files are gold mines for reconnaissance. If database operations fail frequently (network issues, validation errors), an attacker with any log access gains a comprehensive dump of customer records. No special exploitation needed—just read access to application logs yields immediate PII harvesting with low detection risk.

## Defensive takeaways
- Implement parameterized error logging that captures query structure without parameter values; log only error codes and metadata
- Deploy PII/sensitive data detection in logging pipeline to mask names, emails, phone numbers, addresses, SSNs before persistence
- Enforce strict access controls on log files (principle of least privilege, RBAC) and restrict log directory permissions
- Implement log retention policies aligned with business needs; purge error logs containing PII after short retention windows
- Use structured logging with separate sensitive/non-sensitive log streams; route PII-containing errors to encrypted, access-restricted stores
- Sanitize error messages returned to users and logs; avoid echoing user input or database context in error responses
- Conduct regular log file audits and automated scanning for exposed PII patterns (regex, entropy detection)
- Implement centralized, encrypted log management with audit trails; prevent direct log file access via application-layer interfaces only
- Add telemetry to detect excessive failed database operations that may indicate testing for log injection
- Include data handling requirements in threat modeling for error paths and exception handlers

## Variant hunting
Check all logging points in error handlers, especially database, API, and transaction processing layers for unfiltered SQL/query logging
Search codebase for exception handlers that directly log exceptions or stack traces containing parameterized data
Review debug logs, audit logs, and application logs for similar PII exposure patterns across all modules
Examine request/response logging for APIs that accept or return customer data; verify no request bodies/payloads logged
Inspect temporary log files, cache files, and backup logs for orphaned sensitive data
Test error conditions (DB connection failures, validation errors, timeouts) and capture what data appears in logs
Check for similar exposures in third-party dependencies or imported libraries with verbose error logging
Audit centralized logging services (ELK, Splunk, etc.) for indexed PII that may be searchable/exportable

## MITRE ATT&CK
- T1190
- T1552.001
- T1526
- T1213.002
- T1005
- T1123
- T1530

## Notes
This is a classic data minimization failure often overlooked in security reviews because log files are perceived as 'internal' artifacts. The vulnerability is trivial to trigger (simply cause database errors) and requires minimal attacker capability once log access is obtained. Educational institution (dlielc.edu) context suggests FERPA/privacy regulation exposure beyond general data protection. Redacted data in writeup indicates actual sensitive fields were present in original submission. Log files should never be treated as secure storage; they are a common attack surface for both internal and external threats.

## Full report
<details><summary>Expand</summary>

A critical security vulnerability has been identified in the application's error logging system where the ORDER_ERROR_LOG file contains complete database insertion statements that expose Personally Identifiable Information (PII) of customers in plain text format.

#### Root Cause

The application's error handling mechanism is logging full SQL INSERT statements when database operations fail. These statements contain complete customer records including sensitive personal information that should never be stored in log files.

What Data is ExposedThe logs contain complete customer records including:
Full names
Email addresses
Phone numbers
Home addresses
Customer IDs
Transaction amounts
....

simple of data 
```
INSERT INTO dli.dli_customer_data VALUES (
                dli_customer_data_sequence.NEXTVAL,
                SYSDATE,
                ████████,
                ███,
                ██████████,
                ████,
                ██████,
                ██████,
                █████████,
                █████████,
                ███████,
                █████,
                ███,
                █████,
                ███,
                ████████,
                ████,
                ██████████,
                'Surface',
                '14.00',
                '15.4',
                '17.5')

```
███████
████

## Impact

Unintended Data Persistence: Customer PII persists in log files beyond intended retention periods
Expanded Attack Surface: Log files become high-value targets containing concentrated PII
Compliance Violations: Direct violation of data minimization principles required by privacy regulations
Audit Trail Contamination: Security logs contain sensitive data that complicates forensic analysis

## System Host(s)
dlielc.edu

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Access the ORDER_ERROR_LOG file   ███████
2. Review the contents for database INSERT statements.  `INSERT INTO dli.dli_customer_data VALUES (`
3. Observe exposed customer data
```
  INSERT INTO dli.dli_customer_data VALUES (
                dli_customer_data_sequence.NEXTVAL,
                SYSDATE,
                █████████,
                ██████,
                ███████,
                'FPO',
                'AP',
                ██████████,
                ████████,
                ███,
                ██████████,
                'FPO',
                'AP',
                ███████,
                ████████,
                █████,
                ██████,
                ██████,
                'Air',
                '480.00',
                ████████,
                '600')

```

## Suggested Mitigation/Remediation Actions
Implement data sanitization in error logging to prevent PII exposure.



</details>

---
*Analysed by Claude on 2026-05-24*
