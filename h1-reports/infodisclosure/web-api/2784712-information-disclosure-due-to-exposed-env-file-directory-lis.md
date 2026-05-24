# Information Disclosure Due To exposed .env file (Directory Listing) at ████████

## Metadata
- **Source:** HackerOne
- **Report:** 2784712 | https://hackerone.com/reports/2784712
- **Submitted:** 2024-10-16
- **Reporter:** necr0mancer
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Information Exposure Through Directory Listing
- **CVEs:** None
- **Category:** web-api

## Summary
A .env file was discovered on the server at ████, exposing sensitive application configurations, including database credentials, email settings, and more. This information could allow an attacker to gain unauthorized access to critical systems and services.

**Steps to Reproduce:**

1. Open a web browser.
2. Navigate to ████████.
3. The .env file content is displayed, revealing sensitive informati

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

A .env file was discovered on the server at ████, exposing sensitive application configurations, including database credentials, email settings, and more. This information could allow an attacker to gain unauthorized access to critical systems and services.

**Steps to Reproduce:**

1. Open a web browser.
2. Navigate to ████████.
3. The .env file content is displayed, revealing sensitive information.

**PoC Video Link:** ██████

## Impact

The exposed .env file could lead to multiple security threats, including but not limited to:

Unauthorized database access using DB_HOST, DB_USERNAME, and DB_PASSWORD.
Compromise of email services via MAIL_USERNAME and MAIL_PASSWORD.
Ability to access or manipulate other connected services.

</details>

---
*Analysed by Claude on 2026-05-24*
