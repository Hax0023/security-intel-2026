# Disclose any user's private email through API

## Metadata
- **Source:** HackerOne
- **Report:** 196655 | https://hackerone.com/reports/196655
- **Submitted:** 2017-01-08
- **Reporter:** zombiehelp54
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
#Description:
I have found a security vulnerability that allows an attacker to disclose any user's private email.
An attacker can disclose any user's private email by creating a sandbox program then adding that user to a report as a participant.
Now if the attacker issued a request to fetch the report through the API , the response will contain the invited user private email at the activities obje

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

#Description:
I have found a security vulnerability that allows an attacker to disclose any user's private email.
An attacker can disclose any user's private email by creating a sandbox program then adding that user to a report as a participant.
Now if the attacker issued a request to fetch the report through the API , the response will contain the invited user private email at the activities object.


#Steps to reproduce:
1. Go to any report submitted to your program. 
2. Add the victim username as a participant to your report.
3. Generate an API token.
4. Fetch the report through the API

```
curl "https://api.hackerone.com/v1/reports/[report_id]" \
  -u "api_idetifier:token"
```
The response will contain the invited user email at the `activities` object:
```json
"activities":{"data":[{"type":"activity-external-user-invited","id":"1406712","attributes":{"message":null,"created_at":"2017-01-08T01:57:27.614Z","updated_at":"2017-01-08T01:57:27.614Z","internal":true,"email":"<victim's_email@example.com>"}
```



</details>

---
*Analysed by Claude on 2026-05-24*
