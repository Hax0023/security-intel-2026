# Unauthorized Access to Soldier PII via Insecure Direct Object References (IDOR)

## Metadata
- **Source:** HackerOne
- **Report:** 1556950 | https://hackerone.com/reports/1556950
- **Submitted:** 2022-05-03
- **Reporter:** hxhbrofessor
- **Program:** U.S. Military Self-Service Portal (Redacted)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Information Disclosure, Horizontal Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Authenticated users on a U.S. military self-service portal could access sensitive PII and operational data of other soldiers by manipulating user ID parameters in API requests. The vulnerability exposed SSN last 4 digits, MOS codes, schools attended, duty assignments, and pay records for an arbitrary number of military personnel, posing significant security and safety risks.

## Attack scenario
1. Attacker authenticates to the military self-service portal with legitimate credentials
2. Attacker navigates to 'My Data' section and intercepts the HTTP request using Burp Suite
3. Attacker identifies the URL pattern containing a numeric user ID parameter (e.g., 124948002)
4. Attacker modifies the user ID parameter and requests data for other soldier IDs sequentially
5. System returns PII including SSN partial, MOS, home of record, and training data without authorization checks
6. Attacker exfiltrates sensitive military personnel data for potential use in targeting or insider threat scenarios

## Root cause
The application implements inadequate access control by failing to verify that authenticated users can only access their own data. The API endpoints accept user ID parameters without server-side authorization validation, allowing any authenticated user to retrieve arbitrary soldier records by modifying the numeric ID in the request URL.

## Attacker mindset
An insider threat (military personnel or contractor) or foreign adversary with basic portal access could systematically enumerate soldier identities and operational details to identify targets, assess force composition, or support social engineering attacks. The geopolitical context suggests nation-state interest in compromising U.S. military personnel.

## Defensive takeaways
- Implement server-side authorization checks on every data access request to verify the authenticated user owns/has access to the requested resource
- Use indirect references (tokens or hashes) instead of sequential numeric IDs for sensitive resources
- Enforce rate limiting and anomaly detection on API endpoints to identify bulk data exfiltration attempts
- Implement comprehensive logging and alerting for access to PII, especially from unusual patterns
- Conduct access control reviews on all self-service portals handling military personnel data
- Require multi-factor authentication for access to sensitive military personnel databases
- Apply principle of least privilege to authenticated user sessions

## Variant hunting
Search for similar numeric ID parameters in other military/government self-service portals: HR systems, benefits portals, leave management systems, performance evaluation systems, medical records portals, security clearance management systems. Test whether other data sections (Pay, Assignments, Gains/Losses) implement proper authorization. Determine if unauthenticated users can also access these endpoints.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1589: Gather Victim Identity Information
- T1040: Network Sniffing
- T1110: Brute Force
- T1078: Valid Accounts
- T1526: Reconnaissance

## Notes
This is a textbook IDOR vulnerability on a high-value target (U.S. military database). The researchers provided excellent step-by-step reproduction instructions. The impact assessment correctly identifies the geopolitical context and insider threat potential. The use of Burp Suite Intruder to automate enumeration demonstrates practical exploitation. The vulnerability affects multiple data categories across at least 2 host systems, suggesting systemic architectural weakness in access control design rather than isolated misconfiguration.

## Full report
<details><summary>Expand</summary>

**Description:**

Authenticated users on `https://█████████/SelfService/home/selfservice` can view other ████████'s data by following the page site for `My ███ Data` and start manipulating URL requests to view the following tabs: 
* Personnel
* Active Duty Tours
* ADOS
* Assignments
* ATRRS
* Data Discrepancies
* DJMS-RC Pay File Records
* DJMS-RC Pay Voucher
* Drill Attendance
* Education/Training
* Gains/Losses
* GI Bill Programs

Tester primarily focused on Personnel, ATRRS, and Education/Training tabs. 

## References

* CWE-359: Exposure of Private Personal Information to an Unauthorized Actor
* CWE-200 - Information Disclosure
* CWE-284 - Improper Access Control

## Contributers

- badlifeguard
- theonetruepengu

## Impact

The information displayed in Personnel, ATRRS, and Education/Training tabs shows a soldier's Last 4 of an SSN, Home of Record, MOS (Job title), and schools. Due to heightened tensions in today's GEO-Political climate, the availability of this information can be dangerous and potentially put a soldier's life at risk: scenario, insider threat working with an adversarial country to retrieve data.

## System Host(s)
████████, ██████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
* Authenticate to https://█████████/SelfService/home/selfservice with burpsuite
* Turn Intercept off
* Go to the bottome of the page and click on `My █████████ Data`
* On Burp, click proxy
** HTTP History
** Scroll to the last GET request with message 200
** URL should be `https://█████████/SelfService/Home/dynamicdata/section/██████████/██████████%20TPU/61/124948002`
** Right click over the message and send to `Intruder`
* Intruder Set up
** Clear all variables in Postions Tab
** in the get request highlight the `2` in `GET /SelfService/Home/dynamicdata/section/███████/████%20TPU/61/124948002` and on the right hand side of Intruder click `add variable`
** Payload Tab 
*** Payload Set > Payload Type > select numbers
*** Payload Options [Numbers] > From: 1 > To: 9 > Step: 1
** Options Tab
*** Grep Exact > add > refetch response > in the search box: search `Primary MOS` this will display a succesful record found.

Additional URLs  to manipulate utilizing the same steps above are:

```bash
Personnel
https://█████/SelfService/Home/dynamicdata/section/██████/███████%20TPU/61/124948002

ATTRS
https://██████████/SelfService/Home/dynamicdata/section/█████████/█████████%20TPU/444/124948002

Education/Training
https://████████/SelfService/Home/dynamicdata/section/█████/████%20TPU/2001/124948002

```

## Suggested Mitigation/Remediation Actions
Correct permissions on access to these URLs. Authenticated users should be checked against their own ID and data.



</details>

---
*Analysed by Claude on 2026-05-24*
