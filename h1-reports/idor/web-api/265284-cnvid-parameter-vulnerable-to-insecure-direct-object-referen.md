# 'cnvID' parameter vulnerable to Insecure Direct Object References

## Metadata
- **Source:** HackerOne
- **Report:** 265284 | https://hackerone.com/reports/265284
- **Submitted:** 2017-09-01
- **Reporter:** testdefense
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
Installation Information
===
IIS 8, PHP 5.5, Concrete5 (5.7.5.7) [Default install]
### Issue POC
An unauthenticated user can enumerate comments from all blog posts by POSTing requests to /index.php/tools/required/conversations/view_ajax with incremental 'cnvID' integers.

1. An example blog with permissions set for READ/WRITE to Administrators only {F217708}
2. A comment entry with sensitive data 

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Installation Information
===
IIS 8, PHP 5.5, Concrete5 (5.7.5.7) [Default install]
### Issue POC
An unauthenticated user can enumerate comments from all blog posts by POSTing requests to /index.php/tools/required/conversations/view_ajax with incremental 'cnvID' integers.

1. An example blog with permissions set for READ/WRITE to Administrators only {F217708}
2. A comment entry with sensitive data (this could be PII or any other type of sensitive data posted by users) {F217710}
3. POST request by a malicious user without authentication {F217711}
4. Enumeration of comments via brute of 'cnvID' {F217712}

Remediation
---
Preventing insecure direct object references requires selecting an approach for protecting each user accessible object (e.g., object number, filename):
1. Use per user or session indirect object references. This prevents attackers from directly targeting unauthorized resources. For example, instead of using the resource’s database key, a drop down list of six resources authorized for the current user could use the numbers 1 to 6 to indicate which value the user selected. The application has to map the per-user indirect reference back to the actual database key on the server. OWASP’s ESAPI includes both sequential and random access reference maps that developers can use to eliminate direct object references.
2. Check access. Each use of a direct object reference from an untrusted source must include an access control check to ensure the user is authorized for the requested object.

References
---
[OWASP Top 10 2010-A4-Insecure Direct Object References](https://www.owasp.org/index.php/Top_10_2010-A4-Insecure_Direct_Object_References)
Also, crayons

</details>

---
*Analysed by Claude on 2026-05-24*
