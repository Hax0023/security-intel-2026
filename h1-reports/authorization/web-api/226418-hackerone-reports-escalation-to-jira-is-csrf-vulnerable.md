# HackerOne Report Escalation to JIRA CSRF Vulnerability

## Metadata
- **Source:** HackerOne
- **Report:** 226418 | https://hackerone.com/reports/226418
- **Submitted:** 2017-05-05
- **Reporter:** whhackersbr
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Request Forgery (CSRF), Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
HackerOne's report escalation to JIRA feature was vulnerable to CSRF attacks, allowing an attacker to escalate private security reports to JIRA without user consent. An attacker could craft a malicious link to trigger escalation via a simple GET request, potentially exposing sensitive report details. This vulnerability allowed unauthorized escalation of confidential vulnerability reports to external issue tracking systems.

## Attack scenario
1. Attacker identifies the vulnerable GET endpoint: https://hackerone.com/reports/[REPORT_NUMBER]/escalate
2. Attacker crafts a malicious webpage or social engineering email containing an img tag or link to the escalate endpoint
3. Attacker tricks a HackerOne researcher/administrator into visiting the malicious page while logged into HackerOne
4. Browser automatically sends authenticated request to the escalate endpoint due to session cookies
5. Private vulnerability report is escalated to JIRA without the user's knowledge or consent
6. Sensitive report details including vulnerability specifics are transferred to external JIRA instance

## Root cause
The report escalation endpoint used HTTP GET method without CSRF token validation. The application relied solely on session cookies for authentication, allowing any cross-origin request to trigger the escalation action when a user was logged in.

## Attacker mindset
An attacker could exploit this to expose sensitive security research details, manipulate vulnerability tracking workflows, or perform account-based attacks by escalating arbitrary reports to attacker-controlled JIRA instances. This is particularly valuable because private HackerOne reports contain unreleased vulnerability information.

## Defensive takeaways
- Implement CSRF tokens (synchronizer tokens or SameSite cookies) on all state-changing operations
- Use POST/PUT/DELETE HTTP methods instead of GET for state-modifying actions
- Enforce SameSite cookie attribute (Strict or Lax) on session tokens
- Validate request origin and referer headers for sensitive operations
- Implement additional authentication checks for high-impact actions like report escalation
- Use double-submit cookie pattern as secondary CSRF defense
- Require explicit user confirmation for escalation actions

## Variant hunting
Check other report management actions (comment, close, reopen) for similar CSRF issues
Test integration endpoints with external systems (GitHub, GitLab, Azure DevOps) for CSRF
Audit all GET endpoints that modify state in the application
Test other user account actions like settings changes via GET requests
Examine bounty payout and report export features for CSRF vulnerabilities
Test API endpoints for CSRF when called from web context

## MITRE ATT&CK
- T1190
- T1566
- T1048

## Notes
This is a classic CSRF vulnerability made more severe by involving sensitive security research data. The use of GET for state-changing operations is a fundamental violation of REST principles and web security best practices. The impact extends beyond the HackerOne user to potentially affect all stakeholders in the vulnerability report chain.

## Full report
<details><summary>Expand</summary>

**Summary:**

HackerOne reports escalation to JIRA is CSRF vulnerable

**Description (Include Impact):**

An attacker can steal private reports details through a CSRF in HackerOne report escalation to JIRA implementation.

### CSRF

GET https://hackerone.com/reports/[REPORT_NUMBER]/escalate

### Optional: Supporting Material/References (Screenshots)

 * https://youtu.be/N6JSGA_RIV4

</details>

---
*Analysed by Claude on 2026-05-24*
